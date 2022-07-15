import xml.etree.ElementTree as ET
import sqlite3
from staffingsheet_export_to_excel import create_excel_sheet, write_workbook
from timetable_database_interaction import get_v9_fte, createTables, read_in_v9_data, read_in_v10_data, get_faculties
from staffingsheet_get_dataframes import get_df
import xlsxwriter
import json
import pandas as pd

""" 
TODO:
- UI to load tdf files, line strucutre and core groups
- Convert to V10 Files
"""

# Which version of Timetable Solutions are you using?
v9 = False
v10 = True

# Database setup
try:
    conn = sqlite3.connect(':memory:')
    createTables(conn)
    print("Database Created Sucessfully!")
except:
    print("Database failed to create, exiting!")
    quit()

# Run Different apspects based on which application is loaded
if v9:
    print("Using Verion 9 of Timetable Solutions")
    
    # Open tdf File, encoded in xml anyway.
    tdf_semester = ET.parse('staffingsheet\TTDS2-2022.tdf9')
    # Get the root element
    root_semester = tdf_semester.getroot()

    tdf_term = ET.parse('staffingsheet\TTDTerm4-2022.tdf9')
    room_term = tdf_term.getroot()

    # populate database
    try:
        read_in_v9_data(conn, root_semester)
        print("Read in Semester Data")
        read_in_v9_data(conn, room_term)
        print("Read in Term Data")
    except:
        print(sqlite3.Error)
        quit()

    # Create the workbook object with filename
    workbook = xlsxwriter.Workbook('staffing_sheet_output\Subject Allocations.xlsx')

    # Populate excel sheet, do not pass faculty value to get_df function to get entire staff!
    create_excel_sheet(workbook, get_df(conn), get_v9_fte(root_semester), "All Staff")

    # Create separate sheets for each faculty
    for faculty in get_faculties(conn):
        if faculty not in ["Care", "Exec"]:
            create_excel_sheet(workbook, get_df(conn, faculty), get_v9_fte(root_semester), faculty)
        else:
            pass

    # Write out the workbook
    write_workbook(workbook)

elif v10:
    print("Using Verion 10 of Timetable Solutions")
    # Open the json tdx file
    with open('ttd_files\TTDS2-2022.tfx', "r") as read_content:
        tfx_raw = json.load(read_content)
    
    read_in_v10_data(conn, tfx_raw)

else:
    print("You need to ensure either V9 or V10 is set to True!")



# # Create the workbook object with filename
# workbook = xlsxwriter.Workbook('staffing_sheet_output\Subject Allocations.xlsx')

# # Populate excel sheet, do not pass faculty value to get_df function to get entire staff!
# create_excel_sheet(workbook, get_df(conn), database_interaction.get_v9_fte(root_semester), "All Staff")

# # Create separate sheets for each faculty
# for faculty in database_interaction.get_faculties(conn):
#     if faculty not in ["Care", "Exec"]:
#         create_excel_sheet(workbook, get_df(conn, faculty), database_interaction.get_v9_fte(root_semester), faculty)
#     else:
#         pass

# # Write out the workbook
# write_workbook(workbook)

# Testing area
tf_df = pd.json_normalize(tfx_raw, ['Faculties', "FacultyTeachers"], ['Faculties', "FacultyID"])

print(tf_df)