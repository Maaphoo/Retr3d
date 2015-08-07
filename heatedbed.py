from __future__ import division  # allows floating point division from integers
import globalVars as gv
import datetime
import os

# Resistance is in ohms per 100 feet
# for 0 to 40 gauge wire
wireResistance = {0: 0.009827, 1: 0.01239, 2: 0.01563, 3: 0.01970, 4: 0.02485, 5: 0.03133, 6: 0.03951, 7: 0.04982,
                  8: 0.06282, 9: 0.07921, 10: 0.09989, 11: 0.1260, 12: 0.1588, 13: 0.2003, 14: 0.2525, 15: 0.3184,
                  16: 0.4016, 17: 0.5064, 18: 0.6385, 19: 0.8051, 20: 1.015, 21: 1.280, 22: 1.614, 23: 2.036,
                  24: 2.567, 25: 3.237, 26: 4.081, 27: 5.147, 28: 6.490, 29: 8.183, 30: 10.32, 31: 13.01, 32: 16.41,
                  33: 20.69, 34: 26.09, 35: 32.90, 36: 41.48, 37: 52.31, 38: 65.96, 39: 83.18, 40: 104.90}


def computeWireResistance(wireGauge, wireLength):
    if (wireGauge <= 40) and (wireGauge >= 0) and (wireLength >= 0):
        # ohms per meter
        res = wireLength * wireResistance[wireGauge] / 30.48
        res = float(float(res) * 1000) / 1000
        return res
    else:
        return -1

voltage = gv.voltage
amperage = gv.amperage
gauge = gv.gauge

def design():
    # By Ohms Law
    goalResistance = float(voltage/amperage)

    # Get how many meters are needed
    wireLength = goalResistance/computeWireResistance(gauge, 1)

    # print gv.printableWidth
    # print gv.printableLength
    printableLength = str(gv.printableLength)
    printableWidth = str(gv.printableWidth)

    nHoles = int(float(round((int(float(printableLength))-30)/10.5)))
    print nHoles

    # Make dateString and add it to the directory string
    date = datetime.date.today().strftime("%m_%d_%Y")
    printerDir = gv.printerDir+"Printer_"+date+"/"

    filename = os.path.join(printerDir, 'Parts', 'Heated Bed Wire Diagram.svg')
    print filename
    svg = open(filename, 'w')
    svg.write('<svg width="'+printableWidth+'mm" height="'+printableLength+'mm">')
    svg.write('<circle cx="15mm" cy="15mm" r="1.5mm" fill="white" stroke="black" stroke-width=".5mm" />')
    svg.write('<circle cx="'+str(int(float(printableWidth))-15)+'mm" cy="15mm" r="1.5mm" fill="white" stroke="black" stroke-width=".5mm" />')
    for x in range(1,nHoles):
        svg.write('<circle cx="15mm" cy="'+str(15+(10.5*x))+'mm" r="1.5mm" fill="white" stroke="black" stroke-width=".5mm" />')
        svg.write('<circle cx="'+str(int(float(printableWidth))-15)+'mm" cy="'+str(15+(10.5*x))+'mm" r="1.5mm" fill="white" stroke="black" stroke-width=".5mm" />')
    svg.write('<text x = "30mm" y = "30mm" fill = "black" font-size = "50">'+str(round(wireLength, 1))+' Meters of Wire Needed</text>')
    svg.write('</svg>')
    svg.close()



