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
import Part
import Sketcher
import Draft

#Specific to printer
import globalVars as gv
import utilityFunctions as uf


#notes
#Nut facetoface top and bottom should be resolved into a max


class XCarriage(object):
	def __init__(self):
		self.name = "xCarriage"
		
	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape= shape
		
		#Color Part

		#Rotate into correct orientation
		rotateAngle = -90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(1,0,0)
		Draft.rotate([App.ActiveDocument.xCarriage],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		rotateAngle = 180
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,1,0)
		Draft.rotate([App.ActiveDocument.xCarriage],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)
		
		#Define shifts and move the left clamp into place
		xShift = 0
		yShift = ( gv.extruderDepth
 				 - gv.extruderEdgeToCenterLine)
				 
		zShift = -gv.xCarriageBushingHolderOR
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([App.ActiveDocument.xCarriage],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		shape = App.ActiveDocument.xCarriage
		if shape not in gv.xAxisParts:
			gv.xAxisParts.append(shape)
		
	def draw(self):

		#get helper variables ready
		
		height = gv.xRodSpacing+2*gv.xCarriageBushingHolderOR #height of xCarriage face
		
		#Check to see if the part is already open
		try:
			App.getDocument(self.name).recompute()
			App.closeDocument(self.name)
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass
		
		#Make file
		App.newDocument(self.name)
		App.setActiveDocument(self.name)
		App.ActiveDocument=App.getDocument(self.name)

		#profile sketch points
		p1x = 0
		p1y = 0
		p2x = 0
		p2y = gv.xCarriageThickness+gv.xCarriageBushingHolderOR 
		p3x = gv.xCarriageBushingHolderOR
		p3y = gv.xCarriageThickness+gv.xCarriageBushingHolderOR
		#p4x = 
		#p4y = 
		p5x = 3*gv.xCarriageBushingHolderOR
		p5y = gv.xCarriageThickness+gv.xCarriageBushingHolderOR
		p6x = 3*gv.xCarriageBushingHolderOR
		p6y = gv.xCarriageThickness
		p7x = gv.xRodSpacing+2*gv.xCarriageBushingHolderOR - 3*gv.xCarriageBushingHolderOR
		p7y = gv.xCarriageThickness
		p8x = gv.xRodSpacing+2*gv.xCarriageBushingHolderOR - 3*gv.xCarriageBushingHolderOR
		p8y = gv.xCarriageThickness+gv.xCarriageBushingHolderOR
		#p9x = 
		#p9y = 
		p10x = gv.xRodSpacing+2*gv.xCarriageBushingHolderOR - gv.xCarriageBushingHolderOR
		p10y = gv.xCarriageThickness+gv.xCarriageBushingHolderOR
		p11x = gv.xRodSpacing+2*gv.xCarriageBushingHolderOR
		p11y = gv.xCarriageThickness+gv.xCarriageBushingHolderOR
		p12x = gv.xRodSpacing+2*gv.xCarriageBushingHolderOR
		p12y = 0

		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.500000,0.500000,0.500000,0.500000))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x, p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.xCarriageBushingHolderOR),0,math.pi))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.xCarriageBushingHolderOR),math.pi,1.5*math.pi))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p8x,p8y,0),App.Vector(0,0,1),gv.xCarriageBushingHolderOR),-math.pi/2,0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p10x,p10y,0),App.Vector(0,0,1),gv.xCarriageBushingHolderOR),0,math.pi))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p11x,p11y,0),App.Vector(p12x,p12y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p12x,p12y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',5,1,4,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',6,2,5,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',7,1,6,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',8,1,7,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',8,2,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,1,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,1,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',1,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',3,3,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',5,3,2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',5,2,2))
		App.ActiveDocument.recompute()		
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',6,3,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',6,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',7,2,-1)) 
		App.ActiveDocument.recompute()

		App.ActiveDocument.Sketch.toggleConstruction(2) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',7)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',1,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',5,6)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',9,1,3,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',9,2,3,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',9)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.toggleConstruction(9) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',10,1,5,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',10,2,4,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',10)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.toggleConstruction(10) 
		App.ActiveDocument.recompute()

		#Add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Distance',1,3,6,3,gv.xRodSpacing)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',1,gv.xCarriageBushingHolderOR)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Distance',4,2,8,gv.xCarriageThickness)) 
		App.getDocument(self.name).recompute()

		#pad Sketch

		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.xCarriageWidth #width of face
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
 		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#sketch profiles for cutting away extra bushing holder material

		#sketch point variables
		p1x = -height
		p1y =  gv.xBushingNutMaxThickness
		p2x = -height
		p2y =  gv.xCarriageWidth-gv.xBushingNutMaxThickness
		p3x = -(height-3*gv.xCarriageBushingHolderOR)
		p3y = gv.xCarriageWidth-gv.xBushingNutMaxThickness
		p4x = -(height-3*gv.xCarriageBushingHolderOR)
		p4y = gv.xBushingNutMaxThickness
		p5x = -3*gv.xCarriageBushingHolderOR
		p5y = (gv.xCarriageWidth-gv.xBushingNutMaxThickness)/2+gv.xBushingNutMaxThickness
		p6x = -3*gv.xCarriageBushingHolderOR
		p6y = gv.xCarriageWidth
		p7x = 0
		p7y = gv.xCarriageWidth
		p8x = 0
		p8y = (gv.xCarriageWidth-gv.xBushingNutMaxThickness)/2+gv.xBushingNutMaxThickness
		p9x =  -3*gv.xCarriageBushingHolderOR
		p9y = 0
		p10x =  -3*gv.xCarriageBushingHolderOR
		p10y = (gv.xCarriageWidth-gv.xBushingNutMaxThickness)/2
		p11x = 0
		p11y = (gv.xCarriageWidth-gv.xBushingNutMaxThickness)/2
		p12x = 0
		p12y = 0
		p13x = -(height-3*gv.xCarriageBushingHolderOR)
		p13y = gv.xCarriageWidth
		p14x = -(height-3*gv.xCarriageBushingHolderOR)
		p14y = 0

		#make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		

		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
															gv.xCarriageWidth/2,0,
															None,None, 
															gv.xCarriageThickness,0)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad,
 																  gv.xCarriageWidth/2,0,
 																  height,0,
 																  gv.xCarriageThickness,1))#"Edge17")
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
 																  gv.xCarriageWidth/2,0,
 																  height-3*gv.xCarriageBushingHolderOR,0,
 																  gv.xCarriageThickness,0))#"Edge11")
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
 																  gv.xCarriageWidth/2,0,
 																  3*gv.xCarriageBushingHolderOR,0,
 																  gv.xCarriageThickness,0))#"Edge8")
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',0)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',3)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-4))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',5,2,6,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',6,2,7,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',7,2,4,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',4)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',6)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',5)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',7)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',4,1,-5)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',4,2,-5,2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',5,2,-2)) 
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p9x,p9y+2,0),App.Vector(p10x,p10y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p10x,p10y,0),App.Vector(p11x,p11y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p11x,p11y,0),App.Vector(p12x,p12y+2,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p12x,p12y+2,0),App.Vector(p9x,p9y+2,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',8,2,9,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',9,2,10,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',10,2,11,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',11,2,8,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',8)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',10)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',9)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',11))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',8,1,-1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',-5,1,8,1))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',6,10)) 
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p13x,p13y+5,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',12,1,-4,2))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',12,2,1,2))
		App.ActiveDocument.Sketch001.toggleConstruction(12) 
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p14x,p14y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',13,1,2,2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',13,2,-4,1)) 
		App.ActiveDocument.Sketch001.toggleConstruction(13) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',12,13)) 
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p10x,p10y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',14,1,4,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',14,2,8,2)) 
		App.ActiveDocument.Sketch001.toggleConstruction(14) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',13,14)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',9,2,-2))

		#Add dimmensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',6,2,9,2,gv.xBushingNutMaxThickness+gv.bushingNutPadding))
		App.getDocument(self.name).recompute()


		#Make cut to remove excess bushing holder material. Through all option
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.getDocument(self.name).getObject("Pocket").Reversed = True
		App.ActiveDocument.recompute()

		#Refine Shape
		App.ActiveDocument.addObject('Part::Feature','Pocket001').Shape=App.ActiveDocument.Pocket.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pocket001.Label

		App.ActiveDocument.recompute()


		#cut hole for top x axis rod

		#Sketch points
		p1x = height-gv.xCarriageBushingHolderOR
		p1y = gv.xCarriageThickness+gv.xCarriageBushingHolderOR

		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket001,
															gv.xCarriageWidth,0, 
															None,None, 
															None,None) 
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch002.addExternal("Pocket001",uf.getEdge(App.ActiveDocument.Pocket001,
 																  gv.xCarriageWidth,0,
 																  None,None,
 																  gv.xCarriageThickness+gv.xCarriageBushingHolderOR,1))
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.xRodDiaTop/2+1))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,3,-3,3)) 
		App.ActiveDocument.recompute()

		#add dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',0,gv.xRodDiaTop/2+1))#top rod dia with 1mm gap around it
		App.getDocument(self.name).recompute()

		#Cut hole through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket002")
		App.activeDocument().Pocket002.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket002.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket002.Length = 5.000000
		App.ActiveDocument.Pocket002.Type = 1
		App.ActiveDocument.Pocket002.UpToFace = None
		App.ActiveDocument.recompute()

		#cut hole for bottom x axis rod

		#Sketch points
		p1x = gv.xCarriageBushingHolderOR
		p1y = gv.xCarriageThickness+gv.xCarriageBushingHolderOR

		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
		App.activeDocument().Sketch003.Support = uf.getFace(App.ActiveDocument.Pocket002,
															(gv.xCarriageWidth+gv.xBushingNutMaxThickness+gv.bushingNutPadding)/2,0, 
															None, None,
															None, None)# (App.ActiveDocument.Pocket002,["Face6"])
		App.activeDocument().recompute()

		#xCarriage chokes Here
		App.ActiveDocument.Sketch003.addExternal("Pocket002",uf.getEdge(App.ActiveDocument.Pocket002,
 																  gv.xCarriageWidth/2,1,
 																  gv.xCarriageBushingHolderOR,0,
 																  gv.xCarriageThickness+gv.xCarriageBushingHolderOR,1))
 		
		App.ActiveDocument.Sketch003.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.xRodDiaBottom/2+1))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',0,3,-3,3))

		#add dimensions
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Radius',0,gv.xRodDiaBottom/2+1))
		App.getDocument(self.name).recompute()

		#make cut through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket003")
		App.activeDocument().Pocket003.Sketch = App.activeDocument().Sketch003
		App.activeDocument().Pocket003.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket003.Length = 5.000000
		App.ActiveDocument.Pocket003.Type = 1
		App.ActiveDocument.Pocket003.UpToFace = None
		App.ActiveDocument.recompute()

		#Cut out bushing nut trap

		#sketch points
		#sketch points
		mat = uf.hexagonPoints(height-gv.xCarriageBushingHolderOR,
							gv.xCarriageThickness+gv.xCarriageBushingHolderOR,
							gv.xBushingNutTop[2],
							math.pi/6)

		p1x = mat[0][0] 
		p1y = mat[0][1]
		p2x = mat[1][0]
		p2y = mat[1][1]
		p3x = mat[2][0]
		p3y = mat[2][1]
		p4x = mat[3][0]
		p4y = mat[3][1]
		p5x = mat[4][0]
		p5y = mat[4][1]
		p6x = mat[5][0]
		p6y = mat[5][1]
		p7x = mat[6][0]
		p7y = mat[6][1]
		hexRadius = mat[7][0]
		#make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch004')
		App.activeDocument().Sketch004.Support = uf.getFace(App.ActiveDocument.Pocket003,
															gv.xCarriageWidth,0, 
															None,None, 
															None,None) #(App.ActiveDocument.Pocket003,["Face7"])
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch004.addExternal("Pocket003",uf.getEdge(App.ActiveDocument.Pocket003,
 																  gv.xCarriageWidth,0,
 																  None,None,
 																  gv.xCarriageThickness+gv.xCarriageBushingHolderOR,1))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),hexRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('PointOnObject',0,1,6)) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('PointOnObject',0,2,6)) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('PointOnObject',1,2,6)) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('PointOnObject',2,2,6)) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('PointOnObject',3,2,6)) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('PointOnObject',4,2,6)) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Equal',5,0)) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Equal',3,4)) 
		App.ActiveDocument.Sketch004.toggleConstruction(6) 
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',-3,3,6,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Distance',0,2,4,gv.xBushingNutTop[2])) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#make Pocket
		App.activeDocument().addObject("PartDesign::Pocket","Pocket004")
		App.activeDocument().Pocket004.Sketch = App.activeDocument().Sketch004
		App.activeDocument().Pocket004.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket004.Length = gv.xBushingNutTop[3] #nut thickness top
		App.ActiveDocument.Pocket004.Type = 0
		App.ActiveDocument.Pocket004.UpToFace = None
		App.ActiveDocument.recompute()

		#cut nut trap on other top bushing holder
		#sketch points
		mat = uf.hexagonPoints(-height+gv.xCarriageBushingHolderOR,
							gv.xCarriageThickness+gv.xCarriageBushingHolderOR,
							gv.xBushingNutTop[2],
							math.pi/6)

		p1x = mat[0][0] 
		p1y = mat[0][1]
		p2x = mat[1][0]
		p2y = mat[1][1]
		p3x = mat[2][0]
		p3y = mat[2][1]
		p4x = mat[3][0]
		p4y = mat[3][1]
		p5x = mat[4][0]
		p5y = mat[4][1]
		p6x = mat[5][0]
		p6y = mat[5][1]
		p7x = mat[6][0]
		p7y = mat[6][1]
		hexRadius = mat[7][0]
		#make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch005')
		App.activeDocument().Sketch005.Support = uf.getFace(App.ActiveDocument.Pocket004,
															0,0, 
															None,None, 
															None,None)#(App.ActiveDocument.Pocket004,["Face2"])
		App.activeDocument().recompute()

		App.ActiveDocument.Sketch005.addExternal("Pocket004",uf.getEdge(App.ActiveDocument.Pocket004, 
 																  0,0,
 																  None, None,
 																  gv.xCarriageThickness+gv.xCarriageBushingHolderOR,1,
 																  radius = gv.xCarriageBushingHolderOR))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),hexRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',0,1,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',0,2,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',1,2,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',2,2,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',3,2,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',4,2,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Equal',5,0)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Equal',3,4)) 
		App.ActiveDocument.Sketch005.toggleConstruction(6) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',-3,3,6,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Distance',0,2,4,gv.xBushingNutTop[2])) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#make pocket for second bushing nut trap
		App.activeDocument().addObject("PartDesign::Pocket","Pocket005")
		App.activeDocument().Pocket005.Sketch = App.activeDocument().Sketch005
		App.activeDocument().Pocket005.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket005.Length = gv.xBushingNutTop[3]
		App.ActiveDocument.Pocket005.Type = 0
		App.ActiveDocument.Pocket005.UpToFace = None
		App.ActiveDocument.recompute()


		#Make pocket for lower bushing nut
		#sketch points
		mat = uf.hexagonPoints(gv.xCarriageBushingHolderOR,
							gv.xCarriageThickness+gv.xCarriageBushingHolderOR,
							gv.xBushingNutBottom[2],
							math.pi/6)

		p1x = mat[0][0] 
		p1y = mat[0][1]
		p2x = mat[1][0]
		p2y = mat[1][1]
		p3x = mat[2][0]
		p3y = mat[2][1]
		p4x = mat[3][0]
		p4y = mat[3][1]
		p5x = mat[4][0]
		p5y = mat[4][1]
		p6x = mat[5][0]
		p6y = mat[5][1]
		p7x = mat[6][0]
		p7y = mat[6][1]
		hexRadius = mat[7][0]
		#make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch006')
		App.activeDocument().Sketch006.Support = uf.getFace(App.ActiveDocument.Pocket005,
															(gv.xCarriageWidth+gv.xBushingNutMaxThickness+gv.bushingNutPadding)/2,0, 
															None,None, 
															None,None)# (App.ActiveDocument.Pocket005,["Face6"])
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch006.addExternal("Pocket005",uf.getEdge(App.ActiveDocument.Pocket005,
 																  gv.xCarriageWidth/2,1,
 																  gv.xCarriageBushingHolderOR,0,
 																  gv.xCarriageThickness+gv.xCarriageBushingHolderOR,1))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),hexRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('PointOnObject',0,1,6)) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('PointOnObject',0,2,6)) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('PointOnObject',1,2,6)) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('PointOnObject',2,2,6)) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('PointOnObject',3,2,6)) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('PointOnObject',4,2,6)) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Equal',5,0)) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Equal',3,4)) 
		App.ActiveDocument.Sketch006.toggleConstruction(6) 
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Coincident',-3,3,6,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Distance',0,2,4,gv.xBushingNutBottom[2])) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#make pocket for second bushing nut trap
		App.activeDocument().addObject("PartDesign::Pocket","Pocket006")
		App.activeDocument().Pocket006.Sketch = App.activeDocument().Sketch006
		App.activeDocument().Pocket006.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket006.Length = gv.xBushingNutBottom[3]
		App.ActiveDocument.Pocket006.Type = 0
		App.ActiveDocument.Pocket006.UpToFace = None
		App.ActiveDocument.recompute()


		#Make extruder mounting holes
		#sketch points
		p1x = 0
		p1y = gv.xCarriageMountHoleVertOffset
		p2x = gv.xCarriageMountHoleHorizOffset
		p2y = p1y
		p3x = gv.xCarriageWidth-gv.xCarriageMountHoleHorizOffset
		p3y = p1y
		p4x = gv.xCarriageWidth
		p4y = p1y
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch007')
		App.activeDocument().Sketch007.Support = uf.getFace(App.ActiveDocument.Pocket006,
															None,None, 
															None,None, 
															gv.xCarriageThickness,0)#(App.ActiveDocument.Pocket006,["Face3"])
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch007.addExternal("Pocket006",uf.getEdge(App.ActiveDocument.Pocket006,
 																  gv.xCarriageWidth,0,
 																  height/2,-1,
 																  gv.xCarriageThickness,0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Equal',1,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('PointOnObject',1,2,0)) 
		App.ActiveDocument.Sketch007.toggleConstruction(0) 
		App.ActiveDocument.Sketch007.toggleConstruction(1) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Coincident',2,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Coincident',3,3,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Radius',2,gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,1,gv.xCarriageMountHoleVertOffset)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('DistanceX',0,gv.xCarriageMountHoleHorizOffset)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#Make cut through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket007")
		App.activeDocument().Pocket007.Sketch = App.activeDocument().Sketch007
		App.activeDocument().Pocket007.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket007.Length = 5.000000
		App.ActiveDocument.Pocket007.Type = 1
		App.ActiveDocument.Pocket007.UpToFace = None
		App.ActiveDocument.recompute()


		#Make wings on sides of xCarriage
		#Sketch Points
		p1x = 0
		p1y = -height+gv.xCarriageWingHeight
		p2x = 0
		p2y = -height
		p3x = -gv.xCarriageWingWidth
		p3y = p2y
		p4x = gv.xCarriageWidth
		p4y = -height+gv.xCarriageWingHeight
		p5x = gv.xCarriageWidth+gv.xCarriageWingWidth
		p5y = p2y
		p6x = gv.xCarriageWidth
		p6y = p2y

		#Make Sketch of endstop wings
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch008')
		App.activeDocument().Sketch008.Support = uf.getFace(App.ActiveDocument.Pocket007,
															None,None, 
															None,None, 
															0,0)#(App.ActiveDocument.Pocket007,["Face8"])
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch008.addExternal("Pocket007",uf.getEdge(App.ActiveDocument.Pocket007,
 																  gv.xCarriageWidth,0,
 																  height/2,0,
 																  0,0))
		App.ActiveDocument.Sketch008.addExternal("Pocket007",uf.getEdge(App.ActiveDocument.Pocket007, 
 																  gv.xCarriageWidth/2,0,
 																  height,0,
 																  0,0))
		App.ActiveDocument.Sketch008.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-2)) 
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Coincident',0,2,-4,1)) 
		App.ActiveDocument.Sketch008.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch008.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Coincident',2,2,0,1)) 
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Horizontal',1))
		App.ActiveDocument.Sketch008.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('PointOnObject',3,1,-3)) 
		App.ActiveDocument.Sketch008.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Coincident',4,2,-4,2)) 
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.Sketch008.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Coincident',5,2,3,1)) 
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Equal',0,5)) 
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Equal',1,4)) 

		#add dimensions
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('DistanceX',4,-gv.xCarriageWingWidth)) 
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('DistanceY',5,gv.xCarriageWingHeight))
		App.getDocument(self.name).recompute()

		#Pad to thickness of xCarriage face
		App.activeDocument().addObject("PartDesign::Pad","Pad001")
		App.activeDocument().Pad001.Sketch = App.activeDocument().Sketch008
		App.activeDocument().Pad001.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad001.Length = gv.xCarriageThickness #thickness of xCarriage face
		App.ActiveDocument.Pad001.Reversed = 1
		App.ActiveDocument.Pad001.Midplane = 0
		App.ActiveDocument.Pad001.Length2 = 100.000000
		App.ActiveDocument.Pad001.Type = 0
		App.ActiveDocument.Pad001.UpToFace = None
		App.ActiveDocument.recompute()

		#Refine Shape
		App.ActiveDocument.addObject('Part::Feature','Pad002').Shape=App.ActiveDocument.Pad001.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pad002.Label
		App.ActiveDocument.recompute()
		
		#Make Belt Anchor
		#Sketch Points
		p1x = 0
		p1y = gv.xCarriageBushingHolderOR+gv.xRodSpacing/2+gv.xMotorPulleyDia/2-gv.xBeltAnchorThickness/2
		p2x = p1x
		p2y = p1y+gv.xBeltAnchorThickness
		p3x = gv.xCarriageWidth
		p3y = p2y
		p4x = p3x
		p4y = p1y

		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch009')
		App.activeDocument().Sketch009.Support = uf.getFace(App.ActiveDocument.Pad002,
															gv.xCarriageWidth/2,0, 
															None,None, 
															gv.xCarriageThickness,0)#(App.ActiveDocument.Pad002,["Face3"])
		App.activeDocument().recompute()
		#App.ActiveDocument.Sketch009.addExternal("Pad002","Edge30")

		App.ActiveDocument.Sketch009.addExternal("Pad002",uf.getEdge(App.ActiveDocument.Pad002, 
 																  gv.xCarriageWidth,0,
 																  height/2,-1,
 																  gv.xCarriageThickness,0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch009.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch009.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch009.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p1x,p1y,0)))
		
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-3)) 
		App.ActiveDocument.recompute()
	
		#Add Dimensions
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('DistanceY',1,gv.xBeltAnchorThickness)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,p1y)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Extrude Anchor Block
		App.activeDocument().addObject("PartDesign::Pad","Pad003")
		App.activeDocument().Pad003.Sketch = App.activeDocument().Sketch009
		App.activeDocument().Pad003.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad003.Length = gv.xBeltAnchorHeight
		App.ActiveDocument.Pad003.Reversed = 0
		App.ActiveDocument.Pad003.Midplane = 0
		App.ActiveDocument.Pad003.Length2 = 100.000000
		App.ActiveDocument.Pad003.Type = 0
		App.ActiveDocument.Pad003.UpToFace = None
		App.ActiveDocument.recompute()

		#Refine Shape
		App.ActiveDocument.addObject('Part::Feature','Pad004').Shape=App.ActiveDocument.Pad003.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pad004.Label

		App.ActiveDocument.recompute()
		
		#Cut away material between columns
		p1x = -gv.xCarriageWidth+gv.xBeltAnchorWidthBottom
		p1y = gv.xCarriageThickness
		p2x = -gv.xCarriageWidth+gv.xBeltAnchorWidthTop
		p2y = p1y+gv.xBeltAnchorHeight
		p3x = -gv.xBeltAnchorWidthTop
		p3y = p2y
		p4x = -gv.xBeltAnchorWidthBottom
		p4y = p1y
		p5x = -gv.xCarriageWidth/2
		p5y = p2y
		p6x = p5x
		p6y = p1y
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch010')
		App.activeDocument().Sketch010.Support = uf.getFace(App.ActiveDocument.Pad004,
															None,None, 
															gv.xCarriageBushingHolderOR+gv.xRodSpacing/2+gv.xMotorPulleyDia/2+gv.xBeltAnchorThickness/2,0, 
															None, None)#(App.ActiveDocument.Pad004,["Face43"])
		App.activeDocument().recompute()
		#App.ActiveDocument.Sketch010.addExternal("Pad004","Edge127")
		App.ActiveDocument.Sketch010.addExternal("Pad004",uf.getEdge(App.ActiveDocument.Pad004, 
 																  gv.xCarriageWidth/2,0,
 																  gv.xCarriageBushingHolderOR+gv.xRodSpacing/2+gv.xMotorPulleyDia/2+gv.xBeltAnchorThickness/2, 0,
 																  gv.xCarriageThickness+gv.xBeltAnchorHeight,0))
		App.ActiveDocument.Sketch010.addExternal("Pad004",uf.getEdge(App.ActiveDocument.Pad004, 
 																  gv.xCarriageWidth/2,0,
 																  gv.xCarriageBushingHolderOR+gv.xRodSpacing/2+gv.xMotorPulleyDia/2+gv.xBeltAnchorThickness/2, 0,
 																  gv.xCarriageThickness,0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('PointOnObject',2,2,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Point(App.Vector(p5x,p5y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Symmetric',-3,1,-3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Symmetric',0,2,1,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Point(App.Vector(p6x,p6y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Symmetric',-4,2,-4,1,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Symmetric',0,1,2,2,5,1)) 
		App.ActiveDocument.recompute()

# Anchor widths need to be changed!!!		
		#Add dimensions
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Distance',1,2,-3,2,gv.xBeltAnchorWidthTop)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('DistanceX',-2,1,2,2,-gv.xBeltAnchorWidthBottom)) 
		App.ActiveDocument.recompute()
#		App.getDocument('xCarriage').recompute()

		#Cut away excess material
		App.activeDocument().addObject("PartDesign::Pocket","Pocket008")
		App.activeDocument().Pocket008.Sketch = App.activeDocument().Sketch010
#		App.activeDocument().Pocket008.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket008.Length = gv.xBeltAnchorThickness
		App.ActiveDocument.Pocket008.Type = 0
		App.ActiveDocument.Pocket008.UpToFace = (App.ActiveDocument.Pad004,["Face23"])
		App.ActiveDocument.recompute()

		#Refine Shape
		App.ActiveDocument.addObject('Part::Feature','Pocket009').Shape=App.ActiveDocument.Pocket008.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pocket009.Label
		App.ActiveDocument.recompute()
		
		#Cut slots in Belt anchors
		#Sketch Points
		p1x = gv.xBeltAnchorSlotInset
		p1y = gv.xCarriageThickness
		p2x = p1x
		p2y = gv.xCarriageThickness+gv.xBeltAnchorHeight-gv.xBeltAnchorBridgeThickness
		p3x = p1x+gv.xBeltAnchorSlotWidth
		p3y = p2y
		p4x = p3x
		p4y = p1y
		p5x = gv.xCarriageWidth - gv.xBeltAnchorSlotInset-gv.xBeltAnchorSlotWidth
		p5y = p1y
		p6x = p5x
		p6y = p2y
		p7x = gv.xCarriageWidth - gv.xBeltAnchorSlotInset
		p7y = p2y
		p8x = p7x
		p8y = p1y
		p9x = 0
		p9y = p1y
		p10x = gv.xCarriageWidth
		p10y = p1y
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch011')
		App.activeDocument().Sketch011.Support = uf.getFace(App.ActiveDocument.Pocket009,
															gv.xCarriageWidth/2,-1, 
															gv.xCarriageBushingHolderOR+gv.xRodSpacing/2+gv.xMotorPulleyDia/2-gv.xBeltAnchorThickness/2,0, 
															None, None)#(App.ActiveDocument.Pocket009,["Face32"])	

		App.activeDocument().recompute()
		App.ActiveDocument.Sketch011.addExternal("Pocket009",uf.getEdge(App.ActiveDocument.Pocket009,
 																  gv.xBeltAnchorWidthTop/2,0,
 																  gv.xCarriageBushingHolderOR+gv.xRodSpacing/2+gv.xMotorPulleyDia/2-gv.xBeltAnchorThickness/2, 0,
 																  gv.xCarriageThickness+gv.xBeltAnchorHeight,0))
		App.ActiveDocument.Sketch011.addExternal("Pocket009",uf.getEdge(App.ActiveDocument.Pocket009, 
 																  gv.xCarriageWidth/2,-1,
 																  0, 0,
 																  gv.xCarriageThickness,0))
		App.ActiveDocument.Sketch011.addExternal("Pocket009",uf.getEdge(App.ActiveDocument.Pocket009, 
 																  gv.xCarriageWidth-gv.xBeltAnchorWidthTop/2,0,
 																  gv.xCarriageBushingHolderOR+gv.xRodSpacing/2+gv.xMotorPulleyDia/2-gv.xBeltAnchorThickness/2, 0,
 																  gv.xCarriageThickness+gv.xBeltAnchorHeight,0))
		App.ActiveDocument.Sketch011.addExternal("Pocket009",uf.getEdge(App.ActiveDocument.Pocket009, 
 																  gv.xCarriageWidth/2,1,
 																  0, 0,
 																  gv.xCarriageThickness,0))

		App.ActiveDocument.Sketch011.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch011.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch011.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch011.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.Sketch011.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.Sketch011.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch011.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',5,2,6,1)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',6,2,7,1)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',7,2,4,1)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Horizontal',6)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Vertical',5)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Vertical',7)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('PointOnObject',4,1,-6)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addGeometry(Part.Line(App.Vector(p9x,p9y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',8,1,-4,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',8,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addGeometry(Part.Line(App.Vector(p10x,p10y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',9,1,-6,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Coincident',9,2,4,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Equal',8,9)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.toggleConstruction(8) 
		App.ActiveDocument.Sketch011.toggleConstruction(9) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('PointOnObject',6,2,2)) 
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Equal',2,6)) 
		App.ActiveDocument.recompute()
				
		#Add Dimensions
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('DistanceX',-1,1,2,2,gv.xBeltAnchorSlotInset)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('DistanceX',2,-gv.xBeltAnchorSlotWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch011.addConstraint(Sketcher.Constraint('Distance',2,2,-3,gv.xBeltAnchorBridgeThickness)) 
		App.ActiveDocument.recompute()
		App.getDocument('xCarriage').recompute()
		
		#Cut slots
		App.activeDocument().addObject("PartDesign::Pocket","Pocket010")
		App.activeDocument().Pocket010.Sketch = App.activeDocument().Sketch011
		App.activeDocument().Pocket010.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket010.Length = gv.xBeltAnchorThickness
		App.ActiveDocument.Pocket010.Type = 0
		App.ActiveDocument.Pocket010.UpToFace = None
		App.ActiveDocument.recompute()

		#Refine Shape
		App.ActiveDocument.addObject('Part::Feature','Pocket011').Shape=App.ActiveDocument.Pocket010.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pocket011.Label
		App.ActiveDocument.recompute()


		#set View as axometric

