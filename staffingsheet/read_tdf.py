import xml.etree.ElementTree as ET
import sqlite3
from database_interaction import *
from get_dataframes import *
from export_to_excel import *
import xlsxwriter
import pandas as pd

""" 
TODO:
- UI to load tdf files, line strucutre and core groups
- Teacher Loads
- Notes for Early Career Teachers, Leaders etc.
- Year 12 Extra Lesson
"""

# Database setup
try:
    conn = sqlite3.connect(':memory:')
    createTables(conn)
    print("Database Created Sucessfully!")
except:
    print("Database failed to create, exiting!")
    quit()

# Open tdf File, encoded in xml anyway.
tdf_semester = ET.parse('staffingsheet\TTDS2-2022.tdf9')
# Get the root element
root_semester = tdf_semester.getroot()

tdf_term = ET.parse('staffingsheet\TTDTerm4-2022.tdf9')
room_term = tdf_term.getroot()

# populate database
read_in_data(conn, root_semester)
print("Read in Semester Data")
read_in_data(conn, room_term)
print("Read in Term Data")

# Create the workbook object with filename
workbook = xlsxwriter.Workbook('Subject Allocations.xlsx')

# Populate excel sheet, do not pass faculty value to get_df function to get entire staff!
all_staff = get_df(conn)
create_excel_sheet(workbook, all_staff, "All Staff")

# Create separate sheets for each faculty
for faculty in get_faculties(conn):
    if faculty not in ["Care", "Exec"]:
        create_excel_sheet(workbook, get_df(conn, faculty), faculty)
    else:
        pass

# Write out the workbook
write_workbook(workbook)

# Testing area
