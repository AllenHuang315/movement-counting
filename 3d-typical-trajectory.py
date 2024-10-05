import numpy as np
import json

# 读取homography matrix
homography_matrix_obtained = [[-14.129983186752854, -4.308301181030918, -22.749694747148201],
                              [0.601744299539116, -0.710073840593858, -98.135620624052351],
                              [-0.009231195347993, 0.006335739787784, 1.0]]
mat = np.array(homography_matrix_obtained)
matinv = np.linalg.inv(mat)

# 读取JSON文件
filename = "cam.json"
with open(filename) as f:
    data = json.load(f)

# 执行转换并写入结果
filename_results = filename.split('.')[0] + "_results_converted.json"
with open(filename_results, "w") as file_w:
    for movement_key, movement in data.items():
        transformed_movement = {}
        # 转换src中的point_1和point_2
        src = movement['src']
        src_points = {'point_1': [], 'point_2': []}
        for key, value in src.items():
            c_x, c_y = value[0], value[1]
            point = [c_x, c_y, 1]
            hh = np.dot(matinv, point)
            scalar = hh[2]
            transformed_point = [hh[0] / scalar, hh[1] / scalar]
            src_points[key] = transformed_point
        transformed_movement['src'] = src_points
        
        # 转换dst中的point_1和point_2
        dst = movement['dst']
        dst_points = {'point_1': [], 'point_2': []}
        for key, value in dst.items():
            c_x, c_y = value[0], value[1]
            point = [c_x, c_y, 1]
            hh = np.dot(matinv, point)
            scalar = hh[2]
            transformed_point = [hh[0] / scalar, hh[1] / scalar]
            dst_points[key] = transformed_point
        transformed_movement['dst'] = dst_points
        
        # 转换tracklets中的所有坐标
        transformed_tracklets = []
        for tracklet in movement['tracklets']:
            transformed_tracklet = []
            for point in tracklet:
                c_x, c_y = point[0], point[1]
                point = [c_x, c_y, 1]
                hh = np.dot(matinv, point)
                scalar = hh[2]
                transformed_point = [hh[0] / scalar, hh[1] / scalar]
                transformed_tracklet.append(transformed_point)
            transformed_tracklets.append(transformed_tracklet)
        transformed_movement['tracklets'] = transformed_tracklets
        
        # 将转换后的数据写入文件，并添加换行符
        file_w.write(json.dumps({movement_key: transformed_movement}) + '\n')
