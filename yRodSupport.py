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

#notes
#Nut facetoface top and bottom should be resolved into a max


class YRodSupport(object):
	def __init__(self,
				name = "yRodSupport",
				side = "Right",
				):
				
		self.name = name
		self.side = side
		if side == "Right":
			self.rodDia = gv.yRodDiaR
		elif side == "Left":
			self.rodDia = gv.yRodDiaL
		
		
	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		support = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name+"Front").Shape= support

		App.ActiveDocument=App.getDocument(self.name+"Clamp")
		clamp = App.ActiveDocument.ActiveObject.Shape

		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name+"ClampFront").Shape= clamp
			
		#Color Part

		#move into position relative to eachother
		objs = App.ActiveDocument.getObjectsByLabel(self.name+"ClampFront")
		clamp = objs[-1]

		#Rotate clamp 180 around y axis
		#Rotate into correct orientation
		rotateAngle = 180
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,1,0)
		Draft.rotate([clamp],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)	
		
		#Move clamp up z Axis
		xShift = 0
		yShift =0
		zShift = gv.clampThickness+gv.yRodDiaMax/2+gv.yRodStandoff
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([clamp],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		#Group Support and clamp together and move into position
		supportClampFront = App.ActiveDocument.getObjectsByLabel(self.name+"Front")
		supportClampFront.append(clamp)
		
		#Rotate into correct orientation
		rotateAngle = 0
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(1,0,0)
		Draft.rotate(supportClampFront,rotateAngle,rotateCenter,axis = rotateAxis,copy=False)	

		#Define shifts and move the left clamp into place
		if self.side == "Left":
			xShift = -gv.yRodSpacing/2
		else:
			xShift = +gv.yRodSpacing/2
		
		yShift = -gv.yRodLength/2 + gv.frameWidth/2#Front support
			
		zShift = -gv.yRodStandoff
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move(supportClampFront,App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		#Copy the support and clamp and then place it at the top position
		App.ActiveDocument.addObject('Part::Feature',self.name+"Back").Shape= supportClampFront[0].Shape	
		App.ActiveDocument.addObject('Part::Feature',self.name+"ClampBack").Shape= supportClampFront[1].Shape		
		
		#Color Parts

		supportClampBack = App.ActiveDocument.getObjectsByLabel(self.name+"Back")
		supportClampBack.append(App.ActiveDocument.getObjectsByLabel(self.name+"ClampBack")[-1])
		xShift = 0
		yShift = gv.yRodLength - gv.frameWidth
		zShift = 0
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move(supportClampBack,App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		for shape in supportClampFront:
			if shape not in gv.yAxisParts:
				gv.yAxisParts.append(shape)
		for shape in supportClampBack:
			if shape not in gv.yAxisParts:
				gv.yAxisParts.append(shape)
		
	def draw(self):
		if self.side == "Right":
			self.rodDia = gv.yRodDiaR
		elif self.side == "Left":
			self.rodDia = gv.yRodDiaL

		#set up helper Variables
		
		columnWidth = (gv.yRodDiaMax
					  + gv.printedToPrintedDia
					  + gv.clampNutFaceToFace
					  + 2*gv.clampNutPadding)					 
						

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
		
		#Create tabs
		#Sketch points
		p1x = -gv.yRodSupportWidth/2
		p1y = gv.frameWidth/2
		p2x = gv.yRodSupportWidth/2
		p2y = gv.frameWidth/2
		p3x = gv.yRodSupportWidth/2
		p3y = -gv.frameWidth/2
		p4x = -gv.yRodSupportWidth/2
		p4y = -gv.frameWidth/2
		
		#MakeSketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',0,1,1,2,-1,1)) 
		App.ActiveDocument.recompute()
		
		#add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,-gv.frameWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',2,-gv.yRodSupportWidth)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Pad Sketch
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.tabThickness
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#Cut slot on right side
		#Sketch points
		p1x = gv.yRodSupportWidth/2-gv.slotPadding-gv.slotDia/2-gv.slotWidth
		p1y = 0
		p2x = gv.yRodSupportWidth/2-gv.slotPadding-gv.slotDia/2
		p2y = 0
		p3x = gv.yRodSupportWidth/2-gv.slotPadding-gv.slotDia/2-gv.slotWidth
		p3y = -gv.slotDia/2
		p4x = gv.yRodSupportWidth/2-gv.slotPadding-gv.slotDia/2-gv.slotWidth
		p4y = gv.slotDia/2
		p5x = gv.yRodSupportWidth/2-gv.slotPadding-gv.slotDia/2
		p5y = gv.slotDia/2
		p6x = gv.yRodSupportWidth/2-gv.slotPadding-gv.slotDia/2
		p6y = -gv.slotDia/2
		p7x = gv.yRodSupportWidth/2-gv.slotPadding
		p7y = 0
		
		#Make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
														  None, None,
														  None, None,
														  gv.tabThickness, 0)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad,
														  gv.yRodSupportWidth/2,0,
														  None, None,
														  gv.tabThickness, 0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),4.217310),math.pi/2,-math.pi/2))
		App.ActiveDocument.Sketch001.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),4.217310),-math.pi/2,math.pi/2))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Tangent',0,2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Tangent',0,3)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Tangent',1,2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Tangent',1,3)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,1,3,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,2,2,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,1,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,2,1,2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Point(App.Vector(32.724319,-0.106919,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',4,1,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',4,1,1))
		
		#add dimensions 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',2,gv.slotWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',1,gv.slotDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',4,1,-3,gv.slotPadding)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Cut slot through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()

		#Mirror the slot
		App.activeDocument().addObject("PartDesign::Mirrored","Mirrored")
		App.ActiveDocument.recompute()
		App.activeDocument().Mirrored.Originals = [App.activeDocument().Pocket,]
		App.activeDocument().Mirrored.MirrorPlane = (App.activeDocument().Sketch001, ["V_Axis"])
		App.ActiveDocument.Mirrored.Originals = [App.ActiveDocument.Pocket,]
		App.ActiveDocument.Mirrored.MirrorPlane = (App.ActiveDocument.Sketch001,["V_Axis"])
		App.ActiveDocument.recompute()

		#Make rod support column
		#Sketch points
		p1x = -columnWidth/2
		p1y = -gv.frameWidth/2
		p2x = -columnWidth/2
		p2y = gv.frameWidth/2
		p3x = columnWidth/2
		p3y = gv.frameWidth/2
		p4x = columnWidth/2
		p4y = -gv.frameWidth/2
		
		#Make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Mirrored,
														  None, None,
														  None, None,
														  0, 0)
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
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Symmetric',0,1,1,2,-1,1)) 
		App.ActiveDocument.recompute()
		
		#add dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceY',1,gv.frameWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceX',2,-columnWidth)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#pad rod support
		App.activeDocument().addObject("PartDesign::Pad","Pad001")
		App.activeDocument().Pad001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pad001.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad001.Length = gv.yRodStandoff-gv.clampGap/2
		App.ActiveDocument.Pad001.Reversed = 1
		App.ActiveDocument.Pad001.Midplane = 0
		App.ActiveDocument.Pad001.Length2 = 100.000000
		App.ActiveDocument.Pad001.Type = 0
		App.ActiveDocument.Pad001.UpToFace = None
		App.ActiveDocument.recompute()

		#Refine shape
		App.ActiveDocument.addObject('Part::Feature','Refined').Shape=App.ActiveDocument.Pad001.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pad001.Label
		App.ActiveDocument.recompute()
		
		#make cut out for rod
		#Sketch Points
		p1x = 0
		p1y = gv.yRodStandoff
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
		App.activeDocument().Sketch003.Support = uf.getFace(App.ActiveDocument.Refined,
														  0,0,
														  -gv.frameWidth/2,0,
														  None, None)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),self.rodDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-2)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Radius',0,self.rodDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Distance',-1,1,0,3,gv.yRodStandoff)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#Make Cut
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch003
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()

		#Make Clamp hole
		#Sketch Points
		p1x = gv.yRodDiaMax/2+gv.printedToPrintedDia/2
		p1y = 0
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch004')
		App.activeDocument().Sketch004.Support = uf.getFace(App.ActiveDocument.Pocket001,
														  0, 1,
														  None, None,
														  gv.yRodStandoff-gv.clampGap/2, 0)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1)) 
		App.ActiveDocument.recompute()
		
		#Add Dimensions
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,3,gv.yRodDiaMax/2+gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Radius',0,gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()
		
		#Cut clamp hole though all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket002")
		App.activeDocument().Pocket002.Sketch = App.activeDocument().Sketch004
		App.activeDocument().Pocket002.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket002.Length = 5.000000
		App.ActiveDocument.Pocket002.Type = 1
		App.ActiveDocument.Pocket002.UpToFace = None
		App.ActiveDocument.recompute()

		#Mirror clamp hole
		App.activeDocument().addObject("PartDesign::Mirrored","Mirrored001")
		App.ActiveDocument.recompute()
		App.activeDocument().Mirrored001.Originals = [App.activeDocument().Pocket002,]
		App.activeDocument().Mirrored001.MirrorPlane = (App.activeDocument().Sketch004, ["V_Axis"])
		App.ActiveDocument.Mirrored001.Originals = [App.ActiveDocument.Pocket002,]
		App.ActiveDocument.Mirrored001.MirrorPlane = (App.ActiveDocument.Sketch004,["V_Axis"])
		App.ActiveDocument.recompute()

		App.ActiveDocument.addObject('Part::Feature','Refined001').Shape=App.ActiveDocument.Mirrored001.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label='Refined001'

		App.ActiveDocument.recompute()
		
		#Cut nut trap in bottom of support
				#Add Nut trap to right side
		#Sketch Points
		mat = uf.hexagonPoints(gv.yRodDiaMax/2+gv.printedToPrintedDia/2,
								0,
								gv.clampNutFaceToFace,
								0)

		p1x = mat[0][0] 
		p1y = mat[0][1]
		p2x = mat[1][0]
		p2y = mat[1][1]
		p3x = mat[2][0]
		p3y = mat[2][1]
		p4x = mat[3][0]
		p4y = mat[3][1]
		p5x = mat[4][0]
		p5y = mat[4][1]
		p6x = mat[5][0]
		p6y = mat[5][1]
		p7x = mat[6][0]
		p7y = mat[6][1]
		hexRadius = mat[7][0]

		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch005')
		App.activeDocument().Sketch005.Support = uf.getFace(App.ActiveDocument.Refined001,
														  None, None,
														  None, None,
														  0, 0)
		App.activeDocument().recompute()

#error here
		App.ActiveDocument.Sketch005.addExternal("Refined001",uf.getEdge(App.ActiveDocument.Refined001, 
#  														  gv.yRodDiaMax/2+gv.printedToPrintedDia/2, 0,
														  None, None,None, None,
														  0,0,
 														  center = (gv.yRodDiaMax/2+gv.printedToPrintedDia/2,0,0),
 														  makeUnique = 1))
#  														  radius = gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),hexRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',0,1,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',0,2,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',1,2,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',2,2,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',3,2,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('PointOnObject',4,2,6)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Equal',5,0)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Equal',3,4)) 
		App.ActiveDocument.Sketch005.toggleConstruction(6) 
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Coincident',-3,3,6,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Vertical',2))

		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch005.addConstraint(Sketcher.Constraint('Distance',0,2,4,gv.clampNutFaceToFace)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name).recompute()

		#cut nut trap out
		App.activeDocument().addObject("PartDesign::Pocket","Pocket003")
		App.activeDocument().Pocket003.Sketch = App.activeDocument().Sketch005
		App.activeDocument().Pocket003.Length = 5.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pocket003.Length = gv.rodSupportNutTrapDepthMin
		App.ActiveDocument.Pocket003.Type = 0
		App.ActiveDocument.Pocket003.UpToFace = None
		App.ActiveDocument.recompute()

		#Mirror nut trap
		App.activeDocument().addObject("PartDesign::Mirrored","Mirrored002")
		App.ActiveDocument.recompute()
		App.activeDocument().Mirrored002.Originals = [App.activeDocument().Pocket003,]
		App.activeDocument().Mirrored002.MirrorPlane = (App.activeDocument().Sketch005, ["V_Axis"])
		App.ActiveDocument.Mirrored002.Originals = [App.ActiveDocument.Pocket003,]
		App.ActiveDocument.Mirrored002.MirrorPlane = (App.ActiveDocument.Sketch005,["V_Axis"])
		App.ActiveDocument.recompute()

		#Set view to axometric

		#Make Cap
		try:
			App.getDocument(self.name+"Clamp").recompute()
			App.closeDocument(self.name+"Clamp")
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		#make document
		App.newDocument(self.name+"Clamp")
		App.setActiveDocument(self.name+"Clamp")
		App.ActiveDocument=App.getDocument(self.name+"Clamp")
		App.ActiveDocument=App.getDocument(self.name+"Clamp")
		
		#Make clamp body
		#Sketch points
		p1x = -columnWidth/2
		p1y = -gv.frameWidth/2
		p2x = -columnWidth/2
		p2y = gv.frameWidth/2
		p3x = columnWidth/2
		p3y = gv.frameWidth/2
		p4x = columnWidth/2
		p4y = -gv.frameWidth/2

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
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',0,1,1,2,-1,1)) 
		App.ActiveDocument.recompute()
		
		#add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,gv.frameWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',2,-columnWidth)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name+"Clamp").recompute()
		
		#pad rod support
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.yRodDiaMax/2+gv.clampThickness-gv.clampGap/2
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#make cut out for rod
		#sketch points
		p1x = 0
		p1y = gv.yRodDiaMax/2+gv.clampThickness
		p2x = -self.rodDia/2
		p2y = gv.yRodDiaMax+gv.clampThickness
		p3x = self.rodDia/2
		p3y = gv.yRodDiaMax+gv.clampThickness
		
		#Make Sketch
		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
														  None, None,
														  -gv.frameWidth/2, 0,
														  None, None)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad,
														  None, None,
														  -gv.frameWidth/2, 0,
														  gv.yRodDiaMax/2+gv.clampThickness-gv.clampGap/2, 0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),self.rodDia/2),math.pi,2*math.pi))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,1,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,2,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,1)) 
		
		#Add dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',0,3,-3,gv.clampGap/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',0,self.rodDia/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name+"Clamp").recompute()
		
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
		p1x = gv.yRodDiaMax/2+gv.printedToPrintedDia/2
		p1y = 0
		
		#Make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
														  0, 1,
														  0, 0,
														  gv.yRodDiaMax/2+gv.clampThickness-gv.clampGap/2, 0)
		App.activeDocument().recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1)) 
		App.ActiveDocument.recompute()

		
		#Add dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',0,gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Distance',-1,1,0,3,gv.yRodDiaMax/2+gv.printedToPrintedDia/2)) 
		App.ActiveDocument.recompute()
		App.getDocument(self.name+"Clamp").recompute()
		
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

		#Set view as axometric


