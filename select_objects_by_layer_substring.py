import rhinoscriptsyntax as rs

def select_objects_by_layer_substring():
    substring = rs.StringBox("Please enter the substring to search in layer names", "Search String", "Layer Search")
    if not substring:
        print("canceled")
        return

    layers = rs.LayerNames()
      
    target_layers = [layer for layer in layers if substring in layer]
    
    for layer in target_layers:
        layer_objects = rs.ObjectsByLayer(layer)
        
        if layer_objects:
            rs.SelectObjects(layer_objects)

select_objects_by_layer_substring()

# This script allows the user to select all objects from layers whose names contain a specified substring. 
# The user is prompted to input the substring, and the script searches for layers with matching names. 
# It then selects all objects from the matched layers in Rhino.

