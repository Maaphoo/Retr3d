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
import Drawing

#Specific to printer
import globalVars as gv
import utilityFunctions as uf

class ZMotorMount(object):
	def __init__(self):
		self.name = "zMotorMount"

	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name+"L").Shape= shape
		
		#Color Part

		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name+"L")
		shape = objs[-1]		
		
		if gv.zMotorMountLocation == "Top":
			#Rotate into correct orientation
			rotateAngle = 180
			rotateCenter = App.Vector(0,0,0)
			rotateAxis = App.Vector(0,0,1)
			Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

			#Define shifts and move 
			xShift = -gv.zRodSpacing/2+gv.zRodZScrewDist
			yShift = gv.extruderNozzleStandoff + gv.frameHeight 
			'''(+gv.frameHeight
					 +gv.xRodClampOverallThickness/2
					 +gv.xMotorMountPlateThickness
					 +gv.xEndZRodHolderFaceThickness
					 +gv.xEndZRodHolderMaxNutFaceToFace/2
					 +gv.zRodStandoff)'''
				 
			zShift = gv.zRodLength + gv.vertBarDistAboveZRod + gv.frameWidth
			
			Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
			App.ActiveDocument.recompute()
									
			if shape not in gv.zAxisParts:
				gv.zAxisParts.append(shape)

		elif gv.zMotorMountLocation == "Bottom":
			rotateAngle = -90
			rotateCenter = App.Vector(0,0,0)
			rotateAxis = App.Vector(0,0,1)
			Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

			#Define shifts and move 
			xShift = -gv.zRodSpacing/2-gv.frameWidth/2
			yShift = gv.extruderNozzleStandoff - gv.zRodStandoff
			zShift = -gv.yRodStandoff
			
			Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
			App.ActiveDocument.recompute()

		
		#Copy part and move it over to the right hand side
		App.ActiveDocument.addObject('Part::Feature',self.name+"R").Shape= shape.Shape
		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name+"R")
		shape = objs[-1]
		
		if gv.zMotorMountLocation == "Top":
			xShift = 2*(gv.zRodSpacing/2-gv.zRodZScrewDist)
			yShift = 0
			zShift = 0
	
			Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
			App.ActiveDocument.recompute()
			
			if shape not in gv.zAxisParts:
				gv.zAxisParts.append(shape)

		elif gv.zMotorMountLocation == "Bottom":
			rotateAngle = 180
			rotateCenter = App.Vector(0,
									 gv.extruderNozzleStandoff - gv.zRodStandoff,
									 0)
			rotateAxis = App.Vector(0,0,1)
			Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

				
		
	def draw(self):
		#determine the horizontal or verticle component of the shaftToMountHoleDist

		if gv.zMotorMountLocation == "Top":
			gv.zMotorMountMountingFaceWidth = gv.frameHeight
			gv.zMotorMountLength = gv.zMotorMountMountingFaceWidth+gv.zRodStandoff+gv.zMotorBodyWidth/2
			gv.zMotorMountEdgeToShaftHole = gv.zMotorMountMountingFaceWidth + gv.zRodStandoff
		if gv.zMotorMountLocation == "Bottom":
			gv.zMotorMountMountingFaceWidth = gv.frameWidth		
			gv.zMotorMountLength = gv.zMotorMountMountingFaceWidth/2+gv.zRodZScrewDist+gv.zMotorBodyWidth/2
			gv.zMotorMountEdgeToShaftHole = gv.zMotorMountMountingFaceWidth/2 + gv.zRodZScrewDist
		

		
		mountHoleSpacing = gv.zMotorMountPlateWidth/2
		
		#Make file and build part
		try:
			App.getDocument('zMotorMount').recompute()
			App.closeDocument("zMotorMount")
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		#make document
		App.newDocument("zMotorMount")
		App.setActiveDocument("zMotorMount")
		App.ActiveDocument=App.getDocument("zMotorMount")

		#Make plate
		#sketch points
		p1x = -gv.zMotorMountPlateWidth/2
		p1y = 0
		p2x = -gv.zMotorMountPlateWidth/2
		p2y = gv.zMotorMountLength
		p3x = gv.zMotorMountPlateWidth/2
		p3y = gv.zMotorMountLength
		p4x = gv.zMotorMountPlateWidth/2
		p4y = 0
		
		#Make Sketch
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
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',0,2,0,1,-1,1)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,gv.zMotorMountLength)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',0,gv.zMotorMountPlateWidth)) 
		App.ActiveDocument.recompute()
		
		#Pad plate
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.zMotorMountPlateThickness
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#Make holes for mounting plate to frame
		#Sketch Points
		p1x = -mountHoleSpacing/2
		p1y = gv.zMotorMountMountingFaceWidth/2
		p2x = mountHoleSpacing/2
		p2y = gv.zMotorMountMountingFaceWidth/2
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
														  None,None,
														  None, None,
														  gv.zMotorMountPlateThickness, 0)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',0,2,0,1,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.toggleConstruction(0) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,3,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',2,gv.mountToFrameDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',0,mountHoleSpacing)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',-1,1,0,gv.zMotorMountMountingFaceWidth/2)) 
		App.ActiveDocument.recompute()
		App.getDocument('zMotorMount').recompute()
		
		#Cut holes through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()

		#Make motorMountHoles in plate
		#Sketch points

		p1x = -gv.zShaftToMountHoleDistX
		p1y = gv.zMotorMountEdgeToShaftHole-gv.zShaftToMountHoleDistX
		p2x = -gv.zShaftToMountHoleDistX
		p2y = gv.zMotorMountEdgeToShaftHole+gv.zShaftToMountHoleDistX
		p3x = gv.zShaftToMountHoleDistX
		p3y = gv.zMotorMountEdgeToShaftHole+gv.zShaftToMountHoleDistX
		p4x = gv.zShaftToMountHoleDistX
		p4y = gv.zMotorMountEdgeToShaftHole-gv.zShaftToMountHoleDistX
		p5x = 0
		p5y = gv.zMotorMountEdgeToShaftHole
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
														  None,None,
														  None, None,
														  gv.zMotorMountPlateThickness, 0)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.toggleConstruction(2) 
		App.ActiveDocument.Sketch002.toggleConstruction(1) 
		App.ActiveDocument.Sketch002.toggleConstruction(0) 
		App.ActiveDocument.Sketch002.toggleConstruction(3) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.zMotorMountShaftHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',4,3,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.zMotorMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',5,3,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.zMotorMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',6,3,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.zMotorMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',7,3,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p4x,p4y,0),App.Vector(0,0,1),gv.zMotorMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',8,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',5,6)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',6,8)) 
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',8,7)) 
		App.ActiveDocument.recompute()
		
		if gv.zMotorMountHoles ==2:
			App.ActiveDocument.Sketch002.toggleConstruction(5) 
			App.ActiveDocument.Sketch002.toggleConstruction(8) 
			App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceY',1,2*gv.zShaftToMountHoleDistX)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',6,gv.zMotorMountHoleDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',4,gv.zMotorMountShaftHoleDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Distance',-1,1,0,p1y)) 
		App.ActiveDocument.recompute()
		
		#Add symetric constraint
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Symmetric',0,2,2,2,4,3)) 
		App.ActiveDocument.recompute()
		App.getDocument('zMotorMount').recompute()
		
		#Cut holes
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()

		#Set view as axometric

'''
		def dimOptions(d, offset):
			d.ViewObject.ExtLines.Value = offset
			d.ViewObject.ArrowType = "Arrow"
			d.ViewObject.ArrowSize.Value = 2
			d.ViewObject.LineWidth = 1
		
		fontSize = 7
		
		#add dimensions for drawing
		#width
		offset = 20
		p1 = App.Vector(-gv.zMotorMountPlateWidth/2,gv.zMotorMountLength,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,gv.zMotorMountLength,0)
		p3 = App.Vector(0,gv.zMotorMountLength+offset,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
		dim.ViewObject.FontSize = fontSize


		#length
		offset = 55
		p1 = App.Vector(gv.zMotorMountPlateWidth/2,0,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,gv.zMotorMountLength,0)
		p3 = App.Vector(gv.zMotorMountPlateWidth/2+offset,gv.zMotorMountLength/2,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
		dim.ViewObject.TextPosition = (gv.zMotorMountPlateWidth/2+offset+2,-25,0)
		dim.ViewObject.FontSize = fontSize
#		dim.ViewObject.FlipArrows = True
		
		#Mounting holes
		#Along y axis
		offset = 15
		p1 = App.Vector(gv.zMotorMountPlateWidth/2,0,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,gv.zMotorMountMountingFaceWidth/2,0)
		p3 = App.Vector(gv.zMotorMountPlateWidth/2+offset,0,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
		dim.ViewObject.FlipArrows = True
		dim.ViewObject.TextPosition = (gv.zMotorMountPlateWidth/2+offset+2,-25,0)
		dim.ViewObject.FontSize = fontSize
		
		#Inner Motor mount holes y
		offset = 25
		p1 = App.Vector(gv.zMotorMountPlateWidth/2,0,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,gv.zMotorMountEdgeToShaftHole-gv.zShaftToMountHoleDistX,0)
		p3 = App.Vector(gv.zMotorMountPlateWidth/2+offset,0,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
#		dim.ViewObject.FlipArrows = True
		dim.ViewObject.TextPosition = (gv.zMotorMountPlateWidth/2+offset+2,-25,0)
		dim.ViewObject.FontSize = fontSize
		
		#motor Shaft y
		offset = 35
		p1 = App.Vector(gv.zMotorMountPlateWidth/2,0,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,gv.zMotorMountEdgeToShaftHole,0)
		p3 = App.Vector(gv.zMotorMountPlateWidth/2+offset,0,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
#		dim.ViewObject.FlipArrows = True
		dim.ViewObject.TextPosition = (gv.zMotorMountPlateWidth/2+offset+2,-25,0)
		dim.ViewObject.FontSize = fontSize
		
		#Outer Motor Mount holes y
		offset = 45
		p1 = App.Vector(gv.zMotorMountPlateWidth/2,0,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,gv.zMotorMountEdgeToShaftHole+gv.zShaftToMountHoleDistX,0)
		p3 = App.Vector(gv.zMotorMountPlateWidth/2+offset,0,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
#		dim.ViewObject.FlipArrows = True
		dim.ViewObject.TextPosition = (gv.zMotorMountPlateWidth/2+offset+2,-25,0)
		dim.ViewObject.FontSize = fontSize
		
		#RHS motor mount holes x
		offset = 10
		p1 = App.Vector(gv.zShaftToMountHoleDistX,0,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,0,0)
		p3 = App.Vector(0,-offset,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
		dim.ViewObject.FlipArrows = True
		dim.ViewObject.TextPosition = (-gv.zMotorMountPlateWidth/2-15,-offset-2,0)
		dim.ViewObject.FontSize = fontSize
		
		#RHS frame mount hole x
		offset = 20
		p1 = App.Vector(gv.zMotorMountPlateWidth/4,0,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,0,0)
		p3 = App.Vector(0,-offset,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
		dim.ViewObject.FlipArrows = True
		dim.ViewObject.TextPosition = (-gv.zMotorMountPlateWidth/2-17,-offset-2,0)
		dim.ViewObject.FontSize = fontSize
		
		#Motor Shaft hole x
		offset = 30
		p1 = App.Vector(0,0,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,0,0)
		p3 = App.Vector(0,-offset,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
#		dim.ViewObject.FlipArrows = True
		dim.ViewObject.TextPosition = (-gv.zMotorMountPlateWidth/2-17,-offset-2,0)		
		dim.ViewObject.FontSize = fontSize

		#LHS frame mount hole x
		offset = 40
		p1 = App.Vector(-gv.zMotorMountPlateWidth/4,0,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,0,0)
		p3 = App.Vector(0,-offset,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
#		dim.ViewObject.FlipArrows = True
		dim.ViewObject.TextPosition = (-gv.zMotorMountPlateWidth/2-17,-offset-2,0)
		dim.ViewObject.FontSize = fontSize
		
		#LHS motor mount holes x
		offset = 50
		p1 = App.Vector(-gv.zShaftToMountHoleDistX,0,0)
		p2 = App.Vector(gv.zMotorMountPlateWidth/2,0,0)
		p3 = App.Vector(0,-offset,0)
		dim = Draft.makeDimension(p1,p2,p3)
		dimOptions(dim, offset)
#		dim.ViewObject.FlipArrows = True
		dim.ViewObject.TextPosition = (-gv.zMotorMountPlateWidth/2-15,-offset-2,0)
		dim.ViewObject.FontSize = fontSize
'''
'''
		
p1 = FreeCAD.Vector(0,0,0)
p2 = FreeCAD.Vector(100,10,0)
p3 = FreeCAD.Vector(10,200,0)
d = Draft.makeDimension(p1,p2,p3)
d.ViewObject.FontSize = 20
object = App.ActiveDocument.Pocket001.Shape
v1 = App.ActiveDocument.Pocket001.Shape.Edges[3].Vertexes[0]
v2 = App.ActiveDocument.Pocket001.Shape.Edges[3].Vertexes[1]
p3 = FreeCAD.Vector(0,-10,0)
Draft.makeDimension (object,v1,v2,p3)

object = App.ActiveDocument.Pocket001
Draft.makeDimension (object,1,2,p3)

for point in App.ActiveDocument.Pocket001.Shape.Vertexes:
	if point.Point == v1.Point:
		print("yes")
		

'''
				
