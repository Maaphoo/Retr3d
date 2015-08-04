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
import utilityFunctions as uf

class ExtruderBarrel(object):
	def __init__(self):
		self.name = "extruderBarrel"
		
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
		xShift = -gv.xCarriageWidth/2
		yShift = 0
		zShift = (-gv.xCarriageBushingHolderOR
				 + gv.xCarriageMountHoleVertOffset
				 - (gv.extruderMountAngleWidth-gv.extruderMountAngleThickness)/2
				 + gv.extruderMountAngleWidth
				 - gv.extruderBarrelLength)

	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()

		if shape not in gv.xAxisParts:
			gv.xAxisParts.append(shape)

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

		#Revolve barrel body
		#Sketch points
		p1x = gv.extruderBarrelDia/2
		p1y = 0
		p2x = gv.extruderBarrelLinerDia/2
		p2y = p1y
		p3x = p2x
		p3y = gv.extruderBarrelLength
		p4x = p1x
		p4y = p3y

		#Make Sketch

		# make fin outline
		finThickness = ((gv.extruderBarrelLength
					  - 2*gv.extruderBarrelFaceThickness
					  - (gv.extruderBarrelNumFins+1)*gv.extruderBarrelFinGap)
					  / gv.extruderBarrelNumFins)
		y = gv.extruderBarrelLength - gv.extruderBarrelFaceThickness
		x1 = gv.extruderBarrelLinerDia/2 + gv.extruderBarrelCoreThickness
		x2 = gv.extruderBarrelDia/2
		i = 0
		
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-1)) 
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(x2,y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x2,y,0),App.Vector(x1,y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',4)) 

		for i in range(0, gv.extruderBarrelNumFins+1):
			App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x1,y,0),App.Vector(x1,y-gv.extruderBarrelFinGap,0)))
			App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4*i+4,2,4*i+5,1)) 
			App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',4*i+5)) 
			App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x1,y-gv.extruderBarrelFinGap,0),App.Vector(x2,y-gv.extruderBarrelFinGap,0)))
			App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4*i+5,2,4*i+6,1)) 
			App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',4*i+6)) 
				
			if i<gv.extruderBarrelNumFins:
				App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x2,y-gv.extruderBarrelFinGap,0),App.Vector(x2,y-gv.extruderBarrelFinGap-finThickness,0)))
				App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4*i+6,2,4*i+7,1)) 
				App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',4*i+7)) 
				App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x2,y-gv.extruderBarrelFinGap-finThickness,0),App.Vector(x1,y-gv.extruderBarrelFinGap-finThickness,0)))
				App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4*i+8,1,4*i+7,2))
				App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',4*i+8)) 
			y = y-gv.extruderBarrelFinGap-finThickness
			
			#add equal constraints
		for i in range(0, gv.extruderBarrelNumFins-1):
			App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',4*i+7,4*i+11)) 
		for i in range(0, gv.extruderBarrelNumFins):		
			App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',4*i+5,4*i+9)) 
			App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',4*i+4,4*i+6)) 
			App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',4*i+6,4*i+8))
			 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',4*gv.extruderBarrelNumFins+4,4*gv.extruderBarrelNumFins+6)) 

		#close sketch with the last vertical line
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x,p1y+gv.extruderBarrelFaceThickness,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4*gv.extruderBarrelNumFins+7,1,4*gv.extruderBarrelNumFins+6,2)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4*gv.extruderBarrelNumFins+7,2,0,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',4*gv.extruderBarrelNumFins+7)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',4*gv.extruderBarrelNumFins+7,3)) 
		
		#Add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-2,1,1,2,gv.extruderBarrelLinerDia/2)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-2,1,2,2,gv.extruderBarrelDia/2)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',3,-gv.extruderBarrelFaceThickness)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',5,-gv.extruderBarrelFinGap)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,gv.extruderBarrelLength)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Distance',4,2,1,gv.extruderBarrelCoreThickness)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#revolve profile to make barrel
		App.activeDocument().addObject("PartDesign::Revolution","Revolution")
		App.activeDocument().Revolution.Sketch = App.activeDocument().Sketch
		App.activeDocument().Revolution.ReferenceAxis = (App.activeDocument().Sketch,['V_Axis'])
		App.activeDocument().Revolution.Angle = 360.0
		App.activeDocument().Revolution.Reversed = 1
		App.ActiveDocument.recompute()
		App.ActiveDocument.Revolution.Angle = 360.000000
		App.ActiveDocument.Revolution.ReferenceAxis = (App.ActiveDocument.Sketch,['V_Axis'])
		App.ActiveDocument.Revolution.Midplane = 0
		App.ActiveDocument.Revolution.Reversed = 1
		App.ActiveDocument.recompute()

		#Make mounting holes in top face
		#Sketch Points
		p1x = gv.hotEndMountHoleSpacing/2
		p1y = 0

		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
#		App.activeDocument().Sketch001.Support = (App.ActiveDocument.Revolution,["Face3"])
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Revolution,
															0,0,
															0,0, 
															gv.extruderBarrelLength,0)

		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.extruderBarrelMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,gv.hotEndMountHoleSpacing/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',0,gv.extruderBarrelMountHoleDia/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = gv.extruderBarrelMountHoleDepth
		App.ActiveDocument.Pocket.Type = 0
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()

		#Copy hole to other side of face
		App.activeDocument().addObject("PartDesign::PolarPattern","PolarPattern")
		App.ActiveDocument.recompute()
		App.activeDocument().PolarPattern.Originals = [App.activeDocument().Pocket,]
		App.activeDocument().PolarPattern.Axis = (App.activeDocument().Sketch001, ["N_Axis"])
		App.activeDocument().PolarPattern.Angle = 360
		App.activeDocument().PolarPattern.Occurrences = 2
		App.ActiveDocument.PolarPattern.Originals = [App.ActiveDocument.Pocket,]
		App.ActiveDocument.PolarPattern.Axis = (App.ActiveDocument.Sketch001,["N_Axis"])
		App.ActiveDocument.PolarPattern.Reversed = 0
		App.ActiveDocument.PolarPattern.Angle = 360.000000
		App.ActiveDocument.PolarPattern.Occurrences = 2
		App.ActiveDocument.recompute()

		#Make mounting holes on bottom face
		p1x = gv.hotEndMountHoleSpacing/2
		p1y = 0

		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')

		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.PolarPattern,
															0,0,
															0,0, 
															0,0)
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.extruderBarrelMountHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,gv.hotEndMountHoleSpacing/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',0,gv.extruderBarrelMountHoleDia/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Cut holes
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket001.Length = gv.extruderBarrelMountHoleDepth
		App.ActiveDocument.Pocket001.Type = 0
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()

		#Copy hole to other side of bottom face
		App.activeDocument().addObject("PartDesign::PolarPattern","PolarPattern001")
		App.ActiveDocument.recompute()
		App.activeDocument().PolarPattern001.Originals = [App.activeDocument().Pocket001,]
		App.activeDocument().PolarPattern001.Axis = (App.activeDocument().Sketch002, ["N_Axis"])
		App.activeDocument().PolarPattern001.Angle = 360
		App.activeDocument().PolarPattern001.Occurrences = 2
		App.ActiveDocument.PolarPattern001.Originals = [App.ActiveDocument.Pocket001,]
		App.ActiveDocument.PolarPattern001.Axis = (App.ActiveDocument.Sketch002,["N_Axis"])
		App.ActiveDocument.PolarPattern001.Reversed = 0
		App.ActiveDocument.PolarPattern001.Angle = 360.000000
		App.ActiveDocument.PolarPattern001.Occurrences = 2
		App.ActiveDocument.recompute()

		#Set view
