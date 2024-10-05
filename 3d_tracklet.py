import numpy as np

# 定义逆变换矩阵
homography_matrix_obtained = np.array([[-8.640241200711051, -1.852249245716560, 72.845386861406297],
                                       [-0.072187165053932, -0.655624944002555, -70.389620986685799],
                                       [-0.011014684788151, 0.005817765928659, 1.000000000000000]])

# 定义坐标转换函数
def transform_point(point, matrix):
    matrix1 = np.linalg.inv(matrix)
    homogeneous_point = np.array([point[0], point[1], 1])
    transformed_point = np.dot(matrix1, homogeneous_point)
    transformed_point /= transformed_point[2]  # 归一化
    return transformed_point[:2]

# 读取JSON文件
import json

with open('new_tucson_2.json') as f:
    data = json.load(f)

# 对每个movement进行处理
for movement, info in data.items():
    src_point_1 = info['src']['point_1']
    #print(src_point_1)
    src_point_2 = info['src']['point_2']
    dst_point_1 = info['dst']['point_1']
    dst_point_2 = info['dst']['point_2']

    # 对src和dst进行坐标转换
    src_point_1_3d = transform_point(src_point_1, homography_matrix_obtained)
    src_point_2_3d = transform_point(src_point_2, homography_matrix_obtained)
    dst_point_1_3d = transform_point(dst_point_1, homography_matrix_obtained)
    dst_point_2_3d = transform_point(dst_point_2, homography_matrix_obtained)

    # 更新JSON中的src和dst坐标
    data[movement]['src']['point_1'] = src_point_1_3d.tolist()
    data[movement]['src']['point_2'] = src_point_2_3d.tolist()
    data[movement]['dst']['point_1'] = dst_point_1_3d.tolist()
    data[movement]['dst']['point_2'] = dst_point_2_3d.tolist()

    # 对tracklets进行坐标转换
    for i, tracklet in enumerate(info['tracklets']):
        transformed_tracklet = [transform_point(point, homography_matrix_obtained).tolist() for point in tracklet]
        data[movement]['tracklets'][i] = transformed_tracklet

# 将更新后的数据保存回JSON文件
with open('new_tucson_2_3d.json', 'w') as f:
    json.dump(data, f, indent=4)
