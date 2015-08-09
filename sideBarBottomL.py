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

class SideBarBottomL(object):
	def __init__(self):
		self.name = "sideBarBottomL"
		
	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape= shape
		
		#Color Part

		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name)
		shape = objs[-1]		
		
		#Rotate into correct orientation
		rotateAngle = 90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,0,1)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = -gv.zRodSpacing/2
		yShift = -gv.yRodLength/2 + gv.frameWidth
		zShift = -gv.yRodStandoff - gv.frameHeight/2 - gv.frameSpacerLength - gv.frameHeight
		
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

		#extrude crossBarBottom
		uf.extrudeFrameMember(self.name, gv.sideBarLength)
		
		#Make mounting holes for feet
		#Sketch points
		x1 = 0
		y1 = 0
		x2 = 0
		y2 = 2*gv.frameSpacerOffset+gv.frameHeight
		x3 = 0
		y3 = gv.sideBarLength
		x4 = 0
		y4 = gv.sideBarLength-y2

		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
															None, None, 
															None, None, 
															gv.frameHeight/2, 0)

		App.activeDocument().recompute()
# 		Gui.activeDocument().setEdit('Sketch001')
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad,
 																  gv.sideBarLength,0,
 																  0,0,
 																  gv.frameHeight/2,0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(x1,y1,0),App.Vector(x2,y2,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(x3,y3,0),App.Vector(x4,y4,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',1,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',-1,1,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',1,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.toggleConstruction(1) 
		App.ActiveDocument.Sketch001.toggleConstruction(0) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(x2,y2,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(x4,y4,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,3,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',3,2)) 
		App.ActiveDocument.recompute()
		
		#add Dimmensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',0,y2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',2,gv.mountToFrameDia/2)) 
		App.ActiveDocument.recompute()
# 		Gui.getDocument('sideBarBottomL').resetEdit()
		
		#Cut Pocket
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.ActiveDocument.recompute()
		# Gui.activeDocument().hide("Sketch001")
		# Gui.activeDocument().hide("Pad")
		# Gui.activeDocument().setEdit('Pocket')
# 		Gui.ActiveDocument.Pocket.ShapeColor=Gui.ActiveDocument.Pad.ShapeColor
# 		Gui.ActiveDocument.Pocket.LineColor=Gui.ActiveDocument.Pad.LineColor
# 		Gui.ActiveDocument.Pocket.PointColor=Gui.ActiveDocument.Pad.PointColor
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()
# 		Gui.activeDocument().resetEdit()