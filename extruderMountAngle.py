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

class ExtruderMountAngle(object):
	def __init__(self):
		self.name = "extruderMountAngle"

	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Gui.ActiveDocument=Gui.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape= shape
		
		#Color Part
#		Gui.ActiveDocument.getObject(self.name).ShapeColor = (gv.printedR,gv.printedG,gv.printedB,gv.printedA)
		
		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name)
		shape = objs[-1]		
		
		#Rotate into correct orientation
		rotateAngle = 180
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,0,1)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = 0
		yShift = ( gv.extruderDepth
				 - gv.extruderEdgeToCenterLine)
		zShift = (-gv.xCarriageBushingHolderOR
				 + gv.xCarriageMountHoleVertOffset
				 - (gv.extruderMountAngleWidth-gv.extruderMountAngleThickness)/2
				 )
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()

		if shape not in gv.xAxisParts:
			gv.xAxisParts.append(shape)
			
	def draw(self):
	
	
		try:
			Gui.getDocument(self.name)
			Gui.getDocument(self.name).resetEdit()
			App.getDocument(self.name).recompute()
			App.closeDocument(self.name)
			App.setActiveDocument("")
			App.ActiveDocument=None
			Gui.ActiveDocument=None	
		except:
			pass

		#make document
		App.newDocument(self.name)
		App.setActiveDocument(self.name)
		App.ActiveDocument=App.getDocument(self.name)
		Gui.ActiveDocument=Gui.getDocument(self.name)
		
		#Make profile of angle and extrude it
		p1x = 0
		p1y = 0
		p2x = 0
		p2y = gv.extruderMountAngleWidth
		p3x = p2y
		p3y = p2y
		p4x = p3x
		p4y = gv.extruderMountAngleWidth-gv.extruderMountAngleThickness
		p5x = gv.extruderMountAngleThickness
		p5y = p4y
		p6x = p5x
		p6y = p1y

		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.500000,0.500000,0.500000,0.500000))
#		Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA\n  position 87 0 0 \n  orientation 0.57735026 0.57735026 0.57735026  2.0943952 \n  nearDistance -112.887\n  farDistance 287.28699\n  aspectRatio 1\n  focalDistance 87\n  height 143.52005\n\n}')
#		Gui.activeDocument().setEdit('Sketch')
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-2)) 
		App.ActiveDocument.recompute()

		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',5)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',2,5)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',0,gv.extruderMountAngleWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',2,-gv.extruderMountAngleThickness)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument('extruderMountAngle').resetEdit()
		App.getDocument('extruderMountAngle').recompute()
		
		#Extrude the extruder mount angle
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch")
		App.ActiveDocument.Pad.Length = gv.xCarriageWidth
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		
		#Cut holes for mounting to xCarriage
		#Sketch Points
		p1x = (gv.extruderMountAngleWidth-gv.extruderMountAngleThickness)/2
		p1y = gv.xCarriageWidth
		p2x = p1x
		p2y = gv.xCarriageWidth-gv.xCarriageMountHoleHorizOffset
		p3x = p1x
		p3y = gv.xCarriageMountHoleHorizOffset
		p4x = p1x
		p4y = 0
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
															None, None, 
															gv.extruderMountAngleThickness,0, 
															None, None)#(App.ActiveDocument.Pad,["Face5"])
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch001')
#		App.ActiveDocument.Sketch001.addExternal("Pad","Edge16")
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
 																  gv.xCarriageWidth,0,
 																  gv.extruderMountAngleThickness, 0,
 																  (gv.extruderMountAngleWidth-gv.extruderMountAngleThickness)/2,0))
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad, 
 																  0,0,
 																  gv.extruderMountAngleThickness, 0,
 																  (gv.extruderMountAngleWidth-gv.extruderMountAngleThickness)/2,0))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',2,2,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',-3,1,-3,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',0,2)) 
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
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',3,gv.mountToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',0,-gv.xCarriageMountHoleHorizOffset)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Cut mounting holes through all
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
		
		#Make mounting holes for extruderMountPlate
		#SketchPoints
		p1x = (gv.extruderMountAngleWidth+gv.extruderMountAngleThickness)/2
		p1y = gv.xCarriageWidth
		p2x = p1x
		p2y = gv.xCarriageWidth-gv.xCarriageMountHoleHorizOffset
		p3x = p1x
		p3y = gv.xCarriageMountHoleHorizOffset
		p4x = p1x
		p4y = 0
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
															None, None, 
															None, None, 
															gv.extruderMountAngleWidth-gv.extruderMountAngleThickness, 0)#(App.ActiveDocument.Pocket,["Face10"])
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch002')
		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket, 
 																  gv.xCarriageWidth,0,
 																  (gv.extruderMountAngleWidth+gv.extruderMountAngleThickness)/2, 0,
 																  (gv.extruderMountAngleWidth-gv.extruderMountAngleThickness),0))
		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket, 
 																  0,0,
 																  (gv.extruderMountAngleWidth+gv.extruderMountAngleThickness)/2, 0,
 																  (gv.extruderMountAngleWidth-gv.extruderMountAngleThickness),0))

		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',2,2,-4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',2)) 
		App.ActiveDocument.recompute()
		
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Symmetric',-3,1,-3,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.toggleConstruction(0) 
		App.ActiveDocument.Sketch002.toggleConstruction(1) 
		App.ActiveDocument.Sketch002.toggleConstruction(2) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',3,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.mountToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',4,3,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',4,3)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',3,gv.mountToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceY',0,-gv.xCarriageMountHoleHorizOffset)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Cut mounting holes through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch002")
		Gui.activeDocument().hide("Pocket")
#		Gui.ActiveDocument.Pocket001.ShapeColor=Gui.ActiveDocument.Pocket.ShapeColor
#		Gui.ActiveDocument.Pocket001.LineColor=Gui.ActiveDocument.Pocket.LineColor
#		Gui.ActiveDocument.Pocket001.PointColor=Gui.ActiveDocument.Pocket.PointColor
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		
		