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

class VerticalBars(object):
	def __init__(self):
		self.name = "verticalBars"

	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name+"L").Shape= shape
		
		#Color Part

		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name+"L")
		shape = objs[-1]		
		
		#Rotate into correct orientation
		rotateAngle = -90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,1,0)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		rotateAngle = 90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,0,1)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)
		
		#Define shifts and move the left clamp into place
		xShift = -gv.zRodSpacing/2
		yShift = gv.extruderNozzleStandoff+gv.frameHeight/2
		
# 				(gv.frameHeight/2
# 				+ gv.zRodStandoff
# 				+ gv.xRodClampOverallThickness/2
# 				+ gv.xMotorMountPlateThickness
# 				+ gv.xEndZRodHolderFaceThickness
# 				+ gv.xEndZRodHolderMaxNutFaceToFace/2)
								
				 
		zShift = -gv.yRodStandoff
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		#Copy part 
		App.ActiveDocument.addObject('Part::Feature',self.name+"R").Shape= shape.Shape	
		verticalBarL = App.ActiveDocument.getObjectsByLabel(self.name+"R")[-1]
		
		#Color part

		#Move copy to Right side
		xShift = gv.zRodSpacing
		yShift = 0
		zShift = 0
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([verticalBarL],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()		

			
	def draw(self):
		#Helper variables
		mountHoleSpacing = gv.zRodSupportLength+2*gv.slotPadding+gv.slotDia
	
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

		#extrude verticalBar
		uf.extrudeFrameMember(self.name, gv.vertBarLength)
		
			
		#Make Holes for xRodSupports
		#Sketch Points
		p1x = 0 
		p1y = gv.vertBarLength
		p2x = p1x
		p2y = gv.vertBarLength-gv.vertBarDistAboveZRod-gv.zRodSupportLength/2+mountHoleSpacing/2
		p3x = p1x
		p3y = gv.vertBarLength-gv.vertBarDistAboveZRod-gv.zRodSupportLength/2-mountHoleSpacing/2
		p4x = p1x
		p4y = gv.vertBarDistBelowZRod+gv.zRodSupportLength/2+mountHoleSpacing/2
		p5x = p1x
		p5y = gv.vertBarDistBelowZRod+gv.zRodSupportLength/2-mountHoleSpacing/2
		p6x = p1x
		p6y = 0
		p7x = p1x
		p7y = gv.vertBarLength-(gv.zRodSupportLength/2+gv.vertBarDistAboveZRod)
		p8x = p1x
		p8y = gv.vertBarDistBelowZRod+gv.zRodSupportLength/2
		
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
														 gv.vertBarLength/2, 0,
														 None, None,
														 gv.frameHeight/2, 0)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad,
																 gv.vertBarLength, 0,
																 None, None, 
																 gv.frameHeight/2, 0))
		App.ActiveDocument.recompute()		
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
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-2)) 
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
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',3,2,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',4,2,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.delConstraint(8)
		App.ActiveDocument.Sketch001.toggleConstruction(4) 
		App.ActiveDocument.Sketch001.toggleConstruction(3) 
		App.ActiveDocument.Sketch001.toggleConstruction(2) 
		App.ActiveDocument.Sketch001.toggleConstruction(1) 
		App.ActiveDocument.Sketch001.toggleConstruction(0) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',1,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Point(App.Vector(p7x,p7y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',5,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',0,2,1,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Point(App.Vector(p8x,p8y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',6,1,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',3,2,2,2,6,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',7,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',8,3,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p4x,p4y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',9,3,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',10,3,3,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',7,8)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',8,9)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',9,10)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',7,gv.mountToFrameDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',1,-mountHoleSpacing)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',0,1,5,1,gv.zRodSupportLength/2+gv.vertBarDistAboveZRod)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',-1,1,6,1,gv.vertBarDistBelowZRod+gv.zRodSupportLength/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Cut holes through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()

		