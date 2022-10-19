import pandas as pd

# Read in csv file of students,

# Outputs:
# 1 Students with options in right order for timetabler
# 1 Option Order - Arts1, Arts2, Free Choice1, Free Choice2, Reserve1, Reserve2, ReserveArt
# 2 Students who don't have edid or student id
# 3 Students who haven't selected subjects but allocated based on projections

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
# Drop Unneeded Columns
future_students_df.drop(['Student', 'Email', 'Form', 'Group', 'House'], axis=1, inplace=True)
# Correct text case
future_students_df['Firstname'] = future_students_df['Firstname'].str.title()
future_students_df['Surname'] = future_students_df['Surname'].str.title()

# Import Student Subject Selections
subject_selections_df = pd.read_excel('future_students/7 Subject Selections.xlsx')

# Add in Student ID to subject selections dataframe


# Rename Columns
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
        print("Column contains something other than a string")

# Reorder To Correct Order for Selections, change this as needed
subject_selections_df = subject_selections_df[['Surname', 'Firstname', 'DOB', 'Gender', 'EDID', 'Arts1', 'Arts2', 'Free1', 'Free2', 'FreeRes1', 'FreeRes2', 'ArtsRes']]

# Rename Subjects for Consistency, may need to add more in!
for preference in subject_selections_df[['Arts1', 'Arts2', 'Free1', 'Free2', 'FreeRes1', 'FreeRes2', 'ArtsRes']]:
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Art', case=False, na=False), preference] = 'Visual Art'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Product', case=False, na=False), preference] = 'Digital Products'
    subject_selections_df.loc[subject_selections_df[preference].str.contains('Tech', case=False, na=False), preference] = 'Design Technology'

# Remove Students who haven't completed selections into separate dataframe for follow up.
missing_selections_df = subject_selections_df[subject_selections_df.isna().any(axis=1)]

# Get Percentages of Subjects Selected by preference
just_selection_values_df = subject_selections_df.loc[:, subject_selections_df.columns.drop(['Surname', 'Firstname', 'DOB', 'Gender', 'EDID'])]
temp_series_list = []
for column in just_selection_values_df:
    temp_series_list.append(subject_selections_df[column].value_counts(normalize=True))
selection_percentage_df = pd.concat(temp_series_list, axis=1, keys=[s.name for s in temp_series_list])

# print(selection_percentage_df)