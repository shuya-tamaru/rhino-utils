import rhinoscriptsyntax as rs
import json

def load_and_modify_objects(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    for item in data:
        mesh_id = item['meshId']
        obj = rs.coerceguid(mesh_id)
        
        if obj:
            if 'moveVector' in item:
                move_vector = item['moveVector']
                move_x = move_vector['x'] * 1000
                move_y = move_vector['z'] * -1000 
                move_z = move_vector['y'] * 1000
                rs.MoveObject(obj, [move_x, move_y, move_z])

            if 'userText' in item:
                user_text = item['userText']
                key = user_text['key']
                value = user_text['value']
                rs.SetUserText(obj, key, value)
        else:
            print(f"Object with meshId {mesh_id} not found.")

json_path = "json file path"
load_and_modify_objects(json_path)

# Synchronize Web and Rhino data by loading a JSON file containing data about objects in the Rhino document.
# This script loads a JSON file containing data about objects in the Rhino document.
# https://gltf.styublog.com/