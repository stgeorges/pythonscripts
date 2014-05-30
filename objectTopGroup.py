#**********************************************************************************************#
#********* Return the top most group name of an object ****************************************#
#********* by Djordje Spasic ******************************************************************#
#********* issworld2000@yahoo.com 6-May-2014 **************************************************#

"""
This small function replicates the "ObjectTopGroup" RhinoScript function, which still hasn't been implemented 
into PythonScript.
Returns the top most group name that an object is assigned.  This function primarily applies to objects that are 
members of nested groups.
"""

import rhinoscriptsyntax as rs
import scriptcontext as sc

def objectTopGroup(_id):
    groupNames = sc.doc.Groups.GroupNames(False)
    groupName = False
    for i in range(rs.GroupCount()):
        groupRO = sc.doc.Groups.GroupMembers(i)
        for ele in groupRO:
            if rs.coercerhinoobject(ele).Id == _id:
                groupName = groupNames[i]
    if groupName:
        print groupName
    else:
        print "The element you chose does not belong to any group"

id = rs.GetObject()
objectTopGroup(id)
