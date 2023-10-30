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


year_levels = ['07', '08', '09', '10', 'SS', 'SWD']

# Debug and Testing Purposes
pd.set_option('display.max_rows', None)

# File Paths
with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year SWD Students.sfx', "r") as read_content:
    yrSWD_sfx = json.load(read_content)
with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year SS Students.sfx', "r") as read_content:
    yrSS_sfx = json.load(read_content)
with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 10 Students.sfx', "r") as read_content:
    yr10_sfx = json.load(read_content)
with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 9 Students.sfx', "r") as read_content:
    yr09_sfx = json.load(read_content)
with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 8 Students.sfx', "r") as read_content:
    yr08_sfx = json.load(read_content)
with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 7 Students.sfx', "r") as read_content:
    yr07_sfx = json.load(read_content)

conn = sqlite3.connect(':memory:')

def create_tables(conn):
    """
    Create Tables for Student Option Files and Timetable Files
   
    Parameters:
        conn : Database Connection object

    Returns:
        None
    """
    
    # Iterate over the year levels and create the required tables
    for year_level in year_levels:
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
populate_tables(conn)
