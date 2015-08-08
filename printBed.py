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
import utilityFunctions as Util

class PrintBed(object):
	def __init__(self):
		self.name = "printBed"

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
# 		rotateAngle = 0
# 		rotateCenter = App.Vector(0,0,0)
# 		rotateAxis = App.Vector(1,0,0)
# 		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = 0
		yShift = 0
		zShift = gv.PBBHStandoff+gv.printBedSupportThickness+gv.printBedStandoff
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()

		if shape not in gv.yAxisParts:
			gv.yAxisParts.append(shape)
			
		
	def draw(self):
		#helper Variables
		width = gv.printableWidth + gv.printBedPadding
		length = gv.printableLength + gv.printBedPadding
		
		#Make file and build part
		try:
			App.getDocument("printBed").recompute()
			App.closeDocument("printBed")
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		#Create Document
		App.newDocument("printBed")
		App.setActiveDocument("printBed")
		App.ActiveDocument=App.getDocument("printBed")

		#make plate
		#Sketch points
		p1x = -width/2
		p1y = -length/2
		p2x = -width/2
		p2y = length/2
		p3x = width/2
		p3y = length/2
		p4x = width/2
		p4y = -length/2
		p5x = -(width/2-gv.printBedMountHolePadding)
		p5y = -(length/2-gv.printBedMountHolePadding)
		p6x = -(width/2-gv.printBedMountHolePadding)
		p6y = (length/2-gv.printBedMountHolePadding)
		p7x = (width/2-gv.printBedMountHolePadding)
		p7y = (length/2-gv.printBedMountHolePadding)
		p8x = (width/2-gv.printBedMountHolePadding)
		p8y = -(length/2-gv.printBedMountHolePadding)
		p9x = (width/2-gv.printBedMountHolePadding)
		p9y = length/2
		p10x = width/2
		p10y = (length/2-gv.printBedMountHolePadding)
		
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
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',1,2,0,1,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',5,2,6,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',6,2,7,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',7,2,4,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',6)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',5)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',7)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p9x,p9y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',8,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',8,2,5,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p10x,p10y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',8,2,9,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',9,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',9)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',8))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',8,9)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.movePoint(4,0,App.Vector(0.000000,0.000000,0),1)
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.toggleConstruction(6) 
		App.ActiveDocument.Sketch.toggleConstruction(5) 
		App.ActiveDocument.Sketch.toggleConstruction(7) 
		App.ActiveDocument.Sketch.toggleConstruction(4) 
		App.ActiveDocument.Sketch.toggleConstruction(8) 
		App.ActiveDocument.Sketch.toggleConstruction(9) 
		
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(p6x,p6y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',10,3,6,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',11,3,5,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',12,3,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(p8x,p8y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',13,3,4,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',13,12)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',12,10)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',10,11)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',5,2,4,1,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,length)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',0,width)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',9,gv.printBedMountHolePadding+gv.mountToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',10,gv.mountToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.movePoint(4,1,App.Vector(-37.291931,-32.210766,0),0)
		App.ActiveDocument.recompute()

		App.getDocument('printBed').recompute()
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.printBedThickness
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#Make view axiometric
