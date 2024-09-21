import rhinoscriptsyntax as rs

def assign_material_color_to_layer():
    layers = rs.LayerNames()
    if layers:
        for layer in layers:
            materialIndex = rs.LayerMaterialIndex(layer)
            if materialIndex != -1:
                materialColor = rs.MaterialColor(materialIndex)
                if materialColor:
                    rs.LayerColor(layer, materialColor)
                    print(f"Set the color of layer '{layer}' to {materialColor}.")
            else:
                rs.LayerColor(layer, (0, 0, 0))

assign_material_color_to_layer()

# This script assigns the color of the material assigned to each layer to the layer itself.