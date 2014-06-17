#*******************************************************************************************#
#********* Extracting surface/polysurface naked or interior edges **************************#
#********* by Djordje Spasic ***************************************************************#
#********* issworld2000@yahoo.com 05-Feb-2014 **********************************************#

""" Function does similarly to what Rhino command "Silhouette" and rhinoscriptsyntax.DuplicateSurfaceBorder function do:
but it has an option do generate both naked and interior curves, and join each of these. """

import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

def extractPolysrfEdges(_polysurface, _naked_interior, _join):
    if _polysurface:
        brep_o = rs.coercebrep(_polysurface)
        bEdges = brep_o.Edges
        if bEdges:
            nakedE = []
            interiorE = []
            nonManifoldE = []

            for bEdge in bEdges:
                edgAdj = bEdge.Valence
                if edgAdj == Rhino.Geometry.EdgeAdjacency.Naked:
                    nakedE.append(bEdge.DuplicateCurve())
                elif edgAdj == Rhino.Geometry.EdgeAdjacency.Interior:
                    interiorE.append(bEdge.DuplicateCurve())
                else:
                    nonManifoldE.append(bEdge.DuplicateCurve())

            if _naked_interior == "Naked":
                naked_or_InteriorCrvs = nakedE
            elif _naked_interior =="Interior":
                naked_or_InteriorCrvs = interiorE
            sel = []
            if _join == "Yes" or _join == 1:
                joinNaked = Rhino.Geometry.Curve.JoinCurves(naked_or_InteriorCrvs)
                for crv in joinNaked:
                    crv_id = sc.doc.Objects.AddCurve(crv)
                    rs.ObjectColor(crv_id, [255,0,0])
                    sel.append(crv_id)
                rs.SelectObjects(sel)
            elif _join == "No" or _join == 0:
                for crv in naked_or_InteriorCrvs:
                    crv_id = sc.doc.Objects.AddCurve(crv)
                    rs.ObjectColor(crv_id, [255,0,0])
                    sel.append(crv_id)
                rs.SelectObjects(sel)

        else:
            print "Something is wrong with you polysurface edges. Function terminated"
            return
    else:
        print "You did not choose the polysurface. Function terminated"
        return


polysurface = rs.GetObject("Choose polysurface to extract the naked/interior edges", 16, preselect=True)
naked_interior = rs.GetString("Extract Naked or Interior curves", "Naked", ["Naked" , "Interior"])
if naked_interior == "Naked":
    join = rs.GetString("Do you wish to join the naked edges?", "Yes", ["Yes" , "No"])
    extractPolysrfEdges(polysurface, naked_interior, join)
elif naked_interior == "Interior":
    join = rs.GetString("Do you wish to join the interior edges?", "Yes", ["Yes" , "No"])
    extractPolysrfEdges(polysurface,naked_interior, join)
else:
    print "You typed something wrong. Please choose either Naked or Interior option"
