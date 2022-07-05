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
- Output tabs into Excel Sheet
- Fix SWD Lines - DONE!
- Get Class Groups for Core Lines
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
all_staff = get_df(conn, "all")
create_excel_sheet(workbook, all_staff, "All Staff")
write_workbook(workbook)

# Testing Area
sql = """SELECT 
                                    d.name AS day, p.name as lesson, t.first_name, t.last_name, t.code, c.name as subject, f.code as faculty, r.name as room
                                    FROM timetable tt
                                    INNER JOIN periods p ON tt.period_id = p.period_id
                                    INNER JOIN days d ON p.day_id = d.day_id
                                    INNER JOIN classes c ON tt.class_id = c.class_id
                                    INNER JOIN faculties f ON c.faculty_id = f.faculty_id
                                    INNER JOIN rooms r ON tt.room_id = r.room_id
                                    INNER JOIN teachers t ON tt.teacher_id = t.teacher_id
                                    WHERE f.code = ?
                                    ORDER BY t.code ASC;"""
sql = """
SELECT t.code as code, GROUP_CONCAT(f.code, ", ") as faculty
FROM teacher_faculties tf
INNER JOIN faculties f ON tf.faculty_id = f.faculty_id
INNER JOIN teachers t ON tf.teacher_id = t.teacher_id
GROUP BY t.code;
"""

# cur = conn.cursor()
# cur.execute(sql)
# rows = cur.fetchall()
# for r in rows:
#     print(r)
