#! python 3
import Rhino
import rhinoscriptsyntax as rs
import os
import System.IO
import System.Windows.Forms as Forms

def select_file(title="ファイルを選択", filter="Grasshopperファイル (*.gh)|*.gh"):
    dialog = Forms.OpenFileDialog()
    dialog.Title = title
    dialog.Filter = filter
    dialog.Multiselect = False
    
    if dialog.ShowDialog() == Forms.DialogResult.OK:
        return dialog.FileName
    return None

def select_folder(title="フォルダを選択"):
    dialog = Forms.FolderBrowserDialog()
    dialog.Description = title
    dialog.ShowNewFolderButton = True
    
    if dialog.ShowDialog() == Forms.DialogResult.OK:
        return dialog.SelectedPath
    return None

def initialize_grasshopper():
    gh = Rhino.RhinoApp.GetPlugInObject("Grasshopper")
    gh.LoadEditor()
    gh.CloseAllDocuments()
    gh.ShowEditor()
    gh.OpenDocument(gh_file_path)
    return gh

def cleanup_grasshopper(gh):
    gh.CloseAllDocuments()

def process_ply_files():
    gh = initialize_grasshopper()
    
    ply_files = [os.path.join(point_clouds_dir, f) for f in os.listdir(point_clouds_dir) 
                if f.lower().endswith('.ply')]
    file_length = len(ply_files)

    if file_length == 0:
        print(f"指定されたフォルダ '{point_clouds_dir}' に PLY ファイルが見つかりませんでした。")
        cleanup_grasshopper(gh)
        return

    for i, ply_file in enumerate(ply_files):
        progress = round(((i) / file_length) * 100, 2)
        
        file_name = System.IO.Path.GetFileName(ply_file)
        print(f"処理中: {file_name} ({progress}%)")

        import_cmd = f"_-Import \"{ply_file}\" _Enter"
        rs.Command(import_cmd)
        imported_obj = rs.LastCreatedObjects()
        
        if imported_obj:
            if isinstance(imported_obj, list):
                obj_id = imported_obj[0]
            else:
                obj_id = imported_obj
                
            gh.AssignDataToParameter("execute", True)
            gh.AssignDataToParameter("point_cloud_guid", obj_id)
            gh.RunSolver(True)
            gh.AssignDataToParameter("point_cloud_guid", None)

            rs.DeleteObject(obj_id)

    print("すべてのファイルの処理が完了しました (100%)")
    cleanup_grasshopper(gh)

if __name__ == "__main__":
    
    gh_file_path = select_file("Grasshopperファイルを選択")
    if not gh_file_path:
        print("Grasshopperファイルが選択されていません。処理を中止します。")
        exit()
        
    point_clouds_dir = select_folder("PLYファイルを含むフォルダを選択")
    if not point_clouds_dir:
        print("フォルダが選択されていません。処理を中止します。")
        exit()
    
    process_ply_files()