import rhinoscriptsyntax as rs

def clipping_toggle():
    toggle_option = rs.GetString("Do you want to enable or disable the clipping planes?", "Enable", ["Enable", "Disable"])
    
    if not toggle_option:
        print("No option selected. Exiting.")
        return

    clipping_planes = rs.ObjectsByType(536870912, True)

    if clipping_planes:
        for cp in clipping_planes:
            rs.SelectObject(cp)
            
            if toggle_option == "Enable":
                rs.Command("_-EnableClippingPlane", False)
            elif toggle_option == "Disable":
                rs.Command("_-DisableClippingPlane", False)
            
            rs.UnselectObject(cp)
    else:
        print("No clipping planes found.")

clipping_toggle()

# This script toggles the visibility of all clipping planes in the Rhino document.