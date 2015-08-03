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
        # #.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA\n  position 87 0 0 \n  orientation 0.57735026 0.57735026 0.57735026  2.0943952 \n  nearDistance -112.887\n  farDistance 287.28699\n  aspectRatio 1\n  focalDistance 87\n  height 143.52005\n\n}')
        # #.activeDocument().setEdit('Sketch')
        App.ActiveDocument.Sketch.addGeometry(
            Part.Circle(App.Vector(50, 50, 0), App.Vector(0, 0, 1), gv.xRodDiaBottom / 2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius', 0, gv.xRodDiaBottom / 2))
        App.ActiveDocument.recompute()
        # #.getDocument('xRodBottom').resetEdit()
        App.getDocument('xRodBottom').recompute()

        # Pad sketch
        App.activeDocument().addObject("PartDesign::Pad", "Pad")
        App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
        App.activeDocument().Pad.Length = 10.0
        App.ActiveDocument.recompute()
        ##.activeDocument().hide("Sketch")
        App.ActiveDocument.Pad.Length = gv.xRodLength
        App.ActiveDocument.Pad.Reversed = 0
        App.ActiveDocument.Pad.Midplane = 0
        App.ActiveDocument.Pad.Length2 = 100.000000
        App.ActiveDocument.Pad.Type = 0
        App.ActiveDocument.Pad.UpToFace = None
        App.ActiveDocument.recompute()

        # #.activeDocument().resetEdit()

        # set view as axiometric

# #.activeDocument().activeView().viewAxometric()
