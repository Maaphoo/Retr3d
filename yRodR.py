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

class YRodR(object):
	def __init__(self):
		self.name = "yRodR"

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
# 		rotateAngle = 0
# 		rotateCenter = App.Vector(0,0,0)
# 		rotateAxis = App.Vector(1,0,0)
# 		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = gv.yRodSpacing/2
		yShift = gv.yRodLength/2
		zShift = 0
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()


	def draw(self):
		try:
			Gui.getDocument('yRodR')
			Gui.getDocument('yRodR').resetEdit()
			App.getDocument('yRodR').recompute()
			App.closeDocument("yRodR")
			App.setActiveDocument("")
			App.ActiveDocument=None
			Gui.ActiveDocument=None	
		except:
			pass

		#make document
		App.newDocument("yRodR")
		App.setActiveDocument("yRodR")
		App.ActiveDocument=App.getDocument("yRodR")
		Gui.ActiveDocument=Gui.getDocument("yRodR")

		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))
		Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA\n  position 87 0 0 \n  orientation 0.57735026 0.57735026 0.57735026  2.0943952 \n  nearDistance -112.887\n  farDistance 287.28699\n  aspectRatio 1\n  focalDistance 87\n  height 143.52005\n\n}')
#		Gui.activeDocument().setEdit('Sketch')
		App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(0,0,0),App.Vector(0,0,1),gv.yRodDiaR/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',0,gv.yRodDiaR/2)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument('yRodR').resetEdit()
		App.getDocument('yRodR').recompute()

		#Pad sketch
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch")
		App.ActiveDocument.Pad.Length = gv.yRodLength
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()

		#set view as axiometric
#		Gui.activeDocument().activeView().viewAxometric()