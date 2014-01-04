#*******************************************************************#
#********* Surfaces/polysurfaces/extrusions height labeling ********#
#********* by Djordje Spasic ***************************************#
#********* issworld2000@yahoo.com  24-12-2013 **********************#
"""
Function populates surfaces, polysurfaces and extrusions with projected regular grid of points,
and assign it's elevation as annotation text dot
"""

import rhinoscriptsyntax as rs

def surfacePointHeight(ptsInU,ptsInV):
    if ptsInU and ptsInV:
        # selecting, creating a top surface of a boundingbox
        select = rs.Command("_SelSrf ")
        select = rs.Command("_SelPolysrf ")
        select = rs.Command("_SelExtrusion ")
        allSrfPlsrf = rs.GetObjects("",0,False,True,False)
        if allSrfPlsrf:
            rs.EnableRedraw(False)
            boxPts = rs.BoundingBox(allSrfPlsrf)
            rectanglePts = boxPts[-4:]
            rectanglePts.append(boxPts[-4])
            rectangle = rs.AddPolyline(rectanglePts)
            srf = rs.AddPlanarSrf(rectangle)
            rs.DeleteObject(rectangle)
            centroid = rs.SurfaceAreaCentroid(srf)
            srfScaled = rs.ScaleObject(srf,centroid[0],[0.95,0.95,0.95])

            # generating points on top surface
            domainU = rs.SurfaceDomain(srfScaled, 0)
            domainV = rs.SurfaceDomain(srfScaled, 1)
            uRange = domainU[1]-domainU[0]
            vRange = domainV[1]-domainV[0]
            stepU = uRange/(ptsInU - 1)
            stepV = vRange/(ptsInV - 1)
            startDomainU = domainU[0]
            startDomainV = domainV[0]
            uvList = []
            for i in range(ptsInU):
                u =  startDomainU + i*stepU
                for j in range(ptsInV):
                    v = startDomainV + j*stepV
                    uvList.append([u,v])
            ptsHorz = []
            for uv in uvList:
                pt = rs.EvaluateSurface(srfScaled, uv[0], uv[1])
                pt_id = rs.AddPoint(pt)
                ptsHorz.append(pt_id)
            rs.DeleteObject(srfScaled)

            # projecting points to lower srfs,polysrfs and extrusions
            ptsProj = rs.ProjectPointToSurface(ptsHorz, allSrfPlsrf, [0,0,-1])
            rs.DeleteObjects(ptsHorz)
            for ptProj in ptsProj:
                text = ptProj[2]
                text = "%1.0f" % text
                ptZ = rs.AddTextDot(text,ptProj)
                pt_id = rs.AddPoint(ptProj)
                rs.AddLayer("TextDot")
                rs.ObjectLayer(ptZ,"TextDot")
                rs.AddLayer("Point_Z",[0,120,255])
                rs.ObjectLayer(pt_id,"Point_Z")
                rs.Redraw()

        else:
            print "Something went wrong. You probably do not have any surfaces, polysurfaces or extrusions"
            return
    else:
        print "You did not enter the number of points in X and/or Y direction"
        return


# function input
x = rs.GetInteger("How many points in X direction do you want")
y = rs.GetInteger("How many points in Y direction do you want?")

# function call
surfacePointHeight(x,y)
