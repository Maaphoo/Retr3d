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
import FreeCADGui as Gui
import Part
import Sketcher
import Draft

#Specific to printer
import globalVars as gv
import utilityFunctions as uf

class YBeltAnchor(object):
	def __init__(self):
		self.name = "yBeltAnchor"

	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Gui.ActiveDocument=Gui.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape= shape
		
		#Color Part
		Gui.ActiveDocument.getObject(self.name).ShapeColor = (gv.printedR,gv.printedG,gv.printedB,gv.printedA)
		
		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name)
		shape = objs[-1]		
		
		#Rotate into correct orientation
		rotateAngle = 180
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(1,0,0)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Rotate into correct orientation
		rotateAngle = 90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,0,1)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = gv.yMotorPulleyDia/2
		yShift = 0
		zShift = gv.PBBHStandoff
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()

		if shape not in gv.yAxisParts:
			gv.yAxisParts.append(shape)
			
		
	def draw(self):

		#helper Variables
		#Find the widest component of the anchor and set the width to that
		baseWidth = (gv.printedToPrintedDia+2*gv.mountToPrintedPadding
					if gv.printedToPrintedDia+2*gv.mountToPrintedPadding
					> gv.yBeltAnchorWidth else gv.yBeltAnchorWidth)
		baseLength = (gv.yBeltAnchorLength	
					+2*gv.printedToPrintedDia
					+4*gv.mountToPrintedPadding)
		

		#Make file and build part
		try:
			Gui.getDocument("yBeltAnchor")
			Gui.getDocument("yBeltAnchor").resetEdit()
			App.getDocument("yBeltAnchor").recompute()
			App.closeDocument("yBeltAnchor")
			App.setActiveDocument("")
			App.ActiveDocument=None
			Gui.ActiveDocument=None	
		except:
			pass

		#Create Document
		App.newDocument("yBeltAnchor")
		App.setActiveDocument("yBeltAnchor")
		App.ActiveDocument=App.getDocument("yBeltAnchor")
		Gui.ActiveDocument=Gui.getDocument("yBeltAnchor")

		#Make base
		#Sketch points
		p1x = -baseLength/2
		p1y = -baseWidth/2
		p2x = -baseLength/2
		p2y = baseWidth/2
		p3x = baseLength/2
		p3y = baseWidth/2
		p4x = baseLength/2
		p4y = -baseWidth/2
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
		Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
#		Gui.activeDocument().setEdit('Sketch')
		
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
		
		#add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,baseWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',0,baseLength)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument("yBeltAnchor").resetEdit()
		App.getDocument("yBeltAnchor").recompute()
		
		#Pad base
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch")
		App.ActiveDocument.Pad.Length = gv.tabThickness
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		
		#Cut hole on right side
		#Sketch points
		p1x = gv.yBeltAnchorLength/2+gv.mountToPrintedPadding+gv.printedToPrintedDia/2
		p1y = 0
		
		#Make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
														  0,0,
														  0, 0,
														  gv.tabThickness, 0)
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch001')
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',0,gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,p1x)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument('yBeltAnchor').resetEdit()
		App.getDocument('yBeltAnchor').recompute()
		
		#Cut hole through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch001")
		Gui.activeDocument().hide("Pad")
#		Gui.ActiveDocument.Pocket.ShapeColor=Gui.ActiveDocument.Pad.ShapeColor
#		Gui.ActiveDocument.Pocket.LineColor=Gui.ActiveDocument.Pad.LineColor
#		Gui.ActiveDocument.Pocket.PointColor=Gui.ActiveDocument.Pad.PointColor
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		
		#Mirror the hole
		App.activeDocument().addObject("PartDesign::Mirrored","Mirrored")
		App.ActiveDocument.recompute()
		App.activeDocument().Mirrored.Originals = [App.activeDocument().Pocket,]
		App.activeDocument().Mirrored.MirrorPlane = (App.activeDocument().Sketch001, ["V_Axis"])
		Gui.activeDocument().Pocket.Visibility=False
#		Gui.ActiveDocument.Mirrored.ShapeColor=Gui.ActiveDocument.Pocket.ShapeColor
#		Gui.ActiveDocument.Mirrored.DisplayMode=Gui.ActiveDocument.Pocket.DisplayMode
		
		#Make the column
		#Sketch points
		p1x = -gv.yBeltAnchorWidth/2
		p1y = -gv.yBeltAnchorLength/2
		p2x = -gv.yBeltAnchorWidth/2
		p2y = gv.yBeltAnchorLength/2
		p3x = gv.yBeltAnchorWidth/2
		p3y = gv.yBeltAnchorLength/2
		p4x = gv.yBeltAnchorWidth/2
		p4y = -gv.yBeltAnchorLength/2
		
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().recompute()
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Mirrored,
														  0,0,
														  0, 0,
														  gv.tabThickness, 0)
		
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch002')
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Symmetric',1,2,0,1,-1,1)) 
		App.ActiveDocument.recompute()
		
		#Add Dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceY',1,gv.yBeltAnchorWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceX',2,-gv.yBeltAnchorLength)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument('yBeltAnchor').resetEdit()
		App.getDocument('yBeltAnchor').recompute()
		
		#Extrude column
		App.activeDocument().addObject("PartDesign::Pad","Pad001")
		App.activeDocument().Pad001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pad001.Length = 10.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch002")
		Gui.activeDocument().hide("Mirrored")
#		Gui.ActiveDocument.Pad001.ShapeColor=Gui.ActiveDocument.Mirrored.ShapeColor
#		Gui.ActiveDocument.Pad001.LineColor=Gui.ActiveDocument.Mirrored.LineColor
#		Gui.ActiveDocument.Pad001.PointColor=Gui.ActiveDocument.Mirrored.PointColor
		App.ActiveDocument.Pad001.Length = gv.yBeltAnchorHeight-gv.tabThickness
		App.ActiveDocument.Pad001.Reversed = 0
		App.ActiveDocument.Pad001.Midplane = 0
		App.ActiveDocument.Pad001.Length2 = 100.000000
		App.ActiveDocument.Pad001.Type = 0
		App.ActiveDocument.Pad001.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		
		#Cut slot in column
		#Sketch Points
		p1x = -gv.yBeltAnchorSlotWidth/2
		p1y = gv.tabThickness
		p2x = -gv.yBeltAnchorSlotWidth/2
		p2y = gv.yBeltAnchorHeight-gv.yBeltAnchorBridgeThickness
		p3x = gv.yBeltAnchorSlotWidth/2
		p3y = gv.yBeltAnchorHeight-gv.yBeltAnchorBridgeThickness
		p4x = gv.yBeltAnchorSlotWidth/2
		p4y = gv.tabThickness
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
		App.activeDocument().recompute()
		App.activeDocument().Sketch003.Support = uf.getFace(App.ActiveDocument.Pad001,
												  None, None,
												  -gv.yBeltAnchorWidth/2, 0,
												  None, None)
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch003')
		App.ActiveDocument.Sketch003.addExternal("Pad001",uf.getEdge(App.ActiveDocument.Pad001, 
														  0,0,
														  -gv.yBeltAnchorWidth/2, 0,
														  gv.tabThickness,0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Symmetric',1,2,2,2,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addExternal("Pad001","Edge1")
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Distance',1,2,-4,gv.yBeltAnchorBridgeThickness)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('DistanceX',0,gv.yBeltAnchorSlotWidth)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument('yBeltAnchor').resetEdit()
		App.getDocument('yBeltAnchor').recompute()
		
		#Cut Slot through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch003
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch003")
		Gui.activeDocument().hide("Pad001")
#		Gui.ActiveDocument.Pocket001.ShapeColor=Gui.ActiveDocument.Pad001.ShapeColor
#		Gui.ActiveDocument.Pocket001.LineColor=Gui.ActiveDocument.Pad001.LineColor
#		Gui.ActiveDocument.Pocket001.PointColor=Gui.ActiveDocument.Pad001.PointColor
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		
		#Refine Shape
		App.ActiveDocument.addObject('Part::Feature','Pocket001').Shape=App.ActiveDocument.Pocket001.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pocket001.Label
		Gui.ActiveDocument.Pocket001.hide()
#		Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Pocket001.ShapeColor
#		Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Pocket001.LineColor
#		Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Pocket001.PointColor
		App.ActiveDocument.recompute()

		#Make view axiometric
#		Gui.activeDocument().activeView().viewAxometric()