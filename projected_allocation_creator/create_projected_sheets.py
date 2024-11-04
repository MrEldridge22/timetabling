import sqlite3
import xlsxwriter
import json
import pandas as pd
from datetime import date

### DEBUG
pd.set_option('display.max_rows', None)

### NOTE
# Need to create Version 10 Files first for this to work, these are JSON enNamed rather than XML enNamed.
# Using Version 10 in 2023, no point in spending time for Version 9 creation.
# Ensure Network Paths are accessible prior to running.
# Need to edit dictionary below for choice lines from SoF Files

# Put all database creation and data insertion into one file, use the executestatements call to create all tables in one hit.
# Use f strings for the functions to allow for different year levels to be put in.
# Put entire files into database???


# Choice lines, how to do this? Dictionary and have sfx lines as keys changing line number, how do I get semesters / terms then??

### sfx FILES Information ###
# Time table year
year = 2025

# Main file path to sfx files
main_path = f"V:\\Timetabler\\Current Timetable\\{year}"
# main_path = f"C:\\Users\\deldridge\\OneDrive - Department for Education\\Documents\\Timetabling\\{year}"

# sfx Year Levels - No SWD
year_levels = ['SeniorSchool', '10', '9', '8', '7']

# Line Strucutres
choice_lines_SS_dict = {    1:  "S1 Line 1",
                            2:  "S1 Line 2",
                            3:  "S1 Line 3",
                            4:  "S1 Line 4",
                            5:  "S1 Line 5",
                            6:  "S1 Line 6",
                            7:  "S1 Line 7",
                            8:  "S2 Line 1",
                            9:  "S2 Line 2",
                            10: "S2 Line 3",
                            11: "S2 Line 4",
                            12: "S2 Line 5",
                            13: "S2 Line 6",
                            14: "S2 Line 7",
                            15: "S2 Line 8",
                            }

choice_lines_yr10_dict = {  1:  "S1 Line 5",
                            2:  "S1 Line 6",
                            3:  "S1 Line 7",
                            4:  "S1 Line 2",
                            5:  "S1 Line 4",
                            6:  "S2 Line 5",
                            7:  "S2 Line 6",
                            8:  "S2 Line 7",
                            9:  "S2 Line 2",
                            10:  "S2 Line 4"
                            }

choice_lines_yr09_dict = {  1:  "S1 Line 2",
                            2:  "S1 Line 4",
                            3:  "S1 Line 7",
                            4:  "S2 Line 2",
                            5:  "S2 Line 4",
                            6:  "S2 Line 7"
                            }

choice_lines_yr08_dict = { 
                            1:  "S1 Line 1",
                            2:  "S1 Line 1 T1",
                            3:  "S1 Line 1 T2",
                            4:  "S1 Line 4",
                            5:  "S1 Line 4 T1",
                            6:  "S1 Line 4 T2",
                            7:  "S1 Line 6",
                            8:  "S1 Line 6 T1",
                            9:  "S1 Line 6 T2",
                            10:  "S2 Line 1",
                            11:  "S2 Line 1 T3",
                            12:  "S2 Line 1 T4",
                            13:  "S2 Line 4",
                            14:  "S2 Line 4 T3",
                            15:  "S2 Line 4 T4",
                            16:  "S2 Line 6",
                            17:  "S2 Line 6 T3",
                            18:  "S2 Line 6 T4"
                            }

choice_lines_yr07_dict = { 
                            1:  "S1 Line 1",
                            2:  "S1 Line 1 T1",
                            3:  "S1 Line 1 T2",
                            4:  "S1 Line 3",
                            5:  "S1 Line 3 T1",
                            6:  "S1 Line 3 T2",
                            7:  "S1 Line 5",
                            8:  "S1 Line 5 T1",
                            9:  "S1 Line 5 T2",
                            10:  "S2 Line 1",
                            11:  "S2 Line 1 T3",
                            12:  "S2 Line 1 T4",
                            13:  "S2 Line 3",
                            14:  "S2 Line 3 T3",
                            15:  "S2 Line 3 T4",
                            16:  "S2 Line 5",
                            17:  "S2 Line 5 T3",
                            18:  "S2 Line 5 T4"
                            }

# Subjects by Faculty
faculty_subjects_dict = {   
                            'Care Group': [
                                '07 Care Group',
                                '08 Care Group',
                                '09 Care',
                                '10 Care Group',
                                'Stage 1 Care Group',
                                '12 Care Group'],

                            'English':            
                                        [   '07 English',
                                            '07 Literacy P',
                                            '07 Literacy',
                                            '08 English',
                                            '08 Literacy',
                                            '08 Literacy P',
                                            '09 English',
                                            '09 Literacy P',
                                            '09 Literacy',
                                            '10 English',
                                            '10 Creative Writing',
                                            'Stage 1 English 1',
                                            'Stage 1 English 2',
                                            'Stage 1 English',
                                            'Stage 1 Essential English 1',
                                            'Stage 1 Essential English 2',
                                            'Stage 1 Essential English',
                                            'Stage 1 Essential English (Literacy) 1',
                                            'Stage 1 Essential English (Literacy) 2',
                                            'Stage 1 Essential English (Literacy)',
                                            'Stage 2 Essential English',
                                            'Stage 2 Essential English (Modified)',
                                            'Stage 2 English'],
                            
                            'EALD':         
                                        [   '07 EALD Literacy',
                                            '07 Literacy E',
                                            '08 EALD Literacy',
                                            '09 EALD Literacy',
                                            '10 EALD Literacy',
                                            'Stage 1 English as an Additional Language 1',
                                            'Stage 1 English as an Additional Language',
                                            'Stage 1 English as an Additional Language 2',
                                            'Stage 2 English as an Additional Language'],

                            'Hums':         
                                        [   '07 Humanities',
                                            '08 Humanities',
                                            '09 Humanities',
                                            '10 History',
                                            '10 Civics Citizenship Economics & Business',
                                            '10 Civics Citizenship & Economics',
                                            'Stage 1 Modern History',
                                            'Stage 1 Politics Power and People',
                                            'Stage 1 Philosophy',
                                            'Stage 1 Society & Culture',
                                            'Stage 1 Tourism',
                                            "Stage 1 Women's Studies",
                                            'Stage 2 Cultural Explorations (CD)',
                                            'Stage 2 Politics Power & People',
                                            'Stage 2 Society & Culture',
                                            'Stage 2 Society & Culture (Modified)',
                                            'Stage 2 Philosophy',
                                            'Stage 2 Modern History'],

                            'EIF-AIF':           
                                        [   'Stage 1 Exploring Indentities and Futures',
                                            '11 Exploring Identities and Futures',
                                            'Stage 2 Activating Identities and Futures',
                                            'Stage 2 Activating Identities and Futures (ATAR)',
                                            'Stage 2 Workplace Practices'],

                            'Language':     
                                        [   '07 Italian',
                                            '07 Italian (Extra)',
                                            '07 Italian (Optional)',
                                            '08 Italian',
                                            '08 Italian (Extra)',
                                            '09 Italian',
                                            '10 Italian',
                                            '10 Italian (Beginners)',
                                            'Stage 1 Italian (Beginners)',
                                            'Stage 1 Italian (Continuers)'],
                                    
                            'Maths':
                                        [   '07 Mathematics',
                                            '08 Mathematics',
                                            '09 Mathematics',
                                            '10 Mathematics Advanced',
                                            '10 Mathematics Essential',
                                            '10 Mathematics General',
                                            '10 Mathematics Numeracy',
                                            '10 Mathematics A',
                                            'Stage 1 Numeracy Development',
                                            'Stage 1 Specialist Mathematics A',
                                            'Stage 1 Specialist Mathematics B',
                                            'Stage 1 Mathematical Methods A',
                                            'Stage 1 Mathematical Methods B',
                                            'Stage 1 Essential Mathematics (Vocational) 1',
                                            'Stage 1 Essential Mathematics (Vocational) 2',
                                            'Stage 1 Essential Mathematics (Numeracy) 1',
                                            'Stage 1 Essential Mathematics (Numeracy) 2',
                                            'Stage 1 General Mathematics A',
                                            'Stage 1 General Mathematics B',
                                            'Stage 1 Numeracy Development (IL)',
                                            'Stage 2 Essential Mathematics',
                                            'Stage 2 General Mathematics',
                                            'Stage 2 Mathematical Methods',
                                            'Stage 2 Specialist Mathematics',
                                            'Stage 2 Mathematics Skills for Life (Modified)',
                                            'Stage 2 Maths Skills for Life (IL)'],
                                    
                            'Science':      
                                        [   
                                             '07 Science',
                                             '08 Science',
                                             '09 Science',
                                             '10 General Science',
                                            '10 PreSACE Science',
                                            'Stage 1 Biology 1',
                                            'Stage 1 Biology 2',
                                            'Stage 1 Chemistry 1',
                                            'Stage 1 Chemistry 2',
                                            'Stage 1 Nutrition A',
                                            'Stage 1 Nutrition B',
                                            'Stage 1 Psychology A',
                                            'Stage 1 Psychology B',
                                            'Stage 1 Physics 1',
                                            'Stage 1 Physics 2',
                                            'Stage 1 Scientific Studies A',
                                            'Stage 1 Scientific Studies B',
                                            'Stage 2 Biology',
                                            'Stage 2 Chemistry',
                                            'Stage 2 Nutrition',
                                            'Stage 2 Psychology (IL)',
                                            'Stage 2 Psychology',
                                            'Stage 2 Integrated Psychology (IL)',
                                            'Stage 2 Physics',
                                            'Stage 2 Scientific Studies',
                                            'Stage 2 Scientific Studies (Modifed)'],

                            'HPE':      
                                        [   '07 Health & Physical Education',
                                            '08 Health & Physical Education',
                                            '09 Health & Physical Education',
                                            '10 Health & Physical Education 1',
                                            '10 Health & Physical Education A',
                                            '10 Health & Physical Education B',
                                            '10 Health & Physical Education 2',
                                            '10 Aboriginal Careers Exploration',
                                            '10 SAASTA ACE',
                                            '10 Soccer Academy (IL)',
                                            '10 Child Studies',
                                            'Stage 1 Child Studies A',
                                            'Stage 1 Child Studies B',
                                            'Stage 1 Health & Wellbeing A',
                                            'Stage 1 Health & Wellbeing B',
                                            'Stage 1 Positive Education',
                                            'Stage 1 Outdoor Education A',
                                            'Stage 1 Outdoor Education B',
                                            'Stage 1 Physical Education A',
                                            'Stage 1 Physical Education B',
                                            'Stage 1 Soccer Academy (IL)',
                                            'Stage 1 Sports Studies A (IL)',
                                            'Stage 1 Sports Studies B (IL)',
                                            'Stage 1 SAASTA',
                                            'Stage 2 Child Studies',
                                            'Stage 2 Power Cup (Modified)',
                                            'Stage 2 Health & Wellbeing',
                                            'Stage 2 Health & Wellbeing (Modified)',
                                            'Stage 2 SAASTA',
                                            'Stage 2 Child Studies (Modified)',
                                            'Stage 2 Sport Health & Physical Activity (IL)',
                                            'Stage 2 Outdoor Education',
                                            'Stage 2 Sport Health and Physical Activity (Modified)',
                                            'Stage 2 Physical Education',
                                            'Stage 2 Outdoor Education (Modified)',
                                            'Stage 2 Science and Healthy Lifestyle (IL)'],

                            'Food Tech':
                                        [   '07 Food & Nutrition',
                                            '08 Food & Nutrition',
                                            '09 Food & Nutrition',
                                            '09 Food Innovation',
                                            '10 Food & Nutrition',
                                            '10 Food Innovation',
                                            'Stage 1 Food and Hospitality Studies',
                                            'Stage 1 Food & Hospitality',
                                            'Stage 1 Food Innovation',
                                            'Stage 2 Food & Hospitality Studies',
                                            'Stage 2 Food and Hospitality',
                                            'Stage 2 Food & Hospitality (Modified)',
                                            'Stage 2 Food Innovation'],

                            'Digi Tech':
                                        [   '07 Digital Technology',
                                            '07 Digital Products',
                                            '08 Digital Technology',
                                            '08 Digital Products',
                                            '09 Digital Technology',
                                            '09 Digital Products',
                                            '09 Digital Photography',
                                            '09 Photography',
                                            '10 Digital Technology',
                                            '10 Cyber Security Studies',
                                            '10 Digital Products',
                                            '10 Digital Photography',
                                            'Stage 1 Digital Photography A',
                                            'Stage 1 Digital Photography B',
                                            'Stage 1 Digital Products',
                                            'Stage 1 Digital Technology',
                                            'Stage 1 Game Development (IL)',
                                            'Stage 2 Digital Photography',
                                            'Stage 2 Digital Products',
                                            'Stage 2 Digital Technology'],
                            
                            'Arts':
                                        [   '07 Dance',
                                            '07 Drama',
                                            '07 Music',
                                            '07 Visual Art',
                                            '08 Dance',
                                            '08 Drama',
                                            '08 Media',
                                            '08 Music',
                                            '08 Music - Extension',
                                            '08 Visual Art',
                                            '09 Dance',
                                            '09 Drama',
                                            '09 Film & Cinematography',
                                            '09 Animation',
                                            '09 Music',
                                            '09 Music - Extension',
                                            '09 Visual Art',
                                            '10 Dance A',
                                            '10 Dance B',
                                            '10 Drama A',
                                            '10 Drama B',
                                            '10 Film & Cinematography',
                                            '10 Animation',
                                            '10 Music A',
                                            '10 Music B',
                                            '10 Music',
                                            '10 Specialist Music A',
                                            '10 Specialist Music B',
                                            '10 Visual Art A',
                                            '10 Visual Art B',
                                            'Stage 1 Creative Arts Music',
                                            'Stage 1 Creative Arts (Media)',
                                            'Stage 1 Music Experience A',
                                            'Stage 1 Music Experience B',
                                            'Stage 1 Specialist Music - Bands (IL)',
                                            'Stage 1 Urban Street & Community Art',
                                            'Stage 1 Urban & Community Art',
                                            'Stage 1 Dance (IL)',
                                            'Stage 1 Stage Production (IL)',
                                            'Stage 1 Art Practical A',
                                            'Stage 1 Art Practical B',
                                            'Stage 1 Visual Art A',
                                            'Stage 1 Visual Art B',
                                            'Stage 1 Media Film and Animation',
                                            'Stage 2 Urban Street & Community Art (Modified)',
                                            'Stage 2 Urban & Community Art (IL)',
                                            'Stage 2 Stage Production (Modified)',
                                            'Stage 2 Stage Production (IL)',
                                            'Stage 2 Urban Street & Community Art (IL)',
                                            'Stage 2 Visual Arts',
                                            'Stage 2 Creative Arts (Music Focus)'],

                            'Design Tech':
                                        [   '07 Design & Technology',
                                            '08 Metalwork',
                                            '08 Woodwork',
                                            '09 Engineering Technology',
                                            '09 Material Products - Metalwork',
                                            '09 Material Products - Woodwork',
                                            '10 3D Modelling',
                                            '10 Engineering Technology',
                                            '10 Jewllery Design',
                                            '10 Materials Design with Metal',
                                            '10 Material Products - Metalwork',
                                            '10 Materials Design with Wood',
                                            '10 Material Products - Woodwork',
                                            '10 Introduction to Construction',
                                            '10 LEGO Design',
                                            'Stage 1 Material Solutions - Jewellery',
                                            'Stage 1 Material Solutions - Metalwork',
                                            'Stage 1 Material Solutions - Woodwork',
                                            'Stage 1 Robotic & Electronic Systems A',
                                            'Stage 1 Robotic & Electronic Systems B',
                                            'Stage 2 Construction Technology',
                                            'Stage 2 Material Solutions Metal (Modified)',
                                            'Stage 2 Material Solutions Wood (Modified)',
                                            'Stage 2 Material Solutions (Metalwork)',
                                            'Stage 2 Material Solutions (Furniture Construction)',
                                            'Stage 2 Robotic & Electronic Systems',
                                            'Stage 2 Wood and Metal (Modified)',
                                            'Stage 2 Industry Connections Construction',
                                            'Stage 2 Metalwork',
                                            'Stage 2 Furniture Construction',
                                            'Stage 2 Industry Connections'],
                            
                            'Intervention':
                                        [   '07 Learning Support',
                                            '08 Learning Support',
                                            '09 Learning Support',
                                            '10 Learning Support'],


                            'VET': [
                                            "Advanced Animal Care",
                                            "Advanced Bricklaying and Blocklaying",
                                            "Advanced Carpentry Skills",
                                            "Advanced Skills Cluster Electrotechnology (Stackable)",
                                            "Certificate II Animal Studies",
                                            "Certificate II Automotive Servicing",
                                            "Certificate II Automotive Servicing Year 2",
                                            "Certificate II Community Services",
                                            "Certificate II Construction Pathways",
                                            "Certificate II Electro-Technology (Career Start)",
                                            "Certificate II Engineering Pathways",
                                            "Certificate II Food Processing (Bakery Focus)",
                                            "Certificate III Early Childhood Education and Care",
                                            "Certificate III Early Childhood Education and Care (Year 2)",
                                            "Certificate III Health Services Assistance",
                                            "Certificate III Individual Support (Ageing or Disability)",
                                            "Certificate III Information Technology",
                                            "Certificate III Screen and Media",
                                            "Certificate II Plumbing",
                                            "Certificate II Retail Cosmetics",
                                            "Certificate II in Resources and Infrastructure Work Preparation",
                                            "Certificate II Salon Assistant",
                                            "Semester 2 Vocational and General Mathematics Exemption",
                                            "Extra Blk",
                                            "No VET Course"
                                    ]
                                    }

# Create tempory database in memory.
conn = sqlite3.connect(':memory:')

### NEEDS OPTIMISING, USE LOOP AND LIST OF SFX YEARS!! ###
### CREATE TABLES ###
for yrLevel in year_levels:
    # Create Database Table
    # print(yrLevel)
    conn.executescript(f'''
                    CREATE TABLE yr{yrLevel}_lines(
                        LineID TEXT PRIMARY KEY NOT NULL,
                        Subgrid INT NOT NULL,
                        Name INT NOT NULL);
                    CREATE TABLE yr{yrLevel}_subjects(
                        SubjectID TEXT PRIMARY KEY NOT NULL,
                        Name TEXT NOT NULL);
                    CREATE TABLE yr{yrLevel}_options(
                        OptionID TEXT PRIMARY KEY NOT NULL,
                        SubjectID TEXT NOT NULL,
                        FOREIGN KEY (SubjectID) REFERENCES yr{yrLevel}_subjects(SubjectID));
                    CREATE TABLE yr{yrLevel}_classes(
                        ClassID TEXT PRIMARY KEY NOT NULL,
                        OptionID TEXT NOT NULL,
                        LineID TEXT NOT NULL,
                        FOREIGN KEY (OptionID) REFERENCES yr{yrLevel}_options(OptionID),
                        FOREIGN KEY (LineID) REFERENCES yr{yrLevel}_lines(LineID));
                    ''')
    
    # Open sfx file
    with open(f'{main_path}\\{year} Year {yrLevel} Students.sfx', "r") as read_content:
        sfx_file = json.load(read_content)
    
    # Extract Line Info
    lines_df = pd.json_normalize(sfx_file, record_path=['Lines'])
    for col in lines_df.columns:
        if col not in ['LineID', 'Name', 'Subgrid']:
            lines_df.drop([col], inplace=True, axis=1)
    lines_df.to_sql(f'yr{yrLevel}_lines', conn, if_exists='append', index=False)

    # Extract Subject Info
    subjects_df = pd.json_normalize(sfx_file, record_path=['Subjects'])
    for col in subjects_df.columns:
            if col not in ["SubjectID", "Name"]:
                subjects_df.drop([col], inplace=True, axis=1)
    subjects_df.to_sql(f'yr{yrLevel}_subjects', conn, if_exists='append', index=False)
    
    # Check for missing subject names in the faculty_subjects_dict above
    for subject in subjects_df['Name']:
        missing_subject = all(subject not in values for values in faculty_subjects_dict.values())
        if missing_subject:
             print(subject)

    # Extract Options Info
    options_df = pd.json_normalize(sfx_file, record_path=['Options'])
    for col in options_df.columns:
            if col not in ["OptionID", "SubjectID"]:
                options_df.drop([col], inplace=True, axis=1)
    options_df.to_sql(f'yr{yrLevel}_options', conn, if_exists='append', index=False)

    # Extract Classes Info
    classes_df = pd.json_normalize(sfx_file, record_path=['Classes'])
    for col in classes_df.columns:
            if col not in ["ClassID", "OptionID", "LineID"]:
                classes_df.drop([col], inplace=True, axis=1)
    classes_df.to_sql(f'yr{yrLevel}_classes', conn, if_exists='append', index=False)


# Get all subjects by line
def get_subjects (yrLevel):
    query = f"""SELECT s.Name AS subject, l.Name as line, COUNT(s.Name || l.Name) as num_classes from yr{yrLevel}_classes c
            INNER JOIN yr{yrLevel}_options o ON o.OptionID = c.OptionID
            INNER JOIN yr{yrLevel}_subjects s on o.SubjectID = s.SubjectID
            INNER JOIN yr{yrLevel}_lines l on l.LineID = c.LineID
            GROUP BY s.Name, l.Name
            ORDER BY s.Name DESC;"""
    return pd.read_sql(query, conn)


yrSS_df = get_subjects("SeniorSchool")
yr10_df = get_subjects("10")
yr09_df = get_subjects("9")
yr08_df = get_subjects("8")
yr07_df = get_subjects("7")

# Change Lines in Dataframes to match school line names.
yrSS_df.replace({"line": choice_lines_SS_dict}, inplace=True)
yr10_df.replace({"line": choice_lines_yr10_dict}, inplace=True)
yr09_df.replace({"line": choice_lines_yr09_dict}, inplace=True)
yr08_df.replace({"line": choice_lines_yr08_dict}, inplace=True)
yr07_df.replace({"line": choice_lines_yr07_dict}, inplace=True)

# Function to get faculty name from dictionary above
def faculty_name_return(X):
    for key, value in faculty_subjects_dict.items():
        if X == value:
            return key
        if isinstance(value, list) and X in value:
            return key
    return "Key doesnt exist"

# Put Faculties onto Dataframes
yrSS_df['faculty'] = yrSS_df.apply(lambda row: faculty_name_return(row.subject), axis=1)
yr10_df['faculty'] = yr10_df.apply(lambda row: faculty_name_return(row.subject), axis=1)
yr09_df['faculty'] = yr09_df.apply(lambda row: faculty_name_return(row.subject), axis=1)
yr08_df['faculty'] = yr08_df.apply(lambda row: faculty_name_return(row.subject), axis=1)
yr07_df['faculty'] = yr07_df.apply(lambda row: faculty_name_return(row.subject), axis=1)

full_subjects_df = pd.concat([yrSS_df, yr10_df, yr09_df, yr08_df, yr07_df], ignore_index=True)
full_subjects_df = full_subjects_df[full_subjects_df['faculty'] != "Key doesnt exist"]

# Remove HPE and Italian Terms for 7's and 8's as they are semester based subjects
def remove_terms_hpe(r):
    # print(r)
    if 'T1' in r.line or 'T2' in r.line or 'T3' in r.line or 'T4' in r.line:
        r.subject = r.subject + r.line[-3:]
        r.num_classes = r.num_classes / 2
        r.line = r.line[:-3]
    return r


full_subjects_df = full_subjects_df.apply(lambda row: remove_terms_hpe(row), axis=1)

# print(full_subjects_df)

# Split into Semesters and strip off Semester Codes
semester_1_df = full_subjects_df[full_subjects_df.line.str.contains('S1')]
semester_1_df['line'] = semester_1_df['line'].str.replace("S1 ", "")
semester_2_df = full_subjects_df[full_subjects_df.line.str.contains('S2')]
semester_2_df['line'] = semester_2_df['line'].str.replace("S2 ", "")

### OUTPUT ###

# Location
workbook = xlsxwriter.Workbook(f'projected_allocation_creator\\Subject Allocations {year}.xlsx')

# Formats
subject_name_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bottom': True, 'top': True, 'left': 2})
subject_count_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': 'center', 'bottom': True, 'top': True, 'right': 2})

# Create Semester Sheets
semester_1_sheet = workbook.add_worksheet(name="Semester 1")
semester_2_sheet = workbook.add_worksheet(name="Semester 2")

# Write Headings
semester_1_sheet.merge_range('A1:O1', f"PROJECTED SUBJECT ALLOCATION  BY LINES SEMESTER 1 {(date.today().year + 1)}", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': "center"}))
semester_2_sheet.merge_range('A1:O1', f"PROJECTED SUBJECT ALLOCATION  BY LINES SEMESTER 2 {(date.today().year + 1)}", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': "center"}))

# Fucntion to creating the excel sheet
def sheet_writer(semester_df, semester_sheet):
    semester_sheet.set_landscape()  # Set to landscape
    semester_sheet.set_paper(8)     # Set to A3
    semester_sheet.set_margins(left=0.04, right=0.04, top=0.15, bottom=0.15)
    semester_sheet.freeze_panes(2, 0)
    # Set column widths
    semester_sheet.set_column(0, 0, 13)
    for i in range(1, 15):
        if (i % 2) == 0:
            semester_sheet.set_column(i, i, 4)
        else:
            semester_sheet.set_column(i, i, 30.5)
    semester_sheet.fit_to_pages(1, 1)   # Fit to 1 A3 Page
    
    # Write out Headers
    # Need Semester Heading
    semester_sheet.write("A2", "Lines", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': "center"}))
    semester_sheet.merge_range('B2:C2', "Line 1", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': "center", 'bg_color': "#FFC000", 'border': 2}))
    semester_sheet.merge_range('D2:E2', "Line 2", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': "center", 'bg_color': "#8064A2", 'border': 2}))
    semester_sheet.merge_range('F2:G2', "Line 3", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': "center", 'bg_color': "#FF66CC", 'border': 2}))
    semester_sheet.merge_range('H2:I2', "Line 4", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': "center", 'bg_color': "#FF0000", 'border': 2}))
    semester_sheet.merge_range('J2:K2', "Line 5", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': "center", 'bg_color': "#00B050", 'border': 2}))
    semester_sheet.merge_range('L2:M2', "Line 6", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': "center", 'bg_color': "#FFFF00", 'border': 2}))
    semester_sheet.merge_range('N2:O2', "Line 7", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'align': "center", 'bg_color': "#00B0F0", 'border': 2}))

    # Start line to start writing a faculties data to
    line_start = 3

    # Loop through faculties and get each line into a seperate dataframe, then use xlsxwriter to write into columns
    for faculty in faculty_subjects_dict.keys():
        temp_df = semester_df[semester_df['faculty'] == faculty].reset_index(drop=True)

        ### Write each line out as columns, one for subject and corresponding one for number of classes running       
        # Line 1
        line_1_df = temp_df[temp_df['line'] == 'Line 1'].drop(['line', 'faculty'], axis=1).reset_index(drop=True)
        semester_sheet.write_column('B' + str(line_start), line_1_df['subject'], subject_name_format)
        semester_sheet.write_column('C' + str(line_start), line_1_df['num_classes'], subject_count_format)

        # Line 2
        line_2_df = temp_df[temp_df['line'] == 'Line 2'].drop(['line', 'faculty'], axis=1).reset_index(drop=True)
        semester_sheet.write_column('D' + str(line_start), line_2_df['subject'], subject_name_format)
        semester_sheet.write_column('E' + str(line_start), line_2_df['num_classes'], subject_count_format)

        # Line 3
        line_3_df = temp_df[temp_df['line'] == 'Line 3'].drop(['line', 'faculty'], axis=1).reset_index(drop=True)
        semester_sheet.write_column('F' + str(line_start), line_3_df['subject'], subject_name_format)
        semester_sheet.write_column('G' + str(line_start), line_3_df['num_classes'], subject_count_format)

        # Line 4
        line_4_df = temp_df[temp_df['line'] == 'Line 4'].drop(['line', 'faculty'], axis=1).reset_index(drop=True)
        semester_sheet.write_column('H' + str(line_start), line_4_df['subject'], subject_name_format)
        semester_sheet.write_column('I' + str(line_start), line_4_df['num_classes'], subject_count_format)

        # Line 5
        line_5_df = temp_df[temp_df['line'] == 'Line 5'].drop(['line', 'faculty'], axis=1).reset_index(drop=True)
        semester_sheet.write_column('J'+ str(line_start), line_5_df['subject'], subject_name_format)
        semester_sheet.write_column('K' + str(line_start), line_5_df['num_classes'], subject_count_format)
        
        # Line 6
        line_6_df = temp_df[temp_df['line'] == 'Line 6'].drop(['line', 'faculty'], axis=1).reset_index(drop=True)
        semester_sheet.write_column('L' + str(line_start), line_6_df['subject'], subject_name_format)
        semester_sheet.write_column('M' + str(line_start), line_6_df['num_classes'], subject_count_format)

        # Line 7
        line_7_df = temp_df[temp_df['line'] == 'Line 7'].drop(['line', 'faculty'], axis=1).reset_index(drop=True)
        semester_sheet.write_column('N' + str(line_start), line_7_df['subject'], subject_name_format)
        semester_sheet.write_column('O' + str(line_start), line_7_df['num_classes'], subject_count_format)

        # Get largest length line for formatting
        max_line_length = max([len(line_1_df.index), len(line_2_df.index), len(line_3_df.index), len(line_4_df.index), len(line_5_df.index), len(line_6_df.index), len(line_7_df.index)])

        # Add additional formatting
        semester_sheet.write_column('B' + str(line_start + len(line_1_df.index)), [None] * (max_line_length - len(line_1_df.index)), subject_name_format)
        semester_sheet.write_column('C' + str(line_start + len(line_1_df.index)), [None] * (max_line_length - len(line_1_df.index)), subject_count_format)
        semester_sheet.write_column('D' + str(line_start + len(line_2_df.index)), [None] * (max_line_length - len(line_2_df.index)), subject_name_format)
        semester_sheet.write_column('E' + str(line_start + len(line_2_df.index)), [None] * (max_line_length - len(line_2_df.index)), subject_count_format)
        semester_sheet.write_column('F' + str(line_start + len(line_3_df.index)), [None] * (max_line_length - len(line_3_df.index)), subject_name_format)
        semester_sheet.write_column('G' + str(line_start + len(line_3_df.index)), [None] * (max_line_length - len(line_3_df.index)), subject_count_format)
        semester_sheet.write_column('H' + str(line_start + len(line_4_df.index)), [None] * (max_line_length - len(line_4_df.index)), subject_name_format)
        semester_sheet.write_column('I' + str(line_start + len(line_4_df.index)), [None] * (max_line_length - len(line_4_df.index)), subject_count_format)
        semester_sheet.write_column('J' + str(line_start + len(line_5_df.index)), [None] * (max_line_length - len(line_5_df.index)), subject_name_format)
        semester_sheet.write_column('K' + str(line_start + len(line_5_df.index)), [None] * (max_line_length - len(line_5_df.index)), subject_count_format)
        semester_sheet.write_column('L' + str(line_start + len(line_6_df.index)), [None] * (max_line_length - len(line_6_df.index)), subject_name_format)
        semester_sheet.write_column('M' + str(line_start + len(line_6_df.index)), [None] * (max_line_length - len(line_6_df.index)), subject_count_format)
        semester_sheet.write_column('N' + str(line_start + len(line_7_df.index)), [None] * (max_line_length - len(line_7_df.index)), subject_name_format)
        semester_sheet.write_column('O' + str(line_start + len(line_7_df.index)), [None] * (max_line_length - len(line_7_df.index)), subject_count_format)

        # Write faculty name in the first column
        semester_sheet.write('A' + str(line_start), faculty, workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'top': True}))
        # semester_sheet.write('A' + str(line_start + max_line_length), " ", workbook.add_format({'font_name': 'Arial', 'font_size': Stage 1, 'bold': True, 'bottom': True}))
        # Increment start counter by of number of rows in each faculty dataframe with a buffer line
        line_start = 1 + line_start + max_line_length

    # Write out formulas for column sums
    for line_column in ['C', 'E', 'G', 'I', 'K', 'M', 'O']:
         semester_sheet.write_formula(line_column + str(line_start - 1), f'=SUM({line_column}3:{line_column}{str(line_start - 2)})')
  
# Create Semester 1 and Semester 2 Staffing Sheets
sheet_writer(semester_1_df, semester_1_sheet)
sheet_writer(semester_2_df, semester_2_sheet)

# Close the workbook and write it out
workbook.close()