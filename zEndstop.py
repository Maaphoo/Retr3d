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

class ZEndstop(object):
	def __init__(self):
		self.name = "zEndstop"

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

		rotateAngle = -90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,0,1)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the into place
		xShift = -gv.zRodSpacing/2 + gv.zEndstopBodyThickness + gv.zRodDiaL/2
		yShift = gv.extruderNozzleStandoff	- gv.zRodStandoff		 
		zShift = gv.zRodSupportLength
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()

		if shape not in gv.zAxisParts:
			gv.zAxisParts.append(shape)
			

	def draw(self):

		#helper Variables

		#Make the coresponding xRodClamp
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
		App.ActiveDocument=App.getDocument(self.name)
		
		#Make clamp body
		#Sketch points
		p1x = -gv.zEndstopSupportWidth/2
		p1y = 0
		p2x = -gv.zEndstopSupportWidth/2
		p2y = gv.zEndStopClampLength
		p3x = gv.zEndstopSupportWidth/2
		p3y = gv.zEndStopClampLength
		p4x = gv.zEndstopSupportWidth/2
		p4y = p1y

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
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',0,2,0,1,-1,1))
		App.ActiveDocument.recompute()
		
		#add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,gv.zEndStopClampLength)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',2,-gv.zEndstopSupportWidth)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#pad rod support
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.zRodDiaL/2+gv.zEndstopBodyThickness-gv.clampGap/2
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#make cut out for rod
		#sketch points
		p1x = 0
		p1y = gv.zRodDiaL/2+gv.zEndstopBodyThickness
		
		#Make Sketch
		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
														  None, None,
														  0,0,
														  None, None)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad,
														  0,0,
														  0,0,
														  gv.zRodDiaL/2+gv.zEndstopBodyThickness-gv.clampGap/2, 0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.zRodDiaL/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-2)) 
		App.ActiveDocument.recompute()
		
		#add dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',0,3,-3,gv.clampGap/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',0,gv.zRodDiaL/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Cut through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()


		#cut Right clamp hole
		#Sketch points
		p1x = gv.zRodDiaL/2+gv.printedToPrintedDia/2
		p1y = gv.printedToPrintedDia/2 + gv.mountToPrintedPadding
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
														  0,1,
														  None, None,
														  gv.zRodDiaL/2+gv.zEndstopBodyThickness-gv.clampGap/2, 0)
		App.activeDocument().recompute()
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket,
														  gv.zEndstopSupportWidth/2,0,
														  gv.zEndStopClampLength/2,0,
														  gv.zRodDiaL/2+gv.zEndstopBodyThickness-gv.clampGap/2, 0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
#		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Distance',0,3,-3,p1y)) 
		App.ActiveDocument.recompute()
#		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,p1y)) 
		App.ActiveDocument.recompute()
#		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',0,gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Cut clamp hole through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()

		#Mirror clamp hole
		App.activeDocument().addObject("PartDesign::Mirrored","Mirrored")
		App.ActiveDocument.recompute()
		App.activeDocument().Mirrored.Originals = [App.activeDocument().Pocket001,]
		App.activeDocument().Mirrored.MirrorPlane = (App.activeDocument().Sketch002, ["V_Axis"])
		App.ActiveDocument.Mirrored.Originals = [App.ActiveDocument.Pocket001,]
		App.ActiveDocument.Mirrored.MirrorPlane = (App.ActiveDocument.Sketch002,["V_Axis"])
		App.ActiveDocument.recompute()

		#Make channel for contact
		#Sketch Points
		p1x = -gv.zEndstopSupportWidth/2
		p1y = -(2*gv.mountToPrintedPadding
				+ gv.printedToPrintedDia
				+ 2*gv.xEndstopChannelWidth
				+gv.zEndstopJogWidth)
		p2x = p1x
		p2y = -(2*gv.mountToPrintedPadding
				+ gv.printedToPrintedDia
				+gv.zEndstopJogWidth)
		p3x = -gv.zEndstopJogWidth
		p3y = p2y
		p4x = 0
		p4y = -(2*gv.mountToPrintedPadding
			  + gv.printedToPrintedDia)
		p5x = -p3x
		p5y = p2y
		p6x = -p1x
		p6y = p2y
		p7x = p6x
		p7y = p1y
		p8x = p5x-(gv.xEndstopChannelWidth*math.tan(math.pi/8))
		p8y = p1y
		p9x = p8x-math.pow(2,0.5)*gv.xEndstopChannelWidth*math.tan(math.pi/8)
		p9y = p1y+math.pow(2,0.5)*gv.xEndstopChannelWidth*math.tan(math.pi/8)
		p10x = p4x
		p10y = p1y+gv.zEndstopJogWidth-math.pow(2,0.5)*gv.xEndstopChannelWidth*math.tan(math.pi/8)
		p11x = p3x+(gv.xEndstopChannelWidth*math.tan(math.pi/8))+math.pow(2,0.5)*gv.xEndstopChannelWidth*math.tan(math.pi/8)
		p11y = p9y
		p12x = p3x+(gv.xEndstopChannelWidth*math.tan(math.pi/8))
		p12y = p1y

		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
		App.activeDocument().Sketch003.Support = uf.getFace(App.ActiveDocument.Mirrored,
														  0,0,
														  None, None,
														  0, 0)
		App.activeDocument().recompute()
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch003.addExternal("Mirrored",uf.getEdge(App.ActiveDocument.Mirrored,
														  -gv.zEndstopSupportWidth/2,0,
														  gv.zEndStopClampLength/2,0,
														  0, 0))
		App.ActiveDocument.Sketch003.addExternal("Mirrored",uf.getEdge(App.ActiveDocument.Mirrored, 
														  gv.zEndstopSupportWidth/2,0,
														  gv.zEndStopClampLength/2,0,
														  0, 0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Vertical',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',4,2,-4))
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',5,2,6,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',5,2,-4))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p9x,p9y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',6,2,7,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p9x,p9y,0),App.Vector(p10x,p10y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',7,2,8,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
#		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',8,2,-3)) 
		App.ActiveDocument.recompute()
#		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',8)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p10x,p10y,0),App.Vector(p11x,p11y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',8,2,9,1)) 
		App.ActiveDocument.recompute()
#		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Vertical',9)) 
		App.ActiveDocument.recompute()
#		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',3,2,-4)) 
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p11x,p11y,0),App.Vector(p12x,p12y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',9,2,10,1)) 
		App.ActiveDocument.recompute()
#		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',10,2,7)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p12x,p12y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p11x,p11y,0)))
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p9x,p9y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',10,2,11,1)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',11,2,0,1)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',6)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',11)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',2,2,-2)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',8,2,-2)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Parallel',9,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Parallel',3,8)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.toggleConstruction(13) 
		App.ActiveDocument.Sketch003.toggleConstruction(12) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Equal',0,12)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Equal',12,13)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Equal',13,5)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Perpendicular',2,3))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',12,2,9,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',12,1,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',3,2,13,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',13,2,7,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Perpendicular',12,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Perpendicular',13,3)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Parallel',10,9)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Parallel',7,8)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',6,2,11))
		
		
		#add dimensions
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('DistanceY',5,-gv.xEndstopChannelWidth))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('DistanceY',3,2,2,2,gv.zEndstopJogWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('DistanceY',-1,1,2,2,-9.963388))
		App.ActiveDocument.recompute()
		
		App.getDocument('zEndstop').recompute()
		
		#Cut top channel
		App.activeDocument().addObject("PartDesign::Pocket","Pocket002")
		App.activeDocument().Pocket002.Sketch = App.activeDocument().Sketch003
		App.activeDocument().Pocket002.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket002.Length = 3.000000
		App.ActiveDocument.Pocket002.Type = 0
		App.ActiveDocument.Pocket002.UpToFace = None
		App.ActiveDocument.recompute()

		#Use a linear pattern to add other channel
		App.activeDocument().addObject("PartDesign::LinearPattern","LinearPattern")
		App.ActiveDocument.recompute()
		App.activeDocument().LinearPattern.Originals = [App.activeDocument().Pocket002,]
		App.activeDocument().LinearPattern.Direction = (App.activeDocument().Sketch003, ["H_Axis"])
		App.activeDocument().LinearPattern.Length = 100
		App.activeDocument().LinearPattern.Occurrences = 2
		App.ActiveDocument.LinearPattern.Originals = [App.ActiveDocument.Pocket002,]
		App.ActiveDocument.LinearPattern.Direction = (App.ActiveDocument.Sketch003,["V_Axis"])
		App.ActiveDocument.LinearPattern.Reversed = 1
		App.ActiveDocument.LinearPattern.Length = 3.500000
		App.ActiveDocument.LinearPattern.Occurrences = 2
		App.ActiveDocument.recompute()


		#Set view as axometric

