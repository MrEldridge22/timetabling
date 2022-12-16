"""
Script for grabbing the codes from the V10 sfx (formally sof9 file) and compare these to the export from EDSAS
Outputs a csv of all the missing subjects from EDSAS that are in the sfx file
Need to double check these subjects!
"""
import json
import pandas as pd

# Open the json sfx file
with open("V:\\Timetabler\\Current Timetable\\2023\\V10 Files\\TTD_2023_S1.tfx", "r") as read_content:
    sfx_raw = json.load(read_content)

subjects_df = pd.json_normalize(sfx_raw, record_path=['ClassNames'])

# Drop all Columns Except SubjectID, Code and Name
for col in subjects_df.columns:
    if col not in ["SubjectCode", "SubjectName"]:
        subjects_df.drop([col], inplace=True, axis=1)

# Remove Vet Courses
subjects_df = subjects_df[subjects_df['SubjectName'].str.contains("V2|V3|Certificate|Voc|uni|Reserve|No Course") == False]
subjects_df.rename(columns={"SubjectCode": "Code", "SubjectName": "Name"}, inplace=True)

# Read Excel file into Datafame
edsas_subjects_df = pd.read_excel('code_xcheck/EDSAS Codes.xlsx')

# Remove all Unwanted Columns
for col in edsas_subjects_df.columns:
    if col not in ["Subject Code", "Subject Name", "Status", "Subject Length"]:
        edsas_subjects_df.drop([col], inplace=True, axis=1)


# Rename Columns
edsas_subjects_df.rename(columns={"Subject Code": "Code", "Subject Name": "Name", "Subject Length": "Length"}, inplace=True)
# print(subjects_df)
# Compare and get List of Missing Codes
# Missing from sfx file


# Codes online (sfx file) but not in EDSAS, these need to be checked online or added to EDSAS if new subject
missing_subjects = subjects_df.merge(edsas_subjects_df, on='Code', how='left')
missing_subjects.to_csv('code_xcheck/check_length.csv')
missing_subjects = missing_subjects[missing_subjects['Name_y'].isnull()]
missing_subjects.drop(['Name_y'], axis=1, inplace=True)

# print(missing_subjects)
# Output to CSV
missing_subjects.to_csv('code_xcheck/check_subjects.csv', index=False)
