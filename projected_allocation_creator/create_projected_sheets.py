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

# Create tempory database in memory.
conn = sqlite3.connect(':memory:')

conn.execute('''CREATE TABLE yr10_lines(
        LineID TEXT PRIMARY KEY NOT NULL,
        Subgrid INT NOT NULL,
        Code INT NOT NULL        
    );''')
conn.execute('''CREATE TABLE yr10_subjects(
        SubjectID TEXT PRIMARY KEY NOT NULL,
        Name TEXT NOT NULL      
    );''')
conn.execute('''CREATE TABLE yr10_options(
        OptionID TEXT PRIMARY KEY NOT NULL,
        SubjectID TEXT NOT NULL,
        FOREIGN KEY (SubjectID) REFERENCES yr10_subjects(SubjectID)       
    );''')
conn.execute('''CREATE TABLE yr10_classes(
        ClassID TEXT PRIMARY KEY NOT NULL,
        OptionID TEXT NOT NULL,
        LineID TEXT NOT NULL,
        FOREIGN KEY (OptionID) REFERENCES yr10_options(OptionID),
        FOREIGN KEY (LineID) REFERENCES yr10_lines(LineID)     
    );''')

with open('projected_allocation_creator/2023 Year 10 Students.sfx', "r") as read_content:
        tfx_raw = json.load(read_content)

# Extract Line Info
lines_df = pd.json_normalize(tfx_raw, record_path=['Lines'])
lines_df.drop(['Name', 'LineTagID', 'LineNo', 'Classes'], inplace=True, axis=1)
lines_df.to_sql('yr10_lines', conn, if_exists='append', index=False)

# Extract Subject Info
subjects_df = pd.json_normalize(tfx_raw, record_path=['Subjects'])
for col in subjects_df.columns:
        if col not in ["SubjectID", "Name"]:
            subjects_df.drop([col], inplace=True, axis=1)
subjects_df.to_sql('yr10_subjects', conn, if_exists='append', index=False)

# Extract Options Info
options_df = pd.json_normalize(tfx_raw, record_path=['Options'])
for col in options_df.columns:
        if col not in ["OptionID", "SubjectID"]:
            options_df.drop([col], inplace=True, axis=1)
options_df.to_sql('yr10_options', conn, if_exists='append', index=False)

# Extract Classes Info
classes_df = pd.json_normalize(tfx_raw, record_path=['Classes'])
for col in classes_df.columns:
        if col not in ["ClassID", "OptionID", "LineID"]:
            classes_df.drop([col], inplace=True, axis=1)
classes_df.to_sql('yr10_classes', conn, if_exists='append', index=False)


### OUTPUTS
# Semester 1 and Semester 2 Staffing Sheets