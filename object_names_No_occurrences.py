#*******************************************************************************************#
#********* Object names and its number of occurrences **************************************#
#********* by Djordje Spasic ***************************************************************#
#********* issworld2000@yahoo.com 08-Feb-2014 **********************************************#

""" Function shows all object's assigned names and counts the number of its occurrences.
Results could be exported to .csv file or just presented on the screen in a form of a message box """

import rhinoscriptsyntax as rs

def exportNameOcc(_objs_ids):
    # extracting object names
    namesColumn = []
    if _objs_ids:
        for obj in _objs_ids:
            name = rs.ObjectName(obj)
            if name:
                namesColumn.append(name)
        if len(namesColumn) > 0: 
            namesColumnU = set(namesColumn)
            namesColumnU = list(namesColumnU)

            # number of occurrences
            countColumn = []
            for nU in namesColumnU:
                   number = namesColumn.count(nU)
                   countColumn.append(number)

            mergedL = []
            for i in range(len(namesColumnU)):
                mergedL.append((countColumn[i], namesColumnU[i]))
            mergedL.sort(reverse=True)

            # exporting
            export = rs.GetInteger("Export results to .csv file or just show them on the screen?   CSV(1),   Screen(0)", number = 0, minimum = 0, maximum = 1)
            if export == 0:
                message = "Object name - No. of occurrences\n \n"
                for i in range(len(namesColumnU)):
                    print namesColumnU[i]
                    message += " %s - %i\n" % (mergedL[i][1], mergedL[i][0])
                rs.MessageBox(message, 0, "Results")
            else:
                filename = rs.SaveFileName("Save csv file","*.csv||", None, "ObjectNamesOccurrences", "csv")
                file = open(filename, 'w')
                headerline = "Names, Occurrences\n"
                file.write(headerline)
                for i in range(len(namesColumnU)):
                    name = mergedL[i][1]
                    occ = mergedL[i][0]
                    line = "%s,%i \n" %(name, occ)
                    file.write(line)
                file.close()
                print "Done"

        else:
            print "You do not have named objects. Function terminated"
            return

    else:
        print "Your 3dm file is empty or you did not select objects. Function terminated"
        return

# function call
objs_ids = rs.ObjectsByType(0)
exportNameOcc(objs_ids)
