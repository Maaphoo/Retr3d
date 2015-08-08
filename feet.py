# Copyright 2015 Matthew Rogge
# 
# This file is part of Retr3d.
# 
# Retr3d is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Retr3d is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Retr3d.  If not, see <http://www.gnu.org/licenses/>.


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

class Feet(object):
    def __init__(self):
        self.name = "feet"

    def assemble(self):
        
        #Add front Left foot
        App.ActiveDocument=App.getDocument(self.name)
        shape = App.ActiveDocument.ActiveObject.Shape
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Gui.ActiveDocument=Gui.getDocument("PrinterAssembly")
        App.ActiveDocument.addObject('Part::Feature',self.name+"LeftFront").Shape= shape
        
        #Color Part
#        Gui.ActiveDocument.getObject(self.name+"LeftFront").ShapeColor = (gv.printedR,gv.printedG,gv.printedB,gv.printedA)
        
        #Get the feature and move it into position
        objs = App.ActiveDocument.getObjectsByLabel(self.name+"LeftFront")
        shape = objs[-1]        
        
        #Rotate into correct orientation
        rotateAngle = 180
        rotateCenter = App.Vector(0,0,0)
        rotateAxis = App.Vector(1,0,0)
        Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

        #Define shifts and move the left clamp into place
        xShift = -(gv.crossBarLength/2
                   - gv.frameWidth/2)
        yShift = -(gv.sideBarLength/2
                   -2*gv.frameSpacerOffset
                   -gv.frameHeight)
        zShift = -(gv.yRodStandoff
                   + 2*gv.frameHeight
                   + gv.frameSpacerLength)
    
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
        App.ActiveDocument.recompute()

        #Add Back Left foot
        App.ActiveDocument=App.getDocument(self.name)
        shape = App.ActiveDocument.ActiveObject.Shape
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Gui.ActiveDocument=Gui.getDocument("PrinterAssembly")
        App.ActiveDocument.addObject('Part::Feature',self.name+"LeftBack").Shape= shape
        
        #Color Part
#        Gui.ActiveDocument.getObject(self.name+"LeftFront").ShapeColor = (gv.printedR,gv.printedG,gv.printedB,gv.printedA)
        
        #Get the feature and move it into position
        objs = App.ActiveDocument.getObjectsByLabel(self.name+"LeftBack")
        shape = objs[-1]        
        
        #Rotate into correct orientation
        rotateAngle = 180
        rotateCenter = App.Vector(0,0,0)
        rotateAxis = App.Vector(1,0,0)
        Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

        #Define shifts and move the left clamp into place
        xShift = -(gv.crossBarLength/2
                   - gv.frameWidth/2)
        yShift = (gv.sideBarLength/2
                   -2*gv.frameSpacerOffset
                   -gv.frameHeight)
        zShift = -(gv.yRodStandoff
                   + 2*gv.frameHeight
                   + gv.frameSpacerLength)
    
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
        App.ActiveDocument.recompute()

        #Add front Right foot
        App.ActiveDocument=App.getDocument(self.name)
        shape = App.ActiveDocument.ActiveObject.Shape
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Gui.ActiveDocument=Gui.getDocument("PrinterAssembly")
        App.ActiveDocument.addObject('Part::Feature',self.name+"RightFront").Shape= shape
        
        #Color Part
#        Gui.ActiveDocument.getObject(self.name+"LeftFront").ShapeColor = (gv.printedR,gv.printedG,gv.printedB,gv.printedA)
        
        #Get the feature and move it into position
        objs = App.ActiveDocument.getObjectsByLabel(self.name+"RightFront")
        shape = objs[-1]        
        
        #Rotate into correct orientation
        rotateAngle = 180
        rotateCenter = App.Vector(0,0,0)
        rotateAxis = App.Vector(1,0,0)
        Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

        #Define shifts and move the left clamp into place
        xShift = (gv.crossBarLength/2
                   - gv.frameWidth/2)
        yShift = -(gv.sideBarLength/2
                   -2*gv.frameSpacerOffset
                   -gv.frameHeight)
        zShift = -(gv.yRodStandoff
                   + 2*gv.frameHeight
                   + gv.frameSpacerLength)
    
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
        App.ActiveDocument.recompute()

        
        #Add Back Right foot
        App.ActiveDocument=App.getDocument(self.name)
        shape = App.ActiveDocument.ActiveObject.Shape
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Gui.ActiveDocument=Gui.getDocument("PrinterAssembly")
        App.ActiveDocument.addObject('Part::Feature',self.name+"RightBack").Shape= shape
        
        #Color Part
#        Gui.ActiveDocument.getObject(self.name+"LeftFront").ShapeColor = (gv.printedR,gv.printedG,gv.printedB,gv.printedA)
        
        #Get the feature and move it into position
        objs = App.ActiveDocument.getObjectsByLabel(self.name+"RightBack")
        shape = objs[-1]        
        
        #Rotate into correct orientation
        rotateAngle = 180
        rotateCenter = App.Vector(0,0,0)
        rotateAxis = App.Vector(1,0,0)
        Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

        #Define shifts and move the left clamp into place
        xShift = (gv.crossBarLength/2
                   - gv.frameWidth/2)
        yShift = (gv.sideBarLength/2
                   -2*gv.frameSpacerOffset
                   -gv.frameHeight)
        zShift = -(gv.yRodStandoff
                   + 2*gv.frameHeight
                   + gv.frameSpacerLength)
    
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
        App.ActiveDocument.recompute()

            
        
    def draw(self):
        #helper Variables
        width = gv.frameWidth - 2*gv.feetOffset
        height = gv.feetBaseThickness + gv.mountToFrameHeadThickness +gv.feetBoltHeadClearanceVert
        counterSinkRadius = gv.printedToFrameHeadDia/2+gv.feetBoltHeadClearanceHor
        
        #Make file and build part
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

        #Create Document
        App.newDocument(self.name)
        App.setActiveDocument(self.name)
        App.ActiveDocument=App.getDocument(self.name)
        Gui.ActiveDocument=Gui.getDocument(self.name)
        
        #make body of foot
        #Sketch points
        x1 = -width/2
        y1 = x1
        x2 = x1
        y2 = -x1
        x3 = -x1
        y3 = -x1
        x4 = -x1
        y4 = x1
        
        App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
        App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
        Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
#        Gui.activeDocument().setEdit('Sketch')
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x1,y1,0),App.Vector(x2,y2,0)))
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x2,y2,0),App.Vector(x3,y3,0)))
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x3,y3,0),App.Vector(x4,y4,0)))
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x4,y4,0),App.Vector(x1,y1,0)))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1))        
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',1)) 
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',3)) 
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',0)) 
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',2)) 
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',1,2,0,1,-1,1)) 
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',3,2)) 
        App.ActiveDocument.recompute()
 
        #add dimmensions
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',1,width)) 
        App.ActiveDocument.recompute()
 
#         Gui.getDocument(self.name).resetEdit()
        App.getDocument(self.name).recompute()
         
        #Pad foot
        App.activeDocument().addObject("PartDesign::Pad","Pad")
        App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
        Gui.activeDocument().hide("Sketch")
#         Gui.activeDocument().setEdit('Pad',1)
        App.ActiveDocument.Pad.Length = height
        App.ActiveDocument.Pad.Reversed = 0
        App.ActiveDocument.Pad.Midplane = 0
        App.ActiveDocument.Pad.Length2 = 100.000000
        App.ActiveDocument.Pad.Type = 0
        App.ActiveDocument.Pad.UpToFace = None
        App.ActiveDocument.recompute()
        #Add draft to the foot
        App.activeDocument().addObject("PartDesign::Draft","Draft")
        Gui.activeDocument().hide("Pad")
        App.ActiveDocument.Draft.Angle = gv.feetDraftAngle
        App.ActiveDocument.Draft.Reversed = 0
        
        #get faces that will be drafted
        side1 = uf.getFace(App.ActiveDocument.Pad,
                          width/2, 0,
                          None, None,
                          None, None)
  
        side2 = uf.getFace(App.ActiveDocument.Pad,
                          -width/2,0,
                          None, None,
                          None, None)
        side3 = uf.getFace(App.ActiveDocument.Pad,
                          None,None,
                          width/2, 0,
                          None, None)
        side4 = uf.getFace(App.ActiveDocument.Pad,
                          None,None,
                          -width/2, 0,
                          None, None)

        App.ActiveDocument.Draft.Base = (App.ActiveDocument.Pad,[side1[1][0], side2[1][0], side3[1][0], side4[1][0]])
        App.ActiveDocument.Draft.NeutralPlane = uf.getFace(App.ActiveDocument.Pad,
                                                          None,None,
                                                          None, None,
                                                          0, 0)
        App.ActiveDocument.Draft.PullDirection = None
        App.ActiveDocument.recompute()
#         Gui.activeDocument().resetEdit()
        
        #Make through hole for mounting bolt
        App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
        App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Draft,
                                                          None,None,
                                                          None, None,
                                                          height, 0)

        App.activeDocument().recompute()
#         Gui.activeDocument().setEdit('Sketch001')
        App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(0,0,0),App.Vector(0,0,1),gv.printedToFrameDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
        App.ActiveDocument.recompute()
        #add dimmensions
        App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',0,gv.printedToFrameDia/2)) 
        App.ActiveDocument.recompute()
 
#         Gui.getDocument('feet').resetEdit()
        App.getDocument('feet').recompute()
        App.activeDocument().addObject("PartDesign::Pocket","Pocket")
        App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
        App.activeDocument().Pocket.Length = 10
        App.ActiveDocument.recompute()
        Gui.activeDocument().hide("Sketch001")
        Gui.activeDocument().hide("Draft")
#         Gui.activeDocument().setEdit('Pocket')
#         Gui.ActiveDocument.Pocket.ShapeColor=Gui.ActiveDocument.Draft.ShapeColor
#         Gui.ActiveDocument.Pocket.LineColor=Gui.ActiveDocument.Draft.LineColor
#         Gui.ActiveDocument.Pocket.PointColor=Gui.ActiveDocument.Draft.PointColor
        App.ActiveDocument.Pocket.Type = 1
        App.ActiveDocument.Pocket.UpToFace = None
        App.ActiveDocument.recompute()
#         Gui.activeDocument().resetEdit()
  
        #Add countersink hole for bolt head
        App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
        App.activeDocument().Sketch002.Support = (App.ActiveDocument.Pocket,["Face5"])
        App.activeDocument().recompute()
#         Gui.activeDocument().setEdit('Sketch002')
        App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(0.0,0.000000,0),App.Vector(0,0,1),counterSinkRadius))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',0,counterSinkRadius)) 
        App.ActiveDocument.recompute()
#         Gui.getDocument('feet').resetEdit()
        App.getDocument('feet').recompute()
        App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
        App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
        App.activeDocument().Pocket001.Length = height - gv.feetBaseThickness
        App.ActiveDocument.recompute()
        Gui.activeDocument().hide("Sketch002")
        Gui.activeDocument().hide("Pocket")
#         Gui.activeDocument().setEdit('Pocket001')
#         Gui.ActiveDocument.Pocket001.ShapeColor=Gui.ActiveDocument.Pocket.ShapeColor
#         Gui.ActiveDocument.Pocket001.LineColor=Gui.ActiveDocument.Pocket.LineColor
#         Gui.ActiveDocument.Pocket001.PointColor=Gui.ActiveDocument.Pocket.PointColor
        App.ActiveDocument.Pocket001.Type = 0
        App.ActiveDocument.Pocket001.UpToFace = None
        App.ActiveDocument.recompute()
#         Gui.activeDocument().resetEdit()
  
