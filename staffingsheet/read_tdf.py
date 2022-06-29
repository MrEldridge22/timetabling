import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3
from database_interaction import *

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

# Final dataframe for processing into excel sheet?
subject_allocation_df = pd.DataFrame(columns=['code',
                                                'firstname',    
                                                'lastname',
                                                'care', 'care_loc',
                                                'line1_class', 'line1_loc',
                                                'line2_class', 'line2_loc',
                                                'line3_class', 'line3_loc',
                                                'line4_class', 'line4_loc',
                                                'line5_class', 'line5_loc',
                                                'line6_class', 'line6_loc',
                                                'line7_class', 'line7_loc'])

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


# Test
cur = conn.cursor()
for row in cur.execute('SELECT * FROM timetable;'):
    print(row)