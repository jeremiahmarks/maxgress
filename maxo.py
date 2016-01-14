# @Author: jeremiah.marks
# @Date:   2016-01-10 23:31:42
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2016-01-11 07:42:00

# This script is an attempt to provide the maximum onion
# ability out of a series of ports in Ingress.
from turtle import Turtle
from itertools import combinations
import collections
from cenmesport import portals
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from collections import defaultdict

def my_dd():
    return defaultdict(my_dd)



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
    """docstring for Portal
    Portal is the object that represents a portal in Ingress
    Initially, to keep it simple, it is going to consist of
    an x coord and a y coord, but will have many other attributes
    after the testing phase is over.
    """
    def __init__(self, xcoord, ycoord):
        super(Portal, self).__init__()
        self.x=xcoord
        self.y=ycoord
        self.coords=(self.x, self.y)

    def __eq__(self, other):
        return self.coords == other.coords
    def __str__(self):
        return(str(self.coords))

class Link(object):
    """A Link consists of two portals
    """
    def __init__(self, originPortal, destPortal):
        self.op=originPortal
        self.dp=destPortal
        self.drawn=False


    def plot(self, drawer):
        if not self.drawn:
            drawer.pu()
            drawer.goto(self.op.coords)
            drawer.pd()
            drawer.goto(self.dp.coords)
            drawer.pu()
        self.drawn=True

    def __str__(self):
        print str(self.op) + "is linked to " + str(self.dp)

class Field(object):
    """docstring for Field
    The Field object exists to house Portals and Links. It
    can store recursive versions of itself.
    """
    def __init__(self, portals=None):
        global linklist
        if 'linklist' not in globals():
            linklist=[]
        super(Field, self).__init__()
        self.interiorportals=defaultdict()
        self.interiorfields=defaultdict(list)
        self.hullportals=[]
        self.hulllinks=[]
        self.turt=Turtle()
        self.turt.speed(0)

        if portals:
            neededlinks=[[portals[0], portals[1]], [portals[0], portals[2]], [portals[1], portals[2]]]
            print str([str(x[0]) + ",  " + str(x[1]) for x in neededlinks])
            for eachlink in linklist:
                if [eachlink.op, eachlink.dp] in neededlinks:
                    self.hulllinks.append(eachlink)
                    neededlinks.remove([eachlink.op, eachlink.dp])
                    continue
                if [eachlink.dp, eachlink.op] in neededlinks:
                    self.hulllinks.append(eachlink)
                    neededlinks.remove([eachlink.dp, eachlink.op])
                    continue
            for eachlink in neededlinks:
                neededlink=Link(eachlink[0], eachlink[1])
                self.hulllinks.append(neededlink)
                linklist.append(neededlink)

    def draw(self):
        for eachlink in self.hulllinks:
            eachlink.plot(self.turt)



class maxField(object):
    """docstring for maxField
    MaxField will exist to hold all portals and links.
    It will also decide if a link is allowable
    """
    def __init__(self):
        super(maxField, self).__init__()
        self.portalsByX=lambda: defaultdict(my_dd)
        self.portalsByY=lambda: defaultdict(my_dd)
        self.linksByOriginX=lambda: defaultdict(my_dd)
        self.linksByY = lambda: defaultdict(my_dd)

    def getSlopeBetweenPortals(self, portal1, portal2):
        # slope = rise/run == difference in Y/difference in X
        #  ==(Y2-Y1)/(X2-X1)
        return float(portal2.y - portal1.y)/float(portal2.x - portal1.x)

    def getPortal(self, portalData=None, x=None, y=None):
        portalx=x
        portaly=y
        if portalData is not None:
            portalx = float(portalData['lat'])
            portaly = float(portalData['lon'])
        if len(self.portalsByX[portalx][portaly]) > 0:
            return self.portalsByX[portalx][portaly][0]
        thisportal = Portal(portalx, portaly)
        self.portalsByX[portalx][portaly]['portalData']=portalData
        self.portalsByX[portalx][portaly]['portal']=thisportal
        self.portalsByY[portaly][portalx]['portal']=thisportal
        return thisportal

    def getLink(self, originPortal, destPortal):
        if len(self.linksByOriginX[originPortal.x][originPortal.y][destPortal.x][destPortal.y]) > 0:
            #This indicates that this exact link has been thrown
            return self.linksByOriginX[originPortal.x][originPortal.y][destPortal.x][destPortal.y][0]
        if len(self.linksByOriginX[destPortal.x][destPortal.y][originPortal.x][originPortal.y]) > 0:
            #This indicates that the opposite, but operable link has already been created
            return self.linksByOriginX[destPortal.x][destPortal.y][originPortal.x][originPortal.y][0]
        # If we are here then the link has not been created yet. Before we can create it, we need
        # to check if it can exist
        # We will start by finding all links which have an
        # endpoint which falls within(including) the endpoints
        # if any of the links exist both above and below the
        # line between the endpoints, then the line will
        # be invalid.
        xs=[originPortal.x, destPortal.x]
        slope=self.getSlopeBetweenPortals(originPortal, destPortal)
        linky=lambda x: slope*(x-originPortal.x)+originPortal.y
        minx=min(xs)
        maxx=max(xs)
        linkstoinspect=[]
        for eachoriginx in self.linksByOriginX.keys():
            #
            for eachoriginy in self.linksByOriginX[eachoriginx].keys():
                for eachdestx in self.linksByOriginX[eachoriginx][eachoriginy].keys():
                    for eachdesty in self.linksByOriginX[eachoriginx][eachoriginy][eachoriginx].keys():


        opy=originPortal.y




portalslist=[(100,200), (300,50), (50,700)]
pl=[]
for eachportal in portalslist:
    pl.append(Portal(eachportal[0], eachportal[1]))
bb=Field(pl)
bb.draw()
