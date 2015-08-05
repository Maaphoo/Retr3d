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
#Nut facetoface top and bottom should be resolved into a max


class XEndMotorPlate(object):
	def __init__(self):
		pass
		
	def assemble(self):
		App.ActiveDocument=App.getDocument("xEndMotorPlate")
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature','xEndMotorPlate').Shape= shape
		
		#Color Part change colors to metal

		#Rotate into correct orientation
		rotateAngle = -90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(1,0,0)
		Draft.rotate([App.ActiveDocument.xEndMotorPlate],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = -gv.xRodLength/2-gv.xMotorBodyWidth-gv.motorToXRodClampSpacing-gv.xRodClampWidth+gv.xRodClampPocketDepth
		yShift = (gv.extruderNozzleStandoff 
				- gv.zRodStandoff
				- gv.xEndZRodHolderFaceThickness
				- gv.xEndZRodHolderMaxNutFaceToFace/2
				- gv.xMotorMountPlateThickness)
		zShift = gv.xMotorMountPlateWidth+ (gv.xRodSpacing-gv.xMotorMountPlateWidth)/2
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([App.ActiveDocument.xEndMotorPlate],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		shape = App.ActiveDocument.xEndMotorPlate
		if shape not in gv.xAxisParts:
			gv.xAxisParts.append(shape)

	def draw(self):
		#helper Variables
		
		#determine total width of motor mount plate
		xMotorMountWidth = gv.xMotorBodyWidth + gv.motorToXRodClampSpacing + gv.xRodClampWidth

		xRodClampMountHoleSpacingVert = gv.xRodSpacing-2*gv.xRodAxisToMountHoleDist
		xRodClampMountHoleSpacingHoriz =  gv.xRodClampWidth-2*gv.xRodClampEdgeToMountHoleDist


		#safety check
		#xRodSpacing must be wide enough for the motor to be mounted between the rods


		#Create Document
		try:
			App.getDocument('xEndMotorPlate').recompute()
			App.closeDocument("xEndMotorPlate")
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass
			
		App.newDocument("xEndMotorPlate")
		App.setActiveDocument("xEndMotorPlate")
		App.ActiveDocument=App.getDocument("xEndMotorPlate")

		#Make the plate
		#Sketch points
		p1x = 0
		p1y = 0
		p2x = 0
		p2y = gv.xMotorMountPlateWidth 
		p3x = xMotorMountWidth
		p3y = gv.xMotorMountPlateWidth
		p4x = xMotorMountWidth
		p4y = 0


		#Make Sketch
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
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,1,-1,1))
		App.ActiveDocument.recompute()

		#Add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',3,-xMotorMountWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',2,-gv.xMotorMountPlateWidth)) 
		App.ActiveDocument.recompute()

		App.getDocument('xEndMotorPlate').recompute()

		#extrude x motor mount plate
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.xMotorMountPlateThickness
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#cut holes for xRodClamp
		#Sketch Points
		p1x = 0
		p1y = gv.xMotorMountPlateWidth/2
		p2x = xMotorMountWidth
		p2y = gv.xMotorMountPlateWidth/2
		p3x = gv.xMotorBodyWidth+gv.motorToXRodClampSpacing +gv.xRodClampEdgeToMountHoleDist
		p3y = gv.xRodAxisToMountHoleDist
		p4x = gv.xMotorBodyWidth+gv.motorToXRodClampSpacing+gv.xRodClampEdgeToMountHoleDist
		p4y = gv.xMotorMountPlateWidth-gv.xRodAxisToMountHoleDist
		p5x = xMotorMountWidth-gv.xRodClampEdgeToMountHoleDist
		p5y = gv.xMotorMountPlateWidth-gv.xRodAxisToMountHoleDist
		p6x = xMotorMountWidth-gv.xRodClampEdgeToMountHoleDist
		p6y = gv.xRodAxisToMountHoleDist
		p7x = gv.xMotorBodyWidth+gv.motorToXRodClampSpacing+gv.xRodClampEdgeToMountHoleDist
		p7y = gv.xMotorMountPlateWidth/2
		p8x = gv.xMotorBodyWidth+gv.motorToXRodClampSpacing+gv.xRodClampWidth/2
		p8y = gv.xMotorMountPlateWidth/2

		#Make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
															None, None, 
															None, None, 
															gv.xMotorMountPlateThickness, 0)#(App.ActiveDocument.Pad,["Face6"])
		App.activeDocument().recompute()

		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
															  0,0,
															  gv.xMotorMountPlateWidth/2,0,
															  gv.xMotorMountPlateThickness,0))
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
															  xMotorMountWidth,0,
															  gv.xMotorMountPlateWidth/2,0,
															  gv.xMotorMountPlateThickness,0))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-4)) 
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',4,2,1,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.toggleConstruction(0) 
		App.ActiveDocument.Sketch001.toggleConstruction(4) 
		App.ActiveDocument.Sketch001.toggleConstruction(3) 
		App.ActiveDocument.Sketch001.toggleConstruction(2) 
		App.ActiveDocument.Sketch001.toggleConstruction(1) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Point(App.Vector(p7x,p7y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',5,1,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',5,1,0)) 

		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,1,6,3))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p4x,p4y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',7,3,1,2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,8,3))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p6x,p6y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',9,3,3,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',6,7)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',7,8)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',8,9)) 
		App.ActiveDocument.recompute()

		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p8x,p8y,0),App.Vector(0,0,1),gv.xEndIdlerHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',10,3,0)) 
		App.ActiveDocument.recompute()

		#add dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',4, -xRodClampMountHoleSpacingHoriz)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',3,2,-4,gv.xRodClampEdgeToMountHoleDist)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',3,-xRodClampMountHoleSpacingVert))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',8,gv.mountToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',10,gv.xEndIdlerHoleDia/2)) 
		App.ActiveDocument.recompute()

		#add Symmetric constraints
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',1,1,1,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',1,1,2,2,10,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',-1,1,-3,2,0,1)) 
		App.ActiveDocument.recompute()

		#exit sketch
		App.getDocument('xEndMotorPlate').recompute()

		#Cut holes through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()


		#Cut holes for motor
		#Sketch Points
		p1x = 0
		p1y = gv.xMotorMountPlateWidth/2
		p2x = xMotorMountWidth
		p2y = gv.xMotorMountPlateWidth/2
		p3x = gv.xEndMotorMountHoleDia/2+gv.xEndMotorMountHolePadding
		p3y = gv.xMotorMountPlateWidth/2-gv.xMotorShaftToMountHoleDistX
		p4x = gv.xEndMotorMountHoleDia/2+gv.xEndMotorMountHolePadding
		p4y = gv.xMotorMountPlateWidth/2+gv.xMotorShaftToMountHoleDistX
		p5x = gv.xEndMotorMountHoleDia/2+gv.xEndMotorMountHolePadding+2*gv.xMotorShaftToMountHoleDistX
		p5y = gv.xMotorMountPlateWidth/2+gv.xMotorShaftToMountHoleDistX
		p6x = gv.xEndMotorMountHoleDia/2+gv.xEndMotorMountHolePadding+2*gv.xMotorShaftToMountHoleDistX
		p6y = gv.xMotorMountPlateWidth/2-gv.xMotorShaftToMountHoleDistX
		p7x = gv.xEndMotorMountHoleDia/2+gv.xEndMotorMountHolePadding
		p7y = gv.xMotorMountPlateWidth/2
		p8x = gv.xMotorBodyWidth/2
		p8y = gv.xMotorMountPlateWidth/2

		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
															None, None, 
															None, None, 
															gv.xMotorMountPlateThickness, 0)#(App.ActiveDocument.Pocket,["Face5"])
		App.activeDocument().recompute()

		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket, 
															  0,0,
															  gv.xMotorMountPlateWidth/2,0,
															  gv.xMotorMountPlateThickness,0))
		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket, 
															  xMotorMountWidth,0,
															  gv.xMotorMountPlateWidth/2,0,
															  gv.xMotorMountPlateThickness,0))
		
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Symmetric',-1,1,-3,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',0))
		App.ActiveDocument.recompute()

		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p3x,p3y,0)))

		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',4,2,1,1)) 

		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',3))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',1))
		App.ActiveDocument.recompute()

		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',3,4)) 
		App.ActiveDocument.recompute() 
		App.ActiveDocument.recompute()

		App.ActiveDocument.Sketch002.toggleConstruction(0) 
		App.ActiveDocument.Sketch002.toggleConstruction(2) 
		App.ActiveDocument.Sketch002.toggleConstruction(3) 
		App.ActiveDocument.Sketch002.toggleConstruction(4) 
		App.ActiveDocument.Sketch002.toggleConstruction(1) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Point(App.Vector(p7x,p7y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',5,1,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',5,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Distance',1,1,-3,gv.xEndMotorMountHoleDia/2+gv.xEndMotorMountHolePadding)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceX',4,-2*gv.xMotorShaftToMountHoleDistX))
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.xEndMotorMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',6,3,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.xEndMotorMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',7,3,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p8x,p8y,0),App.Vector(0,0,1),gv.xMotorPulleyDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',8,3,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',6,7))
		App.ActiveDocument.recompute()

		#Add dimensions to holes
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',6,gv.xEndMotorMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',8,gv.xMotorPulleyDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Symmetric',1,1,2,2,8,3)) 
		App.ActiveDocument.recompute()

		#Cut 2 more holes if there are 4 motor mount holes
		if gv.xEndNumMountHoles==4:
			App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p4x,p4y,0),App.Vector(0,0,1),gv.xEndMotorMountHoleDia/2))
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',9,3,1,2)) 
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p6x,p6y,0),App.Vector(0,0,1),gv.xEndMotorMountHoleDia/2))
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',10,3,3,2)) 
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',10,9)) 
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',10,7)) 


		#exit Sketch
		App.getDocument('xEndMotorPlate').recompute()

		#Cut holes
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()

		#set view as axiometric
