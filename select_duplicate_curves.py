#********************************************************************************************#
#********* Select duplicate curves **********************************************************#
#********* by Djordje Spasic ****************************************************************#
#********* issworld2000@yahoo.com 16-May-2014 ***********************************************#

"""
Function selects all duplicate curves in document, whether they're positioned on top of each other 
(Rhino's command "SelDup" would find these) or scattered around. It can remove flipped curves too."""

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

def cullDuplicateCurves(_ids, _t, _tol, _flippedCrvs, _overlapped):
    if len(_ids) > 1:
        objs = [sc.doc.Objects.Find(id) for id in _ids]
        nc_objs = [crv.Geometry.ToNurbsCurve() for crv in objs]
        indx = []
        for i in range(len(nc_objs)):
            for k in range(len(nc_objs)):
                if (i != k) and (i not in indx) and (k not in indx) and (round(nc_objs[i].GetLength(), 3) == round(nc_objs[k].GetLength(), 3)):
                        if nc_objs[i].EpsilonEquals(nc_objs[k], _t):
                            crv1TVst = nc_objs[i].TangentAt(nc_objs[i].Domain[0])
                            crv1CVst = nc_objs[i].CurvatureAt(nc_objs[i].Domain[0])
                            crv1t1 = round( nc_objs[i].NormalizedLengthParameter( 0.33, Rhino.Geometry.Interval(0, nc_objs[i].GetLength()) )[1], 3 )
                            crv1CVmid1 = nc_objs[i].CurvatureAt(crv1t1)
                            crv1t2 = round( nc_objs[i].NormalizedLengthParameter( 0.66, Rhino.Geometry.Interval(0, nc_objs[i].GetLength()) )[1], 3 )
                            crv1CVmid2 = nc_objs[i].CurvatureAt(crv1t2)
                            crv1CVend = nc_objs[i].CurvatureAt(nc_objs[i].Domain[1])
                            crv1TVend = nc_objs[i].TangentAt(nc_objs[i].Domain[1])
                            crv2TVst = nc_objs[k].TangentAt(nc_objs[k].Domain[0])
                            crv2CVst = nc_objs[k].CurvatureAt(nc_objs[k].Domain[0])
                            crv2t1 = round( nc_objs[k].NormalizedLengthParameter( 0.33, Rhino.Geometry.Interval(0, nc_objs[k].GetLength()) )[1], 3 )
                            crv2CVmid1 = nc_objs[i].CurvatureAt(crv2t1)
                            crv2t2 = round( nc_objs[k].NormalizedLengthParameter( 0.66, Rhino.Geometry.Interval(0, nc_objs[k].GetLength()) )[1], 3 )
                            crv2CVmid2 = nc_objs[i].CurvatureAt(crv2t2)
                            crv2CVend = nc_objs[k].CurvatureAt(nc_objs[k].Domain[1])
                            crv2TVend = nc_objs[k].TangentAt(nc_objs[k].Domain[1])

                            # Select duplicated curves scattered around the document and overlapped. Flipped ones will not be included.
                            if _flippedCrvs == "No" and _overlapped == "No":
                                if ( crv1TVst.EpsilonEquals(crv2TVst, _tol) and crv1CVst.EpsilonEquals(crv2CVst, _tol) and crv1CVmid1.EpsilonEquals(crv2CVmid1, _tol) and crv1CVmid2.EpsilonEquals(crv2CVmid2, _tol) and crv1CVend.EpsilonEquals(crv2CVend, _tol) and crv1TVend.EpsilonEquals(crv2TVend, _tol) ):
                                    indx.append(i)

                            # Select duplicated curves scattered around the document and overlapped. Flipped ones included too.
                            elif _flippedCrvs == "Yes" and _overlapped == "No":
                                crv2TVstR = Rhino.Geometry.Vector3d(crv2TVst)
                                crv2TVstR.Reverse()
                                crv2TVendR = Rhino.Geometry.Vector3d(crv2TVend)
                                crv2TVendR.Reverse()
                                crv2R = nc_objs[k].Duplicate()
                                crv2R.Reverse()
                                crv2TVstRR = crv2R.TangentAt(crv2R.Domain[0])
                                crv2CVstR = crv2R.CurvatureAt(crv2R.Domain[0])
                                crv2t1R = round( crv2R.NormalizedLengthParameter( 0.33, Rhino.Geometry.Interval(0, crv2R.GetLength()) )[1], 3 )
                                crv2CVmid1R = crv2R.CurvatureAt(crv2t1R)
                                crv2t2R = round( crv2R.NormalizedLengthParameter( 0.66, Rhino.Geometry.Interval(0, crv2R.GetLength()) )[1], 3 )
                                crv2CVmid2R = crv2R.CurvatureAt(crv2t2R)
                                crv2CVendR = crv2R.CurvatureAt(crv2R.Domain[1])
                                crv2TVendRR = crv2R.TangentAt(crv2R.Domain[1])
                                if ( crv1TVst.EpsilonEquals(crv2TVst, _tol) and crv1CVst.EpsilonEquals(crv2CVst, _tol) and crv1CVmid1.EpsilonEquals(crv2CVmid1, _tol) and crv1CVmid2.EpsilonEquals(crv2CVmid2, _tol) and crv1CVend.EpsilonEquals(crv2CVend, _tol) and crv1TVend.EpsilonEquals(crv2TVend, _tol) )\
                                or ( crv1TVst.EpsilonEquals(crv2TVendR, _tol) and crv1CVst.EpsilonEquals(crv2CVend, _tol) and crv1CVmid1.EpsilonEquals(crv2CVmid2, _tol) and crv1CVmid2.EpsilonEquals(crv2CVmid1, _tol) and crv1CVend.EpsilonEquals(crv2CVst, _tol) and crv1TVend.EpsilonEquals(crv2TVstR, _tol) )\
                                or ( crv1TVst.EpsilonEquals(crv2TVstRR, _tol) and crv1CVst.EpsilonEquals(crv2CVstR, _tol) and crv1CVmid1.EpsilonEquals(crv2CVmid1R, _tol) and crv1CVmid2.EpsilonEquals(crv2CVmid2R, _tol) and crv1CVend.EpsilonEquals(crv2CVendR, _tol) and crv1TVend.EpsilonEquals(crv2TVendRR, _tol) ):
                                    indx.append(i)

                            # Select only overlapped duplicated curves. Flipped ones will not be included.
                            elif _flippedCrvs == "No" and _overlapped == "Yes":
                                t1 = (nc_objs[i].Domain[0]+nc_objs[i].Domain[1])/2
                                midCrv1 = nc_objs[i].PointAt(t1)
                                t2 = (nc_objs[k].Domain[0]+nc_objs[k].Domain[1])/2
                                midCrv2 = nc_objs[k].PointAt(t2)
                                if ( midCrv1.EpsilonEquals(midCrv2, _tol) and crv1TVst.EpsilonEquals(crv2TVst, _tol) and crv1CVst.EpsilonEquals(crv2CVst, _t) and crv1CVmid1.EpsilonEquals(crv2CVmid1, _tol) and crv1CVmid2.EpsilonEquals(crv2CVmid2, _tol) and crv1CVend.EpsilonEquals(crv2CVend, _tol) and crv1TVend.EpsilonEquals(crv2TVend, _tol) ):
                                    indx.append(i)

                            # Select only overlapped duplicated curves. Flipped ones will be included too.
                            elif _flippedCrvs == "Yes" and _overlapped == "Yes":
                                crv2TVstR = Rhino.Geometry.Vector3d(crv2TVst)
                                crv2TVstR.Reverse()
                                crv2TVendR = Rhino.Geometry.Vector3d(crv2TVend)
                                crv2TVendR.Reverse()
                                crv2R = nc_objs[k].Duplicate()
                                crv2R.Reverse()
                                crv2TVstRR = crv2R.TangentAt(crv2R.Domain[0])
                                crv2CVstR = crv2R.CurvatureAt(crv2R.Domain[0])
                                crv2t1R = round( crv2R.NormalizedLengthParameter( 0.33, Rhino.Geometry.Interval(0, crv2R.GetLength()) )[1], 3 )
                                crv2CVmid1R = crv2R.CurvatureAt(crv2t1R)
                                crv2t2R = round( crv2R.NormalizedLengthParameter( 0.66, Rhino.Geometry.Interval(0, crv2R.GetLength()) )[1], 3 )
                                crv2CVmid2R = crv2R.CurvatureAt(crv2t2R)
                                crv2CVendR = crv2R.CurvatureAt(crv2R.Domain[1])
                                crv2TVendRR = crv2R.TangentAt(crv2R.Domain[1])
                                t1 = (nc_objs[i].Domain[0]+nc_objs[i].Domain[1])/2
                                midCrv1 = nc_objs[i].PointAt(t1)
                                t2 = (nc_objs[k].Domain[0]+nc_objs[k].Domain[1])/2
                                midCrv2 = nc_objs[k].PointAt(t2)
                                if ( midCrv1.EpsilonEquals(midCrv2, _tol) and crv1TVst.EpsilonEquals(crv2TVst, _tol) and crv1CVst.EpsilonEquals(crv2CVst, _t) and crv1CVmid1.EpsilonEquals(crv2CVmid1, _tol) and crv1CVmid2.EpsilonEquals(crv2CVmid2, _tol) and crv1CVend.EpsilonEquals(crv2CVend, _tol) and crv1TVend.EpsilonEquals(crv2TVend, _tol) )\
                                or ( midCrv1.EpsilonEquals(midCrv2, _tol) and crv1TVst.EpsilonEquals(crv2TVendR, _tol) and crv1CVst.EpsilonEquals(crv2CVend, _tol) and crv1CVmid1.EpsilonEquals(crv2CVmid2, _tol) and crv1CVmid2.EpsilonEquals(crv2CVmid1, _tol) and crv1CVend.EpsilonEquals(crv2CVst, _tol) and crv1TVend.EpsilonEquals(crv2TVstR, _tol) )\
                                or ( midCrv1.EpsilonEquals(midCrv2, _tol) and crv1TVst.EpsilonEquals(crv2TVstRR, _tol) and crv1CVst.EpsilonEquals(crv2CVstR, _tol) and crv1CVmid1.EpsilonEquals(crv2CVmid1R, _tol) and crv1CVmid2.EpsilonEquals(crv2CVmid2R, _tol) and crv1CVend.EpsilonEquals(crv2CVendR, _tol) and crv1TVend.EpsilonEquals(crv2TVendRR, _tol) ):
                                    indx.append(i)

        for index in indx:
            rs.SelectObject(ids[index])
        if len(indx) > 0:
            print "Found %s duplicate curves" % len(indx)
        else:
            print "No duplicate curves found"


t = 100000000
tol = sc.doc.ModelAbsoluteTolerance
ids = rs.GetObjects("Pick up the curves you would like to clean from duplicates", 4, preselect=True)
flippedCrvs = rs.GetString("Consider flipped curves too?", "No", ["Yes" , "No"])
overlapped = rs.GetString("Consider only overlapped (not those scattered around) curves?", "No", ["Yes" , "No"])
cullDuplicateCurves(ids, t, tol, flippedCrvs, overlapped)
