 #import Math stuff
from __future__ import division # allows floating point division from integersimport math
import math
from itertools import product

#import system and file handling stuff
import os
import sys
import datetime

#Change the following line to locate the folder containing the printer building scripts
#Make sure to use forward slashes like this '/' and not back slashes like this '\'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import globalVars as gv

#Change the following line to locate the folder containing FreeCAD's FreeCAD.so or FreeCAD.dll file
#For Mac users it is inside the FreeCAD.app file. Use "show package contents" to locate it. .../FreeCAD.app/Contents/lib
#For Windows users it is in the .../FreeCAD 0.xx/bin or .../FreeCAD 0.xx/lib folder
#This actually shouldn't even be necessary
sys.path.append(gv.freecadDir)




#import FreeCAD modules
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher





#import printer related
import utilityFunctions as uf


#import Part modules
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
import plate
import slic3r
import zipup

#If any of the parameters have been changed, the includes must be reloaded
#Normally, this would just be globalVariables because that is what would be changed,
#But while the rest of the code is in development, the other modules will be reloaded too.
#This will make testing easier.

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
	reload(plate)
	reload(slic3r)
	reload(zipup)

gv.reloadClasses = True	

#instantiate part objects
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
zRodSupportR = zRodSupport.ZRodSupport(name = "zRodSupportR", side = "Right")
zRodSupportL = zRodSupport.ZRodSupport(name = "zRodSupportL", side = "Left")
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

	
#convert standard nut sizes to mm
for i in range(len(gv.standardNuts)):
	for j in range(len(gv.standardNuts[i])):
		gv.standardNuts[i][j] *= 25.4

if gv.bushingNutSizesUsed == "Standard":
	gv.bushingNutTable = gv.standardNuts
elif  gv.bushingNutSizesUsed == "Metric":
	gv.bushingNutTable = gv.metricNuts
elif  gv.bushingNutSizesUsed == "StandardAndMetric":
	gv.bushingNutTable = gv.standardNuts + gv.metricNuts
	gv.bushingNutTable.sort(key=lambda x: x[0])

#Determine printed mounting hole diameters
gv.printedToFrameDia = uf.adjustHole(gv.mountToFrameDia)
gv.printedToPrintedDia = uf.adjustHole(gv.mountToPrintedDia)

#Select Bushing and Lead Screw nuts
gv.xBushingNutBottom = uf.pickBushingNut(gv.xRodDiaBottom)
gv.xBushingNutTop = uf.pickBushingNut(gv.xRodDiaTop)
gv.yBushingNutR = uf.pickBushingNut(gv.yRodDiaR)
gv.yBushingNutL = uf.pickBushingNut(gv.yRodDiaL)
gv.zBushingNutR = uf.pickBushingNut(gv.zRodDiaR)
gv.zBushingNutL = uf.pickBushingNut(gv.zRodDiaL)
gv.leadScrewNut = uf.pickLeadScrewNut(gv.leadScrewDia)

#Determine max rod diameters
gv.xRodDiaMax = (gv.xRodDiaTop
			if gv.xRodDiaTop
			> gv.xRodDiaBottom 
			else gv.xRodDiaBottom)

#Determine the max yRod diameter
gv.yRodDiaMax = (gv.yRodDiaL
			if gv.yRodDiaL
			> gv.yRodDiaR 
			else gv.yRodDiaR)

#Determine xBushingNutMaxThickness
gv.xBushingNutMaxThickness = (gv.xBushingNutTop[3] if gv.xBushingNutTop[3] > 
							gv.xBushingNutBottom[3] else gv.xBushingNutBottom[3])


#Determine zBushingNutMaxThickness
gv.zBushingNutMaxThickness = (gv.zBushingNutR[3] if gv.zBushingNutR[3] > 
							gv.zBushingNutL[3] else gv.zBushingNutL[3])


#Determine xCarriageMaxNutFaceToFace
gv.xBushingNutMaxFacetoFace = (gv.xBushingNutTop[2] if gv.xBushingNutTop[2] > 
							gv.xBushingNutBottom[2] else gv.xBushingNutBottom[2])

#Determine xCarriageBushingHolderOR
gv.xCarriageBushingHolderOR = gv.xBushingNutMaxFacetoFace/math.cos(math.pi/6)/2+gv.bushingNutPadding

#Check/Determind xRodSpacing
gv.xRodSpacing = (gv.xMotorMountPlateWidth
				if gv.xMotorMountPlateWidth
				> gv.xCarriageBushingHolderOR*4 + gv.xMotorPulleyDia+ gv.xBeltAnchorThickness
				else gv.xCarriageBushingHolderOR*4 + gv.xMotorPulleyDia+ gv.xBeltAnchorThickness)
				
#Determine yRodStandoff
gv.yRodStandoff = gv.yRodDiaMax/2 + gv.rodSupportNutTrapDepthMin + gv.rodSupportClampThickness

#The yRodSupportNutTrapDepth is always the minimum nut trap depth 
yRodSupportNutTrapDepth = gv.rodSupportNutTrapDepthMin

#Check to see if the yRodClamps work with available bolt lengths
#If needed adjust the yRodStandoff for the next closest bolt length available.
gv.yRodSupportClampBoltLength = (gv.yRodStandoff 
							   + gv.yRodDiaMax/2
							   + gv.clampThickness
							   - gv.rodSupportNutTrapDepthMin
							   + gv.clampNutThickness)

for i in range(len(gv.clampBoltLengths)):
	if gv.yRodSupportClampBoltLength <= gv.clampBoltLengths[i]:
		gv.yRodSupportClampBoltLength = gv.clampBoltLengths[i]
		break;
	elif i == len(gv.clampBoltLengths):
		raise Exception("No clamp bolt available is long enough for the yRodSupport")
		
#Now redetermine yRodStandoff based on chosen yRodClampBoltLength
gv.yRodStandoff = (gv.yRodSupportClampBoltLength
				 + gv.rodSupportNutTrapDepthMin
				 - gv.clampNutThickness
				 - gv.yRodDiaMax/2
				 - gv.clampThickness)


#Determine the maximum bushing nut face to face for the y axis bushings
gv.PBBHMaxFaceToFace = (gv.yBushingNutL[2] 
						if gv.yBushingNutL[2]
						> gv.yBushingNutR[2] 
						else gv.yBushingNutR[2])

#Determine the PBBHStandoff. Must be large enough to acomodate the bushing holder itself,
# and the yrod support. So take which ever is larger.
gv.PBBHStandoff = (gv.yRodDiaMax/2 + gv.clampThickness + gv.clampBoltHeadThickness + gv.yRodSupportClearance
				if gv.yRodDiaMax/2 + gv.clampThickness + gv.clampBoltHeadThickness + gv.yRodSupportClearance
				> gv.PBBHMaxFaceToFace/2 + gv.tabThickness
				else gv.PBBHMaxFaceToFace/2 + gv.tabThickness)

#Determine yBeltAnchorHeight. Set to allow for clamping down to the surface of the y motor mount plate
gv.yBeltAnchorHeight = (gv.yBeltAnchorBridgeThickness 
					  + gv.yRodStandoff
					  + gv.PBBHStandoff
					  - gv.yMotorMountPlateThickness)

#Determine xRodClampOverallThickness
gv.xRodClampOverallThickness = 2*gv.xRodClampThickness+gv.xRodDiaMax

#determine the horizontal or vertical component of the shaftToMountHoleDist for the x motor
gv.xMotorShaftToMountHoleDistX = math.pow(math.pow(gv.xEndShaftToMountHoleDist,2)/2,0.5)

#determine x motor width/length
gv.xMotorBodyWidth = gv.xMotorShaftToMountHoleDistX*2+gv.xEndMotorMountHoleDia+2*gv.xEndMotorMountHolePadding

#Determine the yMotor x component of the shaft to mount hole distance
gv.yMotorShaftToMountHoleDistX = math.pow(math.pow(gv.yShaftToMountHoleDist,2)/2,0.5)

#Determine the y motor width/length
gv.yMotorBodyWidth = (2*gv.yMotorMountHolePadding+
						gv.yMotorMountHoleDia+
						2*gv.yMotorShaftToMountHoleDistX)

#Determine zShaftToMountHoleDistX
gv.zShaftToMountHoleDistX = math.pow(math.pow(gv.zShaftToMountHoleDist,2)/2,0.5)


#Determine zMotorBodyWidth
gv.zMotorBodyWidth = (2*gv.zMotorMountHolePadding+
						gv.zMotorMountHoleDia+
						2*gv.zShaftToMountHoleDistX)


#Determine zMotor mount variables and zRodStandoff
if gv.zMotorMountLocation == "Top":
	gv.zRodStandoff = gv.zMotorBodyWidth/2
	gv.zMotorMountMountingFaceWidth = gv.frameHeight
	gv.zMotorMountLength = gv.zMotorMountMountingFaceWidth+gv.zRodStandoff+gv.zMotorBodyWidth/2
	gv.zMotorMountEdgeToShaftHole = gv.zMotorMountMountingFaceWidth + gv.zRodStandoff
	gv.zRodZScrewDist = (gv.zRodZScrewDist
						if gv.zRodZScrewDist
						> (gv.frameWidth+gv.zMotorMountPlateWidth)/2
						else (gv.frameWidth+gv.zMotorMountPlateWidth)/2)
if gv.zMotorMountLocation == "Bottom":
	gv.zRodStandoff = gv.zMotorMountPlateWidth/2					
	gv.zMotorMountMountingFaceWidth = gv.frameWidth		
	gv.zRodZScrewDist = (gv.zRodZScrewDist
						if gv.zRodZScrewDist
						> (gv.frameWidth+gv.zMotorBodyWidth+gv.zMotorBodyToFrameSpacing)/2
						else (gv.frameWidth+gv.zMotorBodyWidth+gv.zMotorBodyToFrameSpacing)/2)	
	gv.zMotorMountLength = gv.zMotorMountMountingFaceWidth/2+gv.zRodZScrewDist+gv.zMotorBodyWidth/2
	gv.zMotorMountEdgeToShaftHole = gv.zMotorMountMountingFaceWidth/2 + gv.zRodZScrewDist
					



#Determine zBushingNutMaxFaceToFace
gv.zBushingNutMaxFaceToFace = (gv.zBushingNutL[2] 
								if gv.zBushingNutL[2]
								> gv.zBushingNutR[2] 
								else gv.zBushingNutR[2])

#Determine the max Nut face to face for the xEndZRodHolder between zBushing nuts and lead Screw nuts
gv.xEndZRodHolderMaxNutFaceToFace = (gv.zBushingNutMaxFaceToFace if gv.zBushingNutMaxFaceToFace>gv.leadScrewNut[2] else gv.leadScrewNut[2])

#Determine xRodClampWidth
gv.xRodClampWidth = (gv.zRodZScrewDist
					+ gv.xEndZRodHolderMaxNutFaceToFace/math.cos(math.pi/6)
					+ 2*gv.bushingNutPadding)
#Determine zRod Spacing
gv.zRodSpacing = (gv.xRodLength 
			+ 2*gv.xRodClampWidth
			- 2*gv.xRodClampPocketDepth
			- 2*gv.bushingNutPadding
			- gv.xEndZRodHolderMaxNutFaceToFace/math.cos(math.pi/6)
			)





#Determine the max Nut Thickness for the xEndZRodHolder between both zBushingNuts and LeadScrewNuts
gv.xEndZRodHolderMaxNutThickness = (gv.zBushingNutMaxThickness if gv.zBushingNutMaxThickness>gv.leadScrewNut[3] else gv.leadScrewNut[3])

#Determine the height of the xEndZRodHolder
gv.xEndZRodHolderHeight = 2*(gv.xEndZRodHolderMaxNutThickness+gv.bushingNutPadding)+gv.xRodSpacing - gv.xRodDiaMax

#Determine printableWidth
gv.printableWidth = (gv.xRodLength
				- 2*gv.xRodClampPocketDepth
				- gv.xCarriageWidth/2
				- gv.xCarriageWingWidth)

#Determine yRodSupportWidth
gv.yRodSupportWidth = (gv.yRodDiaMax
				  + gv.clampHoleDia
				  + gv.clampNutFaceToFace
				  + 2*gv.clampNutPadding
				  + 4*gv.slotPadding
				  + 2*gv.slotDia
				  + 2*gv.slotWidth)

#Determine printBedBusingSupportWidth
gv.printBedBusingSupportWidth = (4*gv.slotPadding+
								2*gv.slotDia+
								2*gv.slotWidth+
								2*gv.bushingNutPadding+
								gv.PBBHMaxFaceToFace/math.cos(math.pi/6))


#Determine yRodSpacing
gv.yRodSpacing = ((gv.printableWidth + 2*gv.printBedPadding)/2
				if (gv.printableWidth + 2*gv.printBedPadding)/2
				> gv.yMotorMountPlateWidth + gv.yRodSupportWidth
				else gv.yMotorMountPlateWidth + gv.yRodSupportWidth)
#Check yRodSpacing to make sure that the Bushing supports can be attached to the print bed support
if gv.yRodSpacing+gv.printBedBusingSupportWidth > gv.printableWidth + 2*gv.printBedPadding:
	raise Exception("The yRods can't be spaced far enough apart. Try longer xAxis rods.")

#Determine the maximum thickness of the y axis bushings
gv.yBushingNutMaxThickness = (gv.yBushingNutL[3] 
			if gv.yBushingNutL[3]
			> gv.yBushingNutR[3] 
			else gv.yBushingNutR[3])

#Determine the depth of the y bushing mounts			
gv.PBBHDepth = gv.yBushingNutMaxThickness+gv.bushingNutPadding

#Determine center to center distance between the slots on the y bushing mounts
#This is the spacing used to determine the spacing between mounting holes on the print bed support
gv.yBushingMountSlotSpacing = (gv.PBBHMaxFaceToFace/math.cos(math.pi/6)
								+ 2*gv.bushingNutPadding
								+2*gv.slotPadding
								+gv.slotDia
								+gv.slotWidth)

#Determine the center to center distance between y bushing nuts along the y axis
#Increase printable area by changing the divisor. The price is a less stable print bed. 
gv.yBushingNutSeparation = (gv.yRodLength-2*gv.frameWidth)/3

#Determine the printable length
gv.printableLength = (gv.yRodLength
					-2*gv.frameWidth
					-gv.yBushingNutSeparation
					-gv.PBBHDepth)
					
#Determine the y belt anchor hole spacing
gv.yBeltAnchorHoleSpacing = (gv.yBeltAnchorLength
							+2*gv.mountToPrintedPadding
							+uf.adjustHole(gv.mountToPrintedDia))


#Determine the extruderMountPlateWidth
gv.extruderMountPlateWidth = (gv.xCarriageWidth if gv.xCarriageWidth > 
							gv.extruderWidth else gv.extruderWidth)


#Determine hotEndLength
gv.hotEndLength = gv.nozzleLength + gv.extruderBarrelLength


#Determine zEndStopClampLength
gv.zEndStopClampLength = (2*gv.mountToPrintedPadding
						+ gv.printedToPrintedDia
						+ 2*gv.xEndstopChannelWidth
						+ gv.xEndstopContactSpacing
						+ gv.xEndstopPadding
						+ gv.zEndstopJogWidth)


#Determine vertBarDistBelowZRod
gv.vertBarDistBelowZRod = (gv.yRodStandoff
						 + gv.PBBHStandoff
						 + gv.printBedSupportThickness
						 + gv.printBedStandoff
						 + gv.printBedThickness
						 + gv.hotEndLength
						 - (gv.extruderMountAngleWidth + gv.extruderMountAngleThickness)/2
						 - gv.xCarriageMountHoleVertOffset
						 + gv.xCarriageBushingHolderOR
						 - (gv.xEndZRodHolderHeight-gv.xRodSpacing)/2
						 - gv.zEndStopClampLength #May change to something fancier that incorporates the zOffset screw
						 - gv.zRodSupportLength)

#Determine vertBarDistAboveZRod
if gv.zMotorMountLocation == "Top":
	gv.vertBarDistAboveZRod = (gv.frameJointPadding + gv.frameWidth
								if gv.frameJointPadding + gv.frameWidth
								> gv.leadScrewCouplerLength + 2*gv.leadScrewCouplerGap	
								else gv.leadScrewCouplerLength + 2*gv.leadScrewCouplerGap)

elif gv.zMotorMountLocation == "Bottom":
	gv.vertBarDistAboveZRod = gv.frameJointPadding + 2*gv.slotPadding + gv.slotDia
	
#Determine the vertBarLength
gv.vertBarLength = gv.zRodLength + gv.vertBarDistAboveZRod + gv.vertBarDistBelowZRod

#Determine the cross bar length. Used for all cross bars.
gv.crossBarLength = gv.zRodSpacing + gv.frameWidth

#Determine yRodSupportMountHoleSpacing
gv.yRodSupportMountHoleSpacing = (gv.yRodDiaMax
								+ gv.clampHoleDia
								+ gv.clampNutFaceToFace
								+ 2*gv.clampNutPadding
								+ 2*gv.slotPadding
								+ gv.slotDia
								+ gv.slotWidth)
								
gv.sideBarLength = gv.yRodLength-2*gv.frameWidth

#Determine extruderNozzleStandoff which is the distance between the center of the nozzle and the face of the vertical bars
gv.extruderNozzleStandoff = (gv.zRodStandoff 
						+ gv.xEndZRodHolderMaxNutFaceToFace/2
						+ gv.xEndZRodHolderFaceThickness
						+ gv.xMotorMountPlateThickness
						+ gv.xRodClampOverallThickness/2
						+ gv.xCarriageBushingHolderOR
						+ gv.xCarriageThickness
						+ gv.extruderDepth
						- gv.extruderEdgeToCenterLine)

#Determine xRodAxisToMountHoleDist
gv.xRodAxisToMountHoleDist = (gv.xRodDiaMax/2 + gv.xRodClampMountHoleToRodPadding
							if gv.xRodDiaMax/2 + gv.xRodClampMountHoleToRodPadding
							> (gv.xEndZRodHolderMaxNutThickness
							+gv.bushingNutPadding
							+gv.xEndZRodHolderMountHoleToRodPadding
							+gv.printedToPrintedDia/2)
							else (gv.xEndZRodHolderMaxNutThickness
							+gv.bushingNutPadding
							+gv.xEndZRodHolderMountHoleToRodPadding
							+gv.printedToPrintedDia/2))

#Determine xEndstopLength
gv.xEndstopLength = gv.xEndstopPadding+ gv.mountToPrintedDia/2 +gv.xRodAxisToMountHoleDist			


#Determine xEndstopSupportWidth
gv.zEndstopSupportWidth = (gv.zRodDiaL
						+ 2*gv.printedToPrintedDia
						+ 2*gv.mountToPrintedPadding)

#Determine xEndstopBodyThickness
gv.zEndstopBodyThickness = (gv.zRodZScrewDist/2
						  + gv.xEndstopChannelDepth/2
						  -gv.zRodDiaL/2)

#determind xBeltAnchorHeight
gv.xBeltAnchorHeight = gv.xCarriageBushingHolderOR+gv.xRodClampOverallThickness/2+gv.xBeltAnchorBridgeThickness
#Draw parts, save and make assembly

del gv.xAxisParts[:]
del gv.yAxisParts[:]
del gv.zAxisParts[:]
	
#Make file for assembly
uf.makeAssemblyFile()

#Make components for x-Axis, add to assembly, save and close
xRodBottom.draw()
xRodBottom.assemble()
uf.saveAndClose("xRodBottom",False)
xRodTop.draw()
xRodTop.assemble()
uf.saveAndClose("xRodTop",False)
xCarriage.draw()
xCarriage.assemble()
uf.saveAndClose("xCarriage",True)
extruderMountAngle.draw()
extruderMountAngle.assemble()
uf.saveAndClose("extruderMountAngle", False)
extruderMountPlate.draw()
extruderMountPlate.assemble()
uf.saveAndClose("extruderMountPlate", False)
xRodClampL.draw()
xRodClampL.assemble()
uf.saveAndClose("xRodClampL",True)
xRodClampR.draw()
xRodClampR.assemble()
uf.saveAndClose("xRodClampR",True)
xEndMotorPlate.draw()
xEndMotorPlate.assemble()
uf.saveAndClose("xEndMotorPlate",False)
xEndIdlerPlate.draw()
xEndIdlerPlate.assemble()
uf.saveAndClose("xEndIdlerPlate",False)
extruderBarrel.draw()
extruderBarrel.assemble()
uf.saveAndClose("extruderBarrel",False)
nozzle.draw()
nozzle.assemble()
uf.saveAndClose("nozzle",False)
xEndZRodHolderL.draw()
xEndZRodHolderL.assemble()
uf.saveAndClose("xEndZRodHolderL",True)
xEndZRodHolderR.draw()
xEndZRodHolderR.assemble()
uf.saveAndClose("xEndZRodHolderR",True)
xEndstop.draw()
xEndstop.assemble()
uf.saveAndClose("xEndstop",True)
uf.saveAndClose("xEndstopCap",True)
 
 
uf.positionXAxis()
 
#Make components for ZAxis, add to assembly, save and close#
 
zRodL.draw()
zRodL.assemble()
uf.saveAndClose("zRodL",False)
zRodR.draw()
zRodR.assemble()
uf.saveAndClose("zRodR",False)
zRodSupportR.draw()
zRodSupportR.assemble()
uf.saveAndClose("zRodSupportR",True)
uf.saveAndClose("zRodSupportRClamp",True)
zRodSupportL.draw()
zRodSupportL.assemble()
uf.saveAndClose("zRodSupportL",True)
uf.saveAndClose("zRodSupportLClamp",True)
zMotorMount.draw()
zMotorMount.assemble()
uf.saveAndClose("zMotorMount",True)
zEndstop.draw()
zEndstop.assemble()
uf.saveAndClose("zEndstop",False)

uf.positionZAxis()


#Make components for yAxis, add to assembly, save and close#

yRodL.draw()
yRodL.assemble()
uf.saveAndClose("yRodL",False)
yRodR.draw()
yRodR.assemble()
uf.saveAndClose("yRodR",False)
PBBHR.draw()
PBBHR.assemble()
uf.saveAndClose("printBedBushingHolderR",True)
PBBHL.draw()
PBBHL.assemble()
uf.saveAndClose("printBedBushingHolderL",True)
yBeltAnchor.draw()
yBeltAnchor.assemble()
uf.saveAndClose("yBeltAnchor",True)
printBedSupport.draw()
printBedSupport.assemble()
uf.saveAndClose("printBedSupport",False)
printBed.draw()
printBed.assemble()
uf.saveAndClose("printBed",False)
yMotorMount.draw()
yMotorMount.assemble()
uf.saveAndClose("yMotorMount", True)
yRodSupportR.draw()
yRodSupportR.assemble()
uf.saveAndClose("yRodSupportR", True)
uf.saveAndClose("yRodSupportRClamp", True)
yRodSupportL.draw()
yRodSupportL.assemble()
uf.saveAndClose("yRodSupportL", True)
uf.saveAndClose("yRodSupportLClamp", True)


#Make components for frame, add to assembly, save and close
verticalBars.draw()
verticalBars.assemble()
uf.saveAndClose("verticalBars", False)
crossBarTop.draw()
crossBarTop.assemble()
uf.saveAndClose("crossBarTop", False)
crossBarFrontTop.draw()
crossBarFrontTop.assemble()
uf.saveAndClose("crossBarFrontTop", False)
crossBarFrontBottom.draw()
crossBarFrontBottom.assemble()
uf.saveAndClose("crossBarFrontBottom", False)
crossBarBackTop.draw()
crossBarBackTop.assemble()
uf.saveAndClose("crossBarBackTop", False)
crossBarBackBottom.draw()
crossBarBackBottom.assemble()
uf.saveAndClose("crossBarBackBottom", False)
sideBarTopL.draw()
sideBarTopL.assemble()
uf.saveAndClose("sideBarTopL", False)
sideBarBottomL.draw()
sideBarBottomL.assemble()
uf.saveAndClose("sideBarBottomL", False)
sideBarBottomR.draw()
sideBarBottomR.assemble()
uf.saveAndClose("sideBarBottomR", False)
sideBarTopR.draw()
sideBarTopR.assemble()
uf.saveAndClose("sideBarTopR", False)
frameSpacers.draw()
frameSpacers.assemble()
uf.saveAndClose("frameSpacers", False)

App.ActiveDocument=App.getDocument("PrinterAssembly")
Gui.ActiveDocument=Gui.getDocument("PrinterAssembly")

uf.saveAssembly()

if(gv.plate):
    plate.plate()

if(gv.slic3r):
    slic3r.slic3r()

zipup.zipup()