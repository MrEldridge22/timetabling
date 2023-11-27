### Create Database Schema for sfx and tfx files
# Database in memory, recreated by accessing files each boot up / rerun?
# Pass back database connection?

### NOTE
# In Student Options file under students, they have a list of assigned options (OptionID) and classes (ClassID)
# OptionID is the option nominated, ClassID is the Class Assigned. ClassID can be blank in this case meaning that the class was not assigned to that student.
### Change ClassID of student who changes classes. If changing multiple classes around, ie PE classes to get another subject (3 way swap) have to change multiple classid's


import sqlite3
import json
import pandas as pd
import numpy as np
from constant_values import sfx_year_levels, term_based_subjects

# Debug and Testing Purposes
pd.set_option('display.max_rows', None)

conn = sqlite3.connect(':memory:')

# Unassigned Room ID
unassignedRoom = "{D91A444E-BCA5-4724-A8A2-0D2C7043433A}"

def create_tables(conn):
    """
    Create Tables for Student Option Files and Timetable Files
   
    Parameters:
        conn : Database Connection object

    Returns:
        None
    """
    
    # Iterate over the year levels and create the required tables for Student Options Database
    for year_level in sfx_year_levels:
        print(f"Creating {year_level} Tables")
        conn.executescript(f'''
        CREATE TABLE settings_{year_level}(
            DefaultStudentUnits TEXT,
            LinesProposed INT,
            DefaultPeriods INT,
            DefaultCodeLength INT,
            AddSuffixString TEXT,
            SuffixType TEXT,
            Subgrids INT,
            ShowRollClass TEXT,
            ShowYearLevel TEXT,
            ShowHomeGroup TEXT,
            ShowHouse TEXT,
            ShowGender TEXT,
            ShowStudentCode TEXT,
            RestartSuffixOnLineorSubgrid INT,
            AddSubgridNo TEXT,
            AddLineChar TEXT,
            TimetableNotice TEXT,
            TimetableClassesSaved TEXT,
            StudentSpareField1 TEXT,
            OptionSpareField1 TEXT,
            ConvertedFromV9 TEXT,
            ClassCodeComponents TEXT,
            DateModified REAL);
        
        CREATE TABLE lines_{year_level}(
            LineID TEXT PRIMARY KEY,
            Code TEXT,
            Name TEXT,
            LineTagID TEXT,
            Subgrid INT,
            LineNo INT,
            Classes TEXT);
        
        CREATE TABLE subjects_{year_level}(
            SubjectID TEXT PRIMARY KEY,
            Code TEXT,
            Name TEXT,
            Gender TEXT,
            BOSCode TEXT,
            SpareField TEXT,
            Units INT,
            Subgrids INT,
            ClassSizeMaximum INT,
            CorrespondingLines TEXT,
            SameStudents TEXT,
            SpareField1 TEXT,
            SpareField2 TEXT);

        CREATE TABLE options_{year_level}(
            OptionID TEXT PRIMARY KEY NOT NULL,
            SubjectID TEXT,
            OptionCode TEXT,
            AlternateCode TEXT,
            AlternateName TEXT,
            Subgrid INT,
            Classes INT,
            Lines INT,
            Teachers INT,
            AutoCreate TEXT,
            PrerequisiteType INT,
            LineJoins JSON,
            SubgridConstraints JSON,
            LineRestrictions JSON,
            FOREIGN KEY (SubjectID) REFERENCES subjects_{year_level}(SubjectID));

        CREATE TABLE students_{year_level}(
            StudentID TEXT PRIMARY KEY NOT NULL,
            StudentCode INT NOT NULL,
            FirstName TEXT,
            LastName TEXT,
            MiddleName TEXT,
            PreferredName TEXT,
            Gender TEXT,
            BOSCode TEXT,
            RollClass TEXT,
            YearLevel TEXT,
            House TEXT,
            HomeGroup TEXT,
            SpareField1 TEXT,
            SpareField2 TEXT,
            SpareField3 TEXT,
            Email TEXT,
            Units INT,
            Lock TEXT,
            StudentPreferences JSON);

        CREATE TABLE classes_{year_level}(
            ClassID TEXT PRIMARY KEY NOT NULL,
            OptionID TEXT,
            LineID TEXT,
            SameID TEXT,
            ClassCode TEXT,
            ClassName TEXT,
            Suffix TEXT,
            RollClassCode TEXT,
            TeacherCode TEXT,
            RoomCode TEXT,
            TagLevel INT,
            LessonNo INT,
            Periods INT,
            Maximum_Class_Size INT,
            Lock TEXT,
            FOREIGN KEY (OptionID) REFERENCES options_{year_level}(OptionID),
            FOREIGN KEY (LineID) REFERENCES lines_{year_level}(LineID));
        ''')

    # Timetable Development File Database
    conn.executescript('''
                            CREATE TABLE teachers(
                                teacher_id TEXT PRIMARY KEY NOT NULL,
                                code TEXT NOT NULL,
                                first_name TEXT NOT NULL,
                                last_name TEXT NOT NULL,
                                proposed_load TEXT NOT NULL,
                                actual_load TEXT,
                                notes TEXT
                            );
                            
                            CREATE TABLE faculties(
                                faculty_id TEXT PRIMARY KEY NOT NULL,
                                code TEXT NOT NULL
                            );

                            CREATE TABLE rooms(
                                room_id TEXT PRIMARY KEY NOT NULL,
                                name TEXT NOT NULL
                            );
                       
                            CREATE TABLE roll_classes(
                                roll_class_id TEXT PRIMARY KEY NOT NULL,
                                name TEXT NOT NULL
                            );

                            CREATE TABLE classes(
                                class_id TEXT PRIMARY KEY NOT NULL,
                                faculty_id TEXT NOT NULL,
                                name TEXT NOT NULL,
                                FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id)
                            );

                            CREATE TABLE days(
                                day_id TEXT PRIMARY KEY NOT NULL,
                                name TEXT NOT NULL
                            );

                            CREATE TABLE periods(
                                period_id TEXT PRIMARY KEY NOT NULL,
                                day_id TEXT NOT NULL,
                                name TEXT NOT NULL,
                                load INT,
                                FOREIGN KEY (day_id) REFERENCES days(day_id)
                            );

                            CREATE TABLE timetable(
                                timetable_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                roll_class_id TEXT,
                                period_id TEXT,
                                class_id TEXT,
                                room_id TEXT,
                                teacher_id TEXT,
                                FOREIGN KEY (period_id) REFERENCES periods(period_id),
                                FOREIGN KEY (roll_class_id) REFERENCES roll_classes(roll_class_id)
                                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                                FOREIGN KEY (room_id) REFERENCES rooms(room_id),
                                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
                            );

                            CREATE TABLE teacher_faculties(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                faculty_id TEXT NOT NULL,
                                teacher_id TEXT NOT NULL,
                                FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id),
                                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
                            );
                       ''')


def populate_tfx_data(conn, tfx_file, term):
    """
    Reads in the data from a tfx json encoded file
    
        Parameters:
            conn (sqlite3): A SQLite3 Database Connection
            tfx_file (File): A json encoded tfx (TT V10) file

        Returns:
            None (None)
    """
    
    ### Teachers ###
        # Loads are now not in teacher section, need to manaually get this out at a later point!
    teachers_df = pd.json_normalize(tfx_file, record_path=['Teachers'])
    # print(teachers_df)
    for col in teachers_df.columns:
        if col not in ["TeacherID", "Code", "FirstName", "LastName", "SpareField1", "LoadProposed"]:
            teachers_df.drop([col], inplace=True, axis=1)
    
    # Rename columns to match database table columns
    teachers_df.rename(columns={"TeacherID": "teacher_id",
                                "Code": "code",
                                "FirstName": "first_name",
                                "LastName": "last_name",
                                "SpareField1": "notes",
                                "LoadProposed": "proposed_load"
                                }, inplace=True)
    teachers_df['notes'].replace('', np.nan, inplace=True)
    # print(teachers_df)
    # Write to Database
    for row in teachers_df.itertuples():
        populate_teachers(conn, (row.teacher_id, row.code, row.first_name, row.last_name, row.notes, row.proposed_load))

    ### Faculties ###
    faculties_df = pd.json_normalize(tfx_file, record_path=['Faculties'])
    for col in faculties_df.columns:
        if col not in ["FacultyID", "Code"]:
            faculties_df.drop([col], inplace=True, axis=1)

    # Rename to match database table columns
    faculties_df.rename(columns={"FacultyID": "faculty_id", "Code": "code"}, inplace=True)
    # print(faculties_df)
    # faculties_df.to_sql('faculties', conn, if_exists='append', index=False)
    for row in faculties_df.itertuples():
        populate_faculties(conn, (row.faculty_id, row.code))

    ### Rooms ###
    rooms_df = pd.json_normalize(tfx_file, record_path=['Rooms'])
    for col in rooms_df.columns:
        if col not in ["RoomID", "Code"]:
            rooms_df.drop([col], inplace=True, axis=1)

    # Rename to match database table columns
    rooms_df.rename(columns={"RoomID": "room_id", "Code": "name"}, inplace=True)
    # print(rooms_df)
    # rooms_df.to_sql('rooms', conn, if_exists='append', index=False)
    for row in rooms_df.itertuples():
        populate_rooms(conn, (row.room_id, row.name))

    ### Roll Classes ###
    roll_classes_df = pd.json_normalize(tfx_file, record_path=['RollClasses'])
    for col in roll_classes_df.columns:
        if col not in ["RollClassID", "Code"]:
            roll_classes_df.drop([col], inplace=True, axis=1)

    # Rename to match database table columns
    roll_classes_df.rename(columns={"RollClassID": "roll_class_id", "Code": "name"}, inplace=True)
    # print(roll_classes_df)
    # roll_classes_df.to_sql('roll_classes', conn, if_exists='append', index=False)
    for row in roll_classes_df.itertuples():
        populate_roll_classes(conn, (row.roll_class_id, row.name))

    ### Classes ###
    classes_df = pd.json_normalize(tfx_file, record_path=['ClassNames'])
    for col in classes_df.columns:
        if col not in ["ClassNameID", "FacultyID", "SubjectName"]:
            classes_df.drop([col], inplace=True, axis=1)

    # Rename to match database table columns
    classes_df.rename(columns={"ClassNameID": "class_id", "FacultyID": "faculty_id", "SubjectName": "name"}, inplace=True)
    # print(classes_df)
    # classes_df.to_sql('classes', conn, if_exists='append', index=False)
    # Append Term Based Subjects with T1,T2,T3,T4
    term_sub_name_appended = []
    for i in range(len(term_based_subjects)):
        term_sub_name_appended.append(term_based_subjects[i] + " T" + str(term))
    # print(term_sub_name_appended)
    classes_df.replace(to_replace=term_based_subjects, value=term_sub_name_appended, inplace=True)
    for row in classes_df.itertuples():
        populate_classes(conn, (row.class_id, row.faculty_id, row.name))

    ### Days ###
    days_df = pd.json_normalize(tfx_file, record_path=['Days'])
    for col in days_df.columns:
        if col not in ["DayID", "Name"]:
            days_df.drop([col], inplace=True, axis=1)

    # Rename to match database table columns
    days_df.rename(columns={"DayID": "day_id", "Name": "name"}, inplace=True)
    # print(days_df)
    # days_df.to_sql('days', conn, if_exists='append', index=False)
    for row in days_df.itertuples():
        populate_days(conn, (row.day_id, row.name))

    ### Periods ###
    periods_df = pd.json_normalize(tfx_file, record_path=['Periods'])
    for col in periods_df.columns:
        if col not in ["PeriodID", "DayID", "Name", "Load"]:
            periods_df.drop([col], inplace=True, axis=1)

    # Rename to match database table columns
    periods_df.rename(columns={"PeriodID": "period_id", "DayID": "day_id", "Name": "name", "Load": "load"}, inplace=True)
    # print(periods_df)
    # periods_df.to_sql('periods', conn, if_exists='append', index=False)
    for row in periods_df.itertuples():    
        populate_periods(conn, (row.period_id, row.day_id, row.name, row.load))

    ### Timetables ###
    timetables_df = pd.json_normalize(tfx_file, record_path=['Timetable'])
    # Rename to match database table columns
    timetables_df.index.names = ["timetable_id"]
    # print(timetables_df.index)
    timetables_df.rename(columns={"RollClassID": "roll_class_id", "PeriodID": "period_id", "ClassNameID": "class_id", "TeacherID": "teacher_id", "RoomID": "room_id"}, inplace=True)
    # Fill blank rooms with Temp Room
    timetables_df['room_id'].replace(to_replace="", value=unassignedRoom, inplace=True)
    # print(timetables_df['room_id'])
    # timetables_df.to_sql('timetable', conn, if_exists='append')
    for row in timetables_df.itertuples():
        populate_timetable(conn, (row.roll_class_id, row.period_id, row.class_id, row.room_id, row.teacher_id))

    # ### Teacher Faculties ###
    tf_df = pd.json_normalize(tfx_file, record_path='Faculties')

    # No idea how this work except it does!
    ### From Google Bard ###
    """
    This code snippet involves creating a new DataFrame from an existing DataFrame, tf_df, and manipulating its structure. Let's break down the code step by step:
    Extracting FacultyTeachers:
    *tf_df['FacultyTeachers']: This part extracts the FacultyTeachers column from the tf_df DataFrame.
    The asterisk (*) operator unpacks the list of lists in the FacultyTeachers column, resulting in a single list of individual faculty teachers.
    
    Creating a Temporary DataFrame:
    pd.DataFrame([*tf_df['FacultyTeachers']], tf_df.index): This creates a temporary DataFrame using the extracted list of faculty teachers and
    the index of the tf_df DataFrame. This essentially replicates the FacultyTeachers column as a new DataFrame.
    
    Stacking the DataFrame:
    .stack(): The .stack() method converts the temporary DataFrame from a single column format to a multi-level column format.
    This basically converts the list of faculty teachers into a single column with a hierarchical index representing the original row and column indices.
    
    Renaming Axes:
    .rename_axis([None,'drop1']): This renames the axes of the stacked DataFrame.
    The None value indicates that the first axis (outer level) doesn't have a name, and 'drop1' is the name assigned to the second axis (inner level).
    
    Resetting Index:
    .reset_index(1, name='Teachers'): This resets the index of the stacked DataFrame, removing the hierarchical index created by stacking.
    The 1 parameter specifies that the second axis ('drop1') should be used as the new index, and the name='Teachers' parameter names the
    new index column as 'Teachers'.
    The resulting DataFrame, temp_df, has a structure where each row represents a faculty teacher and the index is named 'Teachers'.
    This new DataFrame effectively transforms the original FacultyTeachers column into a separate DataFrame with a more organized structure.
    """

    temp_df = pd.DataFrame([*tf_df['FacultyTeachers']], tf_df.index).stack().rename_axis([None,'drop1']).reset_index(1, name='Teachers')
    tf_df = tf_df[['FacultyID']].join(temp_df)
    tf_df = pd.concat([tf_df, tf_df["Teachers"].apply(pd.Series)], axis=1)
    tf_df.drop(columns=['drop1', 'Teachers'], inplace=True)
    tf_df.reset_index(drop=True, inplace=True)

    # Rename to match database table columns
    tf_df.rename(columns={"FacultyID": "faculty_id", "TeacherID": "teacher_id"}, inplace=True)
    # print(tf_df)
    # tf_df.to_sql('teacher_faculties', conn, if_exists='append', index=False)
    for row in tf_df.itertuples():
        populate_faculties(conn, (row.faculty_id, row.teacher_id))

    # Populate proposed column with data from tfx file.
    # TODO: Filter out by term based subjects

    calc_actual_load_sql = """
                            SELECT t.code AS code, SUM(p.load) AS actual_load FROM timetable tt
                            INNER JOIN teachers t ON tt.teacher_id = t.teacher_id
                            INNER JOIN periods p on tt.period_id = p.period_id
                            GROUP BY t.code;
                            """  
    load_df = pd.read_sql(calc_actual_load_sql, conn)
    # Iterate over all staff and update values in table
    for row in load_df.itertuples():
        sql = """UPDATE teachers SET actual_load = (?) WHERE code = (?);"""
        cur = conn.cursor()
        cur.execute(sql, (row.actual_load, row.code))
        conn.commit()
    

# Insert data into database
def populate_teachers(conn, teacher_data):
    """
    Insert into Teachers Table
    :param conn:
    :param teachers:
    :return:
    """
    sql = ''' INSERT OR IGNORE INTO teachers(teacher_id, code, first_name, last_name, notes, proposed_load) VALUES(?,?,?,?,?,?)'''
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
    sql = ''' INSERT OR IGNORE INTO faculties(faculty_id, code) VALUES(?,?)'''
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
    sql = ''' INSERT OR IGNORE INTO periods(period_id, day_id, name, load) VALUES(?,?,?,?)'''
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
    sql = ''' INSERT INTO timetable(roll_class_id, period_id, class_id, room_id, teacher_id) VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    # print(tt_data)
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


def populate_tables(conn):
    settings_df = pd.json_normalize(yrSS_sfx, record_path=['Settings'])
    lines_df = pd.json_normalize(yrSS_sfx, record_path=['Lines'])
    subjects_df = pd.json_normalize(yrSS_sfx, record_path=['Subjects'])
    options_df = pd.json_normalize(yrSS_sfx, record_path=['Options'])
    # print(options_df)

    students_df = pd.json_normalize(yrSS_sfx, record_path=['Students'])
    classes_df = pd.json_normalize(yrSS_sfx, record_path=['Classes'])
    
    
    # settings_df.to_sql('settings_SS', conn, if_exists='append', index=False)
    # lines_df.to_sql('lines_SS', conn, if_exists='append', index=False)
    # subjects_df.to_sql('subjects_SS', conn, if_exists='append', index=False)
    # options_df.to_sql('options_SS', conn, if_exists='append', index=False)
    # students_df.to_sql('students_SS', conn, if_exists='append', index=False)
    # classes_df.to_sql('classes_SS', conn, if_exists='append', index=False)

    # print(options_df['SubgridConstraints'])


create_tables(conn)
# populate_tables(conn)
