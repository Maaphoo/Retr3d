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

class PrintBedSupport(object):
	def __init__(self):
		self.name = "printBedSupport"

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

		#Define shifts and move the into place
		xShift = 0
		yShift = 0			 
		zShift = gv.PBBHStandoff
	
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
			App.getDocument("printBedSupport").recompute()
			App.closeDocument("printBedSupport")
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		#Create Document
		App.newDocument("printBedSupport")
		App.setActiveDocument("printBedSupport")
		App.ActiveDocument=App.getDocument("printBedSupport")

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

		App.getDocument('printBedSupport').recompute()
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.printBedSupportThickness
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#Make holes for y bushing mounts
		#Sketch Points
		p1x = -gv.yRodSpacing/2
		p1y = -length/2
		p2x = -gv.yRodSpacing/2
		p2y = length/2
		p3x = gv.yRodSpacing/2
		p3y = -length/2
		p4x = gv.yRodSpacing/2
		p4y = length/2
		p5x = -gv.yRodSpacing/2-gv.yBushingMountSlotSpacing/2
		p5y = -gv.yBushingNutSeparation/2
		p6x = -gv.yRodSpacing/2+gv.yBushingMountSlotSpacing/2
		p6y = -gv.yBushingNutSeparation/2
		p7x = -gv.yRodSpacing/2-gv.yBushingMountSlotSpacing/2
		p7y = gv.yBushingNutSeparation/2
		p8x = -gv.yRodSpacing/2+gv.yBushingMountSlotSpacing/2
		p8y = gv.yBushingNutSeparation/2
		p9x = gv.yRodSpacing/2-gv.yBushingMountSlotSpacing/2
		p9y = -gv.yBushingNutSeparation/2
		p10x = gv.yRodSpacing/2+gv.yBushingMountSlotSpacing/2
		p10y = -gv.yBushingNutSeparation/2
		p11x = gv.yRodSpacing/2-gv.yBushingMountSlotSpacing/2
		p11y = gv.yBushingNutSeparation/2
		p12x = gv.yRodSpacing/2+gv.yBushingMountSlotSpacing/2
		p12y = gv.yBushingNutSeparation/2
		p13x = p1x
		p13y = p5y
		p14x = p1x
		p14y = p7y
		p15x = p3x
		p15y = p5y
		p16x = p3x
		p16y = p7y
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
														  None, None,
														  None, None,
														  gv.printBedSupportThickness, 0)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad,
														  0,0,
														  length/2, 0,
														  gv.printBedSupportThickness, 0))
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
														  0,0,
														  -length/2, 0,
														  gv.printBedSupportThickness, 0))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',1,1,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',1,2,0,2,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p9x,p9y,0),App.Vector(p10x,p10y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p11x,p11y,0),App.Vector(p12x,p12y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',5)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',3,5)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',5,4)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',4,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',3,2,3,1,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',2,2,2,1,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',5,2,5,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',4,2,4,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',3,2,5)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-3)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',2,2,4)) 
		App.ActiveDocument.recompute()
		
		#Add Dimmensions early to avoid squishing sketch
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',5,2,4,gv.yBushingNutSeparation)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',1,1,0,1,gv.yRodSpacing)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',4,gv.yBushingMountSlotSpacing)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',3,1,2,1,-1)) 
		App.ActiveDocument.recompute()
		
		#continue adding other constraints
		App.ActiveDocument.Sketch001.toggleConstruction(0) 
		App.ActiveDocument.Sketch001.toggleConstruction(1) 
		App.ActiveDocument.Sketch001.toggleConstruction(5) 
		App.ActiveDocument.Sketch001.toggleConstruction(4) 
		App.ActiveDocument.Sketch001.toggleConstruction(2) 
		App.ActiveDocument.Sketch001.toggleConstruction(3) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',6,3,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p6x,p6y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',7,3,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',8,3,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p8x,p8y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',9,3,3,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p9x,p9y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',10,3,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p10x,p10y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',11,3,5,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p11x,p11y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',12,3,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p12x,p12y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',13,3,4,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',6,7)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',7,8)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',8,9)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',9,10)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',10,11)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',11,12)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',12,13)) 
		App.ActiveDocument.recompute()
		
		#Add hole Dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',11,gv.mountToPrintedDia/2)) 
		App.ActiveDocument.recompute()

		#Cut bushing mount holes through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()

		#Make holes for y belt anchor
		#Sketch points
		p1x = gv.yMotorPulleyDia/2
		p1y = gv.yBeltAnchorHoleSpacing/2
		p2x = p1x
		p2y = -p1y
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
														  None, None,
														  None, None,
														  gv.printBedSupportThickness, 0)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Symmetric',0,3,1,3,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',0,gv.mountToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceX',-2,1,1,3,gv.yMotorPulleyDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Distance',0,3,1,3,gv.yBeltAnchorHoleSpacing)) 
		App.ActiveDocument.recompute()
		App.getDocument('printBedSupport').recompute()
		
		#Cut holes
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()

		#Make view axiometric
