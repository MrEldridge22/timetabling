import sqlite3
from staffingsheet_export_to_excel import create_excel_sheet, write_workbook
from database_interaction import create_tables, read_in_tfx_data, get_faculties
from staffingsheet_get_dataframes import get_df
import xlsxwriter
import json
import pandas as pd
from pathlib import Path
import sys


""" 
TODO:
- UI to load tdf files, line strucutre and core groups, website?
- Put in ALP program timetable similar to SWD timetable.
- Recalculate Load Column
- Need to have a switch or something for making a term output sheet, for example using semester 1 but
    outputting for term 2

"""
# Debugging
pd.get_option('display.max_columns', None)
pd.set_option('display.max_rows', 200)
pd.set_option("future.no_silent_downcasting", True)


### VARIABLES & SWITCHES ###

# Year Creation
year = 2025

# Set which semester to create sheet for
semester_selected = int(input("Enter 1 for Semester 1 or 2 for Semester 2: "))
title_heading = f"{year} Teaching Staff Semester {semester_selected} DRAFT 1"

""" File Paths """
# School
main_path_school      = f"V:\\Timetabler\\Current Timetable\\{year}"

# Laptop OneDrive
main_path_laptop      = f"C:\\Users\\deldridge\\OneDrive - Department for Education\\Documents\\Timetabling\\{year}"

# Desktop OneDrive
main_path_desktop     = f"C:\\Users\\demg\\OneDrive - Department for Education\\Documents\\Timetabling\\{year}"

# Check if the path exists and set the file path, make it easier to switch between locations.
try:
    if Path(main_path_school).exists():
        filePath = main_path_school
        
    elif Path(main_path_laptop).exists():
        filePath = main_path_laptop
    
    elif Path(main_path_desktop).exists():
        filePath = main_path_desktop

    print(f"Using the following Timetabling Location: {filePath}")

except: 
    print("Timetabling Folder Can Not Be Found!")
    sys.exit(1)


# Semester & Term file names
sem1         = f"\\TTD_{year}_S1.tfx"
sem1_t2      = f"\\TTD_{year}_S1_T2.tfx"
sem2         = f"\\TTD_{year}_S2.tfx"
sem2_t4      = f"\\TTD_{year}_S2_T4.tfx"

# Database setup
conn = sqlite3.connect(':memory:')
create_tables(conn)
print("Database Created Sucessfully!")

# Run program with different semesters or locations
if semester_selected == 1:
    semester_file = f"{filePath}{sem1}"
    term_file = f"{filePath}{sem1_t2}"

    term_a = 1
    term_b = 2
    workbook = xlsxwriter.Workbook('Subject Allocations Semester 1.xlsx')

elif semester_selected == 2:
    semester_file = f"{filePath}{sem2}"
    term_file = f"{filePath}{sem2_t4}"

    # Set semester and term values for creating the T1-T4 subject names.
    term_a = 3
    term_b = 4
    workbook = xlsxwriter.Workbook('Subject Allocations Semester 2.xlsx')

# Open the semester based json tdx file
with open(semester_file, "r") as read_content:
    tfx_raw = json.load(read_content)

# Open the term based json tdx file
with open(term_file, "r") as read_content:
    tfx_raw_term = json.load(read_content)

# Read In The Data!
read_in_tfx_data(conn, tfx_raw, term_a)    
read_in_tfx_data(conn, tfx_raw_term, term_b)

# Populate excel sheet, do not pass faculty value to get_df function to get entire staff!
create_excel_sheet(workbook, get_df(conn), sheet_name="All Staff", heading=title_heading)

# # Create separate sheets for each faculty
for faculty in get_faculties(conn):
    if faculty not in ["Care", "Exec", "PT"]:
        create_excel_sheet(workbook, get_df(conn, faculty), sheet_name=faculty, heading=title_heading)
    else:
        pass

# Write out the workbook
write_workbook(workbook)

# Testing Area

