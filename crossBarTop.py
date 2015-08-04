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

class CrossBarTop(object):
	def __init__(self):
		self.name = "crossBarTop"
		
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
		rotateAngle = 90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(1,0,0)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = -(gv.zRodSpacing+gv.frameWidth)/2
		yShift = gv.extruderNozzleStandoff+gv.frameHeight/2
		zShift =  (-gv.yRodStandoff
				  + gv.vertBarLength
				  + gv.frameWidth/2)
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()


	def draw(self):
		try:
			App.getDocument(self.name).recompute()
			App.closeDocument(self.name)
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		#make document
		App.newDocument(self.name)
		App.setActiveDocument(self.name)
		App.ActiveDocument=App.getDocument(self.name)

		#extrude crossBarTop
		uf.extrudeFrameMember(self.name, gv.crossBarLength)

		if gv.zMotorMountLocation == "Bottom":
			return
					
		#Make Holes for zMotorMount plates
		#Sketch points
		p1x = 0
		p1y = 0
		p2x = p1x
		p2y = gv.frameWidth/2+gv.zRodZScrewDist-gv.zMotorMountPlateWidth/4
		p3x = p1x
		p3y = gv.frameWidth/2+gv.zRodZScrewDist+gv.zMotorMountPlateWidth/4
		p4x = p1x
		p4y = gv.crossBarLength - (gv.frameWidth/2+gv.zRodZScrewDist+gv.zMotorMountPlateWidth/4)
		p5x = p1x
		p5y = gv.crossBarLength - (gv.frameWidth/2+gv.zRodZScrewDist-gv.zMotorMountPlateWidth/4)
		p6x = p1x
		p6y = gv.crossBarLength
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = (App.ActiveDocument.Pad,["Face2"])
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addExternal("Pad","Edge7")
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,1)) 
		App.ActiveDocument.recompute()
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
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',4,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',1,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',4,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.toggleConstruction(0) 
		App.ActiveDocument.Sketch001.toggleConstruction(1) 
		App.ActiveDocument.Sketch001.toggleConstruction(2) 
		App.ActiveDocument.Sketch001.toggleConstruction(3) 
		App.ActiveDocument.Sketch001.toggleConstruction(4) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',5,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',6,3,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p4x,p4y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',7,3,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',8,3,3,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',8,7)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',7,6)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',6,5)) 
		App.ActiveDocument.recompute()
		
		#Add Dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',8,gv.mountToFrameDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',3,gv.zMotorMountPlateWidth/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',4,p2y)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Cut holes through All
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()
