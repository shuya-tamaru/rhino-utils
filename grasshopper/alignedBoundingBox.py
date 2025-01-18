# Grasshopperからメッシュの頂点リストをmesh_verticesとして受け取る
import numpy as np
import Rhino.Geometry as rg


# 入力：Grasshopperからのメッシュ頂点リスト
points = [v.Value for v in mesh_vertices]
vertices = np.array([[p.X, p.Y, p.Z] for p in points])

# 1. 平均を計算して中心化
mean = np.mean(vertices, axis=0)
centered_vertices = vertices - mean

# 2. 共分散行列を計算
cov_matrix = np.cov(centered_vertices.T)

# 3. 固有値と固有ベクトルを計算
eig_values, eig_vectors = np.linalg.eig(cov_matrix)

# 4. 固有値で降順ソートして主成分を取得
sorted_indices = np.argsort(-eig_values)
principal_axes = eig_vectors[:, sorted_indices]

# 5. 主成分に射影してOBBの範囲を計算
projected_data = centered_vertices @ principal_axes
min_vals = np.min(projected_data, axis=0)
max_vals = np.max(projected_data, axis=0)

# 6. OBBの頂点をローカル座標系で生成
obb_vertices_local = np.array([
    [min_vals[0], min_vals[1], min_vals[2]],
    [max_vals[0], min_vals[1], min_vals[2]],
    [max_vals[0], max_vals[1], min_vals[2]],
    [min_vals[0], max_vals[1], min_vals[2]],
    [min_vals[0], min_vals[1], max_vals[2]],
    [max_vals[0], min_vals[1], max_vals[2]],
    [max_vals[0], max_vals[1], max_vals[2]],
    [min_vals[0], max_vals[1], max_vals[2]],
])

# 7. ローカル座標をワールド座標に変換
obb_vertices_world = obb_vertices_local @ principal_axes.T + mean
obb_points = [rg.Point3d(x, y, z) for x, y, z in obb_vertices_world]

corrected_obb_points = []
for obb_point in obb_vertices_world:
    # 最近傍の距離とインデックスを探す
    closest_distance = float("inf")
    closest_point = None
    for vertex in vertices:
        distance = np.linalg.norm(vertex - obb_point)
        if distance < closest_distance:
            closest_distance = distance
            closest_point = vertex
    # 最近傍点をOBBの頂点として使用
    corrected_obb_points.append(rg.Point3d(*closest_point))

# 8. 面を作成するための頂点ペア
face_indices = [
    [0, 1, 2, 3],  # 底面
    [4, 5, 6, 7],  # 上面
    [0, 1, 5, 4],  # 側面1
    [1, 2, 6, 5],  # 側面2
    [2, 3, 7, 6],  # 側面3
    [3, 0, 4, 7],  # 側面4
]

# 9. 各面を作成
brep_faces = []
for indices in face_indices:
    corners = [corrected_obb_points [i] for i in indices]
    corners.append(corners[0])  # 始点を閉じる
    polyline = rg.Polyline(corners)
    brep_faces.append(rg.Brep.CreateFromCornerPoints(
        polyline[0], polyline[1], polyline[2], polyline[3], 0.01))

# 10. 面を結合して閉じたBrepを作成
obb_brep = rg.Brep.JoinBreps(brep_faces, 0.01)[0]

# Grasshopperへの出力
obb_vertices_output = corrected_obb_points   # OBBの頂点
obb_brep_output = obb_brep        # OBBの形状

# 出力
obb_vertices = obb_vertices_output  # 頂点リスト
obb_brep = obb_brep_output          # 閉じたOBB
