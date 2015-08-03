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

class ExtruderMountPlate(object):
	def __init__(self, hotEndMountHoles = True):
		self.hotEndMountHoles = hotEndMountHoles
		self.name = "extruderMountPlate"

	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		#.ActiveDocument=#.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape= shape
		
		#Color Part
		#.ActiveDocument.getObject(self.name).ShapeColor = (gv.printedR,gv.printedG,gv.printedB,gv.printedA)
		
		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name)
		shape = objs[-1]		
		
		#Rotate into correct orientation
		rotateAngle = 180
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,0,1)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = -gv.xCarriageWidth/2
		yShift = ( gv.extruderDepth
				 - gv.extruderEdgeToCenterLine)
		zShift = (-gv.xCarriageBushingHolderOR
				 + gv.xCarriageMountHoleVertOffset
				 - (gv.extruderMountAngleWidth-gv.extruderMountAngleThickness)/2
				 +gv.extruderMountAngleWidth)
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()

		if shape not in gv.xAxisParts:
			gv.xAxisParts.append(shape)
			
	def draw(self):
	
	
		try:
			#.getDocument(self.name)
			#.getDocument(self.name).resetEdit()
			App.getDocument(self.name).recompute()
			App.closeDocument(self.name)
			App.setActiveDocument("")
			App.ActiveDocument=None
			#.ActiveDocument=None
		except:
			pass

		#make document
		App.newDocument(self.name)
		App.setActiveDocument(self.name)
		App.ActiveDocument=App.getDocument(self.name)
		#.ActiveDocument=#.getDocument(self.name)
		
		#Make profile of angle and extrude it
		p1x = -gv.extruderMountPlateWidth/2
		p1y = 0
		p2x = p1x
		p2y = gv.extruderDepth
		p3x = -p1x
		p3y = p2y
		p4x = p3x
		p4y = p1y
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
		#.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
#		#.activeDocument().setEdit('Sketch')
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
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,gv.extruderDepth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',0,gv.extruderMountPlateWidth)) 
		App.ActiveDocument.recompute()
#		#.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Pad extruderMountPlate
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		#.activeDocument().hide("Sketch")
		App.ActiveDocument.Pad.Length = gv.extruderMountPlateThickness
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()
#		#.activeDocument().resetEdit()
		
		#Make holes for mounting plate to angle
		#Sketch Points
		p1x = gv.extruderMountPlateWidth
		p1y = (gv.extruderMountAngleWidth+gv.extruderMountAngleThickness)/2
		p2x = -gv.xCarriageWidth/2+gv.xCarriageMountHoleHorizOffset
		p2y = p1y
		p3x = -p2x
		p3y = p1y
		p4x = -p1x
		p4y = p1y

		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
															None, None, 
															None, None, 
															gv.extruderMountPlateThickness, 0)#(App.ActiveDocument.Pad,["Face6"])
		App.activeDocument().recompute()
#		#.activeDocument().setEdit('Sketch001')
#		App.ActiveDocument.Sketch001.addExternal("Pad","Edge12")
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad ,
 																  -gv.extruderMountPlateWidth/2,0,
 																  None,None,
 																  gv.extruderMountPlateThickness,0))

		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
 																  gv.extruderMountPlateWidth/2,0,
 																  None,None,
 																  gv.extruderMountPlateThickness,0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',0)) 
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
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',2,2,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',2,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.toggleConstruction(0) 
		App.ActiveDocument.Sketch001.toggleConstruction(1) 
		App.ActiveDocument.Sketch001.toggleConstruction(2) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',4,3,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',4,3)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',4,gv.mountToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',0,2,0,1,-(gv.extruderMountPlateWidth/2-gv.xCarriageWidth/2+gv.xCarriageMountHoleHorizOffset))) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,2,(gv.extruderMountAngleWidth+gv.extruderMountAngleThickness)/2)) 
		App.ActiveDocument.recompute()
#		#.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Cut the holes
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		#.activeDocument().hide("Sketch001")
		#.activeDocument().hide("Pad")
#		#.activeDocument().setEdit('Pocket')
#		#.ActiveDocument.Pocket.ShapeColor=#.ActiveDocument.Pad.ShapeColor
#		#.ActiveDocument.Pocket.LineColor=#.ActiveDocument.Pad.LineColor
#		#.ActiveDocument.Pocket.PointColor=#.ActiveDocument.Pad.PointColor
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()
#		#.activeDocument().resetEdit()
		
		#make holes for mounting the extruder
		#Sketch Points
		p1x = -gv.extruderMountPlateWidth/2 
		p1y = gv.extruderDepth-gv.extruderEdgeToCenterLine
		p2x = -gv.extruderMountHoleSpacing/2
		p2y = p1y
		p3x = 0
		p3y = p1y
		p4x = -p2x
		p4y = p1y
		p5x = -p1x
		p5y = p1y
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
															None, None, 
															None, None, 
															gv.extruderMountPlateThickness, 0)#(App.ActiveDocument.Pocket,["Face5"])
		App.activeDocument().recompute()
#		#.activeDocument().setEdit('Sketch002')

		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket ,
 																  -gv.extruderMountPlateWidth/2,0,
 																  None,None,
 																  gv.extruderMountPlateThickness,0))

		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket, 
 																  gv.extruderMountPlateWidth/2,0,
 																  None,None,
 																  gv.extruderMountPlateThickness,0))
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',3,2,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',3,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.toggleConstruction(0) 
		App.ActiveDocument.Sketch002.toggleConstruction(1) 
		App.ActiveDocument.Sketch002.toggleConstruction(2) 
		App.ActiveDocument.Sketch002.toggleConstruction(3) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.extruderMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',4,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p4x,p4y,0),App.Vector(0,0,1),gv.extruderMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',5,3,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.extruderFilamentHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',6,3,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',4,5)) 
		App.ActiveDocument.recompute()
		
		#Add Dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceX',0,2,2,2,gv.extruderMountHoleSpacing)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceY',3,2,-4,2,gv.extruderEdgeToCenterLine)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',4,gv.extruderMountHoleDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',6,gv.extruderFilamentHoleDia/2)) 
		App.ActiveDocument.recompute()
#		#.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Cut holes through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		#.activeDocument().hide("Sketch002")
		#.activeDocument().hide("Pocket")
#		#.ActiveDocument.Pocket001.ShapeColor=#.ActiveDocument.Pocket.ShapeColor
#		#.ActiveDocument.Pocket001.LineColor=#.ActiveDocument.Pocket.LineColor
#		#.ActiveDocument.Pocket001.PointColor=#.ActiveDocument.Pocket.PointColor
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()
#		#.activeDocument().resetEdit()
		
		#Cut holes for hot end mount if needed.
		if self.hotEndMountHoles:
			#Sketch Points
			p1x = -gv.hotEndMountHoleSpacing/2
			p1y = gv.extruderDepth-gv.extruderEdgeToCenterLine
			p2x = -p1x
			p2y = p1y
			
			#Make Sketch
			App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
			App.activeDocument().Sketch003.Support = uf.getFace(App.ActiveDocument.Pocket001,
															None, None, 
															None, None, 
															gv.extruderMountPlateThickness, 0)#(App.ActiveDocument.Pocket001,["Face5"])
			App.activeDocument().recompute()
	#		#.activeDocument().setEdit('Sketch003')
			App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',0)) 
			App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Symmetric',0,1,0,2,-2)) 
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch003.toggleConstruction(0) 
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch003.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.hotEndMountHoleDia/2))
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',1,3,0,1)) 
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch003.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.hotEndMountHoleDia/2))
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',2,3,0,2)) 
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Equal',1,2)) 
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Radius',2,gv.hotEndMountHoleDia/2)) 
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('DistanceX',0,gv.hotEndMountHoleSpacing)) 
			App.ActiveDocument.recompute()
			App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Distance',-1,1,0,p1y))
			
	#		#.getDocument(self.name).resetEdit()
			App.getDocument(self.name).recompute()
			
			#Cut hole Through All
			App.activeDocument().addObject("PartDesign::Pocket","Pocket002")
			App.activeDocument().Pocket002.Sketch = App.activeDocument().Sketch003
			App.activeDocument().Pocket002.Length = 5.0
			App.ActiveDocument.recompute()
			#.activeDocument().hide("Sketch003")
			#.activeDocument().hide("Pocket001")
	#		#.ActiveDocument.Pocket002.ShapeColor=#.ActiveDocument.Pocket001.ShapeColor
	#		#.ActiveDocument.Pocket002.LineColor=#.ActiveDocument.Pocket001.LineColor
	#		#.ActiveDocument.Pocket002.PointColor=#.ActiveDocument.Pocket001.PointColor
			App.ActiveDocument.Pocket002.Length = 5.000000
			App.ActiveDocument.Pocket002.Type = 1
			App.ActiveDocument.Pocket002.UpToFace = None
			App.ActiveDocument.recompute()
	#		#.activeDocument().resetEdit()

		#set View as axometric
	#	#.activeDocument().activeView().viewAxometric()
