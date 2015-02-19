#***********************************************************************************************************#
#********* Get normalized 2-D texture coordinates of a mesh object *****************************************#
#********* by Djordje Spasic *******************************************************************************#
#********* issworld2000@yahoo.com 17-Feb-2015 **************************************************************#
"""
Rhino 5 SR11 (and all older releases) still does not have RhinoScript MeshTextureCoordinates function implemented for PythonScript.
MeshTextureCoordinates returns normalized (between 0 and 1) 2-D texture coordinates of a mesh object.  
Small function bellow replicates this functionality.
"""

import rhinoscriptsyntax as rs

def MeshTextureCoordinates(object_id):
    meshObj = rs.coercemesh(object_id)
    mCoordL = []
    for i in range(meshObj.TextureCoordinates.Count):
        mCoordL.append(meshObj.TextureCoordinates[i])
    return mCoordL

meshId = rs.GetObject("pick up your mesh", 32)
coord = MeshTextureCoordinates(meshId)
print coord
