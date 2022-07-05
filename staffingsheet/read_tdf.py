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
sql_query = pd.read_sql_query('''SELECT 
                                        d.name AS day, p.name as lesson, t.first_name, t.last_name, t.code, c.name as subject, f.code as faculty, r.name as room, c.class_id as id
                                        FROM timetable tt
                                        INNER JOIN periods p ON tt.period_id = p.period_id
                                        INNER JOIN days d ON p.day_id = d.day_id
                                        INNER JOIN classes c ON tt.class_id = c.class_id
                                        INNER JOIN faculties f ON c.faculty_id = f.faculty_id
                                        INNER JOIN rooms r ON tt.room_id = r.room_id
                                        INNER JOIN teachers t ON tt.teacher_id = t.teacher_id
                                        ORDER BY t.last_name ASC;''',
                                        conn)

tt_df = pd.DataFrame(sql_query)
# print(tt_df)
# Sort data out to calculate which subjects are on which line and put into a dataframe with one entry of each
teacher_data_list = []
# Iterates over the tt_df dataframe finding corresponding line for each daily lesson and put into a list if the lesson is found.
for row in tt_df.itertuples(index=False):
    if row.faculty != "SpEd":    # Special Ed Run different line structure, this splits it into correct lines, this is the mainstream sorter
        for i, line_num in mainstream_lines_df[row.day].iteritems():
            # If the subject is found in that day, get the corresponding line which is the cell value, exclude Personal Development from results also
            if row.lesson == i and row.subject.find("Personal Development") == -1:  # Found a Subject on a line!
                teacher_data_list.append([row.id, row.code, row.first_name, row.last_name, row.subject, row.room, line_num])
    else:
        for i, line_num in swd_lines_df[row.day].iteritems():
            # If the subject is found in that day, get the corresponding line which is the cell value, exclude Personal Development from results also
            if row.lesson == i and row.subject.find("Personal Development") == -1:  # Found a Subject on a line!
                teacher_data_list.append([row.id, row.code, row.first_name, row.last_name, row.subject, row.room, line_num])

# Put list into a dataframe, drop the duplicate
teacher_data_df = pd.DataFrame(teacher_data_list, columns=['id', 'code', 'firstname', 'lastname', 'subject', 'room', 'line'])
teacher_data_df.drop_duplicates(inplace=True, ignore_index=True)
teacher_data_df['subject'] = teacher_data_df[['code', 'firstname', 'lastname', 'subject', 'room', 'line']].groupby(['code', 'line'])['subject'].transform(lambda x: '/'.join(x))
teacher_data_df['room'] = teacher_data_df[['code', 'firstname', 'lastname', 'subject', 'room', 'line']].groupby(['code', 'line'])['room'].transform(lambda x: '/'.join(x))
teacher_data_df.drop(columns=['id'], inplace=True)
teacher_data_df.drop_duplicates(inplace=True, ignore_index=True)
print(teacher_data_df.loc[teacher_data_df['code'] == "ELDD"])