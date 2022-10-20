import pandas as pd
import numpy as np

# Read in csv file of students,

# Outputs:
# 1 Students with options in right order for timetabler
# 1 Option Order - Arts1, Arts2, Free Choice1, Free Choice2, Reserve1, Reserve2, ReserveArt
# 2 Students who don't have edid or student id
# 3 Students who haven't selected subjects but allocated based on projections

# TODO
# - Output a csv / excel of students with all data but mis-matched names or no student ID (aka not in EDSAS yet!)

# Choice Subjects
choice_subject_dict = { '7DAN': "Dance", 
                        '7TECH': "Design Technology",
                        '7DPD': "Digital Products",
                        '7DRA': "Drama",
                        '7ITAO': "Italian", # Check This!
                        '7MUS': "Music",
                        '7ART': "Visual Art"}

# import future students from EDSAS Export
future_students_df = pd.read_csv('future_students/future_students_edsas_export.csv')
# Drop Unneeded Columns, this is currently a DayMap export, need to grab EDSAS and modify accordingly
future_students_df.drop(['Student', 'Email', 'Form', 'Group', 'House'], axis=1, inplace=True)
# Correct text case
future_students_df['Firstname'] = future_students_df['Firstname'].str.title()
future_students_df['Surname'] = future_students_df['Surname'].str.title()

# Import Student Subject Selections
subject_selections_df = pd.read_excel('future_students/Subject Selections.xlsx')

# Rename Columns of Subject Selections
subject_selections_df.rename(columns={'Last Name': 'Surname', 
                                        'First Name': 'Firstname',
                                        'DOB': 'DOB',
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
subject_selections_df = subject_selections_df[['Surname', 'Firstname', 'DOB', 'Gender', 'EDID', 'Arts1', 'Arts2', 'Free1', 'Free2', 'FreeRes1', 'FreeRes2', 'ArtsRes']]

# Rename Subjects to Subject Codes, may need to add more rules in to fully sort!
for preference in subject_selections_df[['Arts1', 'Arts2', 'Free1', 'Free2', 'FreeRes1', 'FreeRes2', 'ArtsRes']]:
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Art', case=False, na=False), preference] = '7ART'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Product', case=False, na=False), preference] = '7DPD'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Tech', case=False, na=False), preference] = '7TECH'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Dan', case=False, na=False), preference] = '7DAN'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Dra', case=False, na=False), preference] = '7DRA'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Italian', case=False, na=False), preference] = '7ITAO'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Music', case=False, na=False), preference] = '7MUS'

# Students who haven't completed, orr fully completed selections into separate dataframe for follow up
missing_selections_df = subject_selections_df[subject_selections_df.isna().any(axis=1)]
missing_selections_df.to_csv('future_students/missing_selections.csv')

# Remove duplicate subject selections
for student in subject_selections_df.itertuples():
    if (pd.notnull(student.ArtsRes)) and (student.ArtsRes in [student.Arts1, student.Arts2, student.Free1, student.Free2, student.FreeRes1, student.FreeRes2]):
        subject_selections_df.at[student.Index, 'ArtsRes'] = np.nan
    
    if (pd.notnull(student.FreeRes2)) and (student.FreeRes2 in [student.Arts1, student.Arts2, student.Free1, student.Free2, student.FreeRes1]):
        subject_selections_df.at[student.Index, 'FreeRes2'] = np.nan
    
    if (pd.notnull(student.FreeRes1)) and (student.FreeRes1 in [student.Arts1, student.Arts2, student.Free1, student.Free2]):
        subject_selections_df.at[student.Index, 'FreeRes1'] = np.nan
    
    if (pd.notnull(student.Free2)) and (student.Free2 in [student.Arts1, student.Arts2, student.Free1]):
        subject_selections_df.at[student.Index, 'Free2'] = np.nan
    
    if (pd.notnull(student.Free1)) and (student.Free1 in [student.Arts1, student.Arts2]):
        subject_selections_df.at[student.Index, 'Free1'] = np.nan
    
    if (pd.notnull(student.Arts2)) and (student.Arts2 in [student.Arts1]):
        subject_selections_df.at[student.Index, 'Arts2'] = np.nan

# Get Percentages of Subjects Selected by preference
just_selection_values_df = subject_selections_df.loc[:, subject_selections_df.columns.drop(['Surname', 'Firstname', 'DOB', 'Gender', 'EDID'])]
subject_spread_series_list = []
for column in just_selection_values_df:
    subject_spread_series_list.append(subject_selections_df[column].value_counts(normalize=True))
selection_percentage_df = pd.concat(subject_spread_series_list, axis=1, keys=[s.name for s in subject_spread_series_list])

print(subject_selections_df)
# Assign Subjects to those who haven't completed selections based on those who have selected subjects
for subject in subject_spread_series_list:
    missing_selections_df = subject_selections_df[subject.name].isnull()
    # Add in here check to see if student has picked subject!
    subject_selections_df.loc[missing_selections_df, subject.name] = np.random.choice(subject.index, size=len(subject_selections_df[missing_selections_df]), p=selection_percentage_df[subject.name].dropna())

print(subject_selections_df)
# Add in Student ID to subject selections dataframe
subject_selections_df = pd.merge(subject_selections_df, future_students_df, on=['Firstname', 'Surname'])

# Export CSV Ready for Student Options Import
to_student_options_csv = subject_selections_df.to_csv('future_students/student_options_import.csv')