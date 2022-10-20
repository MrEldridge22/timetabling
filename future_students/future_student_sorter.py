import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('''CREATE TABLE student_selections(
        id INTEGER AUTO INCREMENT PRIMARY KEY,
        Firstname TEXT NOT NULL,
        Surname TEXT NOT NULL,
        Gender TEXT,
        Arts1 TEXT,
        Arts2 TEXT,
        Free1 TEXT,
        Free2 TEXT,
        FreeRes1 TEXT,
        FreeRes2 TEXT,
        ArtsRes TEXT
    );''')

# Subject Faculties
arts_subjects = ['7ART', '7DRA', '7DAN', '7MUS']
free_subjects = ['7ART', '7DRA', '7DAN', '7MUS', '7DPD', '7TECH', '7ITAO']
res_subjects = ['7ART', '7DRA', '7DAN', '7MUS', '7DPD', '7TECH']

# Outputs:
# 1 Students with options in right order for timetabler
# 1 Option Order - Arts1, Arts2, Free Choice1, Free Choice2, Reserve1, Reserve2, ReserveArt
# 2 Students who don't have edid or student id
# 3 Students who haven't selected subjects but allocated based on projections

# TODO
# - Output a csv / excel of students with all data but mis-matched names or no student ID (aka not in EDSAS yet!)

# import future students from EDSAS Export
future_students_df = pd.read_csv('future_students/future_students_edsas_export.csv')
# Drop Unneeded Columns, this is currently a DayMap export, need to grab EDSAS and modify accordingly
future_students_df.drop(['Student', 'Email', 'Form', 'Group', 'House'], axis=1, inplace=True)
# Correct text case
future_students_df['Firstname'] = future_students_df['Firstname'].str.title()
future_students_df['Surname'] = future_students_df['Surname'].str.title()

# Import Student Subject Selections
subject_selections_df = pd.read_excel('future_students/Subject Selections.xlsx')
subject_selections_df.drop(['DOB'], axis=1, inplace=True)

# Rename Columns of Subject Selections
subject_selections_df.rename(columns={'Last Name': 'Surname', 
                                        'First Name': 'Firstname',
                                        'Gender': 'Gender',
                                        'EDID': 'EDID',
                                        'ARTS - 1ST CHOICE': 'Arts1',
                                        'ARTS - 2ND CHOICE': 'Arts2',
                                        'ART - RESERVE': 'ArtsRes',
                                        'FREE -  1ST CHOICE': 'Free1',
                                        'FREE - 2ND CHOICE': 'Free2',
                                        'FREE - RESERVE 1': 'FreeRes1',
                                        'FREE - RESERVE 2': 'FreeRes2'},
                            inplace=True)

# Rename Students, Subjects to be Capital each Word
for column in subject_selections_df:
    try:
        subject_selections_df[column] = subject_selections_df[column].str.title()
    except:
        print("ERR: Column contains something other than a string")

# Remove Middle Names if they are present
subject_selections_df['Firstname'] = subject_selections_df['Firstname'].str.split(" ").str[0]

# Reorder To Correct Order for Selections, change this as needed
subject_selections_df = subject_selections_df[['Surname', 'Firstname', 'Gender', 'EDID', 'Arts1', 'Arts2', 'Free1', 'Free2', 'FreeRes1', 'FreeRes2', 'ArtsRes']]

# Rename Subjects to Subject Codes, may need to add more rules in to fully sort!
for preference in subject_selections_df[['Arts1', 'Arts2', 'Free1', 'Free2', 'FreeRes1', 'FreeRes2', 'ArtsRes']]:
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Art', case=False, na=False), preference] = '7ART'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Product', case=False, na=False), preference] = '7DPD'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Tech', case=False, na=False), preference] = '7TECH'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Dan', case=False, na=False), preference] = '7DAN'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Dra', case=False, na=False), preference] = '7DRA'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Italian', case=False, na=False), preference] = '7ITAO'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Music', case=False, na=False), preference] = '7MUS'

# Sort the Data and Remove Duplicates at the same time, insert into db table
for student in subject_selections_df.itertuples():
    selections = list(dict.fromkeys([student.Firstname,
                                        student.Surname,
                                        student.Gender,
                                        student.Arts1,
                                        student.Arts2,
                                        student.Free1,
                                        student.Free2,
                                        student.FreeRes1,
                                        student.FreeRes2,
                                        student.ArtsRes]))
        
    selections = selections + [np.nan] * (10 - len(selections))
    sql = '''INSERT INTO student_selections
                (Firstname, Surname, Gender, Arts1, Arts2, Free1, Free2, FreeRes1, FreeRes2, ArtsRes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    conn.execute(sql, tuple(selections))
    conn.commit()


# Get percentage of students chosen each subject for each prefernce
subj = "Free1"
sql = f"""SELECT {subj}, 1.0 * COUNT(*) / (SELECT COUNT(*) FROM student_selections WHERE {subj} IS NOT NULL) AS Percentage
            FROM student_selections
            WHERE {subj} IS NOT NULL
            GROUP BY {subj};"""
print(pd.read_sql(sql, conn))
# Students who haven't completed, orr fully completed selections into separate dataframe for follow up
missing_selections_df = subject_selections_df[subject_selections_df.isna().any(axis=1)]
missing_selections_df.to_csv('future_students/missing_selections.csv')

