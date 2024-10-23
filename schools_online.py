import json
import pandas as pd
import datetime

# Year Creation and Open File
year = datetime.date.today().year
main_path_school = f"V:\\Timetabler\\Current Timetable\\{year}"
seniors_sfx_file    = f"\\{year} Year SS Students.sfx"
swd_sfx_file    = f"\\{year} Year SWD Students.sfx"
semester1_tfx_file = f"\\TTD_{year}_S1.tfx"
semester2_tfx_file = f"\\TTD_{year}_S2.tfx"

# School Contact Number
schoolNumber = 245


def expand_studentPreferences_column(df):
    """
    Expands the 'StudentPreferences' column in the DataFrame, which contains dictionaries,
    into separate columns. Drops any rows where 'ClassID' is not assigned to the student.

    Parameters:
    df (pd.DataFrame): The input DataFrame with a 'StudentPreferences' column containing dictionaries.

    Returns:
    pd.DataFrame: The expanded DataFrame with separate columns for each key in the 'StudentPreferences' dictionaries.
    """
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


def generate_class_number(df):
    """
    Generates a Class Number for each unique ClassCode within groups defined by Stage, SACE Code, and Credits.

    Parameters:
    df (pd.DataFrame): The input DataFrame with columns 'Stage', 'SACE Code', 'Credits', and 'ClassCode'.

    Returns:
    pd.DataFrame: The DataFrame with an additional 'Sequence' column containing the sequence numbers.
    """
    # Create a new column for the sequence
    df['Sequence'] = 0
    
    # Group by SubjectCode
    grouped = df.groupby(["Stage", "SACE Code", "Credits"])
    
    for name, group in grouped:
        # Create a dictionary to store the sequence for each ClassCode
        class_code_dict = {}
        sequence = 1
        
        for index, row in group.iterrows():
            class_code = row['ClassCode']
            if class_code not in class_code_dict:
                # print(class_code, sequence)
                class_code_dict[class_code] = sequence
                sequence += 1
            df.at[index, 'Sequence'] = class_code_dict[class_code]
    
    return df


def get_enrollments_dataframe(sfx_file, msswd="ms"):
    """
    Processes the Student Optionsd (.sfx) file to generate an enrollments DataFrame with necessary columns for Schools Online.

    Parameters:
    sfx_file (dict): The input JSON-like structure containing 'Lines', 'Classes', and 'Students'.
    msswd (str): String to ensure that SWD classes are resulted at the end of the year, defaults to ms for MainStream.

    Returns:
    pd.DataFrame: The processed DataFrame with the required columns for Schools Online Enrollments File.
    """
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

    # print(generate_class_number(organised_df))

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
            'D' if row['Credits'] == "20" else
            'D' if msswd == "swd" else
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
    organised_df["Class Number"] = generate_class_number(organised_df)["Sequence"]
    organised_df["Enrolment Status"] = ""
    organised_df["Repeat Indicator"] = "N"
    organised_df["School Class Code"] = organised_df["ClassCode"]
    organised_df["Stage 1 Grade"] = ""
    organised_df["Partial Credits"] = ""
    organised_df["ED ID"] = organised_df["Student Code"]

    # Remove Other Columns
    organised_df.drop(["StudentCode", "FirstName", "LastName", "ClassCode", "Sequence", "SubjectCode", "Subgrid", "YearLevel"], axis=1, inplace=True)

    return organised_df


def organise_teachers_df(df):
    """
    Organises the teachers DataFrame into the Format required by Schools Online.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing teacher information.

    Returns:
    pd.DataFrame: The organized DataFrame with the required columns.
    """
    for col in df.columns:
        if col not in ["LastName", "FirstName", "Code", "Salutation", "TeacherID"]:
            df.drop(columns=col, axis=1, inplace=True)
    
    organised_df = pd.DataFrame()

    organised_df["TeacherID"] = df["TeacherID"]
    organised_df["Contact School Number"] = schoolNumber
    organised_df["TeacherCode"] = df["Code"]
    organised_df["Family Name"] = df["LastName"]
    organised_df["Initials"] = df["FirstName"].str[0]
    organised_df["Title"] = df["Salutation"]
    organised_df["Teachers Registration Number"] = ""
    organised_df["Email Address"] = ""
    organised_df["Given Names"] = df["FirstName"]
    organised_df["Date of Birth"] = ""
    organised_df["Gender"] = ""

    # print(organised_df)
    return organised_df
    

def get_teachers_dataframe(sem1_tfx, sem2_tfx):
    """
    Combines teacher data from two semesters, organises it, removes duplicates, and renames columns.

    Parameters:
    sem1_tfx (dict): The JSON Semester 1 Timetable Development (tfx) file.
    sem2_tfx (dict): The JSON Semester 2 Timetable Development (tfx) file.

    Returns:
    pd.DataFrame: The combined and organized DataFrame with teacher information.
    """
    sem1_teachers_df = pd.json_normalize(sem1_tfx, record_path="Teachers")
    sem2_teachers_df = pd.json_normalize(sem2_tfx, record_path="Teachers")

    teachers_df = pd.concat([organise_teachers_df(sem1_teachers_df), organise_teachers_df(sem2_teachers_df)])

    teachers_df = teachers_df.drop_duplicates()
    
    teachers_df.rename(columns={'TeacherCode': "Teacher Code"}, inplace=True)

    return teachers_df


def organise_classes_dataframe(teacher_df, classes_tfx, semester):
    """
    Organises the classes DataFrame by merging teacher and class information, filtering, and adding necessary columns as required for the Classes Import File for Schools Online.

    Parameters:
    teacher_df (pd.DataFrame): DataFrame containing teacher information.
    classes_tfx (dict): The Timetable Development file (tfx)
    semester (int): The semester number.

    Returns:
    pd.DataFrame: The organised DataFrame with class information.
    """
    classes_df = pd.json_normalize(classes_tfx, record_path="ClassNames")
    timetable_df = pd.json_normalize(classes_tfx, record_path="Timetable")

    teachers_classes_df = pd.merge(teacher_df, timetable_df, how='left', on="TeacherID")
    teachers_class_details_df = pd.merge(teachers_classes_df, classes_df, how='left', on="ClassNameID")

    teachers_class_details_df.drop_duplicates(subset=["TeacherID", "ClassNameID"], inplace=True)
    teachers_class_details_df.dropna(subset=["SubjectCode"], inplace=True)

    organised_classes_df = pd.DataFrame()
    
    organised_classes_df["Stage"] = teachers_class_details_df["SubjectCode"].str.slice(stop=1)
    organised_classes_df["SACE Code"] = teachers_class_details_df["SubjectCode"].str.slice(start=1, stop=4)
    organised_classes_df["Credits"] = teachers_class_details_df["SubjectCode"].str.slice(start=4, stop=6)
    organised_classes_df["Class Number"] = "" # Leave blank and match up by Code Afterwards
    organised_classes_df["Program Variant"] = ""
    organised_classes_df["Semester"] = semester
    organised_classes_df["Teacher Code"] = teachers_class_details_df["Teacher Code"]
    organised_classes_df["School Class Code"] = teachers_class_details_df["Code"]
    organised_classes_df["Results Due"] = organised_classes_df.apply(
        lambda row: (
            'J' if semester == 1 and row['Stage'] == "1" else  # Stage 1, Semester 1
            'D' if semester == 2 and row['Stage'] == "1" else  # Stage 1, Semester 2
            'J' if row['SACE Code'] in ['RPA', 'RPM', 'AIF', 'AIM'] and semester == 1 else  # Stage 2, Semester 1 for special codes
            'D' if row['SACE Code'] in ['RPA', 'RPM', 'AIF', 'AIM'] and semester == 2 else  # Stage 2, Semester 2 for special codes
            'D'  # Default return for all other Stage 2 subjects
        ),
        axis=1
    )
    # Have to put these at the end as they are static values to be filled in
    organised_classes_df["Contact School Number"] = schoolNumber
    organised_classes_df["Year"] = datetime.date.today().year

    # Move the 2 to the front
    organised_classes_df.insert(0, "Contact School Number", organised_classes_df.pop("Contact School Number"))
    organised_classes_df.insert(1, "Year", organised_classes_df.pop("Year"))

    # Filter only Stage 1 and 2
    organised_classes_df = organised_classes_df[
        organised_classes_df["Stage"].isin(["1", "2"]) &
        (~organised_classes_df["School Class Code"].str.contains('Care', case=False))
    ]
    
    return organised_classes_df


def get_classes_dataframe(teachers_df, sem_tfx, semester, sace_enrollments_df):
    """
    Combines and organizes class data from teachers, semester information, and SACE enrollments.

    Parameters:
    teachers_df (pd.DataFrame): DataFrame containing teacher information.
    sem_tfx (dict): The Timetable Development file (tfx)
    semester (int): The semester number.
    sace_enrollments_df (pd.DataFrame): DataFrame containing SACE enrollment information.

    Returns:
    pd.DataFrame: The combined and organized DataFrame with class information.
    """
    df = organise_classes_dataframe(teachers_df, sem_tfx, semester)

    # Merge and handle column name conflicts
    df = pd.merge(df, sace_enrollments_df[["School Class Code", "Class Number"]], on="School Class Code", how='left', suffixes=('', '_y'))
    df["Class Number"] = df["Class Number_y"]
    #  df.insert(5, "Class Number", df.pop("Class Number"))
    df.drop(columns="Class Number_y", axis=1, inplace=True)

    df.drop_duplicates(subset=["Teacher Code", "School Class Code"], ignore_index=True, inplace=True)
    df.dropna(subset=["Class Number"], inplace=True) # This will sort for SWD and Mainstream
    return df


def get_only_sace_teachers(teacher_df, classes_df):
    """
    Filters the teacher DataFrame to include only those who are teaching SACE classes.

    Parameters:
    teacher_df (pd.DataFrame): DataFrame containing teacher information.
    classes_df (pd.DataFrame): DataFrame containing class information, including 'Teacher Code' and 'Year'.

    Returns:
    pd.DataFrame: The filtered DataFrame containing only SACE teachers.
    """
    sace_teachers_df = pd.merge(teacher_df, classes_df[["Teacher Code", "Year"]], how='left', on="Teacher Code")
    sace_teachers_df.dropna(subset=["Year"], inplace=True)
    sace_teachers_df.drop(columns=["TeacherID"], axis=1, inplace=True)
    sace_teachers_df.drop_duplicates(ignore_index=True, inplace=True)

    return sace_teachers_df


### CODE START ###

# Open Files
with open (f"{main_path_school}{semester1_tfx_file}", "r") as semester1_tfx_file:
    semester1_tfx = json.load(semester1_tfx_file)

with open (f"{main_path_school}{semester2_tfx_file}", "r") as semester2_tfx_file:
    semester2_tfx = json.load(semester2_tfx_file)

with open (f"{main_path_school}{seniors_sfx_file}", "r") as seniors_sfx_file:
    seniors_sfx = json.load(seniors_sfx_file)

with open (f"{main_path_school}{swd_sfx_file}", "r") as swd_sfx_file:
    swd_sfx = json.load(swd_sfx_file)

# Get Teachers Dataframe
teachers_df = get_teachers_dataframe(semester1_tfx, semester2_tfx)

# Get Enrollments Dataframes
seniors_df  = get_enrollments_dataframe(seniors_sfx)
swd_df      = get_enrollments_dataframe(swd_sfx, "swd")

# Get Mainstream Classes
semester1_classes_import = get_classes_dataframe(teachers_df, semester1_tfx, 1, seniors_df)
semester2_classes_import = get_classes_dataframe(teachers_df, semester2_tfx, 2, seniors_df)
stage2_classes_import = pd.concat([semester1_classes_import, semester2_classes_import])

# Get SWD Classes
semester1_swd_classes_import = get_classes_dataframe(teachers_df, semester1_tfx, 1, swd_df)
semester2_swd_classes_import = get_classes_dataframe(teachers_df, semester2_tfx, 2, swd_df)
stage2_swd_classes_import = pd.concat([semester1_swd_classes_import, semester2_swd_classes_import])

# Get all classes for Teachers
all_classes = pd.concat([semester1_classes_import, semester2_classes_import, semester1_swd_classes_import, semester2_swd_classes_import])

### OUTPUT FILES ###
# Teachers
get_only_sace_teachers(teachers_df, all_classes).to_csv("Teacher Import.csv")
# Classes
semester1_classes_import[(semester1_classes_import["Stage"] == "1")].to_csv('Stage1 Semester 1 Classes.csv')
semester2_classes_import[(semester2_classes_import["Stage"] == "1")].to_csv('Stage1 Semester 2 Classes.csv')
stage2_classes_import[(stage2_classes_import["Stage"] == "2")].to_csv('Stage2 Semester Classes.csv')

semester1_swd_classes_import[(semester1_swd_classes_import["Stage"] == "1")].to_csv('Stage1 SWD Semester 1 Classes.csv')
semester2_swd_classes_import[(semester2_swd_classes_import["Stage"] == "1")].to_csv('Stage1 SWD Semester 2 Classes.csv')
stage2_swd_classes_import[(stage2_swd_classes_import["Stage"] == "2")].to_csv('Stage2 SWD Semester Classes.csv')

# Enrollments
seniors_df[(seniors_df["Semester"] == 1) & (seniors_df["Stage"] == 1)].to_csv('Stage1 Semester 1 Enrollments.csv')
seniors_df[(seniors_df["Semester"] == 2) & (seniors_df["Stage"] == 1)].to_csv('Stage1 Semester 2 Enrollments.csv')
seniors_df[(seniors_df["Semester"] == 1) & (seniors_df["Stage"] == 2)].to_csv('Stage2 Enrollments.csv')
swd_df[(swd_df["Semester"] == 1) & (swd_df["Stage"] == 1)].to_csv('Stage1 SWD Enrollments.csv')
swd_df[(swd_df["Semester"] == 1) & (swd_df["Stage"] == 2)].to_csv('Stage2 SWD Enrollments.csv')

print("Done!")