import sqlite3
import xlsxwriter
import json
import pandas as pd

### NOTE
# Need to create Version 10 Files first for this to work, these are JSON encoded rather than XML encoded.
# Using Version 10 in 2023, no point in spending time for Version 9 creation.
# Ensure Network Paths are accessible prior to running.
# Need to edit dictionary below for choice lines from SoF Files

# Choice lines, how to do this? Dictionary and have sfx lines as keys changing line number, how do I get semesters / terms then??

### FILE PATHS
# SS    "V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year SS Students.sfx"
# Yr 10 "V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 10 Students.sfx"
# Yr 9  "V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 9 Students.sfx"
# Yr 8  "V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 8 Students.sfx"
# Yr 7  "V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 7 Students.sfx"

# Create tempory database in memory.
conn = sqlite3.connect(':memory:')

### CREATE TABLES ###
conn.executescript('''
                    --- Senior School (11 & 12)
                    CREATE TABLE yrSS_lines(
                        LineID TEXT PRIMARY KEY NOT NULL,
                        Subgrid INT NOT NULL,
                        Code INT NOT NULL);
                    CREATE TABLE yrSS_subjects(
                        SubjectID TEXT PRIMARY KEY NOT NULL,
                        Name TEXT NOT NULL);
                    CREATE TABLE yrSS_options(
                        OptionID TEXT PRIMARY KEY NOT NULL,
                        SubjectID TEXT NOT NULL,
                        FOREIGN KEY (SubjectID) REFERENCES yrSS_subjects(SubjectID));
                    CREATE TABLE yrSS_classes(
                        ClassID TEXT PRIMARY KEY NOT NULL,
                        OptionID TEXT NOT NULL,
                        LineID TEXT NOT NULL,
                        FOREIGN KEY (OptionID) REFERENCES yrSS_options(OptionID),
                        FOREIGN KEY (LineID) REFERENCES yrSS_lines(LineID));
                    
                    --- Year 10
                    CREATE TABLE yr10_lines(
                        LineID TEXT PRIMARY KEY NOT NULL,
                        Subgrid INT NOT NULL,
                        Code INT NOT NULL);
                    CREATE TABLE yr10_subjects(
                        SubjectID TEXT PRIMARY KEY NOT NULL,
                        Name TEXT NOT NULL);
                    CREATE TABLE yr10_options(
                        OptionID TEXT PRIMARY KEY NOT NULL,
                        SubjectID TEXT NOT NULL,
                        FOREIGN KEY (SubjectID) REFERENCES yr10_subjects(SubjectID));
                    CREATE TABLE yr10_classes(
                        ClassID TEXT PRIMARY KEY NOT NULL,
                        OptionID TEXT NOT NULL,
                        LineID TEXT NOT NULL,
                        FOREIGN KEY (OptionID) REFERENCES yr10_options(OptionID),
                        FOREIGN KEY (LineID) REFERENCES yr10_lines(LineID));

                    --- Year 09
                    CREATE TABLE yr09_lines(
                        LineID TEXT PRIMARY KEY NOT NULL,
                        Subgrid INT NOT NULL,
                        Code INT NOT NULL);
                    CREATE TABLE yr09_subjects(
                        SubjectID TEXT PRIMARY KEY NOT NULL,
                        Name TEXT NOT NULL);
                    CREATE TABLE yr09_options(
                        OptionID TEXT PRIMARY KEY NOT NULL,
                        SubjectID TEXT NOT NULL,
                        FOREIGN KEY (SubjectID) REFERENCES yr09_subjects(SubjectID));
                    CREATE TABLE yr09_classes(
                        ClassID TEXT PRIMARY KEY NOT NULL,
                        OptionID TEXT NOT NULL,
                        LineID TEXT NOT NULL,
                        FOREIGN KEY (OptionID) REFERENCES yr09_options(OptionID),
                        FOREIGN KEY (LineID) REFERENCES yr09_lines(LineID));

                    --- Year 08
                    CREATE TABLE yr08_lines(
                        LineID TEXT PRIMARY KEY NOT NULL,
                        Subgrid INT NOT NULL,
                        Name INT NOT NULL);
                    CREATE TABLE yr08_subjects(
                        SubjectID TEXT PRIMARY KEY NOT NULL,
                        Name TEXT NOT NULL);
                    CREATE TABLE yr08_options(
                        OptionID TEXT PRIMARY KEY NOT NULL,
                        SubjectID TEXT NOT NULL,
                        FOREIGN KEY (SubjectID) REFERENCES yr08_subjects(SubjectID));
                    CREATE TABLE yr08_classes(
                        ClassID TEXT PRIMARY KEY NOT NULL,
                        OptionID TEXT NOT NULL,
                        LineID TEXT NOT NULL,
                        FOREIGN KEY (OptionID) REFERENCES yr08_options(OptionID),
                        FOREIGN KEY (LineID) REFERENCES yr08_lines(LineID));

                    --- Year 07
                    CREATE TABLE yr07_lines(
                        LineID TEXT PRIMARY KEY NOT NULL,
                        Subgrid INT NOT NULL,
                        Code INT NOT NULL);
                    CREATE TABLE yr07_subjects(
                        SubjectID TEXT PRIMARY KEY NOT NULL,
                        Name TEXT NOT NULL);
                    CREATE TABLE yr07_options(
                        OptionID TEXT PRIMARY KEY NOT NULL,
                        SubjectID TEXT NOT NULL,
                        FOREIGN KEY (SubjectID) REFERENCES yr07_subjects(SubjectID));
                    CREATE TABLE yr07_classes(
                        ClassID TEXT PRIMARY KEY NOT NULL,
                        OptionID TEXT NOT NULL,
                        LineID TEXT NOT NULL,
                        FOREIGN KEY (OptionID) REFERENCES yr07_options(OptionID),
                        FOREIGN KEY (LineID) REFERENCES yr07_lines(LineID));
                    ''')

# Open all sfx files
with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year SS Students.sfx', "r") as read_content:
        yrSS_sfx = json.load(read_content)
with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 10 Students.sfx', "r") as read_content:
        yr10_sfx = json.load(read_content)
with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 9 Students.sfx', "r") as read_content:
        yr09_sfx = json.load(read_content)
with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 8 Students.sfx', "r") as read_content:
        yr08_sfx = json.load(read_content)

# Year 07
# with open('V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\2023 Year 07 Students.sfx', "r") as read_content:
#         yr07_sfx = json.load(read_content)

### YEAR 11 & 12 ###
# Extract Line Info
lines_df = pd.json_normalize(yrSS_sfx, record_path=['Lines'])
lines_df.drop(['Name', 'LineTagID', 'LineNo', 'Classes'], inplace=True, axis=1)
lines_df.to_sql('yrSS_lines', conn, if_exists='append', index=False)

# Extract Subject Info
subjects_df = pd.json_normalize(yrSS_sfx, record_path=['Subjects'])
for col in subjects_df.columns:
        if col not in ["SubjectID", "Name"]:
            subjects_df.drop([col], inplace=True, axis=1)
subjects_df.to_sql('yrSS_subjects', conn, if_exists='append', index=False)

# Extract Options Info
options_df = pd.json_normalize(yrSS_sfx, record_path=['Options'])
for col in options_df.columns:
        if col not in ["OptionID", "SubjectID"]:
            options_df.drop([col], inplace=True, axis=1)
options_df.to_sql('yrSS_options', conn, if_exists='append', index=False)

# Extract Classes Info
classes_df = pd.json_normalize(yrSS_sfx, record_path=['Classes'])
for col in classes_df.columns:
        if col not in ["ClassID", "OptionID", "LineID"]:
            classes_df.drop([col], inplace=True, axis=1)
classes_df.to_sql('yrSS_classes', conn, if_exists='append', index=False)

# Get all subjects by line
query = """SELECT s.Name AS subject, l.Code as line, COUNT(s.Name || l.Code) as num_classes from yrSS_classes c
        INNER JOIN yrSS_options o ON o.OptionID = c.OptionID
        INNER JOIN yrSS_subjects s on o.SubjectID = s.SubjectID
        INNER JOIN yrSS_lines l on l.LineID = c.LineID
        GROUP BY s.Name, l.Code;"""

yrSS_df = pd.read_sql(query, conn)

### YEAR 10 ###
# Extract Line Info
lines_df = pd.json_normalize(yr10_sfx, record_path=['Lines'])
lines_df.drop(['Name', 'LineTagID', 'LineNo', 'Classes'], inplace=True, axis=1)
lines_df.to_sql('yr10_lines', conn, if_exists='append', index=False)

# Extract Subject Info
subjects_df = pd.json_normalize(yr10_sfx, record_path=['Subjects'])
for col in subjects_df.columns:
        if col not in ["SubjectID", "Name"]:
            subjects_df.drop([col], inplace=True, axis=1)
subjects_df.to_sql('yr10_subjects', conn, if_exists='append', index=False)

# Extract Options Info
options_df = pd.json_normalize(yr10_sfx, record_path=['Options'])
for col in options_df.columns:
        if col not in ["OptionID", "SubjectID"]:
            options_df.drop([col], inplace=True, axis=1)
options_df.to_sql('yr10_options', conn, if_exists='append', index=False)

# Extract Classes Info
classes_df = pd.json_normalize(yr10_sfx, record_path=['Classes'])
for col in classes_df.columns:
        if col not in ["ClassID", "OptionID", "LineID"]:
            classes_df.drop([col], inplace=True, axis=1)
classes_df.to_sql('yr10_classes', conn, if_exists='append', index=False)

# Get all subjects by line
query = """SELECT s.Name AS subject, l.Code as line, COUNT(s.Name || l.Code) as num_classes from yr10_classes c
        INNER JOIN yr10_options o ON o.OptionID = c.OptionID
        INNER JOIN yr10_subjects s on o.SubjectID = s.SubjectID
        INNER JOIN yr10_lines l on l.LineID = c.LineID
        GROUP BY s.Name, l.Code;"""

yr10_df = pd.read_sql(query, conn)

### YEAR 09 ###
# Extract Line Info
lines_df = pd.json_normalize(yr09_sfx, record_path=['Lines'])
lines_df.drop(['Name', 'LineTagID', 'LineNo', 'Classes'], inplace=True, axis=1)
lines_df.to_sql('yr09_lines', conn, if_exists='append', index=False)

# Extract Subject Info
subjects_df = pd.json_normalize(yr09_sfx, record_path=['Subjects'])
for col in subjects_df.columns:
        if col not in ["SubjectID", "Name"]:
            subjects_df.drop([col], inplace=True, axis=1)
subjects_df.to_sql('yr09_subjects', conn, if_exists='append', index=False)

# Extract Options Info
options_df = pd.json_normalize(yr09_sfx, record_path=['Options'])
for col in options_df.columns:
        if col not in ["OptionID", "SubjectID"]:
            options_df.drop([col], inplace=True, axis=1)
options_df.to_sql('yr09_options', conn, if_exists='append', index=False)

# Extract Classes Info
classes_df = pd.json_normalize(yr09_sfx, record_path=['Classes'])
for col in classes_df.columns:
        if col not in ["ClassID", "OptionID", "LineID"]:
            classes_df.drop([col], inplace=True, axis=1)
classes_df.to_sql('yr09_classes', conn, if_exists='append', index=False)

# Get all subjects by line
query = """SELECT s.Name AS subject, l.Code as line, COUNT(s.Name || l.Code) as num_classes from yr09_classes c
        INNER JOIN yr09_options o ON o.OptionID = c.OptionID
        INNER JOIN yr09_subjects s on o.SubjectID = s.SubjectID
        INNER JOIN yr09_lines l on l.LineID = c.LineID
        GROUP BY s.Name, l.Code;"""

yr09_df = pd.read_sql(query, conn)

### YEAR 8 ###
# Extract Line Info
lines_df = pd.json_normalize(yr08_sfx, record_path=['Lines'])
for col in lines_df.columns:
        if col not in ["LineID", "Name", "Subgrid"]:
            lines_df.drop([col], inplace=True, axis=1)
lines_df.to_sql('yr08_lines', conn, if_exists='append', index=False)

# Extract Subject Info
subjects_df = pd.json_normalize(yr08_sfx, record_path=['Subjects'])
for col in subjects_df.columns:
        if col not in ["SubjectID", "Name"]:
            subjects_df.drop([col], inplace=True, axis=1)
subjects_df.to_sql('yr08_subjects', conn, if_exists='append', index=False)

# Extract Options Info
options_df = pd.json_normalize(yr08_sfx, record_path=['Options'])
for col in options_df.columns:
        if col not in ["OptionID", "SubjectID"]:
            options_df.drop([col], inplace=True, axis=1)
options_df.to_sql('yr08_options', conn, if_exists='append', index=False)

# Extract Classes Info
classes_df = pd.json_normalize(yr08_sfx, record_path=['Classes'])
for col in classes_df.columns:
        if col not in ["ClassID", "OptionID", "LineID"]:
            classes_df.drop([col], inplace=True, axis=1)
classes_df.to_sql('yr08_classes', conn, if_exists='append', index=False)

# Get all subjects by line
query = """SELECT s.Name AS subject, l.Name as line, COUNT(s.Name || l.Name) as num_classes from yr08_classes c
        INNER JOIN yr08_options o ON o.OptionID = c.OptionID
        INNER JOIN yr08_subjects s on o.SubjectID = s.SubjectID
        INNER JOIN yr08_lines l on l.LineID = c.LineID
        GROUP BY s.Name, l.Name;"""

yr08_df = pd.read_sql(query, conn)

### OUTPUTS
# Semester 1 and Semester 2 Staffing Sheets