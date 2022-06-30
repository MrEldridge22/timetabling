from logging import logMultiprocessing
import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3
from database_interaction import *
from export_to_excel import create_excel

""" 
TODO:
- Sort into lines
- Read in Term 2 / 4 data
- Output to Excel sheet
- Output tabs into Excel Sheet
- Fix SWD Lines
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

# Line structure
lines_dict = {"Monday": ["Line 6", "Line 4", "Care", "Line 3", "Line 3", "PD", "Line 5"],
                "Tuesday": ["Line 7", "Line 7", "Care", "Line 6", "Line 6", "Line 2", "Line 1"],
                "Wednesday": ["Line 4", "Line 4", "Care", "Line 5", "Line 3", "Line 2", "PLT"],
                "Thursday": ["Line 2", "Line 2", "Care", "Line 1", "Line 1", "Line 6", "Line 7"],
                "Friday": ["Line 1", "Line 7", "Care", "Line 5", "Line 5", "Line 4", "Line 3"]}

# Index is the lesson number for the day
lines_df = pd.DataFrame(data=lines_dict, index=["L1", "L2", "CG", "L3", "L4", "L5", "L6"])

# Get Faculty ID and code (short name) and Insert into Database
for faculties_all in root.findall(".//{http://www.timetabling.com.au/TDV9}Faculties/{http://www.timetabling.com.au/TDV9}Faculty"):
    faculty_id = faculties_all.find('{http://www.timetabling.com.au/TDV9}FacultyID').text
    faculty_code = faculties_all.find('{http://www.timetabling.com.au/TDV9}Code').text
    populate_faculties(conn, (faculty_id, faculty_code))
    # print("{1}: {0}".format(faculty_code, faculty_id))

# Grab Teacher ID, Code and Name, insert into database
# Do I need proposed Load???
for teacher_all in root.findall(".//{http://www.timetabling.com.au/TDV9}Teachers/{http://www.timetabling.com.au/TDV9}Teacher"):   
    teacher_id = teacher_all.find('.{http://www.timetabling.com.au/TDV9}TeacherID').text
    teacher_code = teacher_all.find('.{http://www.timetabling.com.au/TDV9}Code').text
    firstname = teacher_all.find('.{http://www.timetabling.com.au/TDV9}FirstName').text
    lastname = teacher_all.find('.{http://www.timetabling.com.au/TDV9}LastName').text
    populate_teachers(conn, (teacher_id, teacher_code, firstname, lastname))
    # print("{0}: {1} {2}: {3}".format(teacher_code, firstname, lastname, teacher_id))

# Get all rooms and insert into Database
for rooms_all in root.findall(".//{http://www.timetabling.com.au/TDV9}Rooms/{http://www.timetabling.com.au/TDV9}Room"):
    room_id = rooms_all.find('{http://www.timetabling.com.au/TDV9}RoomID').text
    room_name = rooms_all.find('{http://www.timetabling.com.au/TDV9}Code').text
    populate_rooms(conn, (room_id, room_name))

# Get all Classes and insert into database
for classes_all in root.findall(".//{http://www.timetabling.com.au/TDV9}Classes/{http://www.timetabling.com.au/TDV9}Class"):
    class_id = classes_all.find('{http://www.timetabling.com.au/TDV9}ClassID').text
    class_name = classes_all.find('{http://www.timetabling.com.au/TDV9}SubjectName').text
    faculty_id = classes_all.find('{http://www.timetabling.com.au/TDV9}FacultyID').text
    populate_classes(conn, (class_id, faculty_id, class_name))

# Get DayIDs for each day and insert into database
for days in root.findall(".//{http://www.timetabling.com.au/TDV9}Days/{http://www.timetabling.com.au/TDV9}Day"):
   day_id = days.find('{http://www.timetabling.com.au/TDV9}DayID').text
   day_name = days.find('{http://www.timetabling.com.au/TDV9}Name').text
   populate_days(conn, (day_id, day_name))

# Get periods (lessons) and insert into database
for periods in root.findall(".//{http://www.timetabling.com.au/TDV9}Periods/{http://www.timetabling.com.au/TDV9}Period"):
   period_id = periods.find('{http://www.timetabling.com.au/TDV9}PeriodID').text
   day_id = periods.find('{http://www.timetabling.com.au/TDV9}DayID').text
   period_name = periods.find('{http://www.timetabling.com.au/TDV9}Name').text
   populate_periods(conn, (period_id, day_id, period_name))

# Get timetables and insert into database
for timetables in root.findall(".//{http://www.timetabling.com.au/TDV9}Timetables/{http://www.timetabling.com.au/TDV9}Timetable"):
    tt_id = timetables.find('{http://www.timetabling.com.au/TDV9}TimetableID').text
    period_id = timetables.find('{http://www.timetabling.com.au/TDV9}PeriodID').text
    class_id = timetables.find('{http://www.timetabling.com.au/TDV9}ClassID').text
    room_id = timetables.find('{http://www.timetabling.com.au/TDV9}RoomID').text
    teacher_id = timetables.find('{http://www.timetabling.com.au/TDV9}TeacherID').text
    populate_timetable(conn, (tt_id, period_id, class_id, room_id, teacher_id))

# Pull out data in Human Readable Format and into Dataframe
sql_query = pd.read_sql_query('''SELECT 
                                d.name AS day, p.name as lesson, t.first_name, t.last_name, t.code, c.name as subject, r.name as room
                                FROM timetable tt
                                INNER JOIN periods p ON tt.period_id = p.period_id
                                INNER JOIN days d ON p.day_id = d.day_id
                                INNER JOIN classes c ON tt.class_id = c.class_id
                                INNER JOIN rooms r ON tt.room_id = r.room_id
                                INNER JOIN teachers t ON tt.teacher_id = t.teacher_id
                                ORDER BY t.code ASC;''',
                                conn)
tt_df = pd.DataFrame(sql_query)

# Sort data out to calculate which subjects are on which line and put into a dataframe with one entry of each
teacher_data_list = []
# Iterates over the tt_df dataframe finding corresponding line for each daily lesson and put into a list if the lesson is found.
for row in tt_df.itertuples(index=False):
    for i, line_num in lines_df[row.day].iteritems():
        # If the subject is found in that day, get the corresponding line which is the cell value, exclude Personal Development from results also
        if row.lesson == i and row.subject.find("Personal Development") == -1:  # Found a Subject on a line!
            teacher_data_list.append([row.code, row.first_name, row.last_name, row.subject, row.room, line_num])

# Put list into a dataframe, drop the duplicate
teacher_data_df = pd.DataFrame(teacher_data_list, columns=['code', 'firstname', 'lastname', 'subject', 'room', 'line'])
teacher_data_df.drop_duplicates(inplace=True, ignore_index=True)

# Put all data into one line per staff member ready for export
# Get list of staff Codes
staff_codes = teacher_data_df['code'].unique()

# Create list of lists and put into dataframe ready for export
full_line_alloc_list = []

# Iterate through each staff member add their classes and rooms to a blank list based on line numbers
# Check the dataframe below to ensure classes are going in the correct spots
for code in staff_codes:
    flattened_list = [0] * 19
    for row in teacher_data_df.loc[teacher_data_df["code"] == code].itertuples():
        flattened_list[0] = row.code
        flattened_list[1] = row.firstname
        flattened_list[2] = row.lastname
        if row.line[-1].isnumeric():
            flattened_list[2* int(row.line[-1]) + 3] = row.subject
            flattened_list[2* int(row.line[-1]) + 4] = row.room
        else:
            flattened_list[3] = row.subject
            flattened_list[4] = row.room
    
    full_line_alloc_list.append(flattened_list)

# Final dataframe for processing into excel sheet
subject_allocation_df = pd.DataFrame(full_line_alloc_list, columns=['code',
                                                'firstname',    
                                                'lastname',
                                                'care', 'care_room',
                                                'line1_class', 'line1_room',
                                                'line2_class', 'line2_room',
                                                'line3_class', 'line3_room',
                                                'line4_class', 'line4_room',
                                                'line5_class', 'line5_room',
                                                'line6_class', 'line6_room',
                                                'line7_class', 'line7_room'])
subject_allocation_df.sort_values('code', inplace=True)
# print(subject_allocation_df)

create_excel(subject_allocation_df)