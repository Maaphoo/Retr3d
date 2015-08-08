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
import FreeCAD# as #
import Part
import Sketcher
import Draft

#Specific to printer
import globalVars as gv

class XRodTop(object):
	def __init__(self):
		pass

	def assemble(self):
		App.ActiveDocument=App.getDocument("xRodTop")
		xRodTop = App.ActiveDocument.Pad.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature','xRodTop').Shape=xRodTop
		
		#Define shifts and move into place
		xShift = -gv.xRodLength/2
		yShift =  (gv.extruderNozzleStandoff 
 				- gv.zRodStandoff
 				- gv.xEndZRodHolderFaceThickness
 				- gv.xEndZRodHolderMaxNutFaceToFace/2
				- gv.xMotorMountPlateThickness
 				- gv.xRodClampThickness
 				- gv.xRodDiaMax/2
				)
		zShift = gv.xRodSpacing
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([App.ActiveDocument.xRodTop],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()		
		
		xrt = App.ActiveDocument.xRodTop
		if xrt not in gv.xAxisParts:
			gv.xAxisParts.append(xrt)
			
	def draw(self):
		try:
			App.getDocument('xRodTop').recompute()
			App.closeDocument("xRodTop")
			App.setActiveDocument("")
			App.ActiveDocument=None
		except:
			pass

		#make document
		App.newDocument("xRodTop")
		App.setActiveDocument("xRodTop")
		App.ActiveDocument=App.getDocument("xRodTop")

		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.500000,0.500000,0.500000,0.500000))
		App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(50,50,0),App.Vector(0,0,1),gv.xRodDiaTop/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',0,gv.xRodDiaTop/2)) 
		App.ActiveDocument.recompute()
		App.getDocument('xRodTop').recompute()

		#Pad sketch
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		App.ActiveDocument.Pad.Length = gv.xRodLength
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()

		#set view as axiometric


