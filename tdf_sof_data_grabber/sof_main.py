import sqlite3
import json
import pandas as pd
from sof_database import *

# Create the Database
conn = sqlite3.connect(':memory:')
create_sof_tables(conn)

# Open the json sfx file
with open('ttd_files\students.sfx', "r") as read_content:
    sfx_raw = json.load(read_content)

# Populate Databases
# import_sfx_data(sfx_raw, conn)
# import_edsas_codes('EDSAS Codes.xlsx', conn)

subjects_df = pd.json_normalize(sfx_raw, record_path=['Subjects'])

# Drop all Columns Except SubjectID, Code and Name
for col in subjects_df.columns:
    if col not in ["Code", "Name"]:
        subjects_df.drop([col], inplace=True, axis=1)

# Read Excel file into Datafame
edsas_subjects_df = pd.read_excel('EDSAS Codes.xlsx')

# Remove all Unwanted Columns
for col in edsas_subjects_df.columns:
    if col not in ["Subject Code", "Subject Name", "Status"]:
        edsas_subjects_df.drop([col], inplace=True, axis=1)

# Filter out all Old Subjects and only get Active ones, O code in EDSAS
edsas_subjects_df = edsas_subjects_df[edsas_subjects_df.Status == "O"]
# Drop Status Column
edsas_subjects_df.drop(["Status"], inplace=True, axis=1)
# Rename Columns
edsas_subjects_df.rename(columns={"Subject Code": "Code", "Subject Name": "Name"}, inplace=True)

# Compare and get List of Missing Codes
# Missing from sfx file

# Codes online (sfx file) but not in EDSAS, these need to be changed online!
missing_subjects = subjects_df.merge(edsas_subjects_df, on='Code', how='left')
missing_subjects = missing_subjects[missing_subjects['Name_y'].isnull()]
missing_subjects.drop(['Name_y'], axis=1, inplace=True)

print(missing_subjects)

