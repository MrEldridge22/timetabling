import sqlite3
from staffingsheet_export_to_excel import create_excel_sheet, write_workbook
from timetable_database_interaction import createTables, read_in_v10_data, get_faculties
from staffingsheet_get_dataframes import get_df
import xlsxwriter
import json
import pandas as pd

""" 
TODO:
- UI to load tdf files, line strucutre and core groups, website?
- Optimise semester and location if statements
"""
# Debugging
pd.get_option('display.max_columns', None)
pd.set_option('display.max_rows', 200)

### VARIABLES & SWITCHES ###
# Set file location
school = False
home = True

# Year Creation
year = 2023
# Set which semester to create sheet for
semester = 2

# File Paths
# School
main_path_school    = f"V:\\Timetabler\\Current Timetable\\{year}\\V10 Files\\"
school_sem1         = f"{main_path_school}TTD_{year}_S1.tfx"
school_sem1_t2      = f"{main_path_school}TTD_{year}_S1_T2.tfx"
school_sem2         = f"{main_path_school}TTD_{year}_S2.tfx"
school_sem2_t4      = f"{main_path_school}TTD_{year}_S2_T4.tfx"
# Home
main_path_home      = f"C:\\Users\\demg\\OneDrive - Department for Education\\Documents\\Timetabling\\{year}\\V10 Files\\"
home_sem1           = f"{main_path_home}TTD_{year}_S1.tfx"
home_sem1_t2        = f"{main_path_home}TTD_{year}_S1_T2.tfx"
home_sem2           = f"{main_path_home}TTD_{year}_S2.tfx"
home_sem2_t4        = f"{main_path_home}TTD_{year}_S2_T4.tfx"

# Database setup
conn = sqlite3.connect(':memory:')
createTables(conn)
print("Database Created Sucessfully!")

# Run program with different semesters or locations
if semester == 1:
    title_heading = f"{year} Teaching Staff Semester 1"
    if school:
        sem1 = f"{main_path_school}TTD_{year}_S1.tfx"
        sem1_t2 = f"{main_path_school}TTD_{year}_S1_T2.tfx"

    elif home:
        sem1 = f"{main_path_home}TTD_{year}_S1.tfx"
        sem1_t2 = f"{main_path_home}TTD_{year}_S1_T2.tfx"

    else:
        print("You need to set school or home to true!")

    # Open the json tdx file
    with open(sem1, "r") as read_content:
        tfx_raw = json.load(read_content)
    
    # Open the json tdx file
    with open(sem1_t2, "r") as read_content:
        tfx_raw_term = json.load(read_content)
    # Read In The Data!
    read_in_v10_data(conn, tfx_raw, 1)
    read_in_v10_data(conn, tfx_raw_term, 2)
    # Create the workbook object with filename
    workbook = xlsxwriter.Workbook('Subject Allocations Semester 1.xlsx')

    # Populate excel sheet, do not pass faculty value to get_df function to get entire staff!
    create_excel_sheet(workbook, get_df(conn), sheet_name="All Staff", heading=title_heading)

    # Create separate sheets for each faculty
    for faculty in get_faculties(conn):
        if faculty not in ["Care", "Exec", "PT"]:
            create_excel_sheet(workbook, get_df(conn, faculty), sheet_name=faculty, heading=title_heading)
        else:
            pass

    # Write out the workbook
    write_workbook(workbook)

elif semester == 2:
    title_heading = f"{year} Teaching Staff Semester 2"
    if school:
        # Open the json tdx file
        with open(school_sem2, "r") as read_content:
            tfx_raw = json.load(read_content)

        # Open the json tdx file
        with open(school_sem2_t4, "r") as read_content:
            tfx_raw_term = json.load(read_content)

    elif home:
        # Open the json tdx file
        with open(home_sem2, "r") as read_content:
            tfx_raw = json.load(read_content)

        # Open the json tdx file
        with open(home_sem2_t4, "r") as read_content:
            tfx_raw_term = json.load(read_content)

    else:
        print("You need to set school or home to true!")

    # Read In The Data!
    read_in_v10_data(conn, tfx_raw, 3)
    read_in_v10_data(conn, tfx_raw_term, 4)
    # Create the workbook object with filename
    workbook = xlsxwriter.Workbook('Subject Allocations Semester 2.xlsx')

    # Populate excel sheet, do not pass faculty value to get_df function to get entire staff!
    create_excel_sheet(workbook, get_df(conn), sheet_name="All Staff", heading=title_heading)

    # Create separate sheets for each faculty
    for faculty in get_faculties(conn):
        if faculty not in ["Care", "Exec", "PT"]:
            create_excel_sheet(workbook, get_df(conn, faculty), sheet_name=faculty, heading=title_heading)
        else:
            pass

    # Write out the workbook
    write_workbook(workbook)

# Testing Area
# print(get_df(conn))
# teacher_data_df = get_df(conn)
# print(teacher_data_df[teacher_data_df["code"] == "MSK"].transpose())