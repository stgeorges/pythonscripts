#*******************************************************************************************#
#********* Export volume, mass, weight and volume centroid coordinates to .csv file ********#
#********* by Djordje Spasic ***************************************************************#
#********* issworld2000@yahoo.com 28-01-2014 ***********************************************#

"""
Function promts for user input on picking solid(s), and choosing their Material. Then asks for the name/location
where the .csv file will be saved. Exported .csv file consists of following information: Object number, Volume,
Mass, Weight, Volume Centroid coordinates.

Function additionally labels object names or numbers(if names were not set) and volume centroid points to Rhino file.

Depending on Rhino unit system, data will be exported with following units:

    units: Millimeters:  length(mm), volume(mm3), mass(g), weight(N - Newtons)
    units: Centimeters:  length(cm), volume(cm3), mass(g), weight(N)
    units: Meters:  length(m), volume(m3), mass(kg), weight(N)
    units: Inches:  length(in), volume(in3), mass(oz - ounce), weight(N)
    units: Feets:  length(ft), volume(ft3), mass(lb), weight(N)


Author does not guarantee the script will work. Use it at your own risk. Author assumes no 
responsibility if the script harms you, your system, or your applications!!!
"""


import rhinoscriptsyntax as rs

# density data taken from "http://engineeringtoolbox.com/metal-alloys-densities-d_50.html"
### Units are in kg/m3 !!! ###
materials = ["Actinium", "Admiralty Brass", "Aluminum", "Aluminum - melted", "Aluminum - 1100", "Aluminum - 6061", "Aluminum - 7050", "Aluminum - 7178", "Aluminum bronze (3-10% Al)", "Aluminum foil", "Antifriction metal", "Antimony", "Babbitt", "Barium", "Beryllium", "Beryllium copper", "Bismuth", "Brass - casting", "Brass - rolled and drawn", "Brass 60/40", "Bronze - lead", "Bronze - phosphorous", "Bronze (8-14% Sn)", "Brushed metal", "Cadmium", "Caesium", "Calcium", "Cast iron", "Cerium", "Chemical Lead", "Chromium", "Cobalt", "Constantan", "Columbium", "Constantan", "Copper", "Cupronickel", "Delta metal", "Duralumin", "Electrum", "Eroded metal", "Europium", "Gallium", "Germanium", "Gold", "Hafnium", "Hatelloy", "Indium", "Inconel", "Incoloy", "Iridium", "Iron", "Lanthanum", "Lead", "Light alloy based on Al", "Light alloy based on Mg", "Lithium", "Magnesium", "Manganese", "Manganese Bronze", "Manganin", "Mercury", "Molybdenum", "Monel", "Neodymium", "Nichrome", "Nickel", "Nickel 20", "Nickel 200", "Nickel silver", "Nickeline", "Nimonic", "Niobium", "Osmium", "Palladium", "Phosphor bronze", "Platinum", "Plutonium", "Red Brass", "Silver", "Sodium", "Solder 50/50 Pb Sn", "Stainless Steel ", "Steel", "Tin", "Titanium", "Tungsten", "Uranium", "Vanadium", "White metal", "Wrought Iron", "Zinc", "Zirconium", "Yellow Brass"]
densities = [10070.0, 8525.0, 2712.0, 2560.0, 2720.0, 2720.0, 2800.0, 2830.0, 7700.0, 2700.0, 9130.0, 6690.0, 7272.0, 3594.0, 1840.0, 8100.0, 9750.0, 8400.0, 8430.0, 8520.0, 7700.0, 8780.0, 7400.0, 7860.0, 8640.0, 1873.0, 1540.0, 6800.0, 6770.0, 11340.0, 7190.0, 8746.0, 8920.0, 8600.0, 8880.0, 8940.0, 8908.0, 8600.0, 2790.0, 8400.0, 7860.0, 5243.0, 5907.0, 5323.0, 19320.0, 13310.0, 9245.0, 7310.0, 8497.0, 8027.0, 22650.0, 7850.0, 6145.0, 11340.0, 2560.0, 1760.0, 534.0, 1738.0, 7440.0, 8359.0, 8500.0, 13593.0, 10188.0, 8360.0, 7007.0, 8400.0, 8908.0, 8090.0, 8890.0, 8400.0, 8770.0, 8100.0, 8570.0, 22610.0, 12160.0, 8900.0, 21400.0, 19816.0, 8746.0, 10490.0, 971.0, 8885.0, 7480.0, 7850.0, 7280.0, 4500.0, 19600.0, 18900.0, 5494.0, 7100.0, 7750.0, 7135.0, 6570.0, 8470.0]
# If you would like to add another material you can just insert it in the upper two lists, at their ends or beginings



def VolumeMassWeightCentroids(_materials, _densities):
    # object ids
    objects = rs.GetObjects("Pick objects of the same material", 16, preselect = True)
    if objects:
        objectsClosed = []
        for obj in objects:
            if rs.IsPolysurfaceClosed(obj)==True:
                objectsClosed.append(obj)
        if len(objectsClosed) > 0:

            # choose material
            pickedMaterial = rs.ListBox(_materials, "Choose the material", "Material", "Stainless Steel ")
            if pickedMaterial:
                for i in range(len(materials)):
                    if _materials[i] == pickedMaterial:
                        density = _densities[i]
                        break
            
                # units correction
                unitsystemIndex = rs.UnitSystem()
                if unitsystemIndex == 0:
                    print "No unit system. Operation terminated"
                    return
                elif unitsystemIndex == 2:   #mm
                    density = density/1000000
                    massFactor = 0.001
                    massUnits = "g"
                    volumeUnits = "mm3"
                    lengthUnits = "mm"
                elif unitsystemIndex == 3:   #cm
                    density = density/1000
                    massFactor = 0.001
                    massUnits  = "g"
                    volumeUnits = "cm3"
                    lengthUnits = "cm"
                elif unitsystemIndex == 4:   #m
                    density = density
                    massFactor = 1
                    massUnits = "kg"
                    volumeUnits = "m3"
                    lengthUnits = "m"
                elif unitsystemIndex == 8:   #inches
                    density = density * 0.00057803667443635 
                    massFactor = 0.0283495
                    massUnits = "oz"
                    volumeUnits = "in3"
                    lengthUnits = "in"
                elif unitsystemIndex == 9:   #feet
                    density = density * 0.998847
                    massFactor = 0.453592
                    massUnits = "lb"
                    volumeUnits = "ft3"
                    lengthUnits = "ft"
                else:
                    print "You are not using one of these unit systems: mm, cm, m, in, ft. Function terminated"
                    return
            
            # volumes, masses, weights, centroids
                volumes = []
                masses = []
                centroids = []
                weights = []
                for obj in objectsClosed:
                    vol = rs.SurfaceVolume(obj)[0]
                    volumes.append(vol)
                    mass = density * vol
                    masses.append(mass)
                    weight = mass * massFactor * 9.81      # additionally multiply with "0.001" in case you want Kilonewtons instead of Newtons for weight unit
                    weights.append(weight)
                    centr = rs.SurfaceVolumeCentroid(obj)[0]
                    centroids.append(centr)
    
                # export data to csv file
                filename = rs.SaveFileName("Save csv file","*.csv||", None, "VolMassWeigCen", "csv")
                file = open(filename, 'w')
                headerline = "Object name, Volume(%s), Mass(%s), Weight(N), Centroid(%s)[x], Centroid(%s)[y], Centroid(%s)[z]\n" %(volumeUnits, massUnits, lengthUnits, lengthUnits, lengthUnits)
                file.write(headerline)
                index = 0
                for i in range(len(objectsClosed)):
                    objectName = rs.ObjectName(objectsClosed[i])
                    if not objectName:
                        index += 1
                        objectName = "obj%s" % (index)
                    volu = volumes[i]
                    mas = masses[i]
                    weig = weights[i]
                    x = centroids[i][0]
                    y = centroids[i][1]
                    z = centroids[i][2]
                    line = "%s,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f \n" %(objectName, volu, mas, weig, x,y,z)
                    # adding an annotation text dot to Rhino:
                    rs.AddPoint(centroids[i])
                    rs.AddTextDot(objectName, centroids[i])
                    file.write(line)
                file.close()
                print "Done"

            else:
                print "You did not choose material. Function terminated."
                return

        else:
            print "All of objects you picked are not closed (solids). Function terminated"
            return

    else:
        print "You did not choose appropriate or any objects. Function terminated."
        return


VolumeMassWeightCentroids(materials, densities)
