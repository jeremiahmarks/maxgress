# @Author: jeremiah.marks
# @Date:   2015-12-21 14:48:33
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2016-01-10 23:15:26

###
# Maxgress will accept a series of portal coordinates, as
# exported by IITC, and compute the links necessary to
# provide max MU capture.  (I think, the linking relationships
# are what are really getting me about this game. I
# could actually give a rip about the real point. )
#
# Initially it will not expect/be able to work with blocking
# links, however that is in its future, hopefully.
###

###
# So a quick introduction to the logic/vocab I am using:
#   A map is a collection of portals and links.
#   A portal can have resinators and other modifications that
#       change its default values.
#   A link is a connection between two portals. It cannot be
#       crossed by another link
#   A field is a made by linking three portals.
#   When a portal is within a field it cannot link out to
#       other portals
#   The map will be in charge of checking and allowing links
#       based on other links.
from turtle import Turtle
from itertools import combinations
import collections
from cenmesport import portals
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from collections import defaultdict
# combos=[comb for comb in combinations(hullportals, 3)]
# points = np.array(ps)
# hull = ConvexHull(points)
# plt.plot(points[:,0], points[:,1], 'o')

# for simplex in hull.simplices:
#     plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
# plt.show()

def convex_hull(points):
    """Computes the convex hull of a set of 2D points.
    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """
    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    return lower[:-1] + upper[:-1]


class Portal(object):
    """portal:
        a portal represents an Ingress portal. It is literally
        a collection of values. These values include the
        Lat/Long, name currently
    """
    def __init__(self, bookmarkData):
        super(Portal, self).__init__()
        self.name = bookmarkData['label']
        self.lat=float(bookmarkData['lat'])
        self.lon = float(bookmarkData['lon'])
        self.coords = (self.lon, self.lat)
        self.faction = None
        self.bmd=bookmarkData
        self.incominglinks={}
        self.outgoinglinks={}
        self.allLinks = self.getAllLinks

    def getAllLinks(self):
        alllinks={}
        alllinks.update(self.incominglinks)
        alllinks.update(self.outgoinglinks)
        return alllinks

    def __eq__(self, other):
        return self.lat==other.lat and self.lon == other.lon

    def plot(self, someturtle):
        # someturtle.pu()
        someturtle.goto(self.coords)
        someturtle.seth(0)
        someturtle.pd()
        for x in range(8):
            someturtle.left(45)
            someturtle.fd(0.0002)
        someturtle.pu()

class Link(object):
    global linklist
    if 'linklist' not in globals():
        linklist=set()
    """A link serves as a connection between two portals.
    Currently it will remain neutral, but it should either
    adopt the same orientation as its portals.
    It will also provide an equation to define itself
    """
    def __init__(self, originPortal, destinationPortal):
        global linklist
        self.origin=originPortal
        self.origincoords=originPortal.coords
        self.destination=destinationPortal
        self.destcoords=destinationPortal.coords
        self.lat=[originPortal.lat, destinationPortal.lat]
        self.xs=self.lat
        self.lon=[originPortal.lon, destinationPortal.lon]
        self.ys=self.lon
        self.portals=[self.origin, self.destination]
        self.drawn=False
        # for eachlink in linklist:
        #     if eachlink == self:
        #         return eachlink
        # linklist.add(self)
        # return self
        # quick basic math lesson here:
        #
        # The equation for a line between two points is
        #    y = mx + b
        #    "b" is the value for y when X is equal to zero,
        #       however in this case, the b is really meaningless
        #       because we are dealing with lat/lon and are
        #       nowhere near the equator
        #
        #    "m" is the slope, the "rise over the run"
        #       Think of it like the slope of the roof on
        #       your house, it is how many feet up/down you
        #       will move if you walk some distance towards the
        #       the peak of the root.
        # (This would make "b" where the roof would touch the ground,
        # if it extended the all the way to the ground.)
        #
        #   With two points we can treat them as (x,y) coordnates.
                # Let one portal be (x1,y1) = (lon, lat) (or the other way aroudn, I forget)
                # portal 2 = (x2,y2)
        # This means that the slope between the two of them is
            # m = rise/run
            # m = (y2-y1)/(x2-x1)
        # using this, the equation becomes:
            # y = (((y2-y1)/(x2-x1)) * x) + b
        # Since b is the point where the line has y=0
        # it is
            # 0 = (((y2-y1)/(x2-x1)) * x) + b
            # -b = ((y2-y1)/(x2-x1)) * x
            # b = -((y2-y1)/(x2-x1)) * x
        #  Shit, I missed something, I will need to write it out,
        # but what we end up getting to is point-slope form, which
        # Point slope form:
            # y-y1 = m(x-x1)
            # Since we will have the slope, what we will do
            # is set the equation as
                # from x1 to x2 the y value is:
                # y = slope*(xinput-originx) + y input
            # this will allow us to see if a potential link crosses
            # this link by seeing if it is above/below it at all endpoints
            # between and including originx, destinationx, and testingx, if it is within
            # the area.
                #
        #
        #
        #       this breaks down to:
        #
        #
        #
        #
        # self.slope=float(self.ys[0] - self.ys[1])/float(self.xs[0] - self.xs[1])

    def yatx(self,xvalue):
        xslist = list(self.xs).append(xvalue)
        if xvalue not in self.xs:
            if xvalue in max(xslist) or xvalue in min(xslist):
            # This would indicate that this point is not between the two points at all
                return None
        return self.slope * (xvalue - self.xs[0]) + self.ys[0]

    def __eq__(self, other):
        return self.origin in other.portals and self.destination in other.portals

    def plot(self, someturtle):
        if self.drawn:
            pass
        else:
            someturtle.pu()
            someturtle.goto(self.origin.coords)
            someturtle.pd()
            someturtle.circle(0.0001)
            someturtle.goto(self.destination.coords)
            someturtle.circle(0.0001)
            self.drawn=True


class Field(object):
    """Field:
        A field is a collection of portals and links
    """
    global linklist
    if 'linklist' not in globals():
        linklist=set()

    def __init__(self):
        self.drawer=Turtle()
        self.drawer.speed(0)
        self.screen = self.drawer.getscreen()
        self.canvas = self.screen.getcanvas()
        self.screen.screensize(canvwidth=1000000, canvheight=1000000)
        self.name=None
        self.portals=[]
        self.links=[]
        self.portallons=[]
        self.portallats=[]
        self.linksbycoords=defaultdict(list) # linksbycoords

    def findHull(self):
        self.hullcoords = convex_hull([portal.coords for portal in self.portals])

    def addportal(self, portalData):
        newportal=Portal(portalData)
        self.portallats.append(newportal.lat)
        self.portallons.append(newportal.lon)
        self.portals.append(newportal)

    def updateStats(self):
        self.lats = sorted(self.portals, key=lambda k: k.lat)
        self.lons = sorted(self.portals, key=lambda k: k.lon)
        self.latextrema = (self.lats[0].lat, self.lats[-1].lat)
        self.lonextrema = (self.lats[0].lon, self.lons[-1].lon)
        self.latdiff = self.latextrema[0] - self.latextrema[1]
        self.londiff = self.lonextrema[0] - self.lonextrema[1]
        self.findcenter()
        self.lowerleft=(min(self.portallons), min(self.portallats))
        self.upperright=(max(self.portallons), max(self.portallats))
        self.screen.setworldcoordinates(self.lowerleft[0], self.lowerleft[1], self.upperright[0], self.upperright[1])

    def findcenter(self):
        self.latcenter=sum([portal.lat for portal in self.portals])/len(self.portals)
        self.loncenter=sum([portal.lon for portal in self.portals])/len(self.portals)
        self.centerofmass=(self.loncenter, self.latcenter)

    def drawPortal(self):
        for eachportal in self.portals:
            self.drawer.pu()
            self.drawer.goto(eachportal.lon - self.loncenter, eachportal.lat - self.latcenter)
            self.drawer.pd()
            self.drawer.circle(10)

    def findPortal(self, portalcoords):
        returnPortal=None
        for eachportal in self.portals:
            if eachportal.coords == portalcoords:
                returnPortal = eachportal
                break
        return returnPortal

    def addLink(self, origin, destination):
        # outbound = destination in self.linksbycoords[origin.coords]
        # inbound = origin in self.linksbycoords[origin.coords]
        # #
        # # Sigh
        # # y=mx+b
        # # m=rise/run = originlon-destlon/originlat-destlat
        # # y-y1 = m(x-x1) This is the base formula for any
        # #  line through this portal.
        # potentiallink= lambda k: ((origin.lon-destination.lon)/origin.lat-destination.lat)(k-origin.coords[0])+origin.coords[1]
        # lonrange = max(origin.lon, destination.lon) - min(origin.lon, destination.lon)
        global linklist
        testlink=Link(origin, destination)
        if 'linklist' not in globals():
            linklist=set()
        for eachlink in linklist:
            if testlink == eachlink:
                return eachlink
        return testlink


class MUField(object):
    """A MUField is made up of three points and links to define
    the boundries of the field. Within it can exist other
    Portals, links, and fields."""
    def __init__(self, portal1, portal2, portal3, myfield):
        super(MUField, self).__init__()
        self.v1=portal1
        self.v2=portal2
        self.v3=portal3
        self.vertexes=(self.v1, self.v2, self.v3)
        self.links=[myfield.addLink(comb[0], comb[1]) for comb in combinations(self.vertexes, 2)]
        self.interiorportals=set()
        self.potentialInteriorHulls=[]
        self.interiorfields=[]
        self.myfield = myfield

    def PortalWithin(self, portalInQuestion):
        if len(convex_hull([portal.coords for portal in [self.v1, self.v2, self.v3, portalInQuestion]]))>3:
            return False
        else:
            return True

    def testAndAdd(self, portalToTest):
        if portalToTest not in self.vertexes and self.PortalWithin(portalToTest):
            self.interiorportals.add(portalToTest)
            return True
        else:
            return False

    def findcenter(self):
        self.latcenter=sum([portal.lat for portal in self.interiorportals])/len(self.interiorportals)
        self.loncenter=sum([portal.lon for portal in self.interiorportals])/len(self.interiorportals)
        self.centerofmass=(self.loncenter, self.latcenter)

    def findInteriorHulls (self):
        if len(self.interiorportals) == 0:
            pass
        else:
            self.testfields=collections.defaultdict(list)
            for eachlink in self.links:
                potentialportals = [portal.coords for portal in self.interiorportals]
                for eachendpoint in [eachlink.origincoords, eachlink.destcoords]:
                    potentialportals.append(eachendpoint)
                if len(potentialportals) >2:
                    self.potentialInteriorHulls.append(convex_hull(potentialportals))
            for eachpotentialinteriorhull in self.potentialInteriorHulls:
                testfield=MUField(self.field.findPortal(eachpotentialinteriorhull[0]), self.field.findPortal(eachpotentialinteriorhull[1]), self.field.findPortal(eachpotentialinteriorhull[2]), self.myfield)
                testfield.field=self.field
                for eachportal in self.interiorportals:
                    testfield.testAndAdd(eachportal)
                self.testfields[len(testfield.interiorportals)].append(testfield)
            self.maininternalhull=self.testfields[max(self.testfields.keys())][0]
            # self.interiorfields.append(self.maininternalhull)
            newpoint=None
            for eachpoint in self.maininternalhull.vertexes:
                if eachpoint not in self.vertexes:
                    newpoint=eachpoint
            if newpoint is None:
                raise Exception
            for eachlink in self.links:
                thisfield = MUField(eachlink.origin, eachlink.destination, newpoint, self.myfield)
                thisfield.field=self.field
                for eachportal in self.interiorportals:
                    thisfield.testAndAdd(eachportal)
                self.interiorfields.append(thisfield)
            print len(self.interiorfields)
            for eachfield in self.interiorfields:
                eachfield.findInteriorHulls()

    def printSelf(self, indent=0):
        properindent="  "*indent
        retstr="\n\n"
        for eachv in self.vertexes:
            retstr+= properindent + str(eachv.bmd) + "\n"
        for eachfield in self.interiorfields:
            retstr+=eachfield.printSelf(indent=indent+1) + "\n"
        return retstr

    def plotall(self, someturtle):
        for eachlink in self.links:
            eachlink.plot(someturtle)
        for eachfield in self.interiorfields:
            eachfield.plotall(someturtle)

    def plot(self, someturtle):
        for eachlink in self.links:
            eachlink.plot(someturtle)

myfield = Field()
for portal in portals:
    myfield.addportal(portals[portal])
myfield.findHull()
potentialMainFields=[triangle for triangle in combinations(myfield.hullcoords, 3)]
potentialfields=[]
for eachfield in potentialMainFields:

    thisfield = MUField(myfield.findPortal(eachfield[0]), myfield.findPortal(eachfield[1]), myfield.findPortal(eachfield[2]), myfield)
    thisfield.field=myfield
    for eachportal in myfield.portals:
        thisfield.testAndAdd(eachportal)
    potentialfields.append(thisfield)
    print len(thisfield.interiorportals)

prif=potentialfields[2]
prif.findInteriorHulls()
# potentialinteriorfields=[]
# for eachthing in prif.potentialInteriorHulls:
#     subfield=MUField(myfield.findPortal(eachthing[0]), myfield.findPortal(eachthing[1]), myfield.findPortal(eachthing[2]))
#     for eachportal in prif.interiorportals:
#         subfield.testAndAdd(eachportal)
#     print len(potentialinteriorfields), len(subfield.interiorportals)
#     potentialinteriorfields.append(subfield)

# for eachthing in prif.potentialInteriorHulls:
#     subfield=MUField(myfield.findPortal(eachthing[0]), myfield.findPortal(eachthing[1]), myfield.findPortal(eachthing[2]))
#     for eachportal in prif.interiorportals:
#         subfield.testAndAdd(eachportal)
#     print len(potentialinteriorfields), len(subfield.interiorportals)
#     potentialinteriorfields.append(subfield)
# for eachfield in potentialinteriorfields:
#     print "\n"*3
#     for eachv in eachfield.vertexes:
#         print eachv.name
myfield.updateStats()
myfield.drawer.speed(0)
prif.plotall(myfield.drawer)
# for pos, eachportal in enumerate(myfield.portals):
#     for otherpos, otherportal in enumerate(myfield.portals):
#         if otherpos>pos:
#             myfield.drawer.pu()
#             myfield.drawer.goto(eachportal.coords)
#             myfield.drawer.pd()
#             myfield.drawer.goto(otherportal.coords)
