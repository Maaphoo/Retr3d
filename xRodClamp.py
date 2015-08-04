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

class XRodClamp(object):
	def __init__(self, name, side):
		self.name = name
		self.side = side
		
	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		if self.side =="Right":
			xRodClamp = App.ActiveDocument.Pocket002.Shape
		if self.side =="Left":
			xRodClamp = App.ActiveDocument.Part__Mirroring.Shape		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape=xRodClamp
		#Color Part


		objs = App.ActiveDocument.getObjectsByLabel(self.name)
		shape = objs[-1]

		#Rotate into correct orientation
		rotateAngle = 180
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,1,0)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		rotateAngle = 90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(1,0,0)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)
		
		#Define shifts and move the left clamp into place
		if self.side == "Right":
			xShift = +gv.xRodLength/2+gv.xRodClampWidth-gv.xRodClampPocketDepth
		elif self.side == "Left":
			xShift = -gv.xRodLength/2-gv.xRodClampWidth+gv.xRodClampPocketDepth
		yShift = (gv.extruderNozzleStandoff 
				- gv.zRodStandoff
				- gv.xEndZRodHolderFaceThickness
				- gv.xEndZRodHolderMaxNutFaceToFace/2
				- gv.xMotorMountPlateThickness
				- 2*gv.xRodClampThickness
				- gv.xRodDiaMax)
		zShift = 0
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")

		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
 		if shape not in gv.xAxisParts:
			gv.xAxisParts.append(shape)		


	def draw(self):

		#helper Variables
		gv.xRodClampOverallThickness = 2*gv.xRodClampThickness+gv.xRodDiaMax
		mountHoleInsetVert = gv.printedToPrintedDia/2+gv.xRodClampMountHoleToRodPadding+gv.xRodDiaMax/2
		mountHoleInsetHoriz = gv.xRodClampMountHoleToEdgePadding+gv.printedToPrintedDia/2
		beltChannelDepth = (gv.xRodDiaTop if gv.xRodDiaTop>gv.xRodDiaBottom else gv.xRodDiaBottom)+gv.xRodClampThickness

		#Make file and build part
		try:
			App.getDocument(self.name).recompute()
			App.closeDocument(self.name)
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		#Create Document
		App.newDocument(self.name)
		App.setActiveDocument(self.name)
		App.ActiveDocument=App.getDocument(self.name)

		#Extrude body of xRodClamp
		#sketch Points
		p1x = 0
		p1y = 0
		p2x = 0
		p2y = gv.xRodClampOverallThickness/2
		p3x = 0
		p3y = gv.xRodClampOverallThickness
		p4x = gv.xRodSpacing
		p4y = gv.xRodClampOverallThickness
		p5x = gv.xRodSpacing
		p5y = gv.xRodClampOverallThickness/2
		p6x = gv.xRodSpacing
		p6y = 0

		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.500000,0.500000,0.500000,0.500000))
		App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.xRodClampOverallThickness/2),0.5*math.pi,1.5*math.pi))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-2)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,-1,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-2)) 
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.xRodClampOverallThickness/2),1.5*math.pi,0.5*math.pi))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,1,2)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',2,1,-1)) 
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,1,2,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,-1,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',1,3)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',1,2,2,1,2,3))

		#add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',2,gv.xRodClampOverallThickness/2)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',3,-gv.xRodSpacing))
		App.getDocument(self.name).recompute()

		#Pad the xRodClamp body
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.xRodClampWidth # xRodClamp gv.xRodClampWidth
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#Make holes for x rods
		#Sketch Points
		p1x = 0
		p1y = gv.xRodClampOverallThickness/2
		p2x = gv.xRodSpacing
		p2y = gv.xRodClampOverallThickness/2

		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
															gv.xRodClampWidth, 0, 
															None, None, 
															None, None)#(App.ActiveDocument.Pad,["Face6"])
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad,
														  gv.xRodClampWidth,0,
														  0,-1,
														  gv.xRodClampOverallThickness/2,0))
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
														  gv.xRodClampWidth,0,
														  gv.xRodSpacing,1,
														  gv.xRodClampOverallThickness/2,0))
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.xRodDiaBottom/2))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,3,-3,3)) 
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.xRodDiaTop/2))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,3,-4,3)) 

		#add Dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',0,gv.xRodDiaBottom/2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',1,gv.xRodDiaTop/2)) 
		App.getDocument(self.name).recompute()

		#extrude Cut to depth that Rods will be embeded in clamp
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = gv.xRodClampPocketDepth+gv.xRodClampExtraPocketDepth # depth of the holes for the x rods
		App.ActiveDocument.Pocket.Type = 0
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()

		#Make holes for motor mount plate and idler
		#Sketch Points
		p1x = -gv.xRodSpacing
		p1y = gv.xRodClampWidth-mountHoleInsetHoriz
		p2x = -gv.xRodSpacing+gv.xRodAxisToMountHoleDist
		p2y = gv.xRodClampWidth
		p3x = 0
		p3y = mountHoleInsetHoriz
		p4x = -gv.xRodAxisToMountHoleDist
		p4y = 0
		p5x = -gv.xRodSpacing+gv.xRodAxisToMountHoleDist
		p5y = mountHoleInsetHoriz
		p6x = -gv.xRodSpacing+gv.xRodAxisToMountHoleDist
		p6y = gv.xRodClampWidth-mountHoleInsetHoriz
		p7x = -gv.xRodAxisToMountHoleDist 
		p7y = gv.xRodClampWidth-mountHoleInsetHoriz
		p8x = -gv.xRodAxisToMountHoleDist
		p8y = mountHoleInsetHoriz
		p9x = -gv.xRodSpacing/2
		p9y = gv.xRodClampWidth/2

		#Make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
															None, None, 
															None, None, 
															gv.xRodClampOverallThickness, 0)#(App.ActiveDocument.Pocket,["Face2"])
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket,
														  gv.xRodClampWidth,0,
														  gv.xRodSpacing/2,0,
														  gv.xRodClampOverallThickness,0))
		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket, 
														  gv.xRodClampWidth/2,0,
														  gv.xRodSpacing,0,
														  gv.xRodClampOverallThickness,0))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-4)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-3)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',2,1,-2)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',3,2,-1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',1,3)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',2,0)) 
		App.ActiveDocument.Sketch002.toggleConstruction(1) 
		App.ActiveDocument.Sketch002.toggleConstruction(0) 
		App.ActiveDocument.Sketch002.toggleConstruction(2) 
		App.ActiveDocument.Sketch002.toggleConstruction(3) 

		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',5,2,6,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',6,2,7,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',7,2,4,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',6)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',5)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',7)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',4,1,0,2)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',5,2,2,2)) 

		App.ActiveDocument.Sketch002.toggleConstruction(7) 
		App.ActiveDocument.Sketch002.toggleConstruction(4) 
		App.ActiveDocument.Sketch002.toggleConstruction(5) 
		App.ActiveDocument.Sketch002.toggleConstruction(6)
 
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p6x,p6y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',8,3,0,2)) 
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',9,3,4,2)) 
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p8x,p8y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',10,3,2,2)) 
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',11,3,6,2))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',8,9)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',9,10)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',10,11)) 

		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p9x,p9y,0),App.Vector(0,0,1),gv.xRodClampIdlerHoleDia/2))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Symmetric',0,2,2,2,12,3)) 

		#add Dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceX',0,gv.xRodAxisToMountHoleDist)) #distance between rod edge and mouunting hole edge 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceY',1,mountHoleInsetHoriz)) #distance between edge of part and mounting hole edge
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',9,gv.printedToPrintedDia/2)) #mount hole radius
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',12,gv.xRodClampIdlerHoleDia/2))#idler hole radius
		App.getDocument(self.name).recompute()

		#Cut holes through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()

		#Cut away material to make belt channel
		#sketch points
		p1x = -gv.xRodSpacing+gv.xRodAxisToMountHoleDist+gv.printedToPrintedDia/2+gv.xRodClampMountHoleToRodPadding
		p1y = 0
		p2x = p1x
		p2y = gv.xRodClampWidth
		p3x = -(gv.xRodAxisToMountHoleDist+gv.printedToPrintedDia/2+gv.xRodClampMountHoleToRodPadding)
		p3y = gv.xRodClampWidth
		p4x = p3x
		p4y = 0

		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
		App.activeDocument().Sketch003.Support = uf.getFace(App.ActiveDocument.Pocket001,
															None, None, 
															None, None, 
															gv.xRodClampOverallThickness, 0)#(App.ActiveDocument.Pocket001,["Face2"])
		App.activeDocument().recompute()

		App.ActiveDocument.Sketch003.addExternal("Pocket001",uf.getEdge(App.ActiveDocument.Pocket001, 
														  gv.xRodClampWidth,0,
														  gv.xRodSpacing/2,0,
														  gv.xRodClampOverallThickness,0))
		App.ActiveDocument.Sketch003.addExternal("Pocket001",uf.getEdge(App.ActiveDocument.Pocket001, 
														  gv.xRodClampWidth/2,0,
														  gv.xRodSpacing,0,
														  gv.xRodClampOverallThickness,0))
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
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Point(App.Vector(-34.530499,62.111320,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Symmetric',-4,2,-3,1,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.movePoint(2,2,App.Vector(-50.355999,62.922062,0),0)
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.movePoint(1,2,App.Vector(-19.232504,62.922058,0),0)
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Symmetric',2,2,1,2,4,1)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,2,p3x))
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Cut material away
		App.activeDocument().addObject("PartDesign::Pocket","Pocket002")
		App.activeDocument().Pocket002.Sketch = App.activeDocument().Sketch003
		App.activeDocument().Pocket002.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket002.Length = beltChannelDepth
		App.ActiveDocument.Pocket002.Type = 0
		App.ActiveDocument.Pocket002.UpToFace = None
		App.ActiveDocument.recompute()

		if self.side == "Left":
			__doc__=App.getDocument(self.name)
			__doc__.addObject("Part::Mirroring")
			__doc__.ActiveObject.Source=__doc__.getObject("Pocket002")
			__doc__.ActiveObject.Label="Pocket002 (Mirror #1)"
			__doc__.ActiveObject.Normal=(1,0,0)
			__doc__.ActiveObject.Base=(0,0,0)
			del __doc__

		#Make view axiometric


