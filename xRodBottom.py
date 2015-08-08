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

from __future__ import division  # allows floating point division from integers

# import FreeCAD modules
import FreeCAD as App
import Part
import Sketcher
import Draft

# Specific to printer
import globalVars as gv


class XRodBottom(object):
    def __init__(self):
        pass

    def assemble(self):
        App.ActiveDocument = App.getDocument("xRodBottom")
        xRodBottom = App.ActiveDocument.Pad.Shape
        App.ActiveDocument = App.getDocument("PrinterAssembly")
        App.ActiveDocument.addObject('Part::Feature', 'xRodBottom').Shape = xRodBottom

        # Define shifts and move into place
        xshift = -gv.xRodLength / 2
        yshift = (gv.extruderNozzleStandoff
                  - gv.zRodStandoff
                  - gv.xEndZRodHolderFaceThickness
                  - gv.xEndZRodHolderMaxNutFaceToFace / 2
                  - gv.xMotorMountPlateThickness
                  - gv.xRodClampThickness
                  - gv.xRodDiaMax / 2)
        zshift = 0

        App.ActiveDocument = App.getDocument("PrinterAssembly")
        Draft.move([App.ActiveDocument.getObject("xRodBottom")], App.Vector(xshift, yshift, zshift), copy=False)
        App.ActiveDocument.recompute()


        # Add to xAxisParts
        xrb = App.ActiveDocument.getObject("xRodBottom")
        if xrb not in gv.xAxisParts:
            gv.xAxisParts.append(xrb)

    def draw(self):
        try:
            App.getDocument('xRodBottom').recompute()
            App.closeDocument("xRodBottom")
            App.setActiveDocument("")
            App.ActiveDocument = None
        except:
            pass

        # make document
        App.newDocument("xRodBottom")
        App.setActiveDocument("xRodBottom")
        App.ActiveDocument = App.getDocument("xRodBottom")

        # make sketch
        App.activeDocument().addObject('Sketcher::SketchObject', 'Sketch')
        App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000, 0.000000, 0.000000),
                                                              App.Rotation(0.500000, 0.500000, 0.500000, 0.500000))
        App.ActiveDocument.Sketch.addGeometry(
            Part.Circle(App.Vector(50, 50, 0), App.Vector(0, 0, 1), gv.xRodDiaBottom / 2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius', 0, gv.xRodDiaBottom / 2))
        App.ActiveDocument.recompute()
        App.getDocument('xRodBottom').recompute()

        # Pad sketch
        App.activeDocument().addObject("PartDesign::Pad", "Pad")
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


        # set view as axiometric

