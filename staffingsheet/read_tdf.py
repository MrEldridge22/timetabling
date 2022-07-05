import xml.etree.ElementTree as ET
import sqlite3
from database_interaction import *
from get_dataframes import *
from export_to_excel import *
import xlsxwriter

import pandas as pd

""" 
TODO:
- Sort into lines - DONE!
- Read in Term 2 / 4 data
- Output to Excel sheet - All Staff Done!
- Output Faculty tabs into Excel Sheet - Done
- Fix SWD Lines - DONE!
- Get Class Groups for Core Lines - Done!
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
tdf = ET.parse('staffingsheet\TTDS2-2022.tdf9')
# Get the root element
root = tdf.getroot()

# populate database
read_in_data(conn, root)

# Create the workbook object with filename
workbook = xlsxwriter.Workbook('Subject Allocations.xlsx')

# Populate excel sheet, do not pass faculty value to get_df function to get entire staff!
all_staff = get_df(conn)
create_excel_sheet(workbook, all_staff, "All Staff")

for faculty in get_faculties(conn):
    if faculty != "Care":
        create_excel_sheet(workbook, get_df(conn, faculty), faculty)
    else:
        pass

write_workbook(workbook)