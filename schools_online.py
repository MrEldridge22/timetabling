import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import json
import pandas as pd
import datetime

# Year Creation and Open File
year = datetime.date.today().year
main_path_school = f"V:\\Timetabler\\Current Timetable\\{year}"
seniors_sfx_file    = f"\\{year} Year SS Students.sfx"
swd_sfx_file    = f"\\{year} Year SWD Students.sfx"
# semester2_tfx    = f"\\TTD_{year}_S2.tfx"

# School Contact Number
schoolNumber = 245


def expand_studentPreferences_column(df):
    # Expand the dictionary column row by row
    df = df.explode("StudentPreferences")
    expanded_df = df["StudentPreferences"].apply(pd.Series)
    
    # Concatenate the original dataframe (minus the dictionary column) with the expanded columns
    df_expanded = pd.concat([df.drop(columns=["StudentPreferences"]), expanded_df], axis=1)
    try:
        df_expanded.drop(columns=0, axis=1, inplace=True)
    except KeyError:
        print('0 Column can not be found, continuing!')

    # Drop all class options NOT assigned to the student.
    df_expanded = df_expanded[df_expanded["ClassID"].notna()]
    df_expanded.drop(columns="ClassID", axis=1, inplace=True)
    
    return df_expanded


def organise_dataframe(sfx_file):
    ### Get Subjects and Classes ###
    # Get lines and puts into Dataframe
    lines_df = pd.json_normalize(sfx_file, record_path="Lines")
    for col in lines_df.columns:
        if col not in ["LineID", "Subgrid"]:
            lines_df.drop([col], inplace=True, axis=1)


    # Get Classes
    classes_df = pd.json_normalize(sfx_file, record_path="Classes")
    # Remove Unwanted Columns
    for col in classes_df.columns:
        if col not in ["OptionID", "LineID", "ClassCode", "SubjectCode", "SubjectName"]:
            classes_df.drop([col], inplace=True, axis=1)


    # Join classes and Lines
    classes_df = pd.merge(classes_df, lines_df, left_on="LineID", right_on="LineID", how="left").drop("LineID", axis=1)
    # print(classes_df)


    # Get Students and Choices into Dataframe
    students_df = pd.json_normalize(sfx_file, record_path="Students")

    for col in students_df.columns:
        if col not in ["StudentCode", "FirstName", "LastName", "YearLevel", "StudentPreferences"]:
            students_df.drop([col], inplace=True, axis=1)

    studnets_df_expanded = expand_studentPreferences_column(students_df)
    # print(seniors_df_expanded)

    organised_df = pd.merge(studnets_df_expanded, classes_df, left_on="OptionID", right_on="OptionID", how='left').drop("OptionID", axis=1)

    # Add in extra columns needed for Schools Online
    organised_df["Contact School Number"] = schoolNumber
    organised_df["Registration Number"] = ""
    organised_df["Student Code"] = organised_df["StudentCode"]
    organised_df["Year"] = datetime.date.today().year
    organised_df["Semester"] = organised_df["Subgrid"]
    organised_df["Stage"] = pd.to_numeric(organised_df["SubjectCode"].str.slice(stop=1), errors='coerce')
    organised_df["SACE Code"] = organised_df["SubjectCode"].str.slice(start=1, stop=4)
    organised_df["Credits"] = organised_df["SubjectCode"].str.slice(start=4, stop=6)
    organised_df["Enrolment Number"] = ""
    organised_df["Results Due"] = organised_df.apply(
        lambda row: (
            'J' if row['Semester'] == 1 and row['Stage'] == 1 else  # Stage 1, Semester 1
            'D' if row['Semester'] == 2 and row['Stage'] == 1 else  # Stage 1, Semester 2
            'J' if row['SACE Code'] in ['RPA', 'RPM', 'AIF', 'AIM'] and row['Semester'] == 1 else  # Stage 2, Semester 1 for special codes
            'D' if row['SACE Code'] in ['RPA', 'RPM', 'AIF', 'AIM'] and row['Semester'] == 2 else  # Stage 2, Semester 2 for special codes
            'D'  # Default return for all other Stage 2 subjects
        ),
        axis=1
    )
    organised_df["Program Variant"] = ""
    organised_df["Teaching School Number"] = schoolNumber
    organised_df["Assessment School Number"] = schoolNumber
    organised_df["Class Number"] = ""
    organised_df["Enrolment Status"] = ""
    organised_df["Repeat Indicator"] = "N"
    organised_df["School Class Code"] = organised_df["ClassCode"]
    organised_df["Stage 1 Grade"] = ""
    organised_df["Partial Credits"] = ""
    organised_df["ED ID"] = organised_df["Student Code"]

    # Remove Other Columns
    organised_df.drop(["StudentCode", "FirstName", "LastName", "ClassCode", "SubjectCode", "Subgrid", "YearLevel"], axis=1, inplace=True)

    return organised_df


# Import Year SS File
with open (f"{main_path_school}{seniors_sfx_file}", "r") as seniors_sfx_file:
    seniors_sfx = json.load(seniors_sfx_file)

with open (f"{main_path_school}{swd_sfx_file}", "r") as swd_sfx_file:
    swd_sfx = json.load(swd_sfx_file)

seniors_df = organise_dataframe(seniors_sfx)
seniors_df[(seniors_df["Semester"] == 1) & (seniors_df["Stage"] == 1)].to_csv('Stage1 Semester 1 Enrollments.csv')
seniors_df[(seniors_df["Semester"] == 2) & (seniors_df["Stage"] == 1)].to_csv('Stage1 Semester 2 Enrollments.csv')
seniors_df[(seniors_df["Semester"] == 1) & (seniors_df["Stage"] == 2)].to_csv('Stage2 Enrollments.csv')

swd_df = organise_dataframe(swd_sfx)
swd_df[(swd_df["Semester"] == 1) & (swd_df["Stage"] == 1)].to_csv('Stage1 SWD Semester 1 Enrollments.csv')
swd_df[(swd_df["Semester"] == 2) & (swd_df["Stage"] == 1)].to_csv('Stage1 SWD Semester 2 Enrollments.csv')
swd_df[(swd_df["Semester"] == 1) & (swd_df["Stage"] == 2)].to_csv('Stage2 SWD Enrollments.csv')

print("Done!")

### Information Needed: ###
# Classes import file:
#
# 1 Contact School Number
# 2 Year
# 3 SACE Stage 1/2
# 4 SACE Subject Code 3 Character SACE Code ie MRS for Material Solutions
# 5 Credits 10 or 20
# 6 Class Number 1-98 (Allocate based on class Suffix??)
# 7 Program Variant A to Z (Not essential)
# 8 Semester 1 or 2
# 9 Teacher Code 3+ Code ie ELDD for David Eldridge
# 10 School Class Code (Not essential but would be nice)
# 11 Results Due J (June) or D (December)
#
# SACE Enrolments File:
# 1 Contact School Number
# 2 SACE Registration Number (Not essential)
# 3 Student Code ie 230000
# 4 Year
# 5 Semester 1/2
# 6 Stage 1 or 2
# 7 SACE Code 3 Character SACE Code
# 8 Credits 10 or 20
# 9 Enrolment Number False If this is not set, a new enrolment is assumed. (Not Essential) - NOT IN OUR FILE!
# 10 Results Due J (June) or D (December)
# 11 Program Variant A to Z (Not Essential) - NOT IN OUR FILE
# 12 Teaching School Number (SACE Number??) The school at which the subject is taught.
# 13 Assessment School Number (SACE Number??) The school at which the subject is assessed.
# 14 Class Number 1-98 (Allocate based on class Suffix??) - Match above??
# 15 Enrolment Status True C (Completed), D or X (Deleted), P (Proposed), E or F (Enrolled), or W (Withdrawn). Must be in upper case. (What's the default??) - NOT IN OUR FILE
# 16 Repeat Indicator False Defaults to 'N' if not set. Set to Y if repeating the subject – only applies to Stage 1 enrolments. (Not Essential)
# 17 School Class Code False Class identifier, unique within the school. Class Code from Timetabler 1MSRJ101A. (Not Essential)
# 18 Stage 1 Grade 1 Char False A, B, C, D or E.  (Not Essential) - NOT IN OUR FILE
# 19 Partial Credits unctionality not yet implemented.  (Not Essential) - NOT IN OUR FILE
# 20 ED ID Applies to EDSAS and Dux.  (Not Essential)

