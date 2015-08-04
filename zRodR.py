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

class ZRodR(object):
	def __init__(self):
		self.name = "zRodR"
		
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

		#Define shifts and move the left clamp into place
		xShift = +gv.zRodSpacing/2
		yShift = gv.extruderNozzleStandoff - gv.zRodStandoff				 
		zShift = 0
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()

		if shape not in gv.xAxisParts:
			gv.zAxisParts.append(shape)

	def draw(self):
		try:
			App.getDocument('zRodR').recompute()
			App.closeDocument("zRodR")
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		#make document
		App.newDocument("zRodR")
		App.setActiveDocument("zRodR")
		App.ActiveDocument=App.getDocument("zRodR")

		#make sketch
	#	sketch = App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
		App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(50,50,0),App.Vector(0,0,1),gv.zRodDiaR))
		App.ActiveDocument.recompute()
		#sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',0,gv.zRodDiaR/2)) 
		App.ActiveDocument.recompute()
		App.getDocument('zRodR').recompute()
				
		#Pad sketch
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.zRodLength
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#set view as axiometric