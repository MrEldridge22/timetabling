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
- Read and highlight permanent relief classes and/or split classes, ideally show which lessons they are taking
"""
# Debugging
pd.get_option('display.max_columns', None)
pd.set_option('display.max_rows', 200)

# Set file location here
school = False
home = True

# Set which seMester to create sheet for here
semester = 1

# Database setup
conn = sqlite3.connect(':memory:')
createTables(conn)
print("Database Created Sucessfully!")

# Run Different apspects based on which application is loaded

if semester == 1:
    title_heading = "2023 Teaching Staff Semester 1"
    if school:
        # Open the json tdx file
        with open("V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\TTD_2023_S1.tfx", "r") as read_content:
            tfx_raw = json.load(read_content)
        
        # Read In The Data!
        read_in_v10_data(conn, tfx_raw)

        # Open the json tdx file
        with open("V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\TTD_2023_S1_T2.tfx", "r") as read_content:
            tfx_raw_term = json.load(read_content)
        
        # Read In The Data!
        read_in_v10_data(conn, tfx_raw_term)

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

    elif home:
        # Open the json tdx file
        with open("C:\\Users\\demg\\OneDrive - Department for Education\Documents\\Timetabling\\2023\\V10 Files\\TTD_2023_S1.tfx", "r") as read_content:
            tfx_raw = json.load(read_content)
        
        # Read In The Data!
        read_in_v10_data(conn, tfx_raw, 1)

        # Open the json tdx file
        with open("C:\\Users\\demg\\OneDrive - Department for Education\Documents\\Timetabling\\2023\\V10 Files\\TTD_2023_S1_T2.tfx", "r") as read_content:
            tfx_raw_term = json.load(read_content)
        
        # Read In The Data!
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

    else:
        print("You need to set school or home to true!")

elif semester == 2:
    title_heading = "2023 Teaching Staff Semester 2"
    if school:
        # Open the json tdx file
        with open("V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\TTD_2023_S2.tfx", "r") as read_content:
            tfx_raw = json.load(read_content)
        
        # Read In The Data!
        read_in_v10_data(conn, tfx_raw, 3)

        # Open the json tdx file
        with open("V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\TTD_2023_S2_T4.tfx", "r") as read_content:
            tfx_raw_term = json.load(read_content)
        
        # Read In The Data!
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

    elif home:
        # Open the json tdx file
        with open("C:\\Users\\demg\\OneDrive - Department for Education\Documents\\Timetabling\\2023\\V10 Files\\TTD_2023_S2.tfx", "r") as read_content:
            tfx_raw = json.load(read_content)
        
        # Read In The Data!
        read_in_v10_data(conn, tfx_raw)

        # Open the json tdx file
        with open("C:\\Users\\demg\\OneDrive - Department for Education\Documents\\Timetabling\\2023\\V10 Files\\TTD_2023_S2_T4.tfx", "r") as read_content:
            tfx_raw_term = json.load(read_content)
        
        # Read In The Data!
        read_in_v10_data(conn, tfx_raw_term)

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

    else:
        print("You need to set school or home to true!")


# Testing Area
# print(get_df(conn))