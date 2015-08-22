# Copyright 2015 Matthew Rogge and Michael Uttmark
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
import math

import os
import sys
import platform
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import globalVars as gv

sys.path.append(gv.freecadDir)

try:
    import utilityFunctions as uf
except StandardError as e:
    msg = "Unable to import FreeCAD, please check your configuration."
    if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
        print '\033[1m\033[31m' + msg + '\x1b[0m'
    else:
        print msg
    print str(e)

source = os.path.basename(__file__)


class versionError(Exception):
    def __init__(self):
        raise StandardError


def makePrinter():
    if platform.system() == 'Windows':
        subprocess.call('cls', shell=True)
    else:
        subprocess.call('clear', shell=True)
    uf.header("______     _       _____     _           _____     __      _____ ", False)
    uf.header("| ___ \   | |     |____ |   | |         |  _  |   /  |    |  _  |", False)
    uf.header("| |_/ /___| |_ _ __   / / __| |  __   __| |/' |   `| |    | |/' |", False)
    uf.header("|    // _ \ __| '__|  \ \/ _` |  \ \ / /|  /| |    | |    |  /| |", False)
    uf.header("| |\ \  __/ |_| | .___/ / (_| |   \ V / \ |_/ / _ _| |_ _ \ |_/ /", False)
    uf.header("\_| \_\___|\__|_| \____/ \__,_|    \_/   \___/ (_)\___/(_) \___/ ", False)
    uf.bold("Version: 0.1.0 ", False)
    uf.bold("If you encounter any issues, please let us know at https://github.com/maaphoo/retr3d/issues", False)
    print ""
    # import FreeCAD modules
    try:
        import FreeCAD as App
    except ImportError as e:
        uf.critical("Failure to import FreeCAD, check your configuration file.", 'Failure to import FreeCAD: ' + str(e),
                    gv.level, source)

    import FreeCADGui as Gui

    if platform.system() == 'Windows':
        if (App.Version()[1] > '14'):
            try:
                import FreeCAD#
            except AttributeError:
                pass
            finally:
                uf.info("FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2],
                        "FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2], gv.level, source)

    if platform.system() == 'Darwin':  # OSX
        if (App.Version()[1] >= '14'):
            try:
                import FreeCAD#
                FreeCAD#.showMainWindow()
            except AttributeError:
                pass
            finally:
                uf.info("FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2],
                        "FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2], gv.level, source)

    if platform.system() == 'Linux':
        if (App.Version()[1] < '14'):
            uf.warning(
                "Retr3d has not been tested on FreeCAD version .13 and below. You are using version 0." + App.Version()[
                    1] + ". If problems ensue, please upgrade to versions .14 or .16.",
                "Untested FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2], gv.level, source)
        if (App.Version()[1] == '14'):
            if not (os.getcwd() == os.path.dirname(os.path.abspath(__file__))):
                uf.info("FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2],
                        "FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2], gv.level, source)
            else:
                uf.critical(
                    "Retr3d on Linux is not compatible with FreeCAD version .14 for command line usage. Please upgrade to .16 to continue",
                    "VersionError: FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2], gv.level,
                    source)
                raise versionError
        if (App.Version()[1] == '15'):
            uf.critical(
                "Retr3d on Linux is not compatible with FreeCAD version .15. Please upgrade to .16 or downgrade to .14 to continue.",
                "VersionError: FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2], gv.level,
                source)
            raise versionError
        if (App.Version()[1] == '16'):
            try:
                import FreeCAD#
                FreeCAD#.showMainWindow()
            except AttributeError:
                pass
            finally:
                uf.info("FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2],
                        "FreeCAD Version 0." + App.Version()[1] + " Revision " + App.Version()[2], gv.level, source)






    # import Part modules
    import xRodBottom
    import xRodTop
    import yRodL
    import yRodR
    import zRodL
    import zRodR
    import xCarriage
    import xRodClamp
    import xEndZRodHolder
    import xEndMotorPlate
    import xEndIdlerPlate
    import zRodSupport
    import zMotorMount
    import printBedBushingHolder
    import printBedSupport
    import printBed
    import yBeltAnchor
    import yMotorMount
    import yRodSupport
    import extruderMountAngle
    import extruderMountPlate
    import verticalBars
    import crossBarTop
    import crossBarFrontTop
    import crossBarFrontBottom
    import crossBarBackTop
    import crossBarBackBottom
    import sideBarTopL
    import sideBarBottomL
    import sideBarBottomR
    import sideBarTopR
    import frameSpacers
    import extruderBarrel
    import nozzle
    import xEndstop
    import zEndstop
    import feet
    import leadScrewCoupler
    import plate
    import slic3r
    import zipup
    import draw
    import checklist
    import heatedbed
    import marlin

    # If any of the parameters have been changed, the includes must be reloaded
    # Normally, this would just be globalVariables because that is what would be changed,
    # But while the rest of the code is in development, the other modules will be reloaded too.
    # This will make testing easier.

    if gv.reloadClasses:
        reload(gv)
        reload(uf)
        reload(xCarriage)
        reload(xRodClamp)
        reload(xRodBottom)
        reload(xRodTop)
        reload(xEndMotorPlate)
        reload(xEndIdlerPlate)
        reload(xEndZRodHolder)
        reload(yRodL)
        reload(yRodR)
        reload(zRodL)
        reload(zRodR)
        reload(zRodSupport)
        reload(zMotorMount)
        reload(printBedBushingHolder)
        reload(printBedSupport)
        reload(printBed)
        reload(yBeltAnchor)
        reload(yMotorMount)
        reload(yRodSupport)
        reload(extruderMountAngle)
        reload(extruderMountPlate)
        reload(verticalBars)
        reload(crossBarTop)
        reload(crossBarFrontTop)
        reload(crossBarFrontBottom)
        reload(crossBarBackTop)
        reload(crossBarBackBottom)
        reload(sideBarTopL)
        reload(sideBarBottomL)
        reload(sideBarBottomR)
        reload(sideBarTopR)
        reload(frameSpacers)
        reload(extruderBarrel)
        reload(nozzle)
        reload(xEndstop)
        reload(zEndstop)
        reload(feet)
        reload(leadScrewCoupler)
        reload(plate)
        reload(slic3r)
        reload(zipup)
        reload(draw)
        reload(checklist)
        reload(heatedbed)
        reload(marlin)

    gv.reloadClasses = True

    # instantiate part objects
    xRodBottom = xRodBottom.XRodBottom()
    xRodTop = xRodTop.XRodTop()
    yRodL = yRodL.YRodL()
    yRodR = yRodR.YRodR()
    zRodL = zRodL.ZRodL()
    zRodR = zRodR.ZRodR()
    xCarriage = xCarriage.XCarriage()
    xRodClampL = xRodClamp.XRodClamp("xRodClampL", "Left")
    xRodClampR = xRodClamp.XRodClamp("xRodClampR", "Right")
    xEndZRodHolderL = xEndZRodHolder.XEndZRodHolder("xEndZRodHolderL", "Left")
    xEndZRodHolderR = xEndZRodHolder.XEndZRodHolder("xEndZRodHolderR", "Right")
    xEndMotorPlate = xEndMotorPlate.XEndMotorPlate()
    xEndIdlerPlate = xEndIdlerPlate.XEndIdlerPlate()
    zRodSupportR = zRodSupport.ZRodSupport(name="zRodSupportR", side="Right")
    zRodSupportL = zRodSupport.ZRodSupport(name="zRodSupportL", side="Left")
    zMotorMount = zMotorMount.ZMotorMount()
    PBBHR = printBedBushingHolder.PrintBedBushingHolder("printBedBushingHolderR", "Right")
    PBBHL = printBedBushingHolder.PrintBedBushingHolder("printBedBushingHolderL", "Left")
    printBedSupport = printBedSupport.PrintBedSupport()
    printBed = printBed.PrintBed()
    yBeltAnchor = yBeltAnchor.YBeltAnchor()
    yMotorMount = yMotorMount.YMotorMount()
    yRodSupportR = yRodSupport.YRodSupport("yRodSupportR", "Right")
    yRodSupportL = yRodSupport.YRodSupport("yRodSupportL", "Left")
    extruderMountAngle = extruderMountAngle.ExtruderMountAngle()
    extruderMountPlate = extruderMountPlate.ExtruderMountPlate()
    verticalBars = verticalBars.VerticalBars()
    crossBarTop = crossBarTop.CrossBarTop()
    crossBarFrontTop = crossBarFrontTop.CrossBarFrontTop()
    crossBarFrontBottom = crossBarFrontBottom.CrossBarFrontBottom()
    crossBarBackTop = crossBarBackTop.CrossBarBackTop()
    crossBarBackBottom = crossBarBackBottom.CrossBarBackBottom()
    sideBarTopL = sideBarTopL.SideBarTopL()
    sideBarBottomL = sideBarBottomL.SideBarBottomL()
    sideBarBottomR = sideBarBottomR.SideBarBottomR()
    sideBarTopR = sideBarTopR.SideBarTopR()
    frameSpacers = frameSpacers.FrameSpacers()
    extruderBarrel = extruderBarrel.ExtruderBarrel()
    nozzle = nozzle.Nozzle()
    xEndstop = xEndstop.XEndstop()
    zEndstop = zEndstop.ZEndstop()
    feet = feet.Feet()
    leadScrewCoupler = leadScrewCoupler.LeadScrewCoupler()


    # convert standard nut sizes to mm
    for i in range(len(gv.standardNuts)):
        for j in range(len(gv.standardNuts[i])):
            gv.standardNuts[i][j] *= 25.4

    if gv.bushingNutSizesUsed == "Standard":
        gv.bushingNutTable = gv.standardNuts
    elif gv.bushingNutSizesUsed == "Metric":
        gv.bushingNutTable = gv.metricNuts
    elif gv.bushingNutSizesUsed == "StandardAndMetric":
        gv.bushingNutTable = gv.standardNuts + gv.metricNuts
        gv.bushingNutTable.sort(key=lambda x: x[0])

    # Determine printed mounting hole diameters
    gv.printedToFrameDia = uf.adjustHole(gv.mountToFrameDia)
    gv.printedToFrameHeadDia = uf.adjustHole(gv.mountToFrameHeadDia)
    gv.printedToPrintedDia = uf.adjustHole(gv.mountToPrintedDia)
    gv.printedToPrintedNutFaceToFace = uf.adjustHole(gv.mountToPrintedNutFaceToFace)

    # Select Bushing and Lead Screw nuts
    gv.xBushingNutBottom = uf.pickBushingNut(gv.xRodDiaBottom)
    gv.xBushingNutTop = uf.pickBushingNut(gv.xRodDiaTop)
    gv.yBushingNutR = uf.pickBushingNut(gv.yRodDiaR)
    gv.yBushingNutL = uf.pickBushingNut(gv.yRodDiaL)
    gv.zBushingNutR = uf.pickBushingNut(gv.zRodDiaR)
    gv.zBushingNutL = uf.pickBushingNut(gv.zRodDiaL)
    gv.leadScrewNut = uf.pickLeadScrewNut(gv.leadScrewDia)

    # Determine max rod diameters
    gv.xRodDiaMax = (gv.xRodDiaTop
                     if gv.xRodDiaTop
                        > gv.xRodDiaBottom
                     else gv.xRodDiaBottom)

    # Determine the max yRod diameter
    gv.yRodDiaMax = (gv.yRodDiaL
                     if gv.yRodDiaL
                        > gv.yRodDiaR
                     else gv.yRodDiaR)

    # Determine xBushingNutMaxThickness
    gv.xBushingNutMaxThickness = (gv.xBushingNutTop[3] if gv.xBushingNutTop[3] >
                                                          gv.xBushingNutBottom[3] else gv.xBushingNutBottom[3])


    # Determine zBushingNutMaxThickness
    gv.zBushingNutMaxThickness = (gv.zBushingNutR[3] if gv.zBushingNutR[3] >
                                                        gv.zBushingNutL[3] else gv.zBushingNutL[3])


    # Determine xCarriageMaxNutFaceToFace
    gv.xBushingNutMaxFacetoFace = (gv.xBushingNutTop[2] if gv.xBushingNutTop[2] >
                                                           gv.xBushingNutBottom[2] else gv.xBushingNutBottom[2])

    # Determine xCarriageBushingHolderOR
    gv.xCarriageBushingHolderOR = gv.xBushingNutMaxFacetoFace / math.cos(math.pi / 6) / 2 + gv.bushingNutPadding

    # Check/Determind xRodSpacing
    gv.xRodSpacing = (gv.xMotorMountPlateWidth
                      if gv.xMotorMountPlateWidth
                         > gv.xCarriageBushingHolderOR * 4 + gv.xMotorPulleyDia + gv.xBeltAnchorThickness
                      else gv.xCarriageBushingHolderOR * 4 + gv.xMotorPulleyDia + gv.xBeltAnchorThickness)

    # Determine yRodStandoff
    gv.yRodStandoff = gv.yRodDiaMax / 2 + gv.rodSupportNutTrapDepthMin + gv.rodSupportClampThickness

    # The yRodSupportNutTrapDepth is always the minimum nut trap depth
    yRodSupportNutTrapDepth = gv.rodSupportNutTrapDepthMin

    # Check to see if the yRodClamps work with available bolt lengths
    # If needed adjust the yRodStandoff for the next closest bolt length available.
    gv.yRodSupportClampBoltLength = (gv.yRodStandoff
                                     + gv.yRodDiaMax / 2
                                     + gv.clampThickness
                                     - gv.rodSupportNutTrapDepthMin
                                     + gv.clampNutThickness)

    for i in range(len(gv.clampBoltLengths)):
        if gv.yRodSupportClampBoltLength <= gv.clampBoltLengths[i]:
            gv.yRodSupportClampBoltLength = gv.clampBoltLengths[i]
            break
        elif i == len(gv.clampBoltLengths):
            try:
                raise Exception("No clamp bolt available is long enough for the yRodSupport")
            except Exception as e:
                import traceback
                uf.critical("No available clamp bolt is long enough for the yRodSupport",
                            'Part error: No available clamp bolt is long enough for the yRodSupport: \n\n' + str(
                                e) + '\n' + traceback.format_exc(limit=1), gv.level, os.path.basename(__file__))
                raise StandardError

    # Now redetermine yRodStandoff based on chosen yRodClampBoltLength
    gv.yRodStandoff = (gv.yRodSupportClampBoltLength
                       + gv.rodSupportNutTrapDepthMin
                       - gv.clampNutThickness
                       - gv.yRodDiaMax / 2
                       - gv.clampThickness)


    # Determine the maximum bushing nut face to face for the y axis bushings
    gv.PBBHMaxFaceToFace = (gv.yBushingNutL[2]
                            if gv.yBushingNutL[2]
                               > gv.yBushingNutR[2]
                            else gv.yBushingNutR[2])

    # Determine the PBBHStandoff. Must be large enough to acomodate the bushing holder itself,
    # and the yrod support. So take which ever is larger.
    gv.PBBHStandoff = (gv.yRodDiaMax / 2 + gv.clampThickness + gv.clampBoltHeadThickness + gv.yRodSupportClearance
                       if gv.yRodDiaMax / 2 + gv.clampThickness + gv.clampBoltHeadThickness + gv.yRodSupportClearance
                          > gv.PBBHMaxFaceToFace / 2 + gv.tabThickness
                       else gv.PBBHMaxFaceToFace / 2 + gv.tabThickness)

    # Determine yBeltAnchorHeight. Set to allow for clamping down to the surface of the y motor mount plate
    gv.yBeltAnchorHeight = (gv.yBeltAnchorBridgeThickness
                            + gv.yRodStandoff
                            + gv.PBBHStandoff
                            - gv.yMotorMountPlateThickness)

    # Determine xRodClampOverallThickness
    gv.xRodClampOverallThickness = 2 * gv.xRodClampThickness + gv.xRodDiaMax

    # determine the horizontal or vertical component of the shaftToMountHoleDist for the x motor
    gv.xMotorShaftToMountHoleDistX = math.pow(math.pow(gv.xEndShaftToMountHoleDist, 2) / 2, 0.5)

    # determine x motor width/length
    gv.xMotorBodyWidth = gv.xMotorShaftToMountHoleDistX * 2 + gv.xEndMotorMountHoleDia + 2 * gv.xEndMotorMountHolePadding

    # Determine the yMotor x component of the shaft to mount hole distance
    gv.yMotorShaftToMountHoleDistX = math.pow(math.pow(gv.yShaftToMountHoleDist, 2) / 2, 0.5)

    # Determine the y motor width/length
    gv.yMotorBodyWidth = (2 * gv.yMotorMountHolePadding +
                          gv.yMotorMountHoleDia +
                          2 * gv.yMotorShaftToMountHoleDistX)

    # Determine zShaftToMountHoleDistX
    gv.zShaftToMountHoleDistX = math.pow(math.pow(gv.zShaftToMountHoleDist, 2) / 2, 0.5)


    # Determine zMotorBodyWidth
    gv.zMotorBodyWidth = (2 * gv.zMotorMountHolePadding +
                          gv.zMotorMountHoleDia +
                          2 * gv.zShaftToMountHoleDistX)


    # Determine zMotor mount variables and zRodStandoff
    if gv.zMotorMountLocation == "Top":
        gv.zRodStandoff = gv.zMotorBodyWidth / 2
        gv.zMotorMountMountingFaceWidth = gv.frameHeight
        gv.zMotorMountLength = gv.zMotorMountMountingFaceWidth + gv.zRodStandoff + gv.zMotorBodyWidth / 2
        gv.zMotorMountEdgeToShaftHole = gv.zMotorMountMountingFaceWidth + gv.zRodStandoff
        gv.zRodZScrewDist = (gv.zRodZScrewDist
                             if gv.zRodZScrewDist
                                > (gv.frameWidth + gv.zMotorMountPlateWidth) / 2
                             else (gv.frameWidth + gv.zMotorMountPlateWidth) / 2)
    if gv.zMotorMountLocation == "Bottom":
        gv.zRodStandoff = gv.zMotorMountPlateWidth / 2
        gv.zMotorMountMountingFaceWidth = gv.frameWidth
        gv.zRodZScrewDist = (gv.zRodZScrewDist
                             if gv.zRodZScrewDist
                                > (gv.frameWidth + gv.zMotorBodyWidth + gv.zMotorBodyToFrameSpacing) / 2
                             else (gv.frameWidth + gv.zMotorBodyWidth + gv.zMotorBodyToFrameSpacing) / 2)
        gv.zMotorMountLength = gv.zMotorMountMountingFaceWidth / 2 + gv.zRodZScrewDist + gv.zMotorBodyWidth / 2
        gv.zMotorMountEdgeToShaftHole = gv.zMotorMountMountingFaceWidth / 2 + gv.zRodZScrewDist




    # Determine zBushingNutMaxFaceToFace
    gv.zBushingNutMaxFaceToFace = (gv.zBushingNutL[2]
                                   if gv.zBushingNutL[2]
                                      > gv.zBushingNutR[2]
                                   else gv.zBushingNutR[2])

    # Determine the max Nut face to face for the xEndZRodHolder between zBushing nuts and lead Screw nuts
    gv.xEndZRodHolderMaxNutFaceToFace = (
    gv.zBushingNutMaxFaceToFace if gv.zBushingNutMaxFaceToFace > gv.leadScrewNut[2] else gv.leadScrewNut[2])

    # Determine xRodClampWidth
    gv.xRodClampWidth = (gv.zRodZScrewDist
                         + gv.xEndZRodHolderMaxNutFaceToFace / math.cos(math.pi / 6)
                         + 2 * gv.bushingNutPadding)
    # Determine zRod Spacing
    gv.zRodSpacing = (gv.xRodLength
                      + 2 * gv.xRodClampWidth
                      - 2 * gv.xRodClampPocketDepth
                      - 2 * gv.bushingNutPadding
                      - gv.xEndZRodHolderMaxNutFaceToFace / math.cos(math.pi / 6)
                      )





    # Determine the max Nut Thickness for the xEndZRodHolder between both zBushingNuts and LeadScrewNuts
    gv.xEndZRodHolderMaxNutThickness = (
    gv.zBushingNutMaxThickness if gv.zBushingNutMaxThickness > gv.leadScrewNut[3] else gv.leadScrewNut[3])

    # Determine the height of the xEndZRodHolder
    gv.xEndZRodHolderHeight = 2 * (
    gv.xEndZRodHolderMaxNutThickness + gv.bushingNutPadding) + gv.xRodSpacing - gv.xRodDiaMax

    # Determine printableWidth
    gv.printableWidth = (gv.xRodLength
                         - 2 * gv.xRodClampPocketDepth
                         - gv.xCarriageWidth / 2
                         - gv.xCarriageWingWidth)

    # Determine yRodSupportWidth
    gv.yRodSupportWidth = (gv.yRodDiaMax
                           + gv.clampHoleDia
                           + gv.clampNutFaceToFace
                           + 2 * gv.clampNutPadding
                           + 4 * gv.slotPadding
                           + 2 * gv.slotDia
                           + 2 * gv.slotWidth)

    # Determine printBedBusingSupportWidth
    gv.printBedBusingSupportWidth = (4 * gv.slotPadding +
                                     2 * gv.slotDia +
                                     2 * gv.slotWidth +
                                     2 * gv.bushingNutPadding +
                                     gv.PBBHMaxFaceToFace / math.cos(math.pi / 6))


    # Determine yRodSpacing
    gv.yRodSpacing = ((gv.printableWidth + 2 * gv.printBedPadding) / 2
                      if (gv.printableWidth + 2 * gv.printBedPadding) / 2
                         > gv.yMotorMountPlateWidth + gv.yRodSupportWidth
                      else gv.yMotorMountPlateWidth + gv.yRodSupportWidth)
    # Check yRodSpacing to make sure that the Bushing supports can be attached to the print bed support
    if gv.yRodSpacing + gv.printBedBusingSupportWidth > gv.printableWidth + 2 * gv.printBedPadding:
        try:
            raise Exception("The yRods can't be spaced far enough apart. Try longer xAxis rods.")
        except Exception as e:
            import traceback
            uf.critical("The yRods can't be spaced far enough apart. Try longer xAxis rods.",
                        "Part error: The yRods can't be spaced far enough apart.: \n\n" + str(
                            e) + '\n' + traceback.format_exc(limit=1), gv.level, os.path.basename(__file__))
            raise StandardError

    # Determine the maximum thickness of the y axis bushings
    gv.yBushingNutMaxThickness = (gv.yBushingNutL[3]
                                  if gv.yBushingNutL[3]
                                     > gv.yBushingNutR[3]
                                  else gv.yBushingNutR[3])

    # Determine the depth of the y bushing mounts
    gv.PBBHDepth = gv.yBushingNutMaxThickness + gv.bushingNutPadding

    # Determine center to center distance between the slots on the y bushing mounts
    # This is the spacing used to determine the spacing between mounting holes on the print bed support
    gv.yBushingMountSlotSpacing = (gv.PBBHMaxFaceToFace / math.cos(math.pi / 6)
                                   + 2 * gv.bushingNutPadding
                                   + 2 * gv.slotPadding
                                   + gv.slotDia
                                   + gv.slotWidth)

    # Determine the center to center distance between y bushing nuts along the y axis
    # Increase printable area by changing the divisor. The price is a less stable print bed.
    gv.yBushingNutSeparation = (gv.yRodLength - 2 * gv.frameWidth) / 3

    # Determine the printable length
    gv.printableLength = (gv.yRodLength
                          - 2 * gv.frameWidth
                          - gv.yBushingNutSeparation
                          - gv.PBBHDepth)

    # Determine the y belt anchor hole spacing
    gv.yBeltAnchorHoleSpacing = (gv.yBeltAnchorLength
                                 + 2 * gv.mountToPrintedPadding
                                 + uf.adjustHole(gv.mountToPrintedDia))


    # Determine the extruderMountPlateWidth
    gv.extruderMountPlateWidth = (gv.xCarriageWidth if gv.xCarriageWidth >
                                                       gv.extruderWidth else gv.extruderWidth)


    # Determine hotEndLength
    gv.hotEndLength = gv.nozzleLength + gv.extruderBarrelLength


    # Determine zEndStopClampLength
    gv.zEndStopClampLength = (2 * gv.mountToPrintedPadding
                              + gv.printedToPrintedDia
                              + 2 * gv.xEndstopChannelWidth
                              + gv.xEndstopContactSpacing
                              + gv.xEndstopPadding
                              + gv.zEndstopJogWidth)


    # Determine vertBarDistBelowZRod
    gv.vertBarDistBelowZRod = (gv.yRodStandoff
                               + gv.PBBHStandoff
                               + gv.printBedSupportThickness
                               + gv.printBedStandoff
                               + gv.printBedThickness
                               + gv.hotEndLength
                               - (gv.extruderMountAngleWidth + gv.extruderMountAngleThickness) / 2
                               - gv.xCarriageMountHoleVertOffset
                               + gv.xCarriageBushingHolderOR
                               - (gv.xEndZRodHolderHeight - gv.xRodSpacing) / 2
                               - gv.zEndStopClampLength  # May change to something fancier that incorporates the zOffset screw
                               - gv.zRodSupportLength)

    # Determine vertBarDistAboveZRod
    if gv.zMotorMountLocation == "Top":
        gv.vertBarDistAboveZRod = (gv.frameJointPadding + gv.frameWidth
                                   if gv.frameJointPadding + gv.frameWidth
                                      > gv.leadScrewCouplerLength + 2 * gv.leadScrewCouplerGap
                                   else gv.leadScrewCouplerLength + 2 * gv.leadScrewCouplerGap)

    elif gv.zMotorMountLocation == "Bottom":
        gv.vertBarDistAboveZRod = gv.frameJointPadding + 2 * gv.slotPadding + gv.slotDia

    # Determine the vertBarLength
    gv.vertBarLength = gv.zRodLength + gv.vertBarDistAboveZRod + gv.vertBarDistBelowZRod

    # Determine the cross bar length. Used for all cross bars.
    gv.crossBarLength = gv.zRodSpacing + gv.frameWidth

    # Determine yRodSupportMountHoleSpacing
    gv.yRodSupportMountHoleSpacing = (gv.yRodDiaMax
                                      + gv.clampHoleDia
                                      + gv.clampNutFaceToFace
                                      + 2 * gv.clampNutPadding
                                      + 2 * gv.slotPadding
                                      + gv.slotDia
                                      + gv.slotWidth)

    gv.sideBarLength = gv.yRodLength - 2 * gv.frameWidth

    # Determine extruderNozzleStandoff which is the distance between the center of the nozzle and the face of the vertical bars
    gv.extruderNozzleStandoff = (gv.zRodStandoff
                                 + gv.xEndZRodHolderMaxNutFaceToFace / 2
                                 + gv.xEndZRodHolderFaceThickness
                                 + gv.xMotorMountPlateThickness
                                 + gv.xRodClampOverallThickness / 2
                                 + gv.xCarriageBushingHolderOR
                                 + gv.xCarriageThickness
                                 + gv.extruderDepth
                                 - gv.extruderEdgeToCenterLine)

    # Determine xRodAxisToMountHoleDist
    gv.xRodAxisToMountHoleDist = (gv.xRodDiaMax / 2 + gv.xRodClampMountHoleToRodPadding
                                  if gv.xRodDiaMax / 2 + gv.xRodClampMountHoleToRodPadding
                                     > (gv.xEndZRodHolderMaxNutThickness
                                        + gv.bushingNutPadding
                                        + gv.xEndZRodHolderMountHoleToRodPadding
                                        + gv.printedToPrintedDia / 2)
                                  else (gv.xEndZRodHolderMaxNutThickness
                                        + gv.bushingNutPadding
                                        + gv.xEndZRodHolderMountHoleToRodPadding
                                        + gv.printedToPrintedDia / 2))

    # Determine xEndstopLength
    gv.xEndstopLength = gv.xEndstopPadding + gv.mountToPrintedDia / 2 + gv.xRodAxisToMountHoleDist


    # Determine xEndstopSupportWidth
    gv.zEndstopSupportWidth = (gv.zRodDiaL
                               + 2 * gv.printedToPrintedDia
                               + 2 * gv.mountToPrintedPadding)

    # Determine xEndstopBodyThickness
    gv.zEndstopBodyThickness = (gv.zRodZScrewDist / 2
                                + gv.xEndstopChannelDepth / 2
                                - gv.zRodDiaL / 2)

    # determind xBeltAnchorHeight
    gv.xBeltAnchorHeight = gv.xCarriageBushingHolderOR + gv.xRodClampOverallThickness / 2 + gv.xBeltAnchorBridgeThickness
    # Draw parts, save and make assembly

    del gv.xAxisParts[:]
    del gv.yAxisParts[:]
    del gv.zAxisParts[:]
    # Make file for assembly
    uf.makeAssemblyFile()
    uf.info("Starting to draw parts...", "Assembly file made", gv.level, source)

    heatedbed.design()

    # Make components for x-Axis, add to assembly, save and close
    xRodBottom.draw()
    uf.info("Done drawing xRodBottom", "Finished xRodBottom.draw()", gv.level, source)
    xRodBottom.assemble()
    uf.info("Done assembling xRodBottom", "Finished xRodBottom.assemble()", gv.level, source)
    uf.saveAndClose("xRodBottom", False)

    xRodTop.draw()
    uf.info("Done drawing xRodTop", "Finished xRodTop.draw()", gv.level, source)
    xRodTop.assemble()
    uf.info("Done assembling xRodTop", "Finished xRodTop.assemble()", gv.level, source)
    uf.saveAndClose("xRodTop", False)

    xCarriage.draw()
    uf.info("Done drawing xCarriage", "Finished xCarriage.draw()", gv.level, source)
    xCarriage.assemble()
    uf.info("Done assembling xCarriage", "Finished xCarriage.assemble()", gv.level, source)
    uf.saveAndClose("xCarriage", True)

    extruderMountAngle.draw()
    uf.info("Done drawing extruderMountAngle", "Finished extruderMountAngle.draw()", gv.level, source)
    extruderMountAngle.assemble()
    uf.info("Done assembling extruderMountAngle", "Finished extruderMountAngle.assemble()", gv.level, source)
    uf.saveAndClose("extruderMountAngle", False)

    extruderMountPlate.draw()
    uf.info("Done drawing extruderMountPlate", "Finished extruderMountPlate.draw()", gv.level, source)
    extruderMountPlate.assemble()
    uf.info("Done assembling extruderMountPlate", "Finished extruderMountPlate.assemble()", gv.level, source)
    uf.saveAndClose("extruderMountPlate", False)

    xRodClampL.draw()
    uf.info("Done drawing xRodClampL", "Finished xRodClampL.draw()", gv.level, source)
    xRodClampL.assemble()
    uf.info("Done assembling xRodClampL", "Finished xRodClampL.assemble()", gv.level, source)
    uf.saveAndClose("xRodClampL", True)

    xRodClampR.draw()
    uf.info("Done drawing xRodClampR", "Finished xRodClampR.draw()", gv.level, source)
    xRodClampR.assemble()
    uf.info("Done assembling xRodClampR", "Finished xRodClampR.assemble()", gv.level, source)
    uf.saveAndClose("xRodClampR", True)

    xEndMotorPlate.draw()
    uf.info("Done drawing xEndMotorPlate", "Finished xEndMotorPlate.draw()", gv.level, source)
    xEndMotorPlate.assemble()
    uf.info("Done assembling xEndMotorPlate", "Finished xEndMotorPlate.assemble()", gv.level, source)
    uf.saveAndClose("xEndMotorPlate", False)

    xEndIdlerPlate.draw()
    uf.info("Done drawing xEndIdlerPlate", "Finished xEndIdlerPlate.draw()", gv.level, source)
    xEndIdlerPlate.assemble()
    uf.info("Done assembling xEndIdlerPlate", "Finished xEndIdlerPlate.assemble()", gv.level, source)
    uf.saveAndClose("xEndIdlerPlate", False)

    extruderBarrel.draw()
    uf.info("Done drawing extruderBarrel", "Finished extruderBarrel.draw()", gv.level, source)
    extruderBarrel.assemble()
    uf.info("Done assembling extruderBarrel", "Finished extruderBarrel.assemble()", gv.level, source)
    uf.saveAndClose("extruderBarrel", False)

    nozzle.draw()
    uf.info("Done drawing nozzle", "Finished nozzle.draw()", gv.level, source)
    nozzle.assemble()
    uf.info("Done assembling nozzle", "Finished nozzle.assemble()", gv.level, source)
    uf.saveAndClose("nozzle", False)

    xEndZRodHolderL.draw()
    uf.info("Done drawing xEndZRodHolderL", "Finished xEndZRodHolderL.draw()", gv.level, source)
    xEndZRodHolderL.assemble()
    uf.info("Done assembling xEndZRodHolderL", "Finished xEndZRodHolderL.assemble()", gv.level, source)
    uf.saveAndClose("xEndZRodHolderL", True)

    xEndZRodHolderR.draw()
    uf.info("Done drawing xEndZRodHolderR", "Finished xEndZRodHolderR.draw()", gv.level, source)
    xEndZRodHolderR.assemble()
    uf.info("Done assembling xEndZRodHolderR", "Finished xEndZRodHolderR.assemble()", gv.level, source)
    uf.saveAndClose("xEndZRodHolderR", True)

    xEndstop.draw()
    xEndstop.assemble()
    uf.info("Done assembling xEndstop", "Finished xEndstop.assemble()", gv.level, source)
    uf.saveAndClose("xEndstop", True)
    uf.saveAndClose("xEndstopCap", True)

    uf.positionXAxis()

    # Make components for ZAxis, add to assembly, save and close#

    zRodL.draw()
    uf.info("Done drawing zRodL", "Finished zRodL.draw()", gv.level, source)
    zRodL.assemble()
    uf.info("Done assembling zRodL", "Finished zRodL.assemble()", gv.level, source)
    uf.saveAndClose("zRodL", False)

    zRodR.draw()
    uf.info("Done drawing zRodR", "Finished zRodR.draw()", gv.level, source)
    zRodR.assemble()
    uf.info("Done assembling zRodR", "Finished zRodR.assemble()", gv.level, source)
    uf.saveAndClose("zRodR", False)

    zRodSupportR.draw()
    uf.info("Done drawing zRodSupportR", "Finished zRodSupportR.draw()", gv.level, source)
    zRodSupportR.assemble()
    uf.info("Done assembling zRodSupportR", "Finished zRodSupportR.assemble()", gv.level, source)
    uf.saveAndClose("zRodSupportR", True)
    uf.saveAndClose("zRodSupportRClamp", True)

    zRodSupportL.draw()
    uf.info("Done drawing zRodSupportL", "Finished zRodSupportL.draw()", gv.level, source)
    zRodSupportL.assemble()
    uf.info("Done assembling zRodSupportL", "Finished zRodSupportL.assemble()", gv.level, source)
    uf.saveAndClose("zRodSupportL", True)
    uf.saveAndClose("zRodSupportLClamp", True)

    zMotorMount.draw()
    uf.info("Done drawing zMotorMount", "Finished zMotorMount.draw()", gv.level, source)
    zMotorMount.assemble()
    uf.info("Done assembling zMotorMount", "Finished zMotorMount.assemble()", gv.level, source)
    uf.saveAndClose("zMotorMount", True)

    zEndstop.draw()
    uf.info("Done drawing zEndstop", "Finished zEndstop.draw()", gv.level, source)
    zEndstop.assemble()
    uf.info("Done assembling zEndstop", "Finished zEndstop.assemble()", gv.level, source)
    uf.saveAndClose("zEndstop", False)

    leadScrewCoupler.draw()
    uf.info("Done drawing leadScrewCoupler", "Finished leadScrewCoupler.draw()", gv.level, source)
    leadScrewCoupler.assemble()
    uf.info("Done assembling leadScrewCoupler", "Finished leadScrewCoupler.assemble()", gv.level, source)
    uf.saveAndClose("leadScrewCoupler", True)

    uf.positionZAxis()


    # Make components for yAxis, add to assembly, save and close#

    yRodL.draw()
    uf.info("Done drawing yRodL", "Finished yRodL.draw()", gv.level, source)
    yRodL.assemble()
    uf.info("Done assembling yRodL", "Finished yRodL.assemble()", gv.level, source)
    uf.saveAndClose("yRodL", False)

    yRodR.draw()
    uf.info("Done drawing yRodR", "Finished yRodR.draw()", gv.level, source)
    yRodR.assemble()
    uf.info("Done assembling yRodR", "Finished yRodR.assemble()", gv.level, source)
    uf.saveAndClose("yRodR", False)

    PBBHR.draw()
    uf.info("Done drawing Print Bed Bushing Holder Right", "Finished PBBHR.draw()", gv.level, source)
    PBBHR.assemble()
    uf.info("Done assembling Print Bed Bushing Holder Right", "Finished PBBHR.assemble()", gv.level, source)
    uf.saveAndClose("printBedBushingHolderR", True)

    PBBHL.draw()
    uf.info("Done drawing Print Bed Bushing Holder Left", "Finished PBBHL.draw()", gv.level, source)
    PBBHL.assemble()
    uf.info("Done assembling Print Bed Bushing Holder Left", "Finished PBBHL.assemble()", gv.level, source)
    uf.saveAndClose("printBedBushingHolderL", True)

    yBeltAnchor.draw()
    uf.info("Done drawing yBeltAnchor", "Finished yBeltAnchor.draw()", gv.level, source)
    yBeltAnchor.assemble()
    uf.info("Done assembling yBeltAnchor", "Finished yBeltAnchor.assemble()", gv.level, source)
    uf.saveAndClose("yBeltAnchor", True)

    printBedSupport.draw()
    uf.info("Done drawing printBedSupport", "Finished printBedSupport.draw()", gv.level, source)
    printBedSupport.assemble()
    uf.info("Done assembling printBedSupport", "Finished printBedSupport.assemble()", gv.level, source)
    uf.saveAndClose("printBedSupport", False)

    printBed.draw()
    uf.info("Done drawing printBed", "Finished printBed.draw()", gv.level, source)
    printBed.assemble()
    uf.info("Done assembling printBed", "Finished printBed.assemble()", gv.level, source)
    uf.saveAndClose("printBed", False)

    yMotorMount.draw()
    uf.info("Done drawing yMotorMount", "Finished yMotorMount.draw()", gv.level, source)
    yMotorMount.assemble()
    uf.info("Done assembling yMotorMount", "Finished yMotorMount.assemble()", gv.level, source)
    uf.saveAndClose("yMotorMount", True)

    yRodSupportR.draw()
    uf.info("Done drawing yRodSupportR", "Finished yRodSupportR.draw()", gv.level, source)
    yRodSupportR.assemble()
    uf.info("Done assembling yRodSupportR", "Finished yRodSupportR.assemble()", gv.level, source)
    uf.saveAndClose("yRodSupportR", True)
    uf.saveAndClose("yRodSupportRClamp", True)

    yRodSupportL.draw()
    uf.info("Done drawing yRodSupportL", "Finished yRodSupportL.draw()", gv.level, source)
    yRodSupportL.assemble()
    uf.info("Done assembling yRodSupportL", "Finished yRodSupportL.assemble()", gv.level, source)
    uf.saveAndClose("yRodSupportL", True)
    uf.saveAndClose("yRodSupportLClamp", True)



    # Make components for frame, add to assembly, save and close
    verticalBars.draw()
    uf.info("Done drawing verticalBars", "Finished verticalBars.draw()", gv.level, source)
    verticalBars.assemble()
    uf.info("Done assembling verticalBars", "Finished verticalBars.assemble()", gv.level, source)
    uf.saveAndClose("verticalBars", False)

    crossBarTop.draw()
    uf.info("Done drawing crossBarTop", "Finished crossBarTop.draw()", gv.level, source)
    crossBarTop.assemble()
    uf.info("Done assembling crossBarTop", "Finished crossBarTop.assemble()", gv.level, source)
    uf.saveAndClose("crossBarTop", False)

    crossBarFrontTop.draw()
    uf.info("Done drawing crossBarFrontTop", "Finished crossBarFrontTop.draw()", gv.level, source)
    crossBarFrontTop.assemble()
    uf.info("Done assembling crossBarFrontTop", "Finished crossBarFrontTop.assemble()", gv.level, source)
    uf.saveAndClose("crossBarFrontTop", False)

    crossBarFrontBottom.draw()
    uf.info("Done drawing crossBarFrontBottom", "Finished crossBarFrontBottom.draw()", gv.level, source)
    crossBarFrontBottom.assemble()
    uf.info("Done assembling crossBarFrontBottom", "Finished crossBarFrontBottom.assemble()", gv.level, source)
    uf.saveAndClose("crossBarFrontBottom", False)

    crossBarBackTop.draw()
    uf.info("Done drawing crossBarBackTop", "Finished crossBarBackTop.draw()", gv.level, source)
    crossBarBackTop.assemble()
    uf.info("Done assembling crossBarBackTop", "Finished crossBarBackTop.assemble()", gv.level, source)
    uf.saveAndClose("crossBarBackTop", False)

    crossBarBackBottom.draw()
    uf.info("Done drawing rossBarBackBottom", "Finished crossBarBackBottom.draw()", gv.level, source)
    crossBarBackBottom.assemble()
    uf.info("Done assembling rossBarBackBottom", "Finished crossBarBackBottom.assemble()", gv.level, source)
    uf.saveAndClose("crossBarBackBottom", False)

    sideBarTopL.draw()
    uf.info("Done drawing sideBarTopL", "Finished sideBarTopL.draw()", gv.level, source)
    sideBarTopL.assemble()
    uf.info("Done assembling sideBarTopL", "Finished sideBarTopL.assemble()", gv.level, source)
    uf.saveAndClose("sideBarTopL", False)

    sideBarBottomL.draw()
    uf.info("Done drawing sideBarBottomL", "Finished sideBarBottomL.draw()", gv.level, source)
    sideBarBottomL.assemble()
    uf.info("Done assembling sideBarBottomL", "Finished sideBarBottomL.assemble()", gv.level, source)
    uf.saveAndClose("sideBarBottomL", False)

    sideBarBottomR.draw()
    uf.info("Done drawing sideBarBottomR", "Finished sideBarBottomR.draw()", gv.level, source)
    sideBarBottomR.assemble()
    uf.info("Done assembling sideBarBottomR", "Finished sideBarBottomR.assemble()", gv.level, source)
    uf.saveAndClose("sideBarBottomR", False)

    sideBarTopR.draw()
    uf.info("Done drawing sideBarTopR", "Finished sideBarTopR.draw()", gv.level, source)
    sideBarTopR.assemble()
    uf.info("Done assembling sideBarTopR", "Finished sideBarTopR.assemble()", gv.level, source)
    uf.saveAndClose("sideBarTopR", False)

    frameSpacers.draw()
    uf.info("Done drawing frameSpacers", "Finished frameSpacers.draw()", gv.level, source)
    frameSpacers.assemble()
    uf.info("Done assembling frameSpacers", "Finished frameSpacers.assemble()", gv.level, source)
    uf.saveAndClose("frameSpacers", False)

    feet.draw()
    uf.info("Done drawing Feet", "Finished feet.draw()", gv.level, source)
    feet.assemble()
    uf.info("Done assembling feet", "Finished feet.assemble()", gv.level, source)
    uf.saveAndClose("feet", True)



    draw.setup("printBedSupport", 'Pocket001')
    draw.setup("extruderMountPlate", 'Pocket002')
    draw.setup("xEndIdlerPlate", 'Pocket')
    draw.setup("xEndMotorPlate", 'Pocket001')
    App.ActiveDocument = App.getDocument("PrinterAssembly")

    uf.saveAssembly()

    if (gv.plate):
        uf.info("Building the print plates...", "Started building print plates", gv.level, source)
        plate.plate()
        uf.info("Finished building the print plates.", "Finished building print plates", gv.level, source)

    if (gv.slic3r):
        uf.info("Slicing with Slic3er...", "Started slicing.", gv.level, source)
        slic3r.slic3r()
        uf.info("Finished slicing.", "Finished slicing", gv.level, source)

    heatedbed.design()
    checklist.create()
    marlin.marlin()
    zipup.zipup()

try:
    makePrinter()
except KeyboardInterrupt:
    print "Exiting..."
    pass
