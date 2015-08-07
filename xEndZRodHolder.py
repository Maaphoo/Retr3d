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

#notes
#Should the width be determined by the nut face to face, paddings etc? At least a minimum.

class XEndZRodHolder(object):
	def __init__(self, name = "XEndZRodHolder", side = "Right"):
		self.name = name
		self.side = side #0 for Right side 1 for Left Side

	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape= shape
		
		#Color Part

		#Rotate into correct orientation
		objs = App.ActiveDocument.getObjectsByLabel(self.name)
		shape = objs[-1]
		rotateAngle = 90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(1,0,0)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		rotateAngle = 180
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,0,1)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)
		
		if self.side == "Right":
		#Define shifts and move the left clamp into place
			xShift = +gv.xRodLength/2+gv.xRodClampWidth-gv.xRodClampPocketDepth
		else:
			xShift = -gv.xRodLength/2-gv.xRodClampWidth+gv.xRodClampPocketDepth

		yShift = (gv.extruderNozzleStandoff 
				- gv.zRodStandoff
				- gv.xEndZRodHolderFaceThickness
				- gv.xEndZRodHolderMaxNutFaceToFace/2)
		zShift = 0
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		shape = App.ActiveDocument.getObject(self.name)
 		if shape not in gv.xAxisParts:
			gv.xAxisParts.append(shape)	
		
	def draw(self):
		#helper Variables
		if self.side == "Right":
			self.bushingNutFaceToFace = gv.zBushingNutR[2]
			self.bushingNutThickness = gv.zBushingNutR[3]
			self.rodDia = gv.zRodDiaR
		elif self.side == "Left":
			self.bushingNutFaceToFace = gv.zBushingNutL[2]
			self.bushingNutThickness = gv.zBushingNutL[3]
			self.rodDia = gv.zRodDiaL

		mountHoleInsetVert = (gv.xEndZRodHolderMaxNutThickness
							+gv.bushingNutPadding
							+gv.xEndZRodHolderMountHoleToRodPadding
							+gv.printedToPrintedDia/2)
							
		mountHoleInsetHoriz = gv.xEndZRodHolderMountHoletoEdgePadding+gv.printedToPrintedDia/2
		faceToZRodDist = gv.xEndZRodHolderMaxNutFaceToFace/2
		nutTrapBlockWidth = 4*gv.bushingNutPadding+2*math.cos(math.pi/6)*gv.xEndZRodHolderMaxNutFaceToFace+gv.zOffsetNutFaceToFace
		zOffsetNutTrapBlockThickness = gv.zOffsetNutThickness+gv.bushingNutPadding
		bushingNutTrapBlockThickness = gv.xEndZRodHolderMaxNutThickness+gv.bushingNutPadding
		nutTrapOuterRadius = gv.xEndZRodHolderMaxNutFaceToFace/(2*math.cos(math.pi/6))+gv.bushingNutPadding
		#safety check
		minZRodZScrewDist = 2*gv.bushingNutPadding+math.cos(math.pi/6)*gv.xEndZRodHolderMaxNutFaceToFace+math.cos(math.pi/6)*gv.zOffsetNutFaceToFace
#		if minZRodZScrewDist>gv.leadScrewDia:
#			raise Exception("Error: The minimum Z-Rod Z-Screw distance has not been met!")


		#Create Document
		try:
			App.getDocument(self.name).recompute()
			App.closeDocument(self.name)
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		App.newDocument(self.name)
		App.setActiveDocument(self.name)
		App.ActiveDocument=App.getDocument(self.name)

		#Make base
		#sketch Variables
		p1x = 0
		p1y = 0
		p2x = 0
		p2y = gv.xRodSpacing
		p3x = gv.xRodClampWidth
		p3y = gv.xRodSpacing
		p4x = gv.xRodClampWidth
		p4y = 0


		#Make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',3)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',0)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1)) 
		App.ActiveDocument.recompute()

		#add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',2,-gv.xRodSpacing)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',3,-gv.xRodClampWidth)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		#extrude base
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.xEndZRodHolderFaceThickness
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#Make holes for motor mount plate and idler
		#Sketch Points
		p1x = 0
		p1y = gv.xRodSpacing-gv.xRodAxisToMountHoleDist
		p2x = mountHoleInsetHoriz
		p2y = gv.xRodSpacing
		p3x = gv.xRodClampWidth
		p3y = gv.xRodAxisToMountHoleDist
		p4x = gv.xRodClampWidth-mountHoleInsetHoriz
		p4y = 0
		p5x = mountHoleInsetHoriz
		p5y = gv.xRodAxisToMountHoleDist
		p6x = mountHoleInsetHoriz
		p6y = gv.xRodSpacing-gv.xRodAxisToMountHoleDist
		p7x = gv.xRodClampWidth-mountHoleInsetHoriz
		p7y = gv.xRodSpacing-gv.xRodAxisToMountHoleDist
		p8x = gv.xRodClampWidth-mountHoleInsetHoriz
		p8y = gv.xRodAxisToMountHoleDist
		p9x = gv.xRodClampWidth/2
		p9y = gv.xRodSpacing/2
		
		#Make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
															None, None, 
															None, None, 
															gv.xEndZRodHolderFaceThickness, 0)
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad,
														  gv.xRodClampWidth/2,0,
														  gv.xRodSpacing,0,
														  gv.xEndZRodHolderFaceThickness,0))
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
														  gv.xRodClampWidth,0,
														  gv.xRodSpacing/2,0,
														  gv.xEndZRodHolderFaceThickness,0))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.recompute()

		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',2,1,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',3,2,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',1))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.toggleConstruction(0) 
		App.ActiveDocument.Sketch001.toggleConstruction(1) 
		App.ActiveDocument.Sketch001.toggleConstruction(2) 
		App.ActiveDocument.Sketch001.toggleConstruction(3) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',1,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',2,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',5,2,6,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',6,2,7,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',7,2,4,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',6)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',5)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',7)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',4,1,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',5,2,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.toggleConstruction(7) 
		App.ActiveDocument.Sketch001.toggleConstruction(4) 
		App.ActiveDocument.Sketch001.toggleConstruction(5) 
		App.ActiveDocument.Sketch001.toggleConstruction(6) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p6x,p6y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',8,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',9,3,4,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',10,3,6,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p8x,p8y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',11,3,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',8,9)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',9,11)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',11,10)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p9x,p9y,0),App.Vector(0,0,1),gv.xRodClampIdlerHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',0,2,2,2,12,3)) 
		App.ActiveDocument.recompute()

		#add dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',9,gv.printedToPrintedDia/2))#mount hole radius 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',12,gv.xRodClampIdlerHoleDia/2))#idler hole radius 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',0,mountHoleInsetHoriz)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',3,-gv.xRodAxisToMountHoleDist)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#Cut the holes
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()

		#Make lower nut trap block
		#Sketch variables
		p1x = 0
		p1y = gv.xEndZRodHolderFaceThickness
		p2x = 0
		p2y = faceToZRodDist+gv.xEndZRodHolderFaceThickness
		p3x = nutTrapOuterRadius
		p3y = gv.xEndZRodHolderFaceThickness+faceToZRodDist+nutTrapOuterRadius
		p4x = gv.xRodClampWidth-p3x
		p4y = gv.xEndZRodHolderFaceThickness+faceToZRodDist+nutTrapOuterRadius
		p5x = gv.xRodClampWidth
		p5y = faceToZRodDist+gv.xEndZRodHolderFaceThickness
		p6x = gv.xRodClampWidth
		p6y = gv.xEndZRodHolderFaceThickness
		p7x = p3x#gv.xEndZRodHolderMaxNutFaceToFace/2
		p7y = faceToZRodDist+gv.xEndZRodHolderFaceThickness
		p8x = p4x #gv.xEndZRodHolderMaxNutFaceToFace/2
		p8y = faceToZRodDist+gv.xEndZRodHolderFaceThickness

		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
														  gv.xRodClampWidth/2,0,
														  0,0,
														  gv.xEndZRodHolderFaceThickness/2,0)
		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket, 
														  gv.xRodClampWidth/2,0,
														  0,0,
														  gv.xEndZRodHolderFaceThickness,0))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,1,-3,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),nutTrapOuterRadius),math.pi/2,math.pi))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',1,2,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',2,1,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p8x,p8y,0),App.Vector(0,0,1),nutTrapOuterRadius),0,math.pi/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',3,2,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Tangent',3,1,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,1,5,2)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,1,-3,2)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',4,2,-3,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',4))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',1,3)) 
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,2,6,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',6,2,1,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',6,2,7,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',7,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',7)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',6)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.toggleConstruction(6) 
		App.ActiveDocument.Sketch002.toggleConstruction(7) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',2,2,8,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',8,2,3,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',8)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.toggleConstruction(8) 
		App.ActiveDocument.recompute()

		#add dimmensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',3,nutTrapOuterRadius)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceY',0,faceToZRodDist)) 
		App.ActiveDocument.recompute()

		#extrude nut trap block
		App.getDocument(self.name).recompute()
		App.activeDocument().addObject("PartDesign::Pad","Pad001")
		App.activeDocument().Pad001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pad001.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad001.Length = bushingNutTrapBlockThickness
		App.ActiveDocument.Pad001.Reversed = 1
		App.ActiveDocument.Pad001.Midplane = 0
		App.ActiveDocument.Pad001.Length2 = 100.000000
		App.ActiveDocument.Pad001.Type = 0
		App.ActiveDocument.Pad001.UpToFace = None
		App.ActiveDocument.recompute()

		#Refine shape
		App.ActiveDocument.addObject('Part::Feature','Pad002').Shape=App.ActiveDocument.Pad001.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pad002.Label

		App.ActiveDocument.recompute()

		#add z Offset block
		#Sketch Variables
		p1x = nutTrapOuterRadius
		p1y = faceToZRodDist+gv.xEndZRodHolderFaceThickness+nutTrapOuterRadius 
		p2x = gv.xRodClampWidth/2-math.cos(math.pi/6)*gv.zOffsetNutFaceToFace-gv.bushingNutPadding
		p2y = gv.xEndZRodHolderFaceThickness+faceToZRodDist+nutTrapOuterRadius+gv.zOffsetNutFaceToFace+2*gv.bushingNutPadding
		p3x = gv.xRodClampWidth/2+math.cos(math.pi/6)*gv.zOffsetNutFaceToFace+gv.bushingNutPadding
		p3y = gv.xEndZRodHolderFaceThickness+faceToZRodDist+nutTrapOuterRadius+gv.zOffsetNutFaceToFace/2+gv.bushingNutPadding
		p4x = gv.xRodClampWidth-nutTrapOuterRadius
		p4y = p1y

		#make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
		App.activeDocument().recompute()
		App.ActiveDocument.recompute()
		App.activeDocument().Sketch003.Support = uf.getFace(App.ActiveDocument.Pad002,
														  gv.xRodClampWidth/2,0,
														  0,0,
														  None, None)
		App.ActiveDocument.Sketch003.addExternal("Pad002",uf.getEdge(App.ActiveDocument.Pad002, 
														  gv.xRodClampWidth/2,0,
														  0,0,
														  gv.xEndZRodHolderFaceThickness+faceToZRodDist+nutTrapOuterRadius,0))
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',-3,1,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',2,2,-3,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Equal',2,0)) 
		App.ActiveDocument.recompute()


		#add dimensions
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('DistanceX',1,2*gv.bushingNutPadding+math.sin(math.pi/6)*gv.zOffsetNutFaceToFace/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Distance',1,2,3,2*gv.bushingNutPadding+gv.zOffsetNutFaceToFace)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#extrude z offset block
		App.activeDocument().addObject("PartDesign::Pad","Pad003")
		App.activeDocument().Pad003.Sketch = App.activeDocument().Sketch003
		App.activeDocument().Pad003.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad003.Length = zOffsetNutTrapBlockThickness
		App.ActiveDocument.Pad003.Reversed = 1
		App.ActiveDocument.Pad003.Midplane = 0
		App.ActiveDocument.Pad003.Length2 = 100.000000
		App.ActiveDocument.Pad003.Type = 0
		App.ActiveDocument.Pad003.UpToFace = None
		App.ActiveDocument.recompute()

		#Refine Shape
		App.ActiveDocument.addObject('Part::Feature','Pad004').Shape=App.ActiveDocument.Pad003.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pad004.Label

		App.ActiveDocument.recompute()
		
		#Make the top z bushing block
		#sketch points
		p1x = -2*nutTrapOuterRadius
		p1y = gv.xEndZRodHolderFaceThickness
		p2x = -2*nutTrapOuterRadius
		p2y = faceToZRodDist+gv.xEndZRodHolderFaceThickness
		p3x = -nutTrapOuterRadius
		p3y = p2y
		p4x = 0
		p4y = p2y
		p5x = 0
		p5y = gv.xEndZRodHolderFaceThickness

		#Draw the sketch
		
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch004')
		App.activeDocument().Sketch004.Support = uf.getFace(App.ActiveDocument.Pad004,
														  gv.xRodClampWidth/2,0,
														  gv.xRodSpacing,0,
														  None, None)
		App.ActiveDocument.Sketch004.addExternal("Pad004",uf.getEdge(App.ActiveDocument.Pad004, 
														  gv.xRodClampWidth/2,0,
														  gv.xRodSpacing,0,
														  gv.xEndZRodHolderFaceThickness,0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Vertical',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),nutTrapOuterRadius),0,math.pi))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',1,2,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('PointOnObject',1,1,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Tangent',1,1,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Horizontal',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Vertical',2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Equal',0,2))
		App.ActiveDocument.recompute()

		#add Dimensions
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Radius',1,nutTrapOuterRadius)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('DistanceY',2,-faceToZRodDist)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#extrude the top z bushing block
		App.activeDocument().addObject("PartDesign::Pad","Pad005")
		App.activeDocument().Pad005.Sketch = App.activeDocument().Sketch004
		App.activeDocument().Pad005.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad005.Length = bushingNutTrapBlockThickness
		App.ActiveDocument.Pad005.Reversed = 1
		App.ActiveDocument.Pad005.Midplane = 0
		App.ActiveDocument.Pad005.Length2 = 100.000000
		App.ActiveDocument.Pad005.Type = 0
		App.ActiveDocument.Pad005.UpToFace = None
		App.ActiveDocument.recompute()

		#Refine Shape
		App.ActiveDocument.addObject('Part::Feature','Pad006').Shape=App.ActiveDocument.Pad005.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pad006.Label

		App.ActiveDocument.recompute()
		
		#Cut rod and lead screw holes
		#sketch points
		p1x = nutTrapOuterRadius
		p1y = gv.xEndZRodHolderFaceThickness+faceToZRodDist
		p2x = gv.xRodClampWidth-nutTrapOuterRadius
		p2y = gv.xEndZRodHolderFaceThickness+faceToZRodDist

		#make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch005')
		App.activeDocument().Sketch005.Support = uf.getFace(App.ActiveDocument.Pad006,
														  gv.xRodClampWidth/2,0,
														  0,0,
														  None, None)
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addExternal("Pad006",uf.getEdge(App.ActiveDocument.Pad006, 
																	  nutTrapOuterRadius,-1,
																	  0,0,
																	  faceToZRodDist+gv.xEndZRodHolderFaceThickness,1))
		App.ActiveDocument.recompute()
 		App.ActiveDocument.Sketch005.addExternal("Pad006",uf.getEdge(App.ActiveDocument.Pad006, 
														  gv.xRodClampWidth/2,1,
														  0,0,
														  None,None,
														  radius = nutTrapOuterRadius))


		App.ActiveDocument.Sketch005.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),self.rodDia/2+gv.bushingNutRodGap))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',0,3,-3,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.leadScrewDia/2+gv.bushingNutRodGap))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',1,3,-4,3)) 
		App.ActiveDocument.recompute()

		#add Dimensions
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Radius',0,self.rodDia/2+gv.bushingNutRodGap)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Radius',1,gv.leadScrewDia/2+gv.bushingNutRodGap)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#Cut holes
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch005
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()


		mat = uf.hexagonPoints(nutTrapOuterRadius,
							gv.xEndZRodHolderFaceThickness+faceToZRodDist,
							self.bushingNutFaceToFace,
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

		App.activeDocument().addObject('Sketcher::SketchObject','Sketch006')
		App.activeDocument().Sketch006.Support = uf.getFace(App.ActiveDocument.Pocket001,
														  None,None,
														  0,0,
														  None, None)
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
		App.ActiveDocument.Sketch006.addExternal("Pocket001",uf.getEdge(App.ActiveDocument.Pocket001, 
														  gv.xRodClampWidth/2,-1,
														  0,0,
														  None,None,
														  radius = nutTrapOuterRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Coincident',-3,3,6,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch006.addConstraint(Sketcher.Constraint('Distance',0,2,4,self.bushingNutFaceToFace)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#cut nut trap out
		App.activeDocument().addObject("PartDesign::Pocket","Pocket002")
		App.activeDocument().Pocket002.Sketch = App.activeDocument().Sketch006
		App.activeDocument().Pocket002.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket002.Length = self.bushingNutThickness
		App.ActiveDocument.Pocket002.Type = 0
		App.ActiveDocument.Pocket002.UpToFace = None
		App.ActiveDocument.recompute()


		#cut nut trap for lead screw
		#sketch points
		mat = uf.hexagonPoints(gv.xRodClampWidth-nutTrapOuterRadius,
							gv.xEndZRodHolderFaceThickness+faceToZRodDist,
							gv.leadScrewNut[2],
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

		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch007')
		App.activeDocument().Sketch007.Support = uf.getFace(App.ActiveDocument.Pocket002,
														  None,None,
														  0,0,
														  None, None)
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addExternal("Pocket002",uf.getEdge(App.ActiveDocument.Pocket002,
														  gv.xRodClampWidth/2,1,
														  0,0,
														  None,None,
														  radius = nutTrapOuterRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),hexRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('PointOnObject',0,1,6)) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('PointOnObject',0,2,6)) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('PointOnObject',1,2,6)) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('PointOnObject',2,2,6)) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('PointOnObject',3,2,6)) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('PointOnObject',4,2,6)) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Equal',5,0)) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Equal',3,4)) 
		App.ActiveDocument.Sketch007.toggleConstruction(6) 
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Coincident',-3,3,6,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch007.addConstraint(Sketcher.Constraint('Distance',0,2,4,gv.leadScrewNut[2])) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#cut nut trap out
		App.activeDocument().addObject("PartDesign::Pocket","Pocket003")
		App.activeDocument().Pocket003.Sketch = App.activeDocument().Sketch007
		App.activeDocument().Pocket003.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket003.Length = gv.leadScrewNut[3]
		App.ActiveDocument.Pocket003.Type = 0
		App.ActiveDocument.Pocket003.UpToFace = None
		App.ActiveDocument.recompute()

		#Cut hole for z offset adjust
		# sketch points
		p1x = gv.xRodClampWidth/2
		p1y = gv.xEndZRodHolderFaceThickness+faceToZRodDist+nutTrapOuterRadius+2*gv.bushingNutPadding+gv.zOffsetNutFaceToFace
		p2x = gv.xRodClampWidth/2
		p2y = gv.xEndZRodHolderFaceThickness+faceToZRodDist+nutTrapOuterRadius
		p3x = gv.xRodClampWidth/2
		p3y = gv.xEndZRodHolderFaceThickness+faceToZRodDist+nutTrapOuterRadius+gv.bushingNutPadding+gv.zOffsetNutFaceToFace/2
		p4x = nutTrapOuterRadius
		p4y = p2y
		p5x = gv.xRodClampWidth-nutTrapOuterRadius
		p5y = p2y
		
		#make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch008')
		App.activeDocument().Sketch008.Support = uf.getFace(App.ActiveDocument.Pocket003,
														  None,None,
														  0,0,
														  None, None)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch008.addExternal("Pocket003",uf.getEdge(App.ActiveDocument.Pocket003,
														  gv.xRodClampWidth/2,-1,
														  0,0,
														  None,None,
														  radius = nutTrapOuterRadius))
		App.ActiveDocument.Sketch008.addExternal("Pocket003",uf.getEdge(App.ActiveDocument.Pocket003, 
														  gv.xRodClampWidth/2,1,
														  0,0,
														  None,None,
														  radius = nutTrapOuterRadius))
		App.ActiveDocument.Sketch008.addExternal("Pocket003",uf.getEdge(App.ActiveDocument.Pocket003, 
														  gv.xRodClampWidth/2,0,
														  0,0,
														  0,1))
		App.ActiveDocument.Sketch008.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Coincident',0,1,-3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Coincident',0,2,-4,2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('PointOnObject',1,1,-5)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('PointOnObject',1,2,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.toggleConstruction(1) 
		App.ActiveDocument.Sketch008.toggleConstruction(0) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Symmetric',-5,1,-5,2,1,1))
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.zOffsetHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('PointOnObject',2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Symmetric',1,1,1,2,2,3)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch008.addConstraint(Sketcher.Constraint('Radius',2,gv.zOffsetHoleDia/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#Cut hole though all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket004")
		App.activeDocument().Pocket004.Sketch = App.activeDocument().Sketch008
		App.activeDocument().Pocket004.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket004.Length = 5
		App.ActiveDocument.Pocket004.Type = 1
		App.ActiveDocument.Pocket004.UpToFace = None
		App.ActiveDocument.recompute()

		#Cut Nut trap for z offset
		#sketch points
		mat = uf.hexagonPoints(gv.xRodClampWidth/2,
							gv.xEndZRodHolderFaceThickness+faceToZRodDist+nutTrapOuterRadius+gv.zOffsetNutFaceToFace/2+gv.bushingNutPadding,
							gv.zOffsetNutFaceToFace,
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

		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch009')
		App.activeDocument().Sketch009.Support = uf.getFace(App.ActiveDocument.Pocket004,
														  None,None,
														  0,0,
														  None, None)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch009.addExternal("Pocket004",uf.getEdge(App.ActiveDocument.Pocket004,
														  gv.xRodClampWidth/2,0,
														  0,0,
														  None,None,
														  radius = gv.zOffsetHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),hexRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('PointOnObject',0,1,6)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('PointOnObject',0,2,6)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('PointOnObject',1,2,6)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('PointOnObject',2,2,6)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('PointOnObject',3,2,6)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('PointOnObject',4,2,6)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Equal',5,0)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Equal',3,4)) 
		App.ActiveDocument.Sketch009.toggleConstruction(6) 
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Coincident',-3,3,6,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch009.addConstraint(Sketcher.Constraint('Distance',0,2,4,gv.zOffsetNutFaceToFace)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#Cut z Offset nut trap
		App.activeDocument().addObject("PartDesign::Pocket","Pocket005")
		App.activeDocument().Pocket005.Sketch = App.activeDocument().Sketch009
		App.activeDocument().Pocket005.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket005.Length = gv.zOffsetNutThickness
		App.ActiveDocument.Pocket005.Type = 0
		App.ActiveDocument.Pocket005.UpToFace = None
		App.ActiveDocument.recompute()
#
		#Make nut trap for top Z rod bushing
		#sketch points
		mat = uf.hexagonPoints(-nutTrapOuterRadius,
							gv.xEndZRodHolderFaceThickness+faceToZRodDist,
							self.bushingNutFaceToFace,
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
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch010')
		App.activeDocument().Sketch010.Support = uf.getFace(App.ActiveDocument.Pocket005,
														  None,None,
														  gv.xRodSpacing,0,
														  None, None)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch010.addExternal("Pocket005",uf.getEdge(App.ActiveDocument.Pocket005, 
														  gv.xRodClampWidth/2,-1,
														  gv.xRodSpacing,0,
														  None,None,
														  radius = nutTrapOuterRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),hexRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('PointOnObject',0,1,6)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('PointOnObject',0,2,6)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('PointOnObject',1,2,6)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('PointOnObject',2,2,6)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('PointOnObject',3,2,6)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('PointOnObject',4,2,6)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Equal',5,0)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Equal',3,4)) 
		App.ActiveDocument.Sketch010.toggleConstruction(6) 
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Coincident',-3,3,6,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch010.addConstraint(Sketcher.Constraint('Distance',0,2,4,self.bushingNutFaceToFace)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#Cut top bushing nut trap
		App.activeDocument().addObject("PartDesign::Pocket","Pocket006")
		App.activeDocument().Pocket006.Sketch = App.activeDocument().Sketch010
		App.activeDocument().Pocket006.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket006.Length = self.bushingNutThickness
		App.ActiveDocument.Pocket006.Type = 0
		App.ActiveDocument.Pocket006.UpToFace = None
		App.ActiveDocument.recompute()

		#Refine Shape
		App.ActiveDocument.addObject('Part::Feature','Pocket007').Shape=App.ActiveDocument.Pocket006.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pocket007.Label
		App.ActiveDocument.recompute()
	
		if self.side == "Left":
			__doc__=App.getDocument(self.name)
			__doc__.addObject("Part::Mirroring")
			__doc__.ActiveObject.Source=__doc__.getObject("Pocket007")
			__doc__.ActiveObject.Label="Pocket007 (Mirror #1)"
			__doc__.ActiveObject.Normal=(1,0,0)
			__doc__.ActiveObject.Base=(0,0,0)
			del __doc__


		
		#set view as axometric

