import sqlite3


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
        last_name TEXT NOT NULL
    );''')

    conn.execute('''CREATE TABLE faculties(
        faculty_id TEXT PRIMARY KEY NOT NULL,
        code TEXT NOT NULL
    );''')

    conn.execute('''CREATE TABLE rooms(
        room_id TEXT PRIMARY KEY NOT NULL,
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
        period_id TEXT NOT NULL,
        class_id TEXT NOT NULL,
        room_id TEXT NOT NULL,
        teacher_id TEXT NOT NULL,
        FOREIGN KEY (period_id) REFERENCES periods(period_id),
        FOREIGN KEY (class_id) REFERENCES classes(class_id),
        FOREIGN KEY (room_id) REFERENCES rooms(room_id),
        FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
    );''')


def populate_teachers(conn, teacher_data):
    """
    Insert into Teachers Table
    :param conn:
    :param teachers:
    :return:
    """
    sql = ''' INSERT INTO teachers(teacher_id, code, first_name, last_name) VALUES(?,?,?,?)'''
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
    sql = ''' INSERT INTO rooms(room_id, name) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, room_data)
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
    sql = ''' INSERT INTO days(day_id, name) VALUES(?,?)'''
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
    sql = ''' INSERT INTO periods(period_id, day_id, name) VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, period_data)
    conn.commit()


def populate_timetable(conn, tt_data):
    """
    Insert data into Timetable Table
    :param conn (db connection):
    :param tt_data (timetable_id, period_id, class_id, room_id, teacher_id)
    :return:
    """
    sql = ''' INSERT INTO timetable(timetable_id, period_id, class_id, room_id, teacher_id) VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, tt_data)
    conn.commit()