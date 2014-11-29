#***************************************************************************************************#
#********* Generate knots, weights and degree values for rhinoscriptsyntax rs.AddNurbsCurve function********#
#********* by Djordje Spasic **************************************************************************#
#********* issworld2000@yahoo.com 30-Nov-2014 *******************************************************#

"""
rs.AddNurbsCurve rhinoscriptsyntax function simulates Rhino's "Curve" command.
Rhino.Python Programmer's Reference help file nor online documentation does not have an example of knots vector values list generation, and this sometimes causes confussion with usage of rs.AddNurbsCurve.
This function generates reparametarized curve's knots values, and control point's weights (1 by default, which Rhino's "Curve" command use too).
It also checks for the curve's degree, and modifies it if not appropriate.

Based on: http://www.rhino3d.com/nurbs
"""

import rhinoscriptsyntax as rs

def knotsDegreeWeights(pts, degree=None):
    numPts = len(pts)
    if numPts == 1:
        print "Nurbs curve can not be created from one point"
        return None, None, None
    elif numPts <= 4:
        degree = numPts - 1
    elif numPts > 4:
        if degree < 3 or degree==None:
            degree = 3
        elif degree >= numPts:
            degree = numPts-1

    knotsL = [0.0 for i in range(degree)]
    interN = (numPts + degree - 1) - (2*degree)
    if interN > 0:
        interVstep = 1/(interN+1)
        interV = interVstep
        for i in range(interN):
            knotsL.append(interV)
            interV += interVstep
    for i in range(degree):
        knotsL.append(1.0)
    weightsL = [1.0 for i in range(numPts)]
    
    return knotsL, degree, weightsL


degree = 3    # by default
pts = rs.GetObjects("Pick up the control points to draw the Nurbs curve")

knots, degree, weights = knotsDegreeWeights(pts,degree)
if knots:
    crvId = rs.AddNurbsCurve(pts, knots, degree, weights)
    
