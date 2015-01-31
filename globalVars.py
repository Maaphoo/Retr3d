from __future__ import division # allows floating point division from integersimport math

reloadClasses = False

#file handeling
parentDir = "Z:/Design Files/SalvagePrinter/"

#make test hole pattern. True if you would like the test hole pattern to be included in your stl files
printTestHolePattern = True

#xRod vars
xRodDiaTop = 8.01 #Diameter of the top xRod
xRodDiaBottom = 6.99 #Diameter of the bottom xRod
xRodLength = 334 # Length of the shorter xRod
xRodDiaMax = None 					#CALCULATED The largest xRod diameter
xMotorShaftToMountHoleDistX = None 	#CALCULATED The horizontal component of the distance between the shaft and the mounting holes
xMotorBodyWidth = None 				#CALCULATED Width of the xMotor's body
									#xRodSpacing note: Should be changed to purely CALCULATED
xRodSpacing = 2*25.4 					#SEMI-CALCULATED The distance between the axes of the xRods. It is automatically increased if needed


#yRod vars
yRodDiaL = 8.22 #Diameter of the top yRod
yRodDiaR = 7.94 #Diameter of the bottom yRod
yRodLength = 420 # Length of the shorter yRod
yRodSpacing = None	#CALCULATED Distance between yRods
yRodDiaMax = None 	#CALCULATED largest yRod diameter


#zRod vars
zRodDiaR = 8.0 #Diameter of the right zRod
zRodDiaL = 7.96 #Diameter of the left zRod
zRodLength = 355 #Length of the shorter zRod
zRodSpacing = None	#CALCULATED Distance between zRod axes
zRodStandoff = None	#CALCULATED Distance between frame surface and zRod Axis


#Lead Screw Related
leadScrewDia = 6 #Diameter of the leadScrew
zRodZScrewDist = None #SEMI-CALCULATED Distance between the axis of the zRod and the axis of the LeadScrew. Increased if needed


#Frame vars
frameWidth = 19.77 #Width of frame members on the face to which the y and z axes are attached.
frameHeight = 20.06 #Height of frame members. This is the 2nd cross sectional dimension
frameThickness = 1.33 #Thickness of frame wall if frame is hollow.
frameJointPadding = 10 # Required distance at frame joints for welds which might get in the way of mounted parts


#Mounting nut and bolt info
mountToPrintedDia = 3 #Actual diameter of holes that are used to mount items to printed parts. IE other printed parts or sheet metal.
mountToFrameDia = 3 #Actual diameter of holes that are used to mount items to the frame. Printed parts to frame or sheet metal to frame.
mountToPrintedPadding = 3# the minimum distance between the edge of a hole and the edge of the part
printedToFrameDia = None #CALCULATED The adjusted diameter for printed parts that will be mounted to the frame.
printedToPrintedDia = None #CALCULATED The adjusted diameter for printed parts mounted to other printed parts or to non frame parts


#rodClamps - much of this should be combined with mounting bolt info above
clampHoleDia = 3.5 #Diameter of clamping holes on rod clamps and endStop mounts
clampNutPadding = 3 # The minimum wall thickness for the clamp nut cut out
clampNutFaceToFace = 5.6 #Face to face distance of clamp nuts
clampNutThickness = 2.5 #The thickness of the clamp nuts
clampGap = 2 # The gap between the support and the clamp
clampThickness = 3 # The clamp thickness on rod clamps
clampBoltHeadThickness = 3 #The thickness of the head of the clamp bolts
rodSupportNutTrapDepthMin = 5 #The minimum value the rod support nut trap depth can take
rodSupportNutTrapDepthMax = 10 #the maximum value the rod support nut trap depth can take
#rodSupportNutTrapDepth = 5 #CALCULATED The depth of the nut traps on the rod supports
rodSupportClampThickness = 2 # The thickness of plastic below the rod that is clamped. Basically the clamping thickness but in the support.


#mounting tabs - much of this should be combined with mounting bolt info above
#SlotDia should be printedToFrameDia
slotDia = 3.5 # The diameter of the mounting slots
tabThickness = 3 # The thickness of the mounting tabs
slotWidth = 3 # The width of the mounting slots
slotPadding = 3 # Amount of material to sides of slot


#PrintBedRelated
printBedPadding = 5 #extra space around the perimiter of the printBed that is not printable. 
printBedMountHoleDia = 3 #Diameter of mounting bolts
printBedMountHolePadding = 1.55 #Distance from edge of print bed to edge of mounting hole
printBedThickness = 1.5 #Thickness of heated print bed plate
printBedStandoff = 10 #The distance between the top of the print bed support and the print bed
printableWidth = None	#CALCULATED printable dimension in the x direction
printableLength = None	#CALCULATED printable dimension in the y direction
printableHeight = None	#CALCULATED printable dimension in the z direction


#PrintBedSupport related
printBedSupportThickness = 1.55 #The thickness of the printBedSupport plate


#xRodClamp
xRodClampThickness = 3 #Thickness of plastic around the largest diameter rod
xRodClampPocketDepth = 25 #Distance the xRods are inserted into the xRodClamp
xRodClampMountHoleToEdgePadding = 3 #Distance from side of xRodClamp to mountHole edge(ie not center)
xRodClampMountHoleToRodPadding = 1.5  # The vertical distance from the edge of the largest xRod to the edges of the mounting holes
xRodClampEdgeToMountHoleDist = 4.75 #Distance from xRodClamp side to mounting holes
xRodClampIdlerHoleDia = 3.5 #The diameter of the xRodClamp idler hole
xRodClampMountHoleToRodPadding = 1.5
xRodClampExtraPocketDepth = 3 #Extra distance in the pocket as an allowance.
xRodClampWidth = None				#CACLULATED Width of the xRodClamp
xRodClampOverallThickness = None	#CALCULATED The thickness of the xRodClamp
xRodAxisToMountHoleDist = None		#CALCULATED Distance from x Rod axis to mount hole centers in vertical direction


#xEndMotorPlate
xEndIdlerHoleDia = 3 #Diameter of idler hole (as apposed to printed which is larger)
xMotorMountPlateThickness = 3.175 #The thickness of the xMotorMountPlate (idler plate too)
xEndNumMountHoles = 4 # The number of motor mount holes on the xEnd motor
xEndShaftToMountHoleDist = 21.92 #The distance from the shaft to the mount holes
xEndMotorMountHoleDia = 3 # the x motor mount hole diameter
xEndMotorMountHolePadding = 4.39 #The distance between the motor mount holes and the edge of the plate
motorToXRodClampSpacing = 2 # The gap between the xEnd motor and the xRodClamp
xMotorPulleyDia = 12.07 # The diameter of the xMotor Pully


#xEndZRodHolder
xEndZRodHolderFaceThickness = 3 #The thickness of the face of the xEndZRodHolder
xEndZRodHolderMountHoletoEdgePadding = 3 #horizontal distance from edge of xEndZRodHolder to the edges of mounting holes
xEndZRodHolderMountHoleToRodPadding = 1.5 #The vertical distance from the edge of the largest xRod to the edges of the mounting holes
#The above should be consolidated with the xRodClampEdgeToMountHoleDist and xRodAxisToMountHoleDist
zOffsetNutThickness = 3 #The thickness of the zOffsetNut
zOffsetNutFaceToFace = 5.6 #The face to face distance of the zOffsetNut
zOffsetHoleDia = 3.5 #The hole diameter of the xOffSet bolt
zBushingNutMaxFaceToFace = None			#CACLULATED The max Face to face distance between the two z bushing nut sizes
zBushingNutMaxThickness = None			#CACLULATED The max thickness for the z Bushing nuts
xEndZRodHolderMaxNutThickness = None	#CACLULATED The max nut thickness for the xEndZRodHolder
xEndZRodHolderMaxNutFaceToFace = None	#CACLULATED The max Nut face to face for the xEndZRodHolder
xEndZRodHolderHeight = None				#CACLULATED The height of the xEndZRodHolder


#xCarriage
xCarriageWidth = 50 #The width of the xCarriage not including wings
xCarriageThickness = 6 #The thickness of the xCarriage face
xBeltAnchorThickness = 6 #The thickness of the belt anchor
xBeltAnchorSlotWidth = 6 #The width of the slot in the belt anchor
xBeltAnchorSlotInset = 6 # The distance from the edge of the anchor to the slot
xBeltAnchorBridgeThickness = 3 #The thickness of the belt anchor bridge 
xCarriageWingWidth = 10 #The width of the xCarriage wings
xCarriageWingHeight = 10 #The height of the xCarriage wings
xBeltAnchorWidthTop = 18 				#Should be CALCULATED - The width of the top of the belt anchor
xBeltAnchorWidthBottom = 20				#Should be CALCULATED - The width of the bottom of the belt anchor
xCarriageMountHoleVertOffset = 15 		#Should be CALCULATED - The distance from the bottom edge of the face to the extruder mounting holes
xCarriageMountHoleHorizOffset = 4.75	#Should be CALCULATED - The distance from the side of the xCarriage and the extruder mounting holes
xBushingNutMaxFacetoFace = None	#CALCULATED The maximum xBushing nut face to face distance
xBushingNutMaxThickness = None	#CALCULATED The maximum bushing nut thickness for the x axis
xCarriageBushingHolderOR = None	#CALCULATED the bushing holder outside radius on the x carriage
xBeltAnchorHeight = None		#CALCULATED The height of the belt anchor from the back of the xCarriage face


#zMotorMount vars
zMotorMountHoles = 4 #The number of motor mounting holes
zShaftToMountHoleDist = 21.92 #the distance between the shaft and the mounting holes
zMotorMountHoleDia = 3	#the diameter of the motor mounting holes
zMotorMountHolePadding = 4.39 # the minimum space between the edge of the motor mounting holes and the edge of the plate
zMotorMountPlateThickness= 3.41 #The thickness of the z motor mount plate
zMotorMountPlateWidth= 38.17 #Width of motor mount plate
zMotorMountShaftHoleDia = 8 #Diameter of the shaft hole in the zMotorMount.
zMotorMountLocation = "Bottom" #The location of the zMotorMounts. Either Top or Bottom
zMotorMountLength = None 			#CALCULATED The length of the z motor mount plate
zMotorMountMountingFaceWidth = None	#Calculated The width of the frame member to which the z motor mount is attached
zMotorMountEdgeToShaftHole = None 	#CALCULATED The distance from the frame side edge of the motor mount to the shaft hole center
zShaftToMountHoleDistX = None 		#Calculated
zMotorBodyWidth = None 				#CALCULATED Width of the zMotorBody

#yMotorMount vars
yShaftToMountHoleDist = 21.92 #the distance between the shaft and the mounting holes
yMotorMountHolePadding = 4.39 #The distance between the edge of the motor and the edge of the motor mount holes
yMotorMountHoleDia = 3 # Dia of the y motor mount holes
yMotorMountPlateWidth = 2*25.4 # The width of the y motor mount plate
yMotorMountPlateThickness = 3.175
yMotorMountShaftHoleDia = 10 #The diameter of the shaft hole for the y motor mount
yMotorMountHoles = 4 # The number of motor mounting holes for the y motor
yMotorPulleyDia = 12.075 #The diameter of the y motor pulley
yMotorShaftToMountHoleDistX = None	#CALCULATED The x component of the distance from the shaft to the mount hole
yMotorBodyWidth = None				#CALCULATED The width of the y motor body


#zRodSupport vars
zRodSupportLength = 15 # The length of the zrod that is supported


#YRodSupport vars
yRodSupportClearance = 3 #The clearance between the top of the clamping bolts and the bottom of the printBedSupport.
yRodSupportWidth = None				#CALCULATED The total width of the Rod Support including tabs.
yRodStandoff = None					#CALCULATED The distance from the top of the frame to the yRod axis
yRodSupportMountHoleSpacing = None	#CALCULATED The center to center distance for the yRodSupport mounting holes. Middle of slot to middle of slot
yRodSupportClampBoltLength = None	#CALCULATED The length of the clamping bolts used for the yRodClamps
yRodSupportNutTrapDepth = None #CALCULATED The depth of the nut traps on the rod supports


#yBeltAnchor
yBeltAnchorWidth = 6 #The width of the belt anchor column
yBeltAnchorLength = 24 #The length of the belt anchor Column
yBeltAnchorBridgeThickness = 3 #The thickness of the y belt anchor bridge
yBeltAnchorSlotWidth = 6 # The width of the y belt anchor slot
yBeltAnchorHoleSpacing = None	#CALCULATED Center to center distance between yBeltAnchorHoles
yBeltAnchorHeight = None		#CALCULATED The total height (including tab thickness) of the y belt anchor


#extruderMountPlate vars
extruderMountPlateThickness = 1.55 #The thickness of the extruderMountPlate
hotEndMountHoleDia = 3 #The diameter of the hot end mounting holes
extruderMountPlateWidth = None	#CALCULATED The width of the extrtuder mount plate 


#extruderMountAngle vars
extruderMountAngleWidth = 19 # The width of the angle used
extruderMountAngleThickness = 3.1 # The thickness of the angle used


#extruder vars
extruderWidth = 78 #The width of the extruder body
extruderDepth = 60 # The required depth for mounting the extruder front edge of body to back most part of extruder
extruderMountHoleSpacing = 48 #The distance between the extruder's mounting holes
extruderMountHoleDia = 3 #The diameter of the extruder's mounting holes
extruderFilamentHoleDia = 4 #The diameter of extruder's filament hole
extruderEdgeToCenterLine = 14 #The distance from the outer edge of the extruder to it's center line
extruderNozzleStandoff = None	#CALCULATED The distance from the center of the nozzle to the face of the vertical bars


#extruderBarrel vars
extruderBarrelDia = 1*25.4 #Diameter of the extruder barrel
extruderBarrelLength = 42 #The length of the extruderBarrel
extruderBarrelLinerDia = 1/4*25.4 #The diameter of the teflon barrel liner
extruderBarrelNumFins = 7 #The number of cooling fins not including the top and bottom faces.
extruderBarrelFaceThickness = 3 #The thickness of the top and bottom faces
extruderBarrelCoreThickness = 1.5 #The thickness of metal around the barrel liner
extruderBarrelFinGap = 1/8*25.4 #The space between fins
extruderBarrelMountHoleDia = 2.5 #Diameter of mounting holes for extruder barrel. 2.5mm hole will be tapped to 3mm
extruderBarrelMountHoleDepth = 10 #the depth of the mounting holes. 
hotEndMountHoleSpacing = 20 # The center to center distance between the hot end mounting holes


#nozzle vars
nozzleBodyHeight = 10 #The height of the nozzle body
nozzleBodyWidth = 19.05 #The width of the nozzle body
nozzleBodyDepth = 12.7 #The depth of the nozzle body
nozzleResistorDia = 6.5 #The diameter of the heater resistor
nozzleResistorInset = 5 #The distance between the axis of the resistor and the outer edge of the heater block
nozzleThermistorDia = 1.5 #The diameter of the Thermistor bead
nozzleThermistorDepth = 3 #The depth of the thermistor mount hole
nozzleThermistorRetainerDia = 2.5 #The diameter of the thermistor retainer screw
nozzleThermistorRetainerDepth = 5 #The depth of the thermistor retainer hole
nozzleDia = .4 #The diameter of the nozzle
nozzleBaseDia = 8.35 #The diameter of the nozzle base
nozzleStepDia = 3 #The diameter of the step down from the barrel liner. This should be just a bit larger than the filament diameter
nozzleStepOffset = 1 #The distance from the tip of the setp hole to the tip of the nozzle
nozzleDrillAngle = 118 #The drill point angle of the drill bits used
nozzleTipDia = 1 #The diameter of the flat surrounding the nozzle's hole
nozzleThermistorHoleVertOffset = 2 #The distance from the lower edge of the heater block to the center of the thermistor hole.
nozzleThermistorRetainerHorizOffset = 3 #The distance from the outer edge of the heater block to the center of the retainer hole.
nozzleLength = 15	#CALCULATED The total length of the nozzle


#hotEnd vars
hotEndLength = None #CALCULATED The total length of the hot end from the nozzle to the top of the barrel


#Cross bar vars
yBeltIdlerHoleDia = 3 #The diameter of the hole for the yBeltIdler
crossBarLength = None #CALCULATED The length of the cross bars


#Side bar vars
sideBarLength = None #CALCULATED The length of the side bars


#frameSpacer vars
#frameSpacerLength should be calculated depending on the power supply thickness, electronics or motors
frameSpacerLength = 47 # The length of the frameSpacers
frameSpacerOffset = 10 # The distancebetween the end of the sideBar to the edge of the frameSpacer


#xEndstop vars
xEndstopHeight = 4.5 # The height of the body of the endstop
xEndstopContactSpacing = 3 # The distance between the contact strips. Surface to surface not center to center
xEndstopChannelWidth = 0.5 # The width of the channels for the metal contact strips
xEndstopChannelDepth = 3 #The depth of the channels for the metal contact strips
xEndstopPadding = 1.5 # The minimum distance between the edge of a feature (hole or channel) and the edge of the endstop
xEndstopCapThickness = 2 #The thickness of the endstop cap
xEndstopLength = None	#CALCULATED The length of the body of the endstop


#zEndStop vars
zEndstopJogWidth = 2 #The width of the jog used to trap the contacts
zEndstopSupportWidth = None		#CALCULATED The width of the zEndstop
zEndStopClampLength = None		#CALCULATED The length along the z axis of the zEndStop clamp
zEndstopBodyThickness = None 	#CALCULATED The thickness of the zEndstop between the zRod and the zEndStopCap

#LeadScrewCoupler vars
leadScrewCouplerLength = 25 #The length (vertical axis) of the leadScrewCouplers
leadScrewCouplerGap = 5 #The space above and below the leadScrewCoupler. For keeping the coupler from  crashing into zMotor mount plate or xCarriage

#Hole Calibration table
#small hole diameters are adjusted for printed parts using this array.
holeAdjust = [[1,0],
			  [2,1.38],
			  [3,2.44],
			  [4,3.53],
			  [5,4.45],
			  [6,5.6],
			  [7,6.7],
			  [8,7.6],
			  [9,8.64],
			  [10,9.5],
			  [11,10.64],
			  [12,11.6]]


#bushing nut lookup related
bushingNutSizesUsed = "Standard" # The type of bushing nuts used in the printer, standard, metric or standardAndMetric
bushingNutTable = [] #The table of bushing nuts used to build the printer.


#Standard Nut Sizes [Thread dia, Minor dia, Face to face, Thickness] in inches (will be converted)
standardNuts = [[0.1120, 0.0939, 1/4 , 3/32], #4
				[0.1380, 0.1140, 5/16 , 7/64], #6
				[0.1640, 0.1390, 11/32, 1/8], #8
				[0.1900, 0.1560, 3/8 , 1/8],#10
				[0.2160, 0.181, 7/16, 5/32], #12
				[1/4, 0.2070, 7/16, 7/32],
				[5/16,0.2650, 1/2, 17/64],
				[3/8, 0.321, 9/16, 21/64],
				[7/16,0.376, 11/16, 3/8],
				[1/2,0.434, 3/4, 7/16],
#				[9/16,0.490, 7/8, 31/64],	#commented out because this size is uncommon
				[5/8,0.546, 15/16, 35/64]
				]


#Metric Nut Sizes [Thread dia, Minor dia, Face to face, Thickness] in mm
metricNuts =   [[2.5, 1.993, 5, 2],
				[3,2.439, 5.5, 2.4],
#				[3.5, 2.829, 6, 2.8], #NOT COMMON
				[4, 3.220, 7, 3.2],
				[5, 4.110, 8, 4],
				[6, 4.891, 10, 5],
				[8, 6.619, 13, 6.5],
				[10, 8.344, 17, 8],
				[12, 10.072, 19, 10],
				[14, 11.797, 22, 11],
				[16, 13.797, 24, 13]
				]


#Lengths of bolts available
standardBoltLengths = [.5, .75, 1, 1.25, 1.5, 2] #in inches (will be converted to mm)
metricdBoltLengths = [10,12,16,20,25,30,35,40]
clampBoltLengths = [10,12,16,20,25,30,35,40]

#BushingNut and leadScrew related
bushingNutPadding = 3 # minimum thickness of holder around nut and thickness of depth stop
bushingNutRodGap = 1 #extra radius in the hole for the smooth rod
xBushingNutBottom = None	#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia
xBushingNutTop = None 		#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia
yBushingNutR = None			#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia
yBushingNutL = None			#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia
zBushingNutR = None			#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia
zBushingNutL = None			#CALCULATED Bushing nut dimensions selected from the nut tables depends on rod dia
leadScrewNut = None			#CALCULATED Leas screw nut dimensions selected from the nut tables depends on screw dia


#Colors colors are in % RGB
printedR = 255/255
printedG = 253/255
printedB = 232/255
printedA = 0.0 #doesn't seem to do anything!!!

frameR = 0/255
frameG = 0/255
frameB = 156/255
frameA = 0.0 #doesn't seem to do anything!!!


#Verticle Bar vars
vertBarDistAboveZRod = None #CALCULATED The distance from the top of the zRods to the top edge of the vertical bar
vertBarDistBelowZRod = None #CALCULATED The distance from the bottom of the zRods to the bottom edge of the vertical bar
vertBarLength = None #CALCULATED The length of the vertical bar


#Parts lists
xAxisParts = []
yAxisParts = []
zAxisParts = []