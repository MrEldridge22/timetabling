import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('''CREATE TABLE student_selections(
        id INTEGER PRIMARY KEY NOT NULL,
        Firstname TEXT NOT NULL,
        Surname TEXT NOT NULL,
        Gender TEXT,
        Year INT,
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
future_students_df = pd.read_csv('future_students/2023 7 EDSAS Export.TXT', sep='\t', skip_blank_lines=True, skiprows=[0,1])

# Split names into columns, drop columns, and rename each column
future_students_df[['Firstname','Surname']] = future_students_df.Name.apply(lambda x: pd.Series(str(x).split(", ")))
future_students_df.drop(['Name', 'Admin YL', 'Census YL', 'Room', 'Roll Class'], axis=1, inplace=True)

future_students_df.rename(columns={'Student ID': 'StudentID',
                                    'ED ID': 'EDID',
                                    'Roll Class': "RollClass"}, inplace=True)

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

# Merge StudentID into Subject Selections
subject_selections_df = pd.merge(subject_selections_df, future_students_df, on=['EDID'])

# Drop from Selections and Keep EDSAS Surname and Firstname, rename Firstname and Surname columns
subject_selections_df.drop(columns=['Surname_x', 'Firstname_x'], inplace=True)
subject_selections_df.rename(columns={'Surname_y': 'Surname',
                                        'Firstname_y': 'Firstname'},
                                        inplace=True)

# Reorder To Correct Order for Selections, change this as needed
subject_selections_df = subject_selections_df[['Surname', 'Firstname', 'Gender', 'EDID', 'StudentID', 'Arts1', 'Arts2', 'Free1', 'Free2', 'FreeRes1', 'FreeRes2', 'ArtsRes']]

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
    selections = list(dict.fromkeys([student.StudentID,
                                        student.Firstname,
                                        student.Surname,
                                        student.Gender,
                                        '7',
                                        student.Arts1,
                                        student.Arts2,
                                        student.Free1,
                                        student.Free2,
                                        student.FreeRes1,
                                        student.FreeRes2,
                                        student.ArtsRes]))
        
    selections = selections + [np.nan] * (12 - len(selections))
    sql = '''INSERT INTO student_selections
                (id, Firstname, Surname, Gender, Year, Arts1, Arts2, Free1, Free2, FreeRes1, FreeRes2, ArtsRes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    conn.execute(sql, tuple(selections))
    conn.commit()

# Get percentage of students chosen each subject for each prefernce, loop this as needed
percentages_df = pd.DataFrame({'Subject': ['7ART', '7DRA', '7DAN', '7MUS', '7DPD', '7TECH', '7ITAO']})
percentages_df.set_index('Subject', inplace=True)
print(percentages_df)
for preference in subject_selections_df[['Arts1', 'Arts2', 'Free1', 'Free2', 'FreeRes1', 'FreeRes2', 'ArtsRes']]:
    sql = f"""SELECT {preference} as Subject, 1.0 * COUNT(*) / (SELECT COUNT(*) FROM student_selections WHERE {preference} IS NOT NULL) AS {preference}
                FROM student_selections
                WHERE {preference} IS NOT NULL
                GROUP BY {preference};"""
    temp_df = pd.DataFrame(pd.read_sql_query(sql, conn))
    print(temp_df)
    percentages_df.join(temp_df.set_index('Subject'))

print(percentages_df)
# Export all data to csv for import into Student Options
pd.read_sql('SELECT * FROM student_selections', conn).to_csv('future_students/student_options_import.csv')
