#********************************************************************#
#********* Select closed (solid) objects by Volume ******************#
#********* by Djordje Spasic ****************************************#
#********* issworld2000@yahoo.com 17-Aug-2014 ***********************#
"""
Function prompts the user to enter the desired volume amount, and selects the
closed (solid) object with closest amount of volume, to the entered one.
"""

import rhinoscriptsyntax as rs
import Rhino

# for pre SR9 users (rs.UnitSystemName not available)
def unitSystem():
        unitsystemIndex = rs.UnitSystem()

        if unitsystemIndex == 2:
            return "mm3"
        elif unitsystemIndex == 3:
            return"cm3"
        elif unitsystemIndex == 4:
            return "m3"
        elif unitsystemIndex == 8:
            return "in3"
        elif unitsystemIndex == 9:
            return "ft3"
        else:
            return "of unknown unit system"

def selectObjperVolume(ids, targetV):
    volumes = []
    objs = [rs.coercegeometry(id) for id in ids]
    for i,obj in enumerate(objs):
        if isinstance(obj, Rhino.Geometry.Brep):
            if obj.IsSolid:
                volumes.append((rs.SurfaceVolume(obj)[0],ids[i]))
        elif isinstance(obj, Rhino.Geometry.Extrusion):
            if obj.IsSolid:
                volumes.append((rs.SurfaceVolume(obj)[0],ids[i]))
        elif isinstance(obj, Rhino.Geometry.Mesh):
            if obj.IsClosed:
                volumes.append((rs.MeshVolume([obj])[1],ids[i]))

    if len(volumes) > 0:
        subtractL = []
        for i,v in enumerate(volumes):
            subtractL.append((abs(v[0]-targetV),v[0],v[1]))

        subtractL.sort()
        rs.SelectObject(subtractL[0][2])
        print "Selected object with %s %s volume" % (subtractL[0][1],unitSystem())
        return subtractL[0][2]

    else:
        print "No closed object selected"
        return None


_ids = rs.GetObjects("Select objects you wish take into account for volume selection", 48, preselect=True)
_targetV = rs.GetReal("Enter the required volume", 1, 0.001)

# returns an id of the object with closest volume:
if _ids and _targetV:
    selectObjperVolume(_ids, _targetV)
