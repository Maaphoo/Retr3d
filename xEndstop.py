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

class XEndstop(object):
	def __init__(self):
		self.name = "xEndstop"
		
	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		endstop = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape= endstop
		
		#Color Part

		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name)
		endstop = objs[-1]		

		#Add cap to assembly
		App.ActiveDocument=App.getDocument(self.name+"Cap")
		cap = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name+"Cap").Shape= cap
		
		#Color Part

		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name+"Cap")
		cap = objs[-1]		
		
		#Define shifts and move the left clamp into place
		xShift = 0
		yShift = 0
		zShift = gv.xEndstopHeight
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([cap],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		endstopAndCap = [endstop,cap]
		
		#Rotate endstop and cap into correct orientation
		rotateAngle = 90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(1,0,0)
		Draft.rotate(endstopAndCap,rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move into place
		xShift = (-gv.xRodLength/2
				 - gv.xRodClampWidth
				 + gv.xRodClampPocketDepth
				 + gv.xRodClampWidth
				 - gv.xRodClampMountHoleToEdgePadding
				 - gv.printedToPrintedDia/2)
		yShift = (gv.extruderNozzleStandoff 
				- gv.zRodStandoff
				- gv.xEndZRodHolderFaceThickness
				- gv.xEndZRodHolderMaxNutFaceToFace/2
				- gv.xMotorMountPlateThickness
				- 2*gv.xRodClampThickness
				- gv.xRodDiaMax)
		zShift = gv.xRodSpacing - gv.xRodAxisToMountHoleDist
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move(endstopAndCap,App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
 		
 		if endstop not in gv.xAxisParts:
			gv.xAxisParts.append(endstop)	
 		if cap not in gv.xAxisParts:
			gv.xAxisParts.append(cap)				

	def draw(self):
		#Helper variables
		width = 2*gv.xEndstopPadding+2*gv.xEndstopChannelWidth + gv.xEndstopContactSpacing
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

		#Sketch Points
		p1x = -(width/2)
		p1y = -(gv.printedToPrintedDia/2+gv.xEndstopPadding)
		p2x = p1x
		p2y = gv.xEndstopLength+p1y
		p3x = -p1x
		p3y = p2y
		p4x = p3x
		p4y = p1y
		p5x = 0
		p5y = 0

		#make endstop body
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p1x,p1y,0)))
		
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',1,2,2,2,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4,3,-1,1)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,gv.xEndstopLength)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',0,width)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',4,gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Distance',-1,1,0,gv.xEndstopPadding+gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Pad sketch
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.xEndstopHeight
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()
		
		#Cut Channels
		#Sketch Points
		p1x = -width/2
		p1y = (gv.printedToPrintedDia/2
			 + gv.xEndstopPadding
			 + gv.xEndstopChannelWidth
			 + gv.xEndstopContactSpacing)
		p2x = p1x
		p2y = (gv.printedToPrintedDia/2
			 + gv.xEndstopPadding
			 + 2*gv.xEndstopChannelWidth
			 + gv.xEndstopContactSpacing)
		p3x = p1x+gv.xEndstopPadding
		p3y = p2y
		p4x = p3x
		p4y = gv.xEndstopLength-(gv.printedToPrintedDia/2+gv.xEndstopPadding)
		p5x = p4x+gv.xEndstopChannelWidth
		p5y = p4y
		p6x = p5x
		p6y = p1y
		p7x = p1x
		p7y = (gv.printedToPrintedDia/2
			 + gv.xEndstopPadding)
		p8x = p1x
		p8y = p7y+gv.xEndstopChannelWidth
		p9x = p6x+gv.xEndstopContactSpacing
		p9y = p8y
		p10x = p9x
		p10y = p4y
		p11x = p9x+gv.xEndstopChannelWidth
		p11y = p4y
		p12x = p11x
		p12y = p7y
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
														  None,None,
														  None, None,
														  gv.xEndstopHeight, 0)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
														  0,0,
														  0,1,
														  gv.xEndstopHeight, 0))
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
														  -width/2,0,
														  None, None,
														  gv.xEndstopHeight, 0))
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
														  width/2,0,
														  None, None,
														  gv.xEndstopHeight, 0))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',2,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',3,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',5)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',3,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',6,1,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',6,2,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p9x,p9y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',6,2,7,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',7)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p9x,p9y,0),App.Vector(p10x,p10y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',7,2,8,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',8,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',8)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p10x,p10y,0),App.Vector(p11x,p11y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',8,2,9,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',9,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p11x,p11y,0),App.Vector(p12x,p12y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',9,2,10,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',10)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p12x,p12y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',10,2,11,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',11,2,6,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',11)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',6,9)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',9,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p10x,p10y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',12,1,3,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',12,2,8,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',13,1,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',13,2,6,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.toggleConstruction(13) 
		App.ActiveDocument.Sketch001.toggleConstruction(12) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',12,13)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',0,gv.xEndstopChannelWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',13,-gv.xEndstopContactSpacing)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',-1,1,11,p7y)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',9,2,-5,2,gv.xEndstopPadding)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Cut channels
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 3.000000
		App.ActiveDocument.Pocket.Type = 0
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()

		#Make cap
		try:
			App.getDocument(self.name+"Cap").recompute()
			App.closeDocument(self.name+"Cap")
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		#make document
		App.newDocument(self.name+"Cap")
		App.setActiveDocument(self.name+"Cap")
		App.ActiveDocument=App.getDocument(self.name+"Cap")

		#Sketch Points
		p1x = -(width/2)
		p1y = -(gv.printedToPrintedDia/2+gv.xEndstopPadding)
		p2x = p1x
		p2y = gv.xEndstopLength+p1y
		p3x = -p1x
		p3y = p2y
		p4x = p3x
		p4y = p1y
		p5x = 0
		p5y = 0

		#make endstop body
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p1x,p1y,0)))
		
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',1,2,2,2,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4,3,-1,1)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,gv.xEndstopLength)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',0,width)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',4,gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Distance',-1,1,0,gv.xEndstopPadding+gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name+"Cap").recompute()
		
		#Pad sketch
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.xEndstopCapThickness
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()
