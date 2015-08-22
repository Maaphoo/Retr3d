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

from __future__ import division # allows floating point division from integersimport math

reloadClasses = False
test = None

#Change the following to the path to the directory that will hold your printer designs
#Unless using windows, then use \\ instead of either of the above
#Make sure to use forward slashes like this / and not back slashes like this \ 
freecadDir = "/Path/To/FreeCAD/"
printerDir = "/Path/To/Store/3D/Files/"
 
#Output Options
level = 2

#make test hole pattern. True if you would like the test hole pattern to be included in your stl files
printTestHolePattern = True
 
#xRod vars
xRodDiaTop = 7.9 #Diameter of the top xRod
xRodDiaBottom = 7.9 #Diameter of the bottom xRod
xRodLength = 400 # Length of the shorter xRod
xRodDiaMax = None 					#CALCULATED The largest xRod diameter
xMotorShaftToMountHoleDistX = None 	#CALCULATED The horizontal component of the distance between the shaft and the mounting holes
xMotorBodyWidth = None 				#CALCULATED Width of the xMotors body
xRodSpacing = None 					#CALCULATED The distance between the axes of the xRods. 
 
#yRod vars
yRodDiaL = 12.7 #Diameter of the top yRod
yRodDiaR = 12.7 #Diameter of the bottom yRod
yRodLength = 460 # Length of the shorter yRod
yRodSpacing = None	#CALCULATED Distance between yRods
yRodDiaMax = None 	#CALCULATED largest yRod diameter
yBushingNutMaxThickness = None #Calculated The maximum thickness of the y bushing nuts
                                                                                            
#zRod vars                                                                                  
zRodDiaR = 12.7 #Diameter of the right zRod                                                   
zRodDiaL = 12.7 #Diameter of the left zRod                                                 
zRodLength = 460 #Length of the shorter zRod                                                
zRodSpacing = None	#CALCULATED Distance between zRod axes                               
zRodStandoff = None	#CALCULATED Distance between frame surface and zRod Axis             
 
#Lead Screw Related                                                                                                                                                        
leadScrewDia = 6.35 #Diameter of the leadScrew                                                                                                                             
zRodZScrewDist = None #CALCULATED Distance between the axis of the zRod and the axis of the LeadScrew. Increased if needed                                                 
                                                                                                                                                                           
                                                                                                                                                                           
#Frame vars                                                                                                                                                                
frameWidth = 20 #Width of frame members on the face to which the y and z axes are attached.                                                                                
frameHeight = 19.05#Height of frame members. This is the 2nd cross sectional dimension                                                                                    
frameThickness = 1.33 #Thickness of frame wall if frame is hollow.                                                                                                         
frameJointPadding = 10 #ADVANCED Required distance at frame joints for welds which might get in the way of mounted parts                                                   
                                                                                                                                                                           
                                                                                                                                                                           
#Mounting nut and bolt info                                                                                                                                                
mountToPrintedDia = 3 #Actual diameter of holes that are used to mount items to printed parts. IE other printed parts or sheet metal.                                      
mountToFrameDia = 4.12 #Actual diameter of holes that are used to mount items to the frame. Printed parts to frame or sheet metal to frame.                                
mountToFrameHeadDia = 6         #Actual head diameter of bolts used to mount items to the frame.
mountToFrameHeadThickness = 3   #Actual head Thickness of bolts used to mount items to the frame.
mountToPrintedPadding = 3	#ADVANCED the minimum distance between the edge of a hole and the edge of the part                                                          
printedToFrameDia = None 	#CALCULATED The adjusted diameter for printed parts that will be mounted to the frame.                                                      
printedToFrameHeadDia = None    #CALCULATED The adjusted diameter for printed parts that will be mounted to the frame.                                                     
printedToPrintedDia = None 	#CALCULATED The adjusted diameter for printed parts mounted to other printed parts or to non frame parts                                    
                                                                                                                                                                           
                                                                                                                                                                           
#rodClamps - much of this should be combined with mounting bolt info above                                                                                                 
clampHoleDia = 3.5 				#ADVANCED Diameter of clamping holes on rod clamps and endStop mounts                                                       
clampNutPadding = 3 			#ADVANCED The minimum wall thickness for the clamp nut cut out                                                                      
clampNutFaceToFace = 5.6 		#ADVANCED Face to face distance of clamp nuts                                                                                       
clampNutThickness = 2.5 		#ADVANCED The thickness of the clamp nuts                                                                                           
clampGap = 2 					#ADVANCED The gap between the support and the clamp                                                                         
clampThickness = 3 				#ADVANCED The clamp thickness on rod clamps                                                                                 
clampBoltHeadThickness = 3 		#ADVANCED The thickness of the head of the clamp bolts                                                                              
rodSupportNutTrapDepthMin = 5 	#ADVANCED The minimum value the rod support nut trap depth can take                                                                         
rodSupportNutTrapDepthMax = 10 	#ADVANCEDthe maximum value the rod support nut trap depth can take                                                                  
#rodSupportNutTrapDepth = 5 	#CALCULATED The depth of the nut traps on the rod supports                                                                                  
rodSupportClampThickness = 2 	#ADVANCED The thickness of plastic below the rod that is clamped. Basically the clamping thickness but in the support.                      
                                                                                                                                                                           
                                                                                                                                                                           
#mounting tabs - much of this should be combined with mounting bolt info above                                                                                             
#SlotDia should be printedToFrameDia                                                                                                                                       
slotDia = 4.55 		#ADVANCED The diameter of the mounting slots                                                                                                
tabThickness = 4 	#ADVANCED The thickness of the mounting tabs                                                                                                        
slotWidth = 3.5		#ADVANCED The width of the mounting slots                                                                                                   
slotPadding = 3 	#ADVANCED Amount of material to sides of slot                                                                                                       
                                                                                                                                                                           
                                                                                                                                                                           
#PrintBedRelated                                                                                                                                                           
printBedMountHoleDia = 3 #Diameter of mounting bolts                                                                                                                       
printBedThickness = 1.5 #Thickness of heated print bed plate                                                                                                               
printBedPadding = 5 			#ADVANCED extra space around the perimiter of the printBed that is not printable.                                                   
printBedMountHolePadding = 1.5 	#ADVANCED Distance from edge of print bed to edge of mounting hole                                                                  
printBedStandoff = 10 			#ADVANCED The distance between the top of the print bed support and the print bed                                                   
printableWidth = None			#CALCULATED printable dimension in the x direction                                                                                  
printableLength = None			#CALCULATED printable dimension in the y direction                                                                                  
printableHeight = None			#CALCULATED printable dimension in the z direction                                                                                  
                                                                                                                                                                           
#printBedBushingHolder related                                                                                                                                             
PBBHStandoff = None #Calculated The distance from the bottom of the printBedSupport to the axis of the yRod                                                                
printBedBusingSupportWidth = None #The width of the printBedBushingSupport                                                                                                 
PBBHMaxFaceToFace = None                                                                                                                                                  
PBBHDepth = None #CALCULATED the depth of the printBedBushingHolder                                                                                                        
                                                                                                                                                                           
#PrintBedSupport related                                                                                                                                                   
printBedSupportThickness = 1.55 #The thickness of the printBedSupport plate                                                                                                
yBushingNutSeparation = None #Calculated the distance between bushing nuts on the same rod                                                                                 
                                                                                                                                                                           
#xRodClamp                                                                                                                                                                 
xRodClampIdlerHoleDia = 3.5 #The diameter of the xRodClamp idler hole                                                                                                      
xRodClampThickness = 3.5 				#ADVANCED Thickness of plastic around the largest diameter rod
xRodClampPocketDepth = 25 				#ADVANCED Distance the xRods are inserted into the xRodClamp                                                        
xRodClampMountHoleToEdgePadding = 3 	#ADVANCED Distance from side of xRodClamp to mountHole edge(ie not center)                                                          
xRodClampMountHoleToRodPadding = 1.5	#ADVANCED The vertical distance from the edge of the largest xRod to the edges of the mounting holes                                
xRodClampEdgeToMountHoleDist = 4.75 	#ADVANCED Distance from xRodClamp side to mounting holes.THIS SHOULD BE CHANGED TO PADDING                                          
xRodClampMountHoleToRodPadding = 1.5 	#ADVANCED                                                                                                                           
xRodClampExtraPocketDepth = 3 			#ADVANCED Extra distance in the pocket as an allowance.                                                                     
xRodClampWidth = None					#CACLULATED Width of the xRodClamp                                                                                  
xRodClampOverallThickness = None		#CALCULATED The thickness of the xRodClamp                                                                                  
xRodAxisToMountHoleDist = None			#CALCULATED Distance from x Rod axis to mount hole centers in vertical direction                                            
                                                                                                                                                                           
                                                                                                                                                                           
#xEndMotorPlate                                                                                                                                                            
xEndIdlerHoleDia = 3 #Diameter of idler hole (as apposed to printed which is larger)                                                                                       
xMotorMountPlateThickness = 3.175 #The thickness of the xMotorMountPlate (idler plate too)                                                                                 
xMotorMountPlateWidth = 50.8 #The width of the xMotorMountPlate                                                                                                            
xEndNumMountHoles = 4 # The number of motor mount holes on the xEnd motor                                                                                                  
xEndShaftToMountHoleDist = 21.92 #The distance from the shaft to the mount holes                                                                                           
xEndMotorMountHoleDia = 3 # the x motor mount hole diameter                                                                                                                
xEndMotorMountHolePadding = 4.4 #The distance between the motor mount holes and the edge of the plate                                                                      
xMotorPulleyDia = 12.1  # The diameter of the xMotor Pully                                                                                                                 
motorToXRodClampSpacing = 12 #ADVANCED The gap between the xEnd motor and the xRodClamp                                                                                    
                                                                                                                                                                           
                                                                                                                                                                           
#xEndZRodHolder                                                                                                                                                            
xEndZRodHolderFaceThickness = 3  #The thickness of the face of the xEndZRodHolder                                                                                           
xEndZRodHolderMountHoletoEdgePadding = 3 #horizontal distance from edge of xEndZRodHolder to the edges of mounting holes                                                   
xEndZRodHolderMountHoleToRodPadding = 1.5 #The vertical distance from the edge of the largest xRod to the edges of the mounting holes                                      
#The above should be consolidated with the xRodClampEdgeToMountHoleDist and xRodAxisToMountHoleDist                                                                        
zOffsetNutThickness = 3 #The thickness of the zOffsetNut                                                                                                                   
zOffsetNutFaceToFace = 5.6 #The face to face distance of the zOffsetNut                                                                                                    
zOffsetHoleDia = 3.5 #The hole diameter of the xOffSet bolt                                                                                                                
zMotorBodyToFrameSpacing = 5 			#ADVANCED The space between the zMotor and the frame.                                                                       
zBushingNutMaxFaceToFace = None			#CACLULATED The max Face to face distance between the two z bushing nut sizes                                       
zBushingNutMaxThickness = None			#CACLULATED The max thickness for the z Bushing nuts                                                                        
xEndZRodHolderMaxNutThickness = None	#CACLULATED The max nut thickness for the xEndZRodHolder                                                                            
xEndZRodHolderMaxNutFaceToFace = None	#CACLULATED The max Nut face to face for the xEndZRodHolder                                                                         
xEndZRodHolderHeight = None				#CACLULATED The height of the xEndZRodHolder                                                                        
                                                                                                                                                                           
#xCarriage                                                                                                                                                                 
xCarriageWidth = 65 					#ADVANCED The width of the xCarriage not including wings                                                            
xCarriageThickness = 6 					#ADVANCED The thickness of the xCarriage face                                                               
xBeltAnchorThickness = 6 				#ADVANCED The thickness of the belt anchor                                                                          
xBeltAnchorSlotWidth = 6 				#ADVANCED The width of the slot in the belt anchor                                                                  
xBeltAnchorSlotInset = 6 				#ADVANCED The distance from the edge of the anchor to the slot                                                      
xBeltAnchorBridgeThickness = 3 			#ADVANCED The thickness of the belt anchor bridge                                                                   
xCarriageWingWidth = 10 				#ADVANCED The width of the xCarriage wings                                                                          
xCarriageWingHeight = 10 				#ADVANCED The height of the xCarriage wings                                                                         
xBeltAnchorWidthTop = 18 				#ADVANCED Should be CALCULATED - The width of the top of the belt anchor                                            
xBeltAnchorWidthBottom = 25				#ADVANCED Should be CALCULATED - The width of the bottom of the belt anchor                                         
xCarriageMountHoleVertOffset = 20 		#ADVANCED Should be CALCULATED - The distance from the bottom edge of the face to the extruder mounting holes               
xCarriageMountHoleHorizOffset = 4.75	#ADVANCED Should be CALCULATED - The distance from the side of the xCarriage and the extruder mounting holes                        
xBushingNutMaxFacetoFace = None	#CALCULATED The maximum xBushing nut face to face distance                                                                          
xBushingNutMaxThickness = None	#CALCULATED The maximum bushing nut thickness for the x axis                                                                                
xCarriageBushingHolderOR = None	#CALCULATED the bushing holder outside radius on the x carriage                                                                     
xBeltAnchorHeight = None		#CALCULATED The height of the belt anchor from the back of the xCarriage face                                                       
                                                                                                                                                                           
                                                                                                                                                                           
#zMotorMount vars                                                                                                                                                          
#needs a plate thickness                                                                                                                                                   
zMotorMountHoles = 4 #The number of motor mounting holes                                                                                                                   
zShaftToMountHoleDist = 21.92 #the distance between the shaft and the mounting holes                                                                                       
zMotorMountHoleDia = 3.5	#the diameter of the motor mounting holes                                                                                                   
zMotorMountHolePadding = 4.39 # the minimum space between the edge of the motor mounting holes and the edge of the plate                                                   
zMotorMountPlateThickness= 6 #The thickness of the z motor mount plate                                                                                                     
zMotorMountPlateWidth= 42.5 #Width of motor mount plate                                                                                                                    
zMotorMountShaftHoleDia = 24 #Diameter of the shaft hole in the zMotorMount.                                                                                               
zMotorMountLocation = "Bottom" 		#ADVANCED The location of the zMotorMounts. Either Top or Bottom                                                            
zMotorMountLength = None 			#CALCULATED The length of the z motor mount plate                                                                           
zMotorMountMountingFaceWidth = None	#Calculated The width of the frame member to which the z motor mount is attached                                                    
zMotorMountEdgeToShaftHole = None 	#CALCULATED The distance from the frame side edge of the motor mount to the shaft hole center                                       
zShaftToMountHoleDistX = None 		#Calculated                                                                                                                         
zMotorBodyWidth = None 				#CALCULATED Width of the zMotorBody                                                                                 
                                                                                                                                                                           
#yMotorMount vars                                                                                                                                                          
#needs a plate thickness                                                                                                                                                   
yShaftToMountHoleDist = 33.195 #the distance between the shaft and the mounting holes                                                                                      
yMotorMountHolePadding = 4.39 #The distance between the edge of the motor and the edge of the motor mount holes                                                            
yMotorMountHoleDia = 4.4 # Dia of the y motor mount holes                                                                                                                  
yMotorMountPlateWidth = 57 # The width of the y motor mount plate                                                                                                          
yMotorMountPlateThickness = 6 #Thickness of the yMotorMountPlate                                                                                                           
yMotorMountShaftHoleDia = 24 #The diameter of the shaft hole for the y motor mount                                                                                         
yMotorMountHoles = 4 # The number of motor mounting holes for the y motor                                                                                                  
yMotorPulleyDia = 19.5 #The diameter of the y motor pulley                                                                                                                 
yMotorShaftToMountHoleDistX = None	#CALCULATED The x component of the distance from the shaft to the mount hole                                                        
yMotorBodyWidth = None				#CALCULATED The width of the y motor body                                                                                   
                                                                                                                                                                           
                                                                                                                                                                           
#zRodSupport vars                                                                                                                                                          
zRodSupportLength = 15 #ADVANCED The length of the zrod that is supported                                                                                                  
                                                                                                                                                                           
                                                                                                                                                                           
#YRodSupport vars                                                                                                                                                          
yRodSupportClearance = 3 			#ADVANCED The clearance between the top of the clamping bolts and the bottom of the printBedSupport.                        
yRodSupportWidth = None				#CALCULATED The total width of the Rod Support including tabs.                                                      
yRodStandoff = None					#CALCULATED The distance from the top of the frame to the yRod axis                                                 
yRodSupportMountHoleSpacing = None	#CALCULATED The center to center distance for the yRodSupport mounting holes. Middle of slot to middle of slot                      
yRodSupportClampBoltLength = None	#CALCULATED The length of the clamping bolts used for the yRodClamps                                                                
yRodSupportNutTrapDepth = None 		#CALCULATED The depth of the nut traps on the rod supports                                                                  
                                                                                                                                                                           
                                                                                                                                                                           
#yBeltAnchor                                                                                                                                                               
yBeltAnchorWidth = 6 			#ADVANCED The width of the belt anchor column                                                                                       
yBeltAnchorLength = 24 			#ADVANCED The length of the belt anchor Column                                                                              
yBeltAnchorBridgeThickness = 3 	#ADVANCED The thickness of the y belt anchor bridge                                                                                 
yBeltAnchorSlotWidth = 6 		#ADVANCED The width of the y belt anchor slot                                                                                       
yBeltAnchorHoleSpacing = None	#CALCULATED Center to center distance between yBeltAnchorHoles                                                                              
yBeltAnchorHeight = None		#CALCULATED The total height (including tab thickness) of the y belt anchor                                                         
                                                                                                                                                                           
                                                                                                                                                                           
#extruderMountPlate vars                                                                                                                                                   
extruderMountPlateThickness = 1.55 #The thickness of the extruderMountPlate                                                                                                
hotEndMountHoleDia = 3 #The diameter of the hot end mounting holes                                                                                                         
extruderMountPlateWidth = None	#CALCULATED The width of the extrtuder mount plate                                                                                          
                                                                                                                                                                           
                                                                                                                                                                           
#extruderMountAngle vars                                                                                                                                                   
extruderMountAngleWidth = 19.05 # The width of the angle used. (The nominal size of the angle.)                                                                            
extruderMountAngleThickness = 3.175 # The thickness of the angle used.                                                                                                     
                                                                                                                                                                           
                                                                                                                                                                           
#extruder vars                                                                                                                                                             
extruderWidth = 78 #The width of the extruder body                                                                                                                         
extruderDepth = 55 # The required depth for mounting the extruder front edge of body to back most part of extruder                                                         
extruderMountHoleSpacing = 48 #The distance between the extruder's mounting holes                                                                                          
extruderMountHoleDia = 3 #The diameter of the extruder's mounting holes                                                                                                    
extruderFilamentHoleDia = 4 #The diameter of extruder's filament hole                                                                                                      
extruderEdgeToCenterLine = 14 #The distance from the outer edge of the extruder to it's center line                                                                        
extruderNozzleStandoff = None	#CALCULATED The distance from the center of the nozzle to the face of the vertical bars                                                     
                                                                                                                                                                           
                                                                                                                                                                           
#extruderBarrel vars                                                                                                                                                       
extruderBarrelDia = 25.4 #Diameter of the extruder barrel                                                                                                                
extruderBarrelLength = 42 #The length of the extruderBarrel                                                                                                                
extruderBarrelLinerDia = 6.35 #The diameter of the teflon barrel liner                                                                                                 
extruderBarrelNumFins = 7 #The number of cooling fins not including the top and bottom faces.                                                                              
extruderBarrelFaceThickness = 3 #The thickness of the top and bottom faces                                                                                                 
extruderBarrelCoreThickness = 1.5 #The thickness of metal around the barrel liner                                                                                          
extruderBarrelFinGap = 3.175 #The space between fins                                                                                                                    
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
nozzleThermistorRetainerDepth = 3 #The depth of the thermistor retainer hole                                                                                               
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
yBeltIdlerHoleDia = 6 #The diameter of the hole for the yBeltIdler                                                                                                         
crossBarLength = None #CALCULATED The length of the cross bars                                                                                                             
                                                                                                                                                                           
                                                                                                                                                                           
#Side bar vars                                                                                                                                                             
sideBarLength = None #CALCULATED The length of the side bars                                                                                                               
                                                                                                                                                                           
                                                                                                                                                                           
#frameSpacer vars                                                                                                                                                          
#frameSpacerLength should be calculated depending on the power supply thickness, electronics or motors                                                                     
frameSpacerLength = 90 # The length of the frameSpacers                                                                                                                    
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

#feet vars
feetOffset = 2                  #ADVANCED The distance between the edge of the frame and the foot
feetBaseThickness = 3           #ADVANCED The thickness of plastic clamped by the mounting bolt
feetBoltHeadClearanceVert = 3   #ADVANCED The distance between the top of the bolt head and the bottom of the foot 
feetBoltHeadClearanceHor = 0.5  #ADVANCED The gap between the bolt head and the wall of the pocket
feetDraftAngle = 5              #ADVANCED The angle of draft on the feet. This makes the feet taper.

#LeadScrewCoupler vars
leadScrewCouplerLength = 25         #The length (vertical axis) of the leadScrewCouplers 
leadScrewCouplerScrewClampDia = 10  #The diameter of the cut out for clamping the lead screw. Includes space for tubing.
leadScrewCouplerShaftClampDia = 7   #The diameter of the cutout for clamping the motor shaft. Includes space for tubing.
leadScrewCouplerClampGap = 2        #ADVANCED The gap between the two halves of the clamp.
leadScrewCouplerGap = 5             #ADVANCED The space above and below the leadScrewCoupler. For keeping the coupler from  crashing into zMotor mount plate or xCarriage 
leadScrewCouplerBaseThicnkess = 3	#ADVANCED The minimum thickness of the plastic on the clamps.
leadScrewCouplerNutTrapPadding = 1.5#ADVANCED The padding between the nut traps and the edge of the leadScrewCoupler
                                                                                                                                                                           
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
standardNuts = [[0.1120, 0.0939, 1/4 , 3/32],
				[0.1380, 0.1140, 5/16 , 7/64],
				[0.1640, 0.1390, 11/32, 1/8],
				[0.1900, 0.1560, 3/8 , 1/8],
				[0.2160, 0.181, 7/16, 5/32],
				[1/4, 0.2070, 7/16, 7/32],                                                                                                                  
				[5/16,0.2650, 1/2, 17/64],                                                                                                                  
				[3/8, 0.321, 9/16, 21/64],                                                                                                                  
				[7/16,0.376, 11/16, 3/8],                                                                                                                   
				[1/2,0.434, 3/4, 7/16],
				[5/8,0.546, 15/16, 35/64]                                                                                                                   
				]                                                                                                                                           
                                                                                                                                                                           
                                                                                                                                                                           
#Metric Nut Sizes [Thread dia, Minor dia, Face to face, Thickness] in mm                                                                                                   
metricNuts =   [[2.5, 1.993, 5, 2],                                                                                                                                        
				[3,2.439, 5.5, 2.4],
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
bushingNutPadding = 5 # minimum thickness of holder around nut and thickness of depth stop                                                                                 
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

#Plater Variables                                                                                                                                                          
plate = False #To Plate or not to Plate, that is the Question                                                                                                               
platerWidth = 150 #width, width of the plate, in mm (default 150)                                                                                                          
platerHeight = 150 #height of the plate, in mm (default 150)                                                                                                               
platerPrecision = 0.5 #precision, in mm (default 0.5)
platerSpacing = 2 #parts spacing, in mm (default 2)                                                                                                                        
platerDelta = 2 #sets the spacing of the brute forcing (see below), default 2mm                                                                                          
platerRotation = 90 #sets the angle of the brute forcing, default 90                                                     

#Marlin Variables
baudrate = 250000 #ADVANCED Communication speed for the printer
maxTemp = 230 #ADVANCED Max temperature for the extruder
bedMaxTemp = 120 #ADVANCED Max temperature for the heated bed
extruderTempSensor = 1 #ADVANCED Sensor used to measure extruder temperature. Set via the Marlin sensor system
bedTempSensor = 1 #ADVANCED Sensor used to measure bed temperature. Set via the Marlin sensor system
xHomeDir = -1 #ADVANCED Direction to move to home on the X axis
yHomeDir = -1 #ADVANCED Direction to move to home on the Y axis
zHomeDir = -1 #ADVANCED Direction to move to home on the Z axis
maxTolerance = 20 #ADVANCED  Tolerance for initial software defined build area.
invertXDirection = False #ADVANCED Inverts the X stepper motor
invertYDirection = False #ADVANCED Inverts the Y stepper motor
invertZDirection = False #ADVANCED Inverts the Z stepper motor
invertEDirection = False #ADVANCED Inverts the Extruder stepper motor

#Slic3r Variables                                                                                                                                                         
slic3r = False #Slice or nah?                                                                                                                                             
slic3rVars = ""                                                                                                                                                           
                                                                                                                                                         
#Zip Variables                                                                                                                                            
zipName = "Printer_Files" #Name of zip file                 
