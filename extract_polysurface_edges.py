#*******************************************************************************************#
#********* Extracting polysurface naked edges (silhouette edges) ***************************#
#********* by Djordje Spasic ***************************************************************#
#********* issworld2000@yahoo.com 05-Feb-2014 **********************************************#

""" Function does similarly to what Rhino command "Silhouette" does: but it has an option do distinguish
the naked from interior curves, and join each of these.
It prompts for user input on picking polysurface extracts its naked edges.
They can be joined or not. Naked edges get coloured to red, and selected on the output. There's an option 
to extract interior edges too - one only needs to edit the line 37 and replace "nakedE" with "interiorE". """

import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

def extractPolysrfEdges(_polysurface):
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

            join = rs.GetInteger("Do you wish to join the naked edges? Yes(1), No(0)", 1)
            sel = []
            if join > 0 or join < 0:
                joinNaked = Rhino.Geometry.Curve.JoinCurves(nakedE)    # by replacing "nakedE" with "interiorE" one could get interior edges instead
                for crv in joinNaked:
                    crv_id = sc.doc.Objects.AddCurve(crv)
                    rs.ObjectColor(crv_id, [255,0,0])
                    sel.append(crv_id)
                rs.SelectObjects(sel)
            elif join == 0:
                for crv in nakedE:
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
extractPolysrfEdges(polysurface)
