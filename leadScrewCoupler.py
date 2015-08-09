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

class LeadScrewCoupler(object):
    def __init__(self):
        self.name = "leadScrewCoupler"

    def assemble(self):
        # Add first leadScrewCoupler
        App.ActiveDocument=App.getDocument(self.name)
        shape = App.ActiveDocument.ActiveObject.Shape
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        App.ActiveDocument.addObject('Part::Feature',self.name+"1").Shape= shape
        
        #Color Part

        # Get the feature and move it into position
        objs = App.ActiveDocument.getObjectsByLabel(self.name+"1")
        shape = objs[-1]        
        
        # Rotate into correct orientation
        rotateAngle = 90
        rotateCenter = App.Vector(0,0,0)
        rotateAxis = App.Vector(1,0,0)
        Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

        # Define shifts and move the left clamp into place
        xShift = -gv.zRodSpacing/2 + gv.zRodZScrewDist
        yShift = gv.extruderNozzleStandoff - gv.zRodStandoff+(gv.leadScrewCouplerBaseThicnkess
                        +(gv.leadScrewCouplerScrewClampDia if gv.leadScrewCouplerScrewClampDia > gv.leadScrewCouplerShaftClampDia else gv.leadScrewCouplerShaftClampDia)/2)
        zShift = (gv.leadScrewCouplerLength/2
                  - gv.yRodStandoff
                  +gv.zMotorMountPlateThickness
                  +gv.leadScrewCouplerGap)


        # Add second leadScrewCoupler
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
        App.ActiveDocument.recompute()
        App.ActiveDocument=App.getDocument(self.name)
        shape = App.ActiveDocument.ActiveObject.Shape
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        App.ActiveDocument.addObject('Part::Feature',self.name+"2").Shape= shape

        #Color Part

        # Get the feature and move it into position
        objs = App.ActiveDocument.getObjectsByLabel(self.name+"2")
        shape = objs[-1]

        # Rotate into correct orientation
        rotateAngle = 90
        rotateCenter = App.Vector(0,0,0)
        rotateAxis = App.Vector(1,0,0)
        Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

        rotateAngle = 180
        rotateCenter = App.Vector(0,0,0)
        rotateAxis = App.Vector(0,0,1)
        Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

        # Define shifts and move the left clamp into place
        xShift = -gv.zRodSpacing/2 + gv.zRodZScrewDist
        yShift = gv.extruderNozzleStandoff - gv.zRodStandoff -(gv.leadScrewCouplerBaseThicnkess
                                                               +(gv.leadScrewCouplerScrewClampDia if gv.leadScrewCouplerScrewClampDia > gv.leadScrewCouplerShaftClampDia else gv.leadScrewCouplerShaftClampDia)/2)
        zShift = (gv.leadScrewCouplerLength/2
                  - gv.yRodStandoff
                  +gv.zMotorMountPlateThickness
                  +gv.leadScrewCouplerGap)



        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
        App.ActiveDocument.recompute()


        # Add Third leadScrewCoupler
        App.ActiveDocument=App.getDocument(self.name)
        shape = App.ActiveDocument.ActiveObject.Shape
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        App.ActiveDocument.addObject('Part::Feature',self.name+"3").Shape= shape

        #Color Part

        # Get the feature and move it into position
        objs = App.ActiveDocument.getObjectsByLabel(self.name+"3")
        shape = objs[-1]

        # Rotate into correct orientation
        rotateAngle = 90
        rotateCenter = App.Vector(0,0,0)
        rotateAxis = App.Vector(1,0,0)
        Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

        rotateAngle = 180
        rotateCenter = App.Vector(0,0,0)
        rotateAxis = App.Vector(0,0,1)
        Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

        # Define shifts and move the left clamp into place
        xShift = -(-gv.zRodSpacing/2 + gv.zRodZScrewDist)
        yShift = gv.extruderNozzleStandoff - gv.zRodStandoff -(gv.leadScrewCouplerBaseThicnkess
                                                               +(gv.leadScrewCouplerScrewClampDia if gv.leadScrewCouplerScrewClampDia > gv.leadScrewCouplerShaftClampDia else gv.leadScrewCouplerShaftClampDia)/2)
        zShift = (gv.leadScrewCouplerLength/2
                  - gv.yRodStandoff
                  +gv.zMotorMountPlateThickness
                  +gv.leadScrewCouplerGap)

        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
        App.ActiveDocument.recompute()



        # Add 4th leadScrewCoupler
        App.ActiveDocument=App.getDocument(self.name)
        shape = App.ActiveDocument.ActiveObject.Shape
        App.ActiveDocument=App.getDocument("PrinterAssembly")
        App.ActiveDocument.addObject('Part::Feature',self.name+"4").Shape= shape

        #Color Part

        # Get the feature and move it into position
        objs = App.ActiveDocument.getObjectsByLabel(self.name+"4")
        shape = objs[-1]

        # Rotate into correct orientation
        rotateAngle = 90
        rotateCenter = App.Vector(0,0,0)
        rotateAxis = App.Vector(1,0,0)
        Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

        # Define shifts and move the left clamp into place
        xShift = -(-gv.zRodSpacing/2 + gv.zRodZScrewDist)
        yShift = gv.extruderNozzleStandoff - gv.zRodStandoff +(gv.leadScrewCouplerBaseThicnkess
                                                               +(gv.leadScrewCouplerScrewClampDia if gv.leadScrewCouplerScrewClampDia > gv.leadScrewCouplerShaftClampDia else gv.leadScrewCouplerShaftClampDia)/2)
        zShift = (gv.leadScrewCouplerLength/2
                  - gv.yRodStandoff
                  +gv.zMotorMountPlateThickness
                  +gv.leadScrewCouplerGap)



        App.ActiveDocument=App.getDocument("PrinterAssembly")
        Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
        App.ActiveDocument.recompute()

            
    def draw(self):
        #vars

        width = ((gv.leadScrewCouplerScrewClampDia if gv.leadScrewCouplerScrewClampDia > gv.leadScrewCouplerShaftClampDia else gv.leadScrewCouplerShaftClampDia)
                 + 2*gv.printedToPrintedNutFaceToFace/math.sin(math.pi/3)
                 + 2*gv.leadScrewCouplerNutTrapPadding)

        thickness = (gv.leadScrewCouplerBaseThicnkess
                        +(gv.leadScrewCouplerScrewClampDia if gv.leadScrewCouplerScrewClampDia > gv.leadScrewCouplerShaftClampDia else gv.leadScrewCouplerShaftClampDia)/2
                        -gv.leadScrewCouplerGap/2)
        cornerRadius = gv.printedToPrintedNutFaceToFace/(2*math.sin(math.pi/3))+gv.leadScrewCouplerNutTrapPadding
    
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

        #make base of coupler
        #sketch Points
        x1 = -width/2+cornerRadius
        y1 = -gv.leadScrewCouplerLength/2
        x2 = -width/2
        y2 = y1+cornerRadius
        x3 = x2
        y3 = -y2
        x4 = x1
        y4 = -y1
        x5 = -x1
        y5 = y4
        x6 = -x2
        y6 = y3
        x7 = x6
        y7 = y2
        x8 = x5
        y8 = y1
        x9 = x1
        y9 = y2
        x10 = x1
        y10 = y3
        x11 = x5
        y11 = y3
        x12 = x5
        y12 = y2

        App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
        App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
        Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x2,y2,0),App.Vector(x3,y3,0)))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',0))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x4,y4,0),App.Vector(x5,y5,0)))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x6,y6,0),App.Vector(x7,y7,0)))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x8,y8,0),App.Vector(x1,y1,0)))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',3))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x9,y9,0),App.Vector(0,0,1),cornerRadius),-math.pi,-math.pi/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,3,2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4,1,0,1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x10,y10,0),App.Vector(0,0,1),cornerRadius),math.pi/2,math.pi))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',5,1,1,1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,5,2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x11,y11,0),App.Vector(0,0,1),cornerRadius),0,math.pi/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',6,2,1,2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',6,1,2,1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(x12,y12,0),App.Vector(0,0,1),cornerRadius),-math.pi/2,0))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',7,2,2,2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',7,1,3,1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(x10,y10,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',8,3,5,3))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(x9,y9,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',9,3,4,3))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(x11,y11,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',10,3,6,3))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(x12,y12,0),App.Vector(0,0,1),gv.printedToPrintedDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',11,3,7,3))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(x3,y3,0),App.Vector(x6,y6,0)))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(-14.875409,-7.565940,0),App.Vector(14.827794,-7.586103,0)))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',13,1,0,1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',13,2,2,2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(-9.913898,12.500083,0),App.Vector(-9.913898,-12.500041,0)))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',14,1,1,1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',14,2,3,2))
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(9.913898,12.500000,0),App.Vector(9.913898,-12.500000,0)))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',15,1,1,2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',15,2,3,1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',12,1,0,2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',12,2,2,1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',5,6)) 
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',6,7))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',8,10))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',10,11))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',11,9))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',1,3))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal',0,2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.toggleConstruction(14)
        App.ActiveDocument.Sketch.toggleConstruction(12)
        App.ActiveDocument.Sketch.toggleConstruction(15)
        App.ActiveDocument.Sketch.toggleConstruction(13)
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',4,3,13)) 
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',4,3,14))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',5,3,14))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',5,3,12))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',6,3,12))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',6,3,15))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',7,3,15))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',5,3,7,3,-1,1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',10,gv.printedToPrintedDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',15,-gv.leadScrewCouplerLength))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',13,width))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',7,cornerRadius))
        App.ActiveDocument.recompute()

        #Pad coupler body
        App.activeDocument().addObject("PartDesign::Pad","Pad")
        App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
        App.ActiveDocument.recompute()
        Gui.activeDocument().hide("Sketch")
        App.ActiveDocument.Pad.Length = thickness
        App.ActiveDocument.Pad.Reversed = 0
        App.ActiveDocument.Pad.Midplane = 0
        App.ActiveDocument.Pad.Type = 0
        App.ActiveDocument.Pad.UpToFace = None
        App.ActiveDocument.recompute()

        #Cut space for motorShaft
        #sketch points
        x1 = 0
        y1 = gv.leadScrewCouplerBaseThicnkess+(gv.leadScrewCouplerScrewClampDia if gv.leadScrewCouplerScrewClampDia > gv.leadScrewCouplerShaftClampDia else gv.leadScrewCouplerShaftClampDia)/2

        #make Sketch
        App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
        App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
                                                            0,0,
                                                            -gv.leadScrewCouplerLength/2,0,
                                                            None, None)
        App.activeDocument().recompute()
        App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(x1,y1,0),App.Vector(0,0,1),gv.leadScrewCouplerShaftClampDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',0,gv.leadScrewCouplerShaftClampDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',-1,1,0,3,y1))
        App.ActiveDocument.recompute()


        #Cut Pocket
        App.activeDocument().addObject("PartDesign::Pocket","Pocket")
        App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
        Gui.activeDocument().hide("Sketch001")
        Gui.activeDocument().hide("Pad")
        App.ActiveDocument.Pocket.Length = gv.leadScrewCouplerLength/2
        App.ActiveDocument.Pocket.Type = 0
        App.ActiveDocument.Pocket.UpToFace = None
        App.ActiveDocument.recompute()
        Gui.activeDocument().resetEdit()
        
        #Cut space for lead screw
        #Sketch Points
        x1 = 0
        y1 = gv.leadScrewCouplerBaseThicnkess+(gv.leadScrewCouplerScrewClampDia if gv.leadScrewCouplerScrewClampDia > gv.leadScrewCouplerShaftClampDia else gv.leadScrewCouplerShaftClampDia)/2

        #Make Sketch
        App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
        App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
                                                            0,0,
                                                            0,0,
                                                            0, 1)
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket,
                                                                     None, None,
                                                                     0, 0,
                                                                     None, None,
                                                                     radius=gv.leadScrewCouplerShaftClampDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(x1,y1,0),App.Vector(0,0,1),gv.leadScrewCouplerScrewClampDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,3,-3,3))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',0,gv.leadScrewCouplerScrewClampDia/2))
        App.ActiveDocument.recompute()


        #Cut Pocket
        App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
        App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
        App.ActiveDocument.recompute()
        Gui.activeDocument().hide("Sketch002")
        Gui.activeDocument().hide("Pocket")
        App.ActiveDocument.Pocket001.Length = 5.000000
        App.ActiveDocument.Pocket001.Type = 1
        App.ActiveDocument.Pocket001.UpToFace = None
        App.ActiveDocument.recompute()
        Gui.activeDocument().resetEdit()

        #Make nut traps in bottom of clamp
        #Sketch points
        x1 = -width/2+cornerRadius
        y1 = -gv.leadScrewCouplerLength/2+cornerRadius
        x2 = x1
        y2 = -y1
        x3 = -x1
        y3 = y2
        x4 = x3
        y4 = y1

        App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
        App.activeDocument().Sketch003.Support = uf.getFace(App.ActiveDocument.Pocket001,
                                                            None,None,
                                                            None,None,
                                                            0,0)
        App.activeDocument().recompute()
        App.ActiveDocument.Sketch003.addExternal("Pocket001",uf.getEdge(App.ActiveDocument.Pocket,
                                                                     0, -1,
                                                                     0, 1,
                                                                     0, 0,
                                                                     radius=gv.printedToPrintedDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch003.addExternal("Pocket001",uf.getEdge(App.ActiveDocument.Pocket,
                                                                     0, -1,
                                                                     0, -1,
                                                                     0, 0,
                                                                     radius=gv.printedToPrintedDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch003.addExternal("Pocket001",uf.getEdge(App.ActiveDocument.Pocket,
                                                                     0, 1,
                                                                     0, -1,
                                                                     0, 0,
                                                                     radius=gv.printedToPrintedDia/2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch003.addExternal("Pocket001",uf.getEdge(App.ActiveDocument.Pocket,
                                                                     0, 1,
                                                                     0, 1,
                                                                     0, 0,
                                                                     radius=gv.printedToPrintedDia/2))
        App.ActiveDocument.recompute()
        uf.drawHexagon(x1,y1,gv.printedToPrintedNutFaceToFace,0)
        App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',6,3,-3,3)) 
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Vertical',5))
        App.ActiveDocument.recompute()
        uf.drawHexagon(x2,y2,gv.printedToPrintedNutFaceToFace,0)
        uf.drawHexagon(x3,y3,gv.printedToPrintedNutFaceToFace,0)
        uf.drawHexagon(x4,y4,gv.printedToPrintedNutFaceToFace,0)
        App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Vertical',12))
        App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Vertical',19))
        App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Vertical',26))
        App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',13,3,-4,3)) 
        App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',20,3,-5,3))
        App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',27,3,-6,3))

        #Cut Pocket
        App.activeDocument().addObject("PartDesign::Pocket","Pocket002")
        App.activeDocument().Pocket002.Sketch = App.activeDocument().Sketch003
        App.activeDocument().Pocket002.Length = gv.mountToPrintedNutThickness
        App.ActiveDocument.recompute()
        Gui.activeDocument().hide("Sketch003")
        Gui.activeDocument().hide("Pocket001")
        App.ActiveDocument.Pocket002.Type = 0
        App.ActiveDocument.Pocket002.UpToFace = None
        App.ActiveDocument.recompute()

