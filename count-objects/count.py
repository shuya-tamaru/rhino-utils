#! python3
import rhinoscriptsyntax as rs
import csv

def calculate_layer_stats():
    unit_system = rs.UnitSystem()
    target_unit_factor = 4
    unit_conversion_factor = rs.UnitScale(unit_system, target_unit_factor)
    
    layers = rs.LayerNames()
    if not layers:
        print("レイヤーが存在しません")
        return

    layer_stats = {}

    for layer in layers:
        objects = rs.ObjectsByLayer(layer)
        if not objects:
            continue
        
        total_area = 0.0
        total_length = 0.0
        object_count = len(objects)
        
        for obj in objects:

            if rs.IsClippingPlane(obj):
                continue
            elif rs.IsBrep(obj) or rs.IsSurface(obj):
                area = rs.SurfaceArea(obj)
                if area:
                    total_area += area[0] / (unit_conversion_factor ** 2)
            elif rs.IsCurve(obj):
                length = rs.CurveLength(obj)
                if length:
                    total_length += length / (unit_conversion_factor)
            elif rs.IsMesh(obj):
                area = rs.MeshArea(obj)
                if area:
                    total_area += area[1] / (unit_conversion_factor ** 2)

        layer_stats[layer] = {
            "total_area": total_area,
            "total_length": total_length,
            "object_count": object_count
        }
    
    save_to_csv(layer_stats)
    
    return layer_stats

def save_to_csv(layer_stats):
    file_name = rs.SaveFileName("CSVファイルを保存", "CSVファイル (*.csv)|*.csv||")
    if not file_name:
        print("ファイル保存がキャンセルされました")
        return

    headers = ["レイヤー名", "面積 (m²)", "長さ (m)", "個数"]

    try:
        with open(file_name, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)
            
            for layer, stats in layer_stats.items():
                row = [
                    layer,
                    f"{stats['total_area']:.2f}",
                    f"{stats['total_length']:.2f}",
                    stats['object_count']
                ]
                writer.writerow(row)

        print(f"CSVファイルが保存されました: {file_name}")
    except Exception as e:
        print(f"CSVファイルの保存中にエラーが発生しました: {e}")

        
calculate_layer_stats()