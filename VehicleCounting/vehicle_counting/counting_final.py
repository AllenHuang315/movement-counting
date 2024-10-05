import os
import sys
import json
import cv2
import numpy as np
import heapq
from shapely.geometry import Point, Polygon
from openpyxl import Workbook
from hausdorff_dist_average_polygram import hausdorff_distance
import pandas as pd
from tabulate import tabulate
import csv

# For 3d coordinate use only
# Convert the parsed data into a DataFrame
def create_dataframe(data):
    rows = []
    for trajectory, vehicles in data.items():
        row = {'Trajectory': trajectory, 'Sedans': vehicles.get(2, 0), 'Trucks': vehicles.get(3, 0)}
        rows.append(row)
    df = pd.DataFrame(rows)
    return df

def count_video(data_root, save_root):
    # Load movements typical trajs annotation
    cam_conf = os.path.join('C:/Users/Allen/Desktop/tracking/StrongSORT-YOLO/VehicleCounting/cam-configs/interpolation_typical_trajectory.json')
    typical_trajs = {}
    results = {}
    with open(cam_conf, 'r') as fc:
        movements = json.load(fc)
        for movement_id, movement_info in movements.items():
            tracklets = movement_info['tracklets']
            typical_trajs[movement_id] = tracklets
            results[int(movement_id)] = {}

    # Read mask image
    cam_mask = os.path.join('C:/Users/Allen/Desktop/tracking/StrongSORT-YOLO/VehicleCounting/mask/mask_update.jpg')
    mask = cv2.imread(cam_mask)
    h, w, c = mask.shape

    # Load tracks
    tracks = {}
    track_file = os.path.join(data_root, 'tracking_new.txt')
    with open(track_file, 'r') as ft:
        lines = [line.strip('\n').split(' ') for line in ft]
        for line in lines:
            frameid = int(line[0])
            trackid = int(line[1])
            lat = float(line[3])
            lon = float(line[4])
            label = line[2]
            if trackid in tracks:
                tracks[trackid]['endframe'] = frameid
                tracks[trackid]['bbox'].append([frameid, lat, lon, label])
                tracks[trackid]['tracklet'].append([lat, lon])
            else:
                tracks[trackid] = {'startframe': frameid,
                                   'endframe': frameid,
                                   'bbox': [[frameid, lat, lon, label]],
                                   'tracklet': [[lat, lon]]}

    trackids = sorted(tracks.keys())

    # Save count results
    os.makedirs(save_root, exist_ok=True)
    savefile = os.path.join(save_root, 'counting.txt')
    savefile_qgis = os.path.join(save_root, 'qgis.txt')
    csv_output_file = os.path.join(save_root, 'counting.csv')

    # Start counting
    qgis = []
    print("processing...")
    for trackid in trackids:
        track_traj = tracks[trackid]['tracklet']
        if len(track_traj) > 20:
            typical_trajectory_distance = []
            for m_id, m_t in typical_trajs.items():
                movement = int(m_id)
                typical_traj_tracklet = m_t[0]
                average_dist = hausdorff_distance(track_traj, typical_traj_tracklet)
                heapq.heappush(typical_trajectory_distance, [average_dist, movement])
            
            dis, movement_id = heapq.heappop(typical_trajectory_distance)
            label = int(tracks[trackid]['bbox'][0][-1])
            if label not in results[movement_id]:
                results[movement_id][label] = 0
            results[movement_id][label] += 1
            qgis.append([movement_id, trackid, track_traj])

    # Save gt & vehicle counting result
    print(results)
    with open(savefile, 'w') as dst_out:
        for row_key, inner_dict in results.items():
            row_str = f"{row_key}: {inner_dict}"
            dst_out.write(row_str + '\n')
    print('vehicle counting done.')

    with open(savefile_qgis, 'w') as dst_out:
        for row in qgis:
            row_str = ' '.join(map(str, row))
            dst_out.write(row_str + '\n')
    print('qgis counting done.')

    # Convert qgis_integrate.txt to CSV
    qgis_data = []
    with open(savefile_qgis, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(' ')
            movement_id = int(parts[0])
            track_id = int(parts[1])
            coordinates = eval(' '.join(parts[2:])) 
            for point in coordinates:
                qgis_data.append((movement_id, track_id, point[0], point[1]))

    # Write to CSV file
    csv_output_file_qgis = os.path.join(save_root, 'qgis.csv')
    with open(csv_output_file_qgis, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['movement_id', 'track_id', 'latitude', 'longitude'])
        for row in qgis_data:
            writer.writerow(row)

    # Convert results to DataFrame and save as CSV
    df = create_dataframe(results)
    df.to_csv(csv_output_file, index=False)
    print(f"CSV output has been saved to '{csv_output_file}'")
    print(f"CSV output from QGIS data has been saved to '{csv_output_file_qgis}'")

if __name__ == '__main__':
    data_root = 'C:/Users/Allen/Desktop/tracking/StrongSORT-YOLO/VehicleCounting'
    save_root = 'C:/Users/Allen/Desktop/tracking/StrongSORT-YOLO/VehicleCounting/counting_result'
    count_video(data_root, save_root)
