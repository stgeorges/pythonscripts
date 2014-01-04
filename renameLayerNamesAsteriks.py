#******************************************************************#
#********* Rename layer names with/without asteriks symbol ********#
#********* by Djordje Spasic **************************************#
#********* issworld2000@yahoo.com  30-12-2013 *********************#

"""
These functions promt for user input on word/character within layer names which needs 
to be replaced. Convenient option includes asteriks symbol as a wildcard character. Example:

-  current layers: Layer01, Layer02, Layer03
-  find: L*0*
-  replace: Pl*1*
-  results in: Player11, Player12, Player13

Layer names could be replaced on a number of levels: parent, sub-layer, sub-sub-layer or mutual
combinations of mentioned three.

In order for function to work properly, an equal number of group characters for both find and replace needs to be supplied:
- an example of equal group characters:
    find: *ayer*0*   (two group characters)
    replace: *itres*9*   (two group characters)
- example of unequal group characters:
    find: *ayer*0*   (two group characters)
    replace: *itres*9*2   (three group characters)   <- last "2" is excessive
Function will still work with unequal number of group characters, but the last excessive group will be omitted from replacement

Author does not guarantee the script will work. Use it at your own risk. Author assumes no 
responsibility if the script harms you, your system, or your applications!!!

@Special thanks to Daniel Vianna for introducing me to regular expressions"""

import rhinoscriptsyntax as rs
import re

# extracting original layer names
def layerNames():
    layersL = rs.LayerNames()
    parentLayers = []
    subLayers1 = []
    subLayers2 = []
    for layer in layersL:
        if layer.count("::") == 0:
            parentLayers.append(layer)
        elif layer.count("::") == 1:
           subLayers1.append(layer.split("::")[-1])
        elif layer.count("::") == 2:
           subLayers2.append(layer.split("::")[-1])
    return [parentLayers, subLayers1, subLayers2]

# generating layer names combinations by level
def layersList(_layersLevelInput):
    if _layersLevelInput == 0:
        return layerNames()[0]
    elif _layersLevelInput == 1:
        return layerNames()[1]
    elif _layersLevelInput == 2:
        return layerNames()[2]
    elif _layersLevelInput == 10:
        return layerNames()[0]+layerNames()[1]
    elif _layersLevelInput == 20:
        return layerNames()[0]+layerNames()[2]
    elif _layersLevelInput == 21 or _layersLevelInput == 12: # in case of error
        return layerNames()[1]+layerNames()[2]
    elif _layersLevelInput == 210 or _layersLevelInput == 120 or _layersLevelInput == 102 or _layersLevelInput == 201: # in case of error
        return layerNames()[0]+layerNames()[1]+ layerNames()[2]
    else:
        print "That combination is not available. Please run the script again, and choose available combination"
        return None

# removing asteriks characters from find and replace
def cleaningUp(_find, _replace):
    if _find and _replace:
        find2 = _find.split("*")
        for item3 in find2:
           if item3 == "":
            find2.remove(item3)
        replace2 = _replace.split("*")
        for item4 in replace2:
           if item4 == "":
            replace2.remove(item4)
        return [find2, replace2]
    else:
        print "You did not enter find and replace words/characters."
        return None

# regular expressions search-and-replace:
def searchAndReplaceRe(_layer, _find2, _replace2):
    if _layer and _find2 and _replace2:
        if len(_find2) == len(_replace2):
            charactGN = _find2
        elif len(_find2) < len(_replace2):
            charactGN = _find2
        elif len(_find2) > len(_replace2):
            charactGN = _replace2
        find2String = ""
        replace2String = ""
        for i in range(len(charactGN)):
            find2String += str(_find2[i])
            replace2String += str(_replace2[i])
            if i < len(charactGN)-1:
                find2String += "(.*)"
                replace2String += "\\g<"
                replace2String += str(i+1)
                replace2String += ">"
        return re.sub(find2String, replace2String, _layer)
    else:
        print "You did not enter find and replace words/characters"
        return None

# rename layer names
def renameLayers(_originalLayersList, _newLayersList):
    if _originalLayersList and _newLayersList:
        for i in range(len(_originalLayersList)):
           new_name = rs.RenameLayer(_originalLayersList[i],_newLayersList[i])
        print "Done"
        return
    else:
        print "Something went wrong with re.sub() function. Function terminated"
        return

# function inputs:
find = rs.StringBox("Which part of your Layer's name do you want to replace?",None,"Find")
replace = rs.StringBox("Replace with?",None,"Replace")
if find and replace:
    # comment out line 126 if you want to remove the Message box:
    layersLevelInfo = rs.MessageBox("At what level do you want to replace your layer names?\n \n- Choose some of the following numbers:\nparent layers level: 0\nsub-layers level: 1\nsub-sub-layers level: 2\n \n- Combinations (always from lower level to higher):\nreplace layer names at all levels: 210\nreplace only at parent level: 0\nreplace only at sub-sub and parent: 20\nreplace at sub-sub and sub: 21\netc.", 64)
    layersLevelInput = int(rs.StringBox("Enter the level code (210 will cover all levels):","210","Layers level code"))
    if layersLevelInput:
        originalLayersList = layersList(layersLevelInput)
        find2 = cleaningUp(find, replace)[0]
        replace2 = cleaningUp(find, replace)[1]
        newLayersList = []
        for layer2 in originalLayersList:
            newLayersList.append(searchAndReplaceRe(layer2, find2, replace2))

        renameLayers(originalLayersList, newLayersList)
    else:
        print "You did not enter the level code. Function terminated."
else:
    print "You did not enter the part you want to replace or its replacement. Function terminated."
