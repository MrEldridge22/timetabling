import xml.etree.ElementTree as ET
import sqlite3
from database_interaction import *
from get_dataframes import *
from export_to_excel import *
import xlsxwriter

""" 
TODO:
- Sort into lines - DONE!
- Read in Term 2 / 4 data
- Output to Excel sheet - All Staff Done!
- Output tabs into Excel Sheet
- Fix SWD Lines - DONE!
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

# Populate excel sheet
# all_staff = get_df(conn, "all")
# create_excel_sheet(workbook, all_staff, "All Staff")
# write_workbook(workbook)

faculty_list = [r[0] for r in conn.cursor().execute('SELECT code FROM faculties').fetchall()]

