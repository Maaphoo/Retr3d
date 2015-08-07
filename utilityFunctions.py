# import Math related
from __future__ import division  # allows floating point division from integersimport math
import math
from itertools import product

# import system and file handling stuff
import os
import datetime
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import platform
import __main__

# Specific to printer
import globalVars as gv

if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/logs/'):
    os.makedirs(os.path.dirname(os.path.abspath(__file__)) + '/logs/')

q = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
LOG_FILENAME = os.path.join(q, "retr3d.log")
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w')

logging.info('Retr3d Log File')
logging.info('Version 0.1.0')


def setStatus():
    App.Console.SetStatus("Console", "Msg", 1)
    App.Console.SetStatus("Console", "Wrn", 1)
    App.Console.SetStatus("Console", "Err", 1)
    App.Console.SetStatus("Console", "Log", 0)


def log(msg, level, source):
    eval('logging.getLogger(source).' + level + '(msg)')


def bold(msg, log):
    if log:
        logging.info(msg)
    if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print '\033[1m' + msg + '\x1b[0m'
    elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        attr = []
        attr.append('1')
        print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
    else:
        if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print msg
        else:
            setStatus()
            App.Console.PrintMessage(msg + '\n')


def underline(msg, log):
    if log:
        logging.info(msg)
    if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print '\033[4m' + msg + '\x1b[0m'
    else:
        if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print msg
        else:
            setStatus()
            App.Console.PrintMessage(msg + '\n')


def header(msg, log):
    if log:
        logging.info(msg)
    if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print '\033[95m' + msg + '\x1b[0m'
    elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        attr = []
        attr.append('35')
        attr.append('1')
        print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
    else:
        if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print msg
        else:
            setStatus()
            App.Console.PrintMessage(msg + '\n')


def critical(msg, log, level, source):
    logging.getLogger(source).critical(log)
    if level <= 5:
        if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print '\033[1m\033[31m' + msg + '\x1b[0m'
        elif platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            attr = []
            attr.append('1')
            attr.append('31')
            print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
        else:
            if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                print msg
            else:
                setStatus()
                App.Console.PrintError(msg + '\n')
                try:
                    from PySide import QtGui
                    QtGui.QMessageBox.critical(None, "Retr3d: Error", msg)
                except:
                    pass


def error(msg, log, level, source):
    logging.getLogger(source).error(log)
    if level <= 4:
        if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print '\033[91m' + msg + '\x1b[0m'
        elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            attr = []
            attr.append('31')
            print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
        else:
            if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                print msg
            else:
                setStatus()
                App.Console.PrintError(msg + '\n')


def warning(msg, log, level, source):
    logging.getLogger(source).warning(log)
    if level <= 3:
        if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print '\033[93m' + msg + '\x1b[0m'
        elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            attr = []
            attr.append('33')
            print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
        else:
            if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                print msg
            else:
                setStatus()
                App.Console.PrintWarning(msg + '\n')


def info(msg, log, level, source):
    logging.getLogger(source).info(log)
    if level <= 2:
        if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print '\033[92m' + msg + '\x1b[0m'
        elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            attr = []
            attr.append('32')
            print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
        else:
            if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                print msg
            else:
                setStatus()
                App.Console.PrintMessage(msg + '\n')


def debug(msg, log, level, source):
    logging.getLogger(source).debug(log)
    if level <= 1:
        if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print '\033[94m' + msg + '\x1b[0m'
        elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            attr = []
            attr.append('34')
            print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
        else:
            if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                print msg
            else:
                setStatus()
                App.Console.PrintLog(msg + '\n')


# FreeCAD related
try:
    import FreeCAD as App
except ImportError:
    critical("Failure to import FreeCAD, check your configuration file.", "", gv.level, os.path.basename(__file__))
    raise StandardError

import FreeCAD# as #
import Draft
import Part
import Sketcher


def getFace(feature, x, compX, y, compY, z, compZ):
    possibleFaces = []
    for i in range(len(feature.Shape.Faces)):
        possibleFaces.append([feature.Shape.Faces[i], i])

    # check to see if x condition is met by any of the faces
    i = 0
    if x is not None and compX == 0:
        while i < len(possibleFaces):
            if abs(possibleFaces[i][0].CenterOfMass.x - x) > 0.00001:
                possibleFaces.pop(i)
            else:
                i = i + 1
    if x is not None and compX == -1:
        while i < len(possibleFaces):
            if possibleFaces[i][0].CenterOfMass.x - .00001 >= x:
                possibleFaces.pop(i)
            else:
                i = i + 1
    if x is not None and compX == 1:
        while i < len(possibleFaces):
            if possibleFaces[i][0].CenterOfMass.x + .00001 <= x:
                possibleFaces.pop(i)
            else:
                i = i + 1
    i = 0
    if y is not None and compY == 0:
        while i < len(possibleFaces):
            if abs(possibleFaces[i][0].CenterOfMass.y - y) > 0.00001:
                possibleFaces.pop(i)
            else:
                i = i + 1
    if y is not None and compY == -1:
        while i < len(possibleFaces):
            if possibleFaces[i][0].CenterOfMass.y - .00001 >= y:
                possibleFaces.pop(i)
            else:
                i = i + 1
    if y is not None and compY == 1:
        while i < len(possibleFaces):
            if possibleFaces[i][0].CenterOfMass.y + .00001 <= y:
                possibleFaces.pop(i)
            else:
                i = i + 1
    i = 0
    if z is not None and compZ == 0:
        while i < len(possibleFaces):
            if abs(possibleFaces[i][0].CenterOfMass.z - z) > 0.00001:
                possibleFaces.pop(i)
            else:
                i = i + 1
    if z is not None and compZ == -1:
        while i < len(possibleFaces):
            if possibleFaces[i][0].CenterOfMass.z - .00001 >= z:
                possibleFaces.pop(i)
            else:
                i = i + 1
    if z is not None and compZ == 1:
        while i < len(possibleFaces):
            if possibleFaces[i][0].CenterOfMass.z + .00001 <= z:
                possibleFaces.pop(i)
            else:
                i = i + 1

    if len(possibleFaces) == 1:
        string = "Face" + str(possibleFaces[0][1] + 1)
        return (feature, [string])
    elif len(possibleFaces) > 1:
        raise Exception("getFace() error: Unable to determine a unique face.")
    else:
        raise Exception("getFace() error: No such face exists.")


def getEdge(feature,
            x, compX,
            y, compY,
            z, compZ,
            radius=None,
            face=None,
            center=None,
            makeUnique=None):
    possibleEdges = []
    for i in range(len(feature.Shape.Edges)):
        possibleEdges.append([feature.Shape.Edges[i], i])

    # If a face is defined, automatically remove all edges not on that face
    # Can't just use the Face's edges directly because there is no way to get their index in the feature
    # The following isn't the most efficient way to find the overlap.
    if face is not None:
        possibleEdgesTemp = []

        for i in range(len(possibleEdges)):
            for j in range(len(face.Edges)):
                if possibleEdges[i][0].CenterOfMass == face.Edges[j].CenterOfMass:
                    possibleEdgesTemp.append(possibleEdges[i])

        possibleEdges = possibleEdgesTemp

    # check to see if x condition is met by any of the faces
    i = 0
    if x is not None and compX == 0:
        while i < len(possibleEdges):
            if abs(possibleEdges[i][0].CenterOfMass.x - x) > 0.00001:
                possibleEdges.pop(i)
            else:
                i = i + 1
    if x is not None and compX == -1:
        while i < len(possibleEdges):
            if possibleEdges[i][0].CenterOfMass.x + .00001 >= x:
                possibleEdges.pop(i)
            else:
                i = i + 1
    if x is not None and compX == 1:
        while i < len(possibleEdges):
            if possibleEdges[i][0].CenterOfMass.x - .00001 <= x:
                possibleEdges.pop(i)
            else:
                i = i + 1
    i = 0

    if y is not None and compY == 0:
        while i < len(possibleEdges):
            if abs(possibleEdges[i][0].CenterOfMass.y - y) > 0.00001:
                possibleEdges.pop(i)
            else:
                i = i + 1
    if y is not None and compY == -1:
        while i < len(possibleEdges):
            if possibleEdges[i][0].CenterOfMass.y + .00001 >= y:
                possibleEdges.pop(i)
            else:
                i = i + 1
    if y is not None and compY == 1:
        while i < len(possibleEdges):
            if possibleEdges[i][0].CenterOfMass.y - .00001 <= y:
                possibleEdges.pop(i)
            else:
                i = i + 1

    i = 0
    if z is not None and compZ == 0:
        while i < len(possibleEdges):
            if abs(possibleEdges[i][0].CenterOfMass.z - z) > 0.00001:
                possibleEdges.pop(i)
            else:
                i = i + 1
    if z is not None and compZ == -1:
        while i < len(possibleEdges):
            if possibleEdges[i][0].CenterOfMass.z + .00001 >= z:
                possibleEdges.pop(i)
            else:
                i = i + 1
    if z is not None and compZ == 1:
        while i < len(possibleEdges):
            if possibleEdges[i][0].CenterOfMass.z - .00001 <= z:
                possibleEdges.pop(i)
            else:
                i = i + 1

    if radius is not None:
        i = 0
        while i < len(possibleEdges):
            if not hasattr(possibleEdges[i][0].Curve, 'Radius') or abs(
                            possibleEdges[i][0].Curve.Radius - radius) > 0.0001:
                possibleEdges.pop(i)
            else:
                i = i + 1

    if center is not None:
        if center[0] is not None:
            while i < len(possibleEdges):
                if not hasattr(possibleEdges[i][0].Curve, 'Center') or abs(
                                possibleEdges[i][0].Curve.Center[0] - center[0]) > 0.0001:
                    possibleEdges.pop(i)
                else:
                    i = i + 1
        if center[1] is not None:
            while i < len(possibleEdges):
                if not hasattr(possibleEdges[i][0].Curve, 'Center') or abs(
                                possibleEdges[i][0].Curve.Center[1] - center[1]) > 0.0001:
                    possibleEdges.pop(i)
                else:
                    i = i + 1
        if center[0] is not None:
            while i < len(possibleEdges):
                if not hasattr(possibleEdges[i][0].Curve, 'Center') or abs(
                                possibleEdges[i][0].Curve.Center[2] - center[2]) > 0.0001:
                    possibleEdges.pop(i)
                else:
                    i = i + 1
    if makeUnique is not None:
        possibleEdges = possibleEdges[:1]

    # return possibleEdges
    if len(possibleEdges) == 1:
        string = "Edge" + str(possibleEdges[0][1] + 1)
        return (string)
    elif len(possibleEdges) > 1:
        raise Exception("getEdge() error: Unable to determine a unique edge." + str(possibleEdges))
    else:
        raise Exception("getEdge() error: No such edge.")


def positionXAxis():
    App.ActiveDocument = App.getDocument("PrinterAssembly")
    xShift = 0
    yShift = 0
    zShift = (gv.vertBarDistBelowZRod
              + gv.zRodSupportLength
              + gv.zEndStopClampLength
              + gv.xRodClampThickness
              + gv.xRodDiaMax
              - 22)

    Draft.move(gv.xAxisParts, App.Vector(xShift, yShift, zShift), copy=False)
    App.ActiveDocument.recompute()


def positionZAxis():
    App.ActiveDocument = App.getDocument("PrinterAssembly")
    xShift = 0
    yShift = 0
    zShift = gv.vertBarDistBelowZRod - gv.yRodStandoff

    Draft.move(gv.zAxisParts, App.Vector(xShift, yShift, zShift), copy=False)
    App.ActiveDocument.recompute()


def saveAssembly():
    # Make dateString and add it to the directory string
    date = datetime.date.today().strftime("%m_%d_%Y")

    # make the printer's directory if it doesn't exist
    printerDir = gv.printerDir + "Printer_" + date + "/"
    if not os.path.exists(printerDir):
        os.makedirs(printerDir)

    # Save the FCStd file
    if os.path.isfile(printerDir + "PrinterAssembly.FCStd"):
        os.remove(printerDir + "PrinterAssembly.FCStd")
    App.getDocument("PrinterAssembly").saveAs(printerDir + "PrinterAssembly.FCStd")


def saveAndClose(name, saveSTL):
    # Make dateString and add it to the directory string
    date = datetime.date.today().strftime("%m_%d_%Y")

    # make the printer's directory if it doesn't exist
    printerDir = gv.printerDir + "Printer_" + date + "/"
    if not os.path.exists(printerDir):
        try:
            os.makedirs(printerDir)
        except OSError as e:
            import traceback
            critical("Failure to save files, check your configuration file.",
                     'Error making "printerDir" in saveAndClose: ' + str(e) + '\n' + traceback.format_exc(limit=1),
                     gv.level, os.path.basename(__file__))
            raise StandardError

    # make the Parts directory if it doesn't exist
    partsDir = printerDir + "Parts/"
    if not os.path.exists(partsDir):
        os.makedirs(partsDir)

    # Save the FCStd file
    if os.path.isfile(partsDir + name + ".FCStd"):
        os.remove(partsDir + name + ".FCStd")
    App.getDocument(name).saveAs(partsDir + name + ".FCStd")

    if saveSTL:
        # make the STLs directory if it doesn't exist
        stlDir = printerDir + "STL_Files/"
        if not os.path.exists(stlDir):
            os.makedirs(stlDir)

        # Export an STL
        if os.path.isfile(stlDir + name + ".stl"):
            os.remove(stlDir + name + ".stl")
        __objs__ = []
        __objs__.append(App.getDocument(name).Objects[-1])
        import Mesh
        Mesh.export(__objs__, stlDir + name + ".stl")
        del __objs__

    # close document
    App.closeDocument(name)


def makeAssemblyFile():
    try:
        App.getDocument('PrinterAssembly').recompute()
        App.closeDocument("PrinterAssembly")
        App.setActiveDocument("")
        App.ActiveDocument = None
    except:
        pass

    # make document
    # Make Assembly file
    App.newDocument("PrinterAssembly")
    App.setActiveDocument("PrinterAssembly")
    App.ActiveDocument = App.getDocument("PrinterAssembly")


def assemble(part):
    # Copy part from its document to the PrinterAssembly
    App.ActiveDocument = App.getDocument(part.name)
    xRodTop = App.ActiveDocument.Pad.Shape
    App.ActiveDocument = App.getDocument("PrinterAssembly")
    App.ActiveDocument.addObject('Part::Feature', part.name).Shape = xRodTop

    # Get handle on part in the assembly
    App.ActiveDocument = App.getDocument("PrinterAssembly")
    listOfParts = App.ActiveDocument.getObjectsByLabel(part.name)
    assemblyPart = listOfParts[-1]

    # Rotate and move part into position
    App.ActiveDocument = App.getDocument("PrinterAssembly")
    if part.rotateAngle:
        Draft.rotate([assemblyPart], part.rotateAngle, part.rotateCenter, part.rotateAxis, copy=False)
    Draft.move([assemblyPart], App.Vector(part.xShift, part.yShift, part.zShift), copy=False)
    App.ActiveDocument.recompute()


def adjustHole(desiredDia):
    # if desiredDia is smaller than the first data point. just retrun the smallest printable diameter.
    if desiredDia <= gv.holeAdjust[0][1]:
        return gv.holeAdjust[0][0];

    # find the interval the desiredDia is in and adjust using linear interpolation
    for i in range(len(gv.holeAdjust) - 1):
        if desiredDia == gv.holeAdjust[i][1]:
            return gv.holeAdjust[i][0]

        if desiredDia > gv.holeAdjust[i][1] and desiredDia < gv.holeAdjust[i + 1][1]:
            x1 = (gv.holeAdjust[i][0])
            y1 = (gv.holeAdjust[i][1])
            x2 = (gv.holeAdjust[i + 1][0])
            y2 = (gv.holeAdjust[i + 1][1])
            return ((desiredDia - y1) * (x2 - x1) / (y2 - y1) + x1)
    # not in largest interval so just return the desiredDia
    return desiredDia


def multiply(matr_a, matr_b):
    cols = len(matr_b[0])
    rows = len(matr_b)
    resRows = xrange(len(matr_a))
    rMatrix = [[0] * cols for _ in resRows]
    for idx in resRows:
        for j, k in product(xrange(cols), xrange(rows)):
            rMatrix[idx][j] += matr_a[idx][k] * matr_b[k][j]
    return rMatrix


# hexagonPoints is depreciated. Use drawHexagon instead.
def hexagonPoints(x, y, faceToFace, theta):
    # make an array of points
    matrix = [[-faceToFace / 2, faceToFace * math.tan(math.pi / 6) / 2],
              [0, faceToFace / math.cos(math.pi / 6) / 2],
              [faceToFace / 2, faceToFace * math.tan(math.pi / 6) / 2],
              [faceToFace / 2, -faceToFace * math.tan(math.pi / 6) / 2],
              [0, -faceToFace / math.cos(math.pi / 6) / 2],
              [-faceToFace / 2, -faceToFace * math.tan(math.pi / 6) / 2],
              [0, 0]]

    rotation = [[math.cos(theta), -math.sin(theta)],
                [math.sin(theta), math.cos(theta)]]
    rotated = multiply(matrix, rotation)
    translated = [[rotated[0][0] + x, rotated[0][1] + y],
                  [rotated[1][0] + x, rotated[1][1] + y],
                  [rotated[2][0] + x, rotated[2][1] + y],
                  [rotated[3][0] + x, rotated[3][1] + y],
                  [rotated[4][0] + x, rotated[4][1] + y],
                  [rotated[5][0] + x, rotated[5][1] + y],
                  [x, y],
                  [faceToFace / math.cos(math.pi / 6) / 2, 0]]
    return translated


def drawHexagon(x, y, faceToFace, theta):
    # Theta is in radians
    # make an array of points
    matrix = [[-faceToFace / 2, faceToFace * math.tan(math.pi / 6) / 2],
              [0, faceToFace / math.cos(math.pi / 6) / 2],
              [faceToFace / 2, faceToFace * math.tan(math.pi / 6) / 2],
              [faceToFace / 2, -faceToFace * math.tan(math.pi / 6) / 2],
              [0, -faceToFace / math.cos(math.pi / 6) / 2],
              [-faceToFace / 2, -faceToFace * math.tan(math.pi / 6) / 2],
              [0, 0]]

    rotation = [[math.cos(theta), -math.sin(theta)],
                [math.sin(theta), math.cos(theta)]]
    rotated = multiply(matrix, rotation)
    translated = [[rotated[0][0] + x, rotated[0][1] + y],
                  [rotated[1][0] + x, rotated[1][1] + y],
                  [rotated[2][0] + x, rotated[2][1] + y],
                  [rotated[3][0] + x, rotated[3][1] + y],
                  [rotated[4][0] + x, rotated[4][1] + y],
                  [rotated[5][0] + x, rotated[5][1] + y],
                  [x, y],
                  [faceToFace / math.cos(math.pi / 6) / 2, 0]]
    count = App.ActiveDocument.ActiveObject.GeometryCount
    App.ActiveDocument.ActiveObject
    App.ActiveDocument.ActiveObject.addGeometry(
        Part.Line(App.Vector(translated[0][0], translated[0][1], 0), App.Vector(translated[1][0], translated[1][1], 0)))
    App.ActiveDocument.recompute()
    App.ActiveDocument.ActiveObject.addGeometry(
        Part.Line(App.Vector(translated[1][0], translated[1][1], 0), App.Vector(translated[2][0], translated[2][1], 0)))
    App.ActiveDocument.ActiveObject.addConstraint(Sketcher.Constraint('Coincident', count + 0, 2, count + 1, 1))
    App.ActiveDocument.recompute()
    App.ActiveDocument.ActiveObject.addGeometry(
        Part.Line(App.Vector(translated[2][0], translated[2][1], 0), App.Vector(translated[3][0], translated[3][1], 0)))
    App.ActiveDocument.ActiveObject.addConstraint(Sketcher.Constraint('Coincident', count + 1, 2, count + 2, 1))
    App.ActiveDocument.recompute()
    App.ActiveDocument.ActiveObject.addGeometry(
        Part.Line(App.Vector(translated[3][0], translated[3][1], 0), App.Vector(translated[4][0], translated[4][1], 0)))
    App.ActiveDocument.ActiveObject.addConstraint(Sketcher.Constraint('Coincident', count + 2, 2, count + 3, 1))
    App.ActiveDocument.recompute()
    App.ActiveDocument.ActiveObject.addGeometry(
        Part.Line(App.Vector(translated[4][0], translated[4][1], 0), App.Vector(translated[5][0], translated[5][1], 0)))
    App.ActiveDocument.ActiveObject.addConstraint(Sketcher.Constraint('Coincident', count + 3, 2, count + 4, 1))
    App.ActiveDocument.recompute()
    App.ActiveDocument.ActiveObject.addGeometry(
        Part.Line(App.Vector(translated[5][0], translated[5][1], 0), App.Vector(translated[0][0], translated[0][1], 0)))
    App.ActiveDocument.ActiveObject.addConstraint(Sketcher.Constraint('Coincident', count + 4, 2, count + 5, 1))
    App.ActiveDocument.ActiveObject.addConstraint(Sketcher.Constraint('Coincident', count + 5, 2, count + 0, 1))
    App.ActiveDocument.recompute()
    App.ActiveDocument.ActiveObject.addGeometry(
        Part.Circle(App.Vector(x, y, 0), App.Vector(0, 0, 1), faceToFace / math.cos(math.pi / 6) / 2))
    App.ActiveDocument.recompute()
    App.ActiveDocument.ActiveObject.toggleConstruction(count + 6)
    for i in range(5):
        App.ActiveDocument.ActiveObject.addConstraint(Sketcher.Constraint('Equal', count + i, count + i + 1))
    for i in range(6):
        App.ActiveDocument.ActiveObject.addConstraint(Sketcher.Constraint('PointOnObject', count + i, 1, count + 6))
    App.ActiveDocument.ActiveObject.addConstraint(Sketcher.Constraint('Distance', count + 2, 2, count + 5, faceToFace))


# function to extrude frame member length
def extrudeFrameMember(name, length):
    App.ActiveDocument = App.getDocument(name)
    App.activeDocument().addObject('Sketcher::SketchObject', 'Sketch')
    App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000, 0.000000, 0.000000),
                                                          App.Rotation(0.500000, 0.500000, 0.500000, 0.500000))

    # Sketch Points

    p1x = -gv.frameWidth / 2
    p1y = -gv.frameHeight / 2
    p2x = p1x
    p2y = -p1y
    p3x = -p1x
    p3y = -p1y
    p4x = -p1x
    p4y = p1y

    App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x, p1y, 0), App.Vector(p4x, p4y, 0)))
    App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p4x, p4y, 0), App.Vector(p3x, p3y, 0)))
    App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x, p3y, 0), App.Vector(p2x, p2y, 0)))
    App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x, p2y, 0), App.Vector(p1x, p1y, 0)))
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 2, 2, 3, 1))
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 3, 2, 0, 1))
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal', 0))
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal', 2))
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical', 1))
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical', 3))
    App.ActiveDocument.recompute()

    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric', 1, 2, 2, 2, -2))
    App.ActiveDocument.recompute()
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric', 0, 2, 1, 2, -1))
    App.ActiveDocument.recompute()

    # Add Dimensions
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY', 1, gv.frameHeight))
    App.ActiveDocument.recompute()
    App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX', 2, -gv.frameWidth))
    App.ActiveDocument.recompute()

    if gv.frameThickness:
        p1x = -(gv.frameWidth - gv.frameThickness) / 2
        p1y = -(gv.frameHeight - gv.frameThickness) / 2
        p2x = p1x
        p2y = -p1y
        p3x = -p1x
        p3y = -p1y
        p4x = -p1x
        p4y = p1y
        p5x = p3x
        p5y = p3y + gv.frameThickness
        p6x = p3x + gv.frameThickness
        p6y = p3y

        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x, p1y, 0), App.Vector(p4x, p4y, 0)))
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p4x, p4y, 0), App.Vector(p3x, p3y, 0)))
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x, p3y, 0), App.Vector(p2x, p2y, 0)))
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x, p2y, 0), App.Vector(p1x, p1y, 0)))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 4, 2, 5, 1))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 5, 2, 6, 1))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 6, 2, 7, 1))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 7, 2, 4, 1))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal', 4))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal', 6))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical', 5))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical', 7))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric', 5, 2, 6, 2, -2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric', 4, 2, 5, 2, -1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p5x, p5y, 0), App.Vector(p3x, p3y, 0)))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject', 8, 1, 2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 8, 2, 5, 2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical', 8))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x, p3y, 0), App.Vector(p6x, p6y, 0)))
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 8, 2, 9, 1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject', 9, 2, 1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal', 9))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.toggleConstruction(9)
        App.ActiveDocument.Sketch.toggleConstruction(8)
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Equal', 9, 8))
        App.ActiveDocument.recompute()

        # Add Dimension
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY', 8, -gv.frameThickness))
        App.ActiveDocument.recompute()

    App.getDocument(name).recompute()

    # Extrude frame member
    App.activeDocument().addObject("PartDesign::Pad", "Pad")
    App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
    App.activeDocument().Pad.Length = 10.0
    App.ActiveDocument.recompute()
    App.ActiveDocument.Pad.Length = length
    App.ActiveDocument.Pad.Reversed = 0
    App.ActiveDocument.Pad.Midplane = 0
    App.ActiveDocument.Pad.Length2 = 100.000000
    App.ActiveDocument.Pad.Type = 0
    App.ActiveDocument.Pad.UpToFace = None
    App.ActiveDocument.recompute()



def pickBushingNut(rodDia):
    for i in reversed(range(len(gv.bushingNutTable))):
        if (gv.bushingNutTable[i][1] < rodDia
            and (gv.bushingNutTable[i][0] + gv.bushingNutTable[i][2] / 2 > rodDia)):
            return gv.bushingNutTable[i]

    # Throw exception here because no proper bushing nut was found
    try:
        raise Exception("A bushing nut with the proper size was not found")
    except Exception as e:
        import traceback
        critical("A bushing nut with the proper size was not found",
                    'Part error: A bushing nut with the proper size was not found: \n\n' + str(
                        e) + '\n' + traceback.format_exc(limit=1), gv.level, os.path.basename(__file__))
        raise StandardError


def pickLeadScrewNut(rodDia):
    # Check standard nut table
    for i in range(len(gv.standardNuts)):
        if abs(gv.standardNuts[i][0] - rodDia) < 0.01:
            return gv.standardNuts[i]

    # Check metric nut table
    for i in range(len(gv.metricNuts)):
        if abs(gv.metricNuts[i][0] - rodDia) < 0.01:
            return gv.metricNuts[i]

    # Throw exception here because no proper bushing nut was found
    try:
        raise Exception("A lead screw nut with the proper size was not found")
    except Exception as e:
        import traceback
        critical("A lead screw nut with the proper size was not found",
                    'Part error: A lead screw nut with the proper size was not found: \n\n' + str(
                        e) + '\n' + traceback.format_exc(limit=1), gv.level, os.path.basename(__file__))
        raise StandardError
