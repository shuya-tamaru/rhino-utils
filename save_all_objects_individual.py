#! python3
import rhinoscriptsyntax as rs

objs = rs.AllObjects()
save_path = "C:\\Users\\81803\\Desktop\\"
for obj in objs: 
    filename = obj
    rs.SelectObject(obj)
    rs.Command("_-Export "+ save_path +str(filename)+".3dm", False) 
    rs.UnselectObject(obj)
    
rs.MessageBox("Export completed!", 0, "Notification")

# This script exports all objects in the Rhino document to individual 3dm files.