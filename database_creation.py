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


def create_tables(conn):
    """
    Create Tables for Student Option Files and Timetable Files
   
    Parameters:
        conn : Database Connection object

    Returns:
        None
    """

    conn.executescript('''
        --- Year 07 Student Options File
        CREATE TABLE settings_07(
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
        
        CREATE TABLE lines_07(
            LineID TEXT PRIMARY KEY,
            Code TEXT,
            Name TEXT,
            LineTagID TEXT,
            Subgrid INT,
            LineNo INT,
            Classes TEXT);
        
        CREATE TABLE subjects_07(
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

        CREATE TABLE options_07(
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
            PrerequisiteType TEXT,
            LineJoins JSON,
            SubgridConstraints JSON,
            LineRestrictions JSON,
            FOREIGN KEY (SubjectID) REFERENCES subjects_07(SubjectID));

        CREATE TABLE students_07(
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

        CREATE TABLE classes_07(
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
            FOREIGN KEY (OptionID) REFERENCES options_07(OptionID),
            FOREIGN KEY (LineID) REFERENCES lines_07(LineID));

    --- Year 08 Student Options File
        CREATE TABLE settings_08(
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
        
        CREATE TABLE lines_08(
            LineID TEXT PRIMARY KEY,
            Code TEXT,
            Name TEXT,
            LineTagID TEXT,
            Subgrid INT,
            LineNo INT,
            Classes TEXT);
        
        CREATE TABLE subjects_08(
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

        CREATE TABLE options_08(
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
            PrerequisiteType TEXT,
            LineJoins JSON,
            SubgridConstraints JSON,
            LineRestrictions JSON,
            FOREIGN KEY (SubjectID) REFERENCES subjects_08(SubjectID));

        CREATE TABLE students_08(
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

        CREATE TABLE classes_08(
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
            FOREIGN KEY (OptionID) REFERENCES options_08(OptionID),
            FOREIGN KEY (LineID) REFERENCES lines_08(LineID));

    --- Year 09 Student Options File
        CREATE TABLE settings_09(
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
        
        CREATE TABLE lines_09(
            LineID TEXT PRIMARY KEY,
            Code TEXT,
            Name TEXT,
            LineTagID TEXT,
            Subgrid INT,
            LineNo INT,
            Classes TEXT);
        
        CREATE TABLE subjects_09(
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

        CREATE TABLE options_09(
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
            PrerequisiteType TEXT,
            LineJoins JSON,
            SubgridConstraints JSON,
            LineRestrictions JSON,
            FOREIGN KEY (SubjectID) REFERENCES subjects_09(SubjectID));

        CREATE TABLE students_09(
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

        CREATE TABLE classes_09(
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
            FOREIGN KEY (OptionID) REFERENCES options_09(OptionID),
            FOREIGN KEY (LineID) REFERENCES lines_09(LineID));

        
    --- Year 10 Student Options File
        CREATE TABLE settings_10(
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
        
        CREATE TABLE lines_10(
            LineID TEXT PRIMARY KEY,
            Code TEXT,
            Name TEXT,
            LineTagID TEXT,
            Subgrid INT,
            LineNo INT,
            Classes TEXT);
        
        CREATE TABLE subjects_10(
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

        CREATE TABLE options_10(
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
            PrerequisiteType TEXT,
            LineJoins JSON,
            SubgridConstraints JSON,
            LineRestrictions JSON,
            FOREIGN KEY (SubjectID) REFERENCES subjects_10(SubjectID));

        CREATE TABLE students_10(
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

        CREATE TABLE classes_10(
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
            FOREIGN KEY (OptionID) REFERENCES options_10(OptionID),
            FOREIGN KEY (LineID) REFERENCES lines_10(LineID));

        
    --- Year SS Student Options File
        CREATE TABLE settings_SS(
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
        
        CREATE TABLE lines_SS(
            LineID TEXT PRIMARY KEY,
            Code TEXT,
            Name TEXT,
            LineTagID TEXT,
            Subgrid INT,
            LineNo INT,
            Classes TEXT);
        
        CREATE TABLE subjects_SS(
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

        CREATE TABLE options_SS(
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
            PrerequisiteType TEXT,
            LineJoins JSON,
            SubgridConstraints JSON,
            LineRestrictions JSON,
            FOREIGN KEY (SubjectID) REFERENCES subjects_SS(SubjectID));

        CREATE TABLE students_SS(
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

        CREATE TABLE classes_SS(
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
            FOREIGN KEY (OptionID) REFERENCES options_SS(OptionID),
            FOREIGN KEY (LineID) REFERENCES lines_SS(LineID));

    --- Year SWD Student Options File
        CREATE TABLE settings_SWD(
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
        
        CREATE TABLE lines_SWD(
            LineID TEXT PRIMARY KEY,
            Code TEXT,
            Name TEXT,
            LineTagID TEXT,
            Subgrid INT,
            LineNo INT,
            Classes TEXT);
        
        CREATE TABLE subjects_SWD(
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

        CREATE TABLE options_SWD(
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
            PrerequisiteType TEXT,
            LineJoins JSON,
            SubgridConstraints JSON,
            LineRestrictions JSON,
            FOREIGN KEY (SubjectID) REFERENCES subjects_SWD(SubjectID));

        CREATE TABLE students_SWD(
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

        CREATE TABLE classes_SWD(
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
            FOREIGN KEY (OptionID) REFERENCES options_SWD(OptionID),
            FOREIGN KEY (LineID) REFERENCES lines_SWD(LineID));
        ''')


def populate_tables(conn):
    settings_df = pd.json_normalize(yrSS_sfx, record_path=['Settings'])
    lines_df = pd.json_normalize(yrSS_sfx, record_path=['Lines'])
    subjects_df = pd.json_normalize(yrSS_sfx, record_path=['Subjects'])
    options_df = pd.json_normalize(yrSS_sfx, record_path=['Options'])
    students_df = pd.json_normalize(yrSS_sfx, record_path=['Students'])
    classes_df = pd.json_normalize(yrSS_sfx, record_path=['Classes'])
    settings_df.to_sql('settings_SS', conn, if_exists='append', index=False)
    lines_df.to_sql('lines_SS', conn, if_exists='append', index=False)
    subjects_df.to_sql('subjects_SS', conn, if_exists='append', index=False)
    options_df.to_sql('options_SS', conn, if_exists='append', index=False)
    students_df.to_sql('students_SS', conn, if_exists='append', index=False)
    classes_df.to_sql('classes_SS', conn, if_exists='append', index=False)

conn = sqlite3.connect(':memory:')
create_tables(conn)
populate_tables(conn)

