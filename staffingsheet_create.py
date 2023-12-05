import sqlite3
from staffingsheet_export_to_excel import create_excel_sheet, write_workbook
from database_creation import create_tables, populate_tfx_data, get_faculties
from staffingsheet_get_dataframes import get_df
import xlsxwriter
import json
import pandas as pd

""" 
TODO:
- UI to load tdf files, line strucutre and core groups, website?
- Put in ALP program timetable similar to SWD timetable.
"""
# Debugging
pd.get_option('display.max_columns', None)
pd.set_option('display.max_rows', 200)

### VARIABLES & SWITCHES ###
# Set file location
school = True
home = False

# Year Creation
year = 2024
# Set which semester to create sheet for
semester_selected = 2

### File Paths
# School
main_path_school    = f"V:\\Timetabler\\Current Timetable\\{year}"

# Home
main_path_home      = f"C:\\Users\\demg\\OneDrive - Department for Education\\Documents\\Timetabling\\{year}"

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
    title_heading = f"{year} Teaching Staff Semester 1 v9"
    if school:
        semester_file = f"{main_path_school}{sem1}"
        term_file = f"{main_path_school}{sem1_t2}"

    elif home:
        semester_file = f"{main_path_home}{sem1}"
        term_file = f"{main_path_home}{sem1_t2}"

    else:
        print("You need to set school or home to true!")
        
    term_a = 1
    term_b = 2
    workbook = xlsxwriter.Workbook('Subject Allocations Semester 1.xlsx')

elif semester_selected == 2:
    title_heading = f"{year} Teaching Staff Semester 2 v5"
    if school:
        semester_file = f"{main_path_school}{sem2}"
        term_file = f"{main_path_school}{sem2_t4}"

    elif home:
        semester_file = f"{main_path_home}{sem2}"
        term_file = f"{main_path_home}{sem2_t4}"

    else:
        print("You need to set school or home to true!")

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
populate_tfx_data(conn, tfx_raw, term_a)
populate_tfx_data(conn, tfx_raw_term, term_b)

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
