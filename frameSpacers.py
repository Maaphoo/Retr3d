# Copyright 2015 Matthew Rogge
# 
# This file is part of Retr3d.
# 
# Retr3d is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Retr3d is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Retr3d.  If not, see <http://www.gnu.org/licenses/>.

#import Math stuff
from __future__ import division # allows floating point division from integersimport math
import math
from itertools import product

#import FreeCAD modules
import FreeCAD as App
import FreeCAD# as #
import Part
import Sketcher
import Draft

#Specific to printer
import globalVars as gv
import utilityFunctions as uf

class FrameSpacers(object):
	def __init__(self):
		self.name = "frameSpacers"
		
	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name+"FrontL").Shape= shape
		
		#Color Part

		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name+"FrontL")
		shape = objs[-1]		
		
		#Rotate into correct orientation
		rotateAngle = 90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,1,0)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		rotateAngle = 90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,0,1)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left spacer into place
		xShift = -gv.zRodSpacing/2
		yShift = -gv.yRodLength/2 + gv.frameWidth + gv.frameHeight/2 + gv.frameSpacerOffset
		zShift = -gv.yRodStandoff - gv.frameHeight
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		#Copy the front Left spacer and move it to the back
		
		App.ActiveDocument.addObject('Part::Feature',self.name+"BackL").Shape = shape.Shape
		
		#Color Part

		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name+"BackL")
		shape = objs[-1]
		
		#Define shifts and move the back left spacer into place
		xShift = 0
		yShift = gv.sideBarLength - gv.frameHeight - 2*gv.frameSpacerOffset
		zShift = 0
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		#Copy the back Left spacer and move it to the right back
		
		App.ActiveDocument.addObject('Part::Feature',self.name+"BackR").Shape = shape.Shape
		
		#Color Part

		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name+"BackR")
		shape = objs[-1]
		
		#Define shifts and move the back left spacer into place
		xShift = gv.zRodSpacing
		yShift = 0
		zShift = 0
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()

		#Copy the front Left spacer and move it to the front right
		objs = App.ActiveDocument.getObjectsByLabel(self.name+"FrontL")
		shape = objs[-1]		
		
		App.ActiveDocument.addObject('Part::Feature',self.name+"FrontR").Shape = shape.Shape
		
		#Color Part

		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name+"FrontR")
		shape = objs[-1]
		
		#Define shifts and move the back left spacer into place
		xShift = gv.zRodSpacing
		yShift = 0
		zShift = 0
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()


	def draw(self):
		try:
			App.getDocument(self.name).recompute()
			App.closeDocument(self.name)
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		#make document
		App.newDocument(self.name)
		App.setActiveDocument(self.name)
		App.ActiveDocument=App.getDocument(self.name)

		#extrude crossBarTop
		uf.extrudeFrameMember(self.name, gv.frameSpacerLength)
		
