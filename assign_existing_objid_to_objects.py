# Get the ObjectId and set the value to UserText. It is saved in the form of {id: ObjectId}.

import rhinoscriptsyntax as rs

def assign_existing_objid_to_objects():
    objs = rs.GetObjects("Select objects to assign existing objId", preselect=True)
    if not objs:
        print("No objects selected.")
        return
    
    for obj in objs:
        obj
        rs.SetUserText(obj, "id", obj)
        print(f"Assigned existing objId {obj} to object {obj}")

assign_existing_objid_to_objects()

