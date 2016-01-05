# @Author: jeremiah.marks
# @Date:   2015-12-21 14:48:33
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2016-01-05 01:34:30

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
        self.lat=bookmarkData['lat']
        self.lon = bookmarkData['lon']
        self.ilat = int(bookmarkData['lat']*10**6)
        self.ilon = int(bookmarkData['lon']*10**6)
        self.coords = (self.lon, self.lat)
        self.faction = None
        self.bmd=bookmarkData

class Link(object):
    """A link serves as a connection between two portals.
    Currently it will remain neutral, but it should either
    adopt the same orientation as its portals.
    It will also provide an equation to define itself
    """
    def __init__(self, originPortal, destinationPortal):
        self.origin=originPortal
        self.origincoords=originPortal.coords
        self.destination=destinationPortal
        self.destcoords=destinationPortal.coords
        self.lat=[originPortal.lat, destinationPortal.lat]
        self.lon=[originPortal.lon, destinationPortal.lon]




class Field(object):
    """Field:
        A field is a collection of portals and links
    """

    def __init__(self):
        self.drawer=Turtle()
        self.drawer.speed(0)
        self.screen = self.drawer.getscreen()
        self.canvas = self.screen.getcanvas()
        self.screen.screensize(canvwidth=1000000, canvheight=1000000)
        self.name=None
        self.portals=[]
        self.links=[]

    def findHull(self):
        self.hullcoords = convex_hull([portal.coords for portal in self.portals])

    def addportal(self, portalData):
        self.portals.append(Portal(portalData))

    def updateStats(self):
        self.lats = sorted(self.portals, key=lambda k: k.lat)
        self.lons = sorted(self.portals, key=lambda k: k.lon)
        self.latextrema = (self.lats[0].ilat, self.lats[-1].ilat)
        self.lonextrema = (self.lats[0].ilon, self.lons[-1].ilon)
        self.latdiff = self.latextrema[0] - self.latextrema[1]
        self.londiff = self.lonextrema[0] - self.lonextrema[1]
        self.findcenter()

    def findcenter(self):
        self.latcenter=sum([portal.ilat for portal in self.portals])/len(self.portals)
        self.loncenter=sum([portal.ilon for portal in self.portals])/len(self.portals)
        self.centerofmass=(self.loncenter, self.latcenter)

    def drawPortal(self):
        for eachportal in self.portals:
            self.drawer.pu()
            self.drawer.goto(eachportal.ilon - self.loncenter, eachportal.ilat - self.latcenter)
            self.drawer.pd()
            self.drawer.circle(10)

    def findPortal(self, portalcoords):
        returnPortal=None
        for eachportal in self.portals:
            if eachportal.coords == portalcoords:
                returnPortal = eachportal
                break
        return returnPortal


class MUField(object):
    """A MUField is made up of three points and links to define
    the boundries of the field. Within it can exist other
    Portals, links, and fields."""
    def __init__(self, portal1, portal2, portal3):
        super(MUField, self).__init__()
        self.v1=portal1
        self.v2=portal2
        self.v3=portal3
        self.vertexes=(self.v1, self.v2, self.v3)
        self.links=[Link(comb[0], comb[1]) for comb in combinations(self.vertexes, 2)]
        self.interiorportals=set()
        self.potentialInteriorHulls=[]
        self.interiorfields=[]

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
                testfield=MUField(self.field.findPortal(eachpotentialinteriorhull[0]), self.field.findPortal(eachpotentialinteriorhull[1]), self.field.findPortal(eachpotentialinteriorhull[2]))
                testfield.field=self.field
                for eachportal in self.interiorportals:
                    testfield.testAndAdd(eachportal)
                self.testfields[len(testfield.interiorportals)].append(testfield)
            self.maininternalhull=self.testfields[max(self.testfields.keys())][0]
            for eachpoint in self.maininternalhull.vertexes:
                if eachpoint not in self.vertexes:
                    newpoint=eachpoint
                    break
            for eachlink in self.links:
                thisfield = MUField(eachlink.origin, eachlink.destination, newpoint)
                thisfield.field=self.field
                for eachportal in self.interiorportals:
                    thisfield.testAndAdd(eachportal)
                self.interiorfields.append(thisfield)
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



myfield = Field()
for portal in portals:
    myfield.addportal(portals[portal])
myfield.findHull()
potentialMainFields=[triangle for triangle in combinations(myfield.hullcoords, 3)]
potentialfields=[]
for eachfield in potentialMainFields:

    thisfield = MUField(myfield.findPortal(eachfield[0]), myfield.findPortal(eachfield[1]), myfield.findPortal(eachfield[2]))
    thisfield.field=myfield
    for eachportal in myfield.portals:
        thisfield.testAndAdd(eachportal)
    potentialfields.append(thisfield)
    print len(thisfield.interiorportals)

prif=potentialfields[2]
prif.findInteriorHulls()
potentialinteriorfields=[]
for eachthing in prif.potentialInteriorHulls:
    subfield=MUField(myfield.findPortal(eachthing[0]), myfield.findPortal(eachthing[1]), myfield.findPortal(eachthing[2]))
    for eachportal in prif.interiorportals:
        subfield.testAndAdd(eachportal)
    print len(potentialinteriorfields), len(subfield.interiorportals)
    potentialinteriorfields.append(subfield)

for eachthing in prif.potentialInteriorHulls:
    subfield=MUField(myfield.findPortal(eachthing[0]), myfield.findPortal(eachthing[1]), myfield.findPortal(eachthing[2]))
    for eachportal in prif.interiorportals:
        subfield.testAndAdd(eachportal)
    print len(potentialinteriorfields), len(subfield.interiorportals)
    potentialinteriorfields.append(subfield)
for eachfield in potentialinteriorfields:
    print "\n"*3
    for eachv in eachfield.vertexes:
        print eachv.name

