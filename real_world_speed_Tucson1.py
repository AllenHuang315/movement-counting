import numpy as np
import cv2

homography_matrix_obtained = [[-14.129983186752854, -4.308301181030918, -22.749694747148201],[0.601744299539116, -0.710073840593858, -98.135620624052351],[-0.009231195347993, 0.006335739787784, 1.000000000000000]]



mat=homography_matrix_obtained
matinv=np.linalg.inv(mat)#.I

filename = "Tucson2_test"
file = open(filename+".txt")
file_w = open(filename+"_results_converted_sort.txt","w")

track_map ={}
for line in file:
	s = line.split(" ")

	if s[2] in track_map:
		track_map[s[2]].append(line)
	else:
		track_map[s[2]]= [line]


for trk in track_map:
	for i in range(len(track_map[trk])):
		s = track_map[trk][i].split(" ")
		x = int(float(s[3]))
		y = int(float(s[4]))
		w = int(float(s[5]))
		h = int(float(s[6]))
		c_x = x+w/2
		c_y = y+h/2
		point = [c_x,c_y,1]
		hh=np.dot(matinv,point)
		scalar=hh[2]
		file_w.write(track_map[trk][i].replace("-1 -1",str(hh[0]/scalar)+" "+str(hh[1]/scalar)))

track_speed = {}
file_3d = open(filename+"_results_converted_sort.txt")
for line in file_3d:
	s = line.split(" ")
	cid = s[2]
	if cid in track_speed:
		track_speed[cid].append(line)
	else:
		track_speed[cid]= [line]




from math import radians, cos, sin, asin, sqrt
 
def haversine(lon1, lat1, lon2, lat2): 
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r #* 1000

track_speed_km = {}
track_speed_mile = {}
import math
fps = 20
for trk in track_speed:
	trk_len = len(track_speed[trk])

	for i in range(trk_len):
		s1 = track_speed[trk][i].replace(" \n","").split(" ")
		s2 = track_speed[trk][-1].replace(" \n","").split(" ")

		c3d_x1 = float(s1[-2])
		c3d_y1 = float(s1[-1])

		c3d_x2 = float(s2[-2])
		c3d_y2 = float(s2[-1])

		distance = haversine(c3d_y1, c3d_x1, c3d_y2, c3d_x2)


		frameId1 = int(s1[0])
		frameId2 = int(s2[0])
		time_diff = float(frameId2-frameId1)/(3600*fps)

		#print(time_diff)
		if time_diff>0:
			speed = distance/time_diff
			print("trk: ",trk)
			print("speed KM:",speed)
			print("speed Mile:",speed /1.6)
			print("frame diff: "+str(float(frameId2-frameId1)))
			if trk in track_speed_km:
				track_speed_km[trk].append(speed)
				track_speed_mile[trk].append(speed / 1.6)
			else:
				track_speed_km[trk] = [speed]
				track_speed_mile[trk] = [speed / 1.6]
		else:
			if trk in track_speed_km:
				track_speed_km[trk].append(0.0)
				track_speed_mile[trk].append(0.0)
			else:
				track_speed_km[trk] = [0.0]
				track_speed_mile[trk] = [0.0]



file_speed_w = open(filename+"_results_converted_sort_speed.txt","w")
for trk in track_speed:
	trk_len = len(track_speed[trk])
	for i in range(trk_len):
		file_speed_w.write(track_speed[trk][i].replace("\n"," "+str(track_speed_mile[trk][i-1])+"\n"))