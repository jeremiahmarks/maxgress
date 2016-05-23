# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2016-05-23 00:07:18
# @Last Modified by:   Jeremiah Marks
# @Last Modified time: 2016-05-23 10:43:56

# maxgress0, where I start at step zero of the 
# maxgress idea

# the first challenge will be: given a large set of portals, and a set of
# portals to form a hull, find all portals within the hull

# from someportals import allportals as allportals
from turtle import Turtle

boundries={"maps":{"idOthers":{"label":"Others","state":1,"bkmrk":{}}},"portals":{"idOthers":{"label":"Others","state":1,"bkmrk":{"id1463984069890":{"guid":"925443ac12f74ff9864a10074ca36c4d.16","latlng":"33.514272,-111.681958","label":"Frog Pit Stop"},"id1463984090704":{"guid":"647853527f8f4f72aaea3dfea2c697c6.16","latlng":"33.466636,-111.742608","label":"Stonebridge"},"id1463984138627":{"guid":"7bd931cefc2b4e3fbe003737020a4787.16","latlng":"33.436699,-111.603513","label":"Hi Way Baptist Church "}}}}}

# First, let's define what a portal is

class IngressPortal(object):
	"""docstring for IngressPortal"""
	def __init__(self, dictOfData):
		"""This is a sample of the dictOfData which is currently expected
			{"guid":"925443ac12f74ff9864a10074ca36c4d.16","latlng":"33.514272,-111.681958","label":"Frog Pit Stop"},
		"""

		super(IngressPortal, self).__init__()
		
		# Assigning values
		self.guid = dictOfData['guid']
		self.lat, self.long = dictOfData['latlng'].split(',')
		# This is probably a bad practice
		try:
			self.label = dictOfData['label']
		except Exception, e:
			print self.guid + " is missing label data"
			self.label = "No Label"

		# I am giving each portal object their own turtle
		# in the hopes that they will clean up after themselves
		self.drawer = Turtle()
		self.drawer.speed(0)
		self.drawer.ht()
		self.drawer.pu()

	def __eq__(self, other):
		return self.guid == other.guid

	def clearDrawing(self):
		self.drawer.clear()

# And, well, the map is an important part of the whole thing.

class IngressMap(object):
	"""IngressMap is a place to hold the portals as well as manage the 
	physical drawing of the map
	"""
	def __init__(self):
		super(IngressMap, self).__init__()
		self.portals={}

		# This is the stuff used for drawing
		self.drawer = Turtle()
		self.drawer.speed(0)
		self.screen = self.drawer.getscreen()
		self.canvas = self.screen.getcanvas()
		self.screen.screensize(canvwidth=1000000, canvheight=1000000)

	def addPortal(self, portalToAdd):
		thisportal = IngressPortal(portalToAdd)
		if thisportal.guid not in self.portals:
			self.portals[thisportal.guid] = thisportal

	def removePortal(self, GUIDOfPortalToRemove):
		removedportal = self.portals.pop(GUIDOfPortalToRemove)
		removedportal.deleteDrawing()

	def clearDrawing(self):
		for eachportal in self.portals:
			self.portals[eachportal].clearDrawing()

	def drawPortals(self):
		# Sigh, this is going to be a litte more complicated 
		# than I want. We will need to find the center 
		# of the portals and then lay them out with a zoom that 
		# maximizes available area.

		


