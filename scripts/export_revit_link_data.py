import clr
import csv
import math
import os
from datetime import datetime

# Import Revit Services
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

# Import Revit API
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

def get_link_base_point(link_instance, link_transform):
    """
    Gets the project base point (not shared) from the linked document,
    transformed into the host model's coordinate system.
    """
    link_doc = link_instance.GetLinkDocument()
    if link_doc is not None:
        collector = FilteredElementCollector(link_doc).OfClass(BasePoint)
        for base_point in collector:
            if not base_point.IsShared:
                link_base_point_in_link = base_point.Position
                link_base_point_in_host = link_transform.OfPoint(link_base_point_in_link)
                return link_base_point_in_host
    return None

# Input from Dynamo
file_path = r'\\arcadis-nl.local\dfs\ADPS_PJ\Philadelphia\PPR_Proj\2024\D24PA044\05 Design\14 Drawings\01 WIP\13 BIM Mgr\Clarity\Scripts\Output\revit_link_data.csv'

# Get active document
doc = DocumentManager.Instance.CurrentDBDocument

# Get all RevitLinkInstance elements
collector = FilteredElementCollector(doc).OfClass(RevitLinkInstance)
link_instances = list(collector)
non_nested_link_instances = []

for link in link_instances:
    type_id = link.GetTypeId()
    element = doc.GetElement(type_id)

    if isinstance(element, RevitLinkType):
        revit_link_type = element

        if not revit_link_type.IsNestedLink:
            non_nested_link_instances.append(link)

# Get project's angle to True North (in radians)
project_location = doc.ActiveProjectLocation
project_position = project_location.GetProjectPosition(XYZ(0,0,0))
angle_to_true_north_rad = project_position.Angle

header = ["Document Title", "Link Name", "Workset Name", "Pinned", "Origin X", "Origin Y", "Origin Z", "Angle to True North (deg)", "Date and Time"]
data_rows = []

for link_inst in non_nested_link_instances:
    try:
        link_name = link_inst.Name
    except:
        link_name = "Unknown"
    
    # Get pinned property
    pinned = link_inst.Pinned

    # Get workset
    ws_id = link_inst.WorksetId
    ws = doc.GetWorksetTable().GetWorkset(ws_id)
    ws_name = ws.Name if ws else "None"
    
    # Get transform and base point
    transform = link_inst.GetTransform()
    base_point = get_link_base_point(link_inst, transform)

    if base_point:
        x = base_point.X
        y = base_point.Y
        z = base_point.Z
    else:
        x, y, z = None, None, None

    # Get angle to true north
    basisX = transform.BasisX
    link_angle_rad = math.atan2(basisX.Y, basisX.X)
    angle_true_north_rad = link_angle_rad + angle_to_true_north_rad
    angle_true_north_deg = math.degrees(angle_true_north_rad)
    revised_angle_deg = (360 - angle_true_north_deg) % 360

    # Get current date and time
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Add data
    data_rows.append([doc.Title, link_name, ws_name, pinned, x, y, z, revised_angle_deg, date_time])

# Only export headers if the file does NOT exist
try:
    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(header)
        for row in data_rows:
            writer.writerow(row)
    result = "CSV appended to: " + file_path
except Exception as e:
    result = "Error: " + str(e)

OUT = result