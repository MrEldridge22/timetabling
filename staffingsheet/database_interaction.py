import sqlite3
"""
Database interaction for the Staffing Sheet Creator"""


def createTables(conn):
    """
    Create all the database tables needed for the script
    :param conn:
    :return:
    """
    conn.execute('''CREATE TABLE teachers(
        teacher_id TEXT PRIMARY KEY NOT NULL,
        code TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        proposed_load TEXT NOT NULL,
        actual_load TEXT NOT NULL,
        notes TEXT
    );''')

    conn.execute('''CREATE TABLE faculties(
        faculty_id TEXT PRIMARY KEY NOT NULL,
        code TEXT NOT NULL
    );''')

    conn.execute('''CREATE TABLE rooms(
        room_id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL
    );''')

    conn.execute('''CREATE TABLE roll_classes(
        roll_class_id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL
    );''')

    conn.execute('''CREATE TABLE classes(
        class_id TEXT PRIMARY KEY NOT NULL,
        faculty_id TEXT NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id)
    );''')

    conn.execute('''CREATE TABLE days(
        day_id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL
    );''')

    conn.execute('''CREATE TABLE periods(
        period_id TEXT PRIMARY KEY NOT NULL,
        day_id TEXT NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (day_id) REFERENCES days(day_id)
    );''')

    conn.execute('''CREATE TABLE timetable(
        timetable_id TEXT PRIMARY KEY NOT NULL,
        roll_class_id TEXT NOT NULL,
        period_id TEXT NOT NULL,
        class_id TEXT NOT NULL,
        room_id TEXT NOT NULL,
        teacher_id TEXT NOT NULL,
        FOREIGN KEY (period_id) REFERENCES periods(period_id),
        FOREIGN KEY (roll_class_id) REFERENCES roll_classes(roll_class_id)
        FOREIGN KEY (class_id) REFERENCES classes(class_id),
        FOREIGN KEY (room_id) REFERENCES rooms(room_id),
        FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
    );''')

    conn.execute('''CREATE TABLE teacher_faculties(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_id TEXT NOT NULL,
        teacher_id TEXT NOT NULL,
        FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id),
        FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
    );''')


def read_in_data(conn, root):
    """
    Reads in the tdf xml file data to the database
    :param conn (database connection):
    :param root (xml root):
    :return None:
    """
   
    # Get Faculty ID and code (short name) and Insert into Database
    for faculties_all in root.findall(".//{http://www.timetabling.com.au/TDV9}Faculties/{http://www.timetabling.com.au/TDV9}Faculty"):
        faculty_id = faculties_all.find('{http://www.timetabling.com.au/TDV9}FacultyID').text
        faculty_code = faculties_all.find('{http://www.timetabling.com.au/TDV9}Code').text
        populate_faculties(conn, (faculty_id, faculty_code))
        # print("{1}: {0}".format(faculty_code, faculty_id))

    # Grab Teacher ID, Code and Name, insert into database
    # Do I need proposed Load??? - YES!
    for teacher_all in root.findall(".//{http://www.timetabling.com.au/TDV9}Teachers/{http://www.timetabling.com.au/TDV9}Teacher"):   
        teacher_id = teacher_all.find('.{http://www.timetabling.com.au/TDV9}TeacherID').text
        teacher_code = teacher_all.find('.{http://www.timetabling.com.au/TDV9}Code').text
        firstname = teacher_all.find('.{http://www.timetabling.com.au/TDV9}FirstName').text
        lastname = teacher_all.find('.{http://www.timetabling.com.au/TDV9}LastName').text
        proposed_load = teacher_all.find('.{http://www.timetabling.com.au/TDV9}ProposedLoad').text
        actual_load = teacher_all.find('.{http://www.timetabling.com.au/TDV9}ActualLoad').text
        notes = teacher_all.find('.{http://www.timetabling.com.au/TDV9}SpareField1').text
        populate_teachers(conn, (teacher_id, teacher_code, firstname, lastname, proposed_load, actual_load, notes))
        # print("{0}: {1} {2}: {3}".format(teacher_code, firstname, lastname, teacher_id))

    # Get all rooms and insert into Database
    for rooms_all in root.findall(".//{http://www.timetabling.com.au/TDV9}Rooms/{http://www.timetabling.com.au/TDV9}Room"):
        room_id = rooms_all.find('{http://www.timetabling.com.au/TDV9}RoomID').text
        room_name = rooms_all.find('{http://www.timetabling.com.au/TDV9}Code').text
        populate_rooms(conn, (room_id, room_name))
    
    # Get all Roll Class Groups and insert into Database
    for roll_class_all in root.findall(".//{http://www.timetabling.com.au/TDV9}RollClasses/{http://www.timetabling.com.au/TDV9}RollClass"):
        roll_class_id = roll_class_all.find("{http://www.timetabling.com.au/TDV9}RollClassID").text
        roll_class_name = roll_class_all.find("{http://www.timetabling.com.au/TDV9}Name").text
        populate_roll_classes(conn, (roll_class_id, roll_class_name))
        

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
        roll_class_id = timetables.find('{http://www.timetabling.com.au/TDV9}RollClassID').text
        period_id = timetables.find('{http://www.timetabling.com.au/TDV9}PeriodID').text
        class_id = timetables.find('{http://www.timetabling.com.au/TDV9}ClassID').text
        room_id = timetables.find('{http://www.timetabling.com.au/TDV9}RoomID').text
        teacher_id = timetables.find('{http://www.timetabling.com.au/TDV9}TeacherID').text
        populate_timetable(conn, (tt_id, roll_class_id, period_id, class_id, room_id, teacher_id))
    
    for teacher_faculties in root.findall(".//{http://www.timetabling.com.au/TDV9}FacultyTeachers/{http://www.timetabling.com.au/TDV9}FacultyTeacher"):
        faculty_id = teacher_faculties.find('{http://www.timetabling.com.au/TDV9}FacultyID').text
        teacher_id = teacher_faculties.find('{http://www.timetabling.com.au/TDV9}TeacherID').text
        populate_teacher_faculties(conn, (faculty_id, teacher_id))


def get_fte(root):
    """
    Get the Full Time Equalvent Value
    
    Parameters
    root: xml root
    
    Returns
    Text: Proposed Full Time Teacher Load
    """
    for settings_all in root.findall(".//{http://www.timetabling.com.au/TDV9}Settings"):
        return(settings_all.find('{http://www.timetabling.com.au/TDV9}ProposedTeacherLoad').text)


def populate_teachers(conn, teacher_data):
    """
    Insert into Teachers Table
    :param conn:
    :param teachers:
    :return:
    """
    sql = ''' INSERT OR IGNORE INTO teachers(teacher_id, code, first_name, last_name, proposed_load, actual_load, notes) VALUES(?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, teacher_data)
    conn.commit()


def populate_faculties(conn, faculty_data):
    """
    Insert into Faculties Table
    :param conn:
    :param faculty_data(FacultyID, code):
    :return:
    """
    sql = ''' INSERT INTO faculties(faculty_id, code) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, faculty_data)
    conn.commit()


def populate_rooms(conn, room_data):
    """
    Insert into Rooms Table
    :param conn:
    :param room_data:
    :return:
    """
    sql = ''' INSERT OR IGNORE INTO rooms(room_id, name) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, room_data)
    conn.commit()


def populate_roll_classes(conn, roll_class_data):
    """
    Insert into Roll Class table
    
    Parameters
    conn: database connection
    roll_class_data: tuple (roll_class_id, roll_class_name)
    
    Returns
    None
    """
    sql = '''INSERT OR IGNORE INTO roll_classes(roll_class_id, name) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, roll_class_data)
    conn.commit()


def populate_classes(conn, class_data):
    """
    Insert into Faculties Table
    :param conn:
    :param class_data(class_id, faculty_id, name):
    :return:
    """
    sql = ''' INSERT INTO classes(class_id, faculty_id, name) VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, class_data)
    conn.commit()


def populate_days(conn, day_data):
    """
    Insert into Days Table
    :param conn:
    :param day_data (day_id, day_name):
    :return:
    """
    sql = ''' INSERT OR IGNORE INTO days(day_id, name) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, day_data)
    conn.commit()


def populate_periods(conn, period_data):
    """
    Insert into Periods Table
    :param conn:
    :param perioddata (period_id, day_id, period_name):
    :return:
    """
    sql = ''' INSERT OR IGNORE INTO periods(period_id, day_id, name) VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, period_data)
    conn.commit()


def populate_timetable(conn, tt_data):
    """
    Insert data into Timetable Table

    Parameters
    conn : db connection:
    tt_data (tuple) : Timetable Data (timetable_id, roll_class_id, period_id, class_id, room_id, teacher_id)
    
    Return
    None : 
    """
    sql = ''' INSERT INTO timetable(timetable_id, roll_class_id, period_id, class_id, room_id, teacher_id) VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, tt_data)
    conn.commit()


def populate_teacher_faculties(conn, teacher_faculties):
    """
    Insert data into Teacher Faculties Table

    Parameters
    conn : db connection:
    teacher_faculties (tuple) : Teachers in Faculty Data (faculty_id, teacher_id)
    
    Return
    None : 
    """
    sql = ''' INSERT INTO teacher_faculties(faculty_id, teacher_id) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, teacher_faculties)
    conn.commit()


def get_faculties(conn):
    """
    Retrieve Faculty List from Database

    Parameters:
    conn : Database Connection object
    
    Returns:
    faculty_list (list) : List of all faculties in database
    
    """
    faculty_list = [r[0] for r in conn.cursor().execute('SELECT DISTINCT code FROM faculties ORDER BY code ASC').fetchall()]
    return faculty_list
