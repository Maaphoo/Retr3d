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

class SideBarTopL(object):
	def __init__(self):
		self.name = "sideBarTopL"
		
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
		rotateAxis = App.Vector(0,0,1)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = -gv.zRodSpacing/2
		yShift = -gv.yRodLength/2 + gv.frameWidth
		zShift = -gv.yRodStandoff - gv.frameHeight/2
		
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
		uf.extrudeFrameMember(self.name, gv.sideBarLength)
		
		if gv.zMotorMountLocation == "Top":
			return
		
		#Add holes for zMotorMount
		#Sketch points
		p1x = 0 
		p1y = 0
		p2x = 0
		p2y = gv.sideBarLength/2+gv.extruderNozzleStandoff-gv.zMotorMountPlateWidth/4 
		p3x = 0
		p3y = gv.sideBarLength/2+gv.extruderNozzleStandoff-3*gv.zMotorMountPlateWidth/4
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
														 gv.sideBarLength/2, 0,
														 None, None,
														 gv.frameHeight/2, 0)
		App.activeDocument().recompute()
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
		App.ActiveDocument.Sketch001.toggleConstruction(1) 
		App.ActiveDocument.Sketch001.toggleConstruction(0) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,3,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		App.ActiveDocument.recompute()
		
		#Add Dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',2,gv.mountToFrameDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',1,gv.zMotorMountPlateWidth/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',0,p3y)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Cut holes through Bar
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()
