using System;
using System.Collections.Generic;
using System.IO;
using Rhino;
using Rhino.DocObjects;

public class ScriptInstance
{
    private static double GetUnitConversionFactor(UnitSystem targetUnitSystem)
    {
        var modelUnitSystem = RhinoDoc.ActiveDoc.ModelUnitSystem;
        return RhinoMath.UnitScale(modelUnitSystem, targetUnitSystem);
    }

    private static string GetLayerFullPath(Rhino.DocObjects.Layer layer)
    {
        if (layer.ParentLayerId == Guid.Empty)
            return layer.Name;
        
        var parentLayer = RhinoDoc.ActiveDoc.Layers.FindId(layer.ParentLayerId);
        return GetLayerFullPath(parentLayer) + "::" + layer.Name;
    }

    private static void SaveResultsToCsv(string filePath, List<(string LayerName, double TotalArea, double TotalLength, int ObjectCount)> results)
    {
        using (var writer = new StreamWriter(filePath))
        {
            writer.WriteLine("レイヤ名,面積 (m²),長さ (m),個数");

            foreach (var result in results)
            {
                writer.WriteLine($"{result.LayerName},{result.TotalArea:F2},{result.TotalLength:F2},{result.ObjectCount}");
            }
        }
    }

    public static void Main()
    {
        var targetUnitSystem = UnitSystem.Meters;
        double unitConversionFactor = GetUnitConversionFactor(targetUnitSystem);
  
        var layers = RhinoDoc.ActiveDoc.Layers;
        if (layers.Count == 0)
        {
            RhinoApp.WriteLine("レイヤーが存在しません。");
            return;
        }

        var results = new List<(string LayerName, double TotalArea, double TotalLength, int ObjectCount)>();

        foreach (var layer in layers)
        {
            
            if (layer.IsDeleted) continue;

            string layerFullPath = GetLayerFullPath(layer);
            var objects = RhinoDoc.ActiveDoc.Objects.FindByLayer(layer);
            if (objects.Length == 0) continue;

            double totalArea = 0.0;
            double totalLength = 0.0;
            int objectCount = objects.Length;

            foreach (var obj in objects)
            {
                var geometry = obj.Geometry;

                if (geometry is Rhino.Geometry.ClippingPlaneSurface){
                    RhinoApp.WriteLine("Clipping PLaneをSkipしました。");
                    continue;
                } 
                else if (geometry is Rhino.Geometry.Curve curve)
                {
                    var length = curve.GetLength() * unitConversionFactor;
                    totalLength += length;
                    continue;
                } 
                else if (geometry is Rhino.Geometry.Brep brep)
                {
                    var area = brep.GetArea();
                    totalArea += area * Math.Pow(unitConversionFactor, 2);
                    continue;
                }
                else if (geometry is Rhino.Geometry.Extrusion extrusion)
                {
                    var area = extrusion.ToBrep().GetArea();
                    totalArea += area * Math.Pow(unitConversionFactor, 2);
                    continue;
                }
                else if (geometry is Rhino.Geometry.Mesh mesh)
                {
                    var area = Rhino.Geometry.AreaMassProperties.Compute(mesh).Area;
                    totalArea += area * Math.Pow(unitConversionFactor, 2);
                    continue;
                }      
                else
                {
                    Console.WriteLine($"レイヤー: {layerFullPath}に計算外のオブジェクトが存在しました。確認してください！！！！！！オブジェクトタイプは{geometry.ObjectType}です！");
                }
            }

            results.Add((layerFullPath, totalArea, totalLength, objectCount));            
        }

        var fd = new Rhino.UI.SaveFileDialog
        {
            Title = "Save CSV File",
            Filter = "CSV Files (*.csv)|*.csv|All Files (*.*)|*.*",
            DefaultExt = "csv"
        };

        if (fd.ShowDialog() == System.Windows.Forms.DialogResult.OK)
        {
            string path = fd.FileName;
            RhinoApp.WriteLine($"Selected path: {path}");
            SaveResultsToCsv(fd.FileName, results);
        }

    }
}

ScriptInstance.Main();
