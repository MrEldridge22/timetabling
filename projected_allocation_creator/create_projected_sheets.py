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
year = 2024

# Main file path to sfx files
main_path = f"V:\\Timetabler\\Current Timetable\\{year}"

# sfx Year Levels - No SWD
year_levels = ['SS', '10', '9', '8', '7']

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
                            14: "S2 Line 7"
                            }

choice_lines_yr10_dict = {  1:  "S1 Line 1",
                            2:  "S1 Line 4",
                            3:  "S1 Line 6",
                            4:  "S1 Line 7",
                            5:  "S2 Line 1",
                            6:  "S2 Line 4",
                            7:  "S2 Line 6",
                            8:  "S2 Line 7"
                            }

choice_lines_yr09_dict = {  1:  "S1 Line 2",
                            2:  "S1 Line 3",
                            3:  "S1 Line 5",
                            4:  "S2 Line 2",
                            5:  "S2 Line 3",
                            6:  "S2 Line 5"
                            }

choice_lines_yr08_dict = { 
                            1:  "S1 Line 1",
                            2:  "S1 Line 1 T1",
                            3:  "S1 Line 1 T2",
                            4:  "S1 Line 3",
                            5:  "S1 Line 3 T1",
                            6:  "S1 Line 3 T2",
                            7:  "S1 Line 7",
                            8:  "S1 Line 7 T1",
                            9:  "S1 Line 7 T2",
                            10:  "S2 Line 1",
                            11:  "S2 Line 1 T3",
                            12:  "S2 Line 1 T4",
                            13:  "S2 Line 3",
                            14:  "S2 Line 3 T3",
                            15:  "S2 Line 3 T4",
                            16:  "S2 Line 7",
                            17:  "S2 Line 7 T3",
                            18:  "S2 Line 7 T4"
                            }

choice_lines_yr07_dict = { 
                            1:  "S1 Line 2",
                            2:  "S1 Line 2 T1",
                            3:  "S1 Line 2 T2",
                            4:  "S1 Line 4",
                            5:  "S1 Line 4 T1",
                            6:  "S1 Line 4 T2",
                            7:  "S1 Line 6",
                            8:  "S1 Line 6 T1",
                            9:  "S1 Line 6 T2",
                            10:  "S2 Line 2",
                            11:  "S2 Line 2 T3",
                            12:  "S2 Line 2 T4",
                            13:  "S2 Line 4",
                            14:  "S2 Line 4 T3",
                            15:  "S2 Line 4 T4",
                            16:  "S2 Line 6",
                            17:  "S2 Line 6 T3",
                            18:  "S2 Line 6 T4"
                            }

# Subjects by Faculty
faculty_subjects_dict = {   'English':            
                                        [   '07 Literacy P',
                                            '07 Literacy',
                                            '08 Literacy',
                                            '08 Literacy P',
                                            '09 Literacy P',
                                            '09 Literacy',
                                            '10 Creative Writing',
                                            '11 English 1',
                                            '11 English 2',
                                            '11 Essential English 1',
                                            '11 Essential English 2',
                                            '11 Essential English (Literacy) 1',
                                            '11 Essential English (Literacy) 2',
                                            '12 Essential English',
                                            '12 Essential English (Modified)',
                                            '12 English'],
                            
                            'EALD':         
                                        [   '07 EALD Literacy',
                                            '08 EALD Literacy',
                                            '09 EALD Literacy',
                                            '10 EALD Literacy',
                                            '11 English as an Additional Language 1',
                                            '11 English as an Additional Language 2',
                                            '12 English as an Additional Language'],

                            'Hums':         
                                        [   '10 Civics Citizenship & Economics',
                                            '11 Modern History',
                                            '11 Politics Power & People',
                                            '11 Philosophy',
                                            '11 Society & Culture',
                                            '11 Tourism',
                                            '12 Cultural Explorations',
                                            '12 Politics Power & People',
                                            '12 Society & Culture',
                                            '12 Society & Culture (Modified)',
                                            '12 Philosophy'],

                            'RP':           
                                        [   '12 Research Project A (Yr 11s)',
                                            '12 Research Project A',
                                            '12 Research Project (Modified)'],

                            'Language':     
                                        [   '07 Italian',
                                            '07 Italian (Optional)',
                                            '08 Italian',
                                            '08 Italian (Optional)',
                                            '09 Italian',
                                            '10 Italian',
                                            '10 Italian (Beginners)',
                                            '11 Italian (Beginners)',
                                            '11 Italian (Continuers)'],
                                    
                            'Maths':
                                        [   '10 Mathematics Advanced',
                                            '10 Mathematics Essential',
                                            '10 Mathematics General',
                                            '10 Mathematics Numeracy',
                                            '10 Mathematics A',
                                            '11 Numeracy Development',
                                            '11 Specialist Mathematics A',
                                            '11 Specialist Mathematics B',
                                            '11 Mathematical Methods A',
                                            '11 Mathematical Methods B',
                                            '11 Essential Mathematics (Vocational) 1',
                                            '11 Essential Mathematics (Vocational) 2',
                                            '11 Essential Mathematics (Numeracy) 1',
                                            '11 Essential Mathematics (Numeracy) 2',
                                            '11 General Mathematics A',
                                            '11 General Mathematics B',
                                            '12 Essential Mathematics',
                                            '12 General Mathematics',
                                            '12 Mathematical Methods',
                                            '12 Specalist Mathematics',
                                            '12 Mathematics Skills for Life (Modified)',
                                            '12 Math Skills for Life (IL)'],
                                    
                            'Science':      
                                        [   '11 Biology A',
                                            '11 Biology B',
                                            '11 Chemistry 1',
                                            '11 Chemistry 2',
                                            '11 Nutrition A',
                                            '11 Nutrition B',
                                            '11 Psychology A',
                                            '11 Psychology B',
                                            '11 Physics 1',
                                            '11 Physics 2',
                                            '11 Scientific Studies A',
                                            '11 Scientific Studies B',
                                            '12 Biology',
                                            '12 Chemistry',
                                            '12 Nutrition',
                                            '12 Psychology (IL)',
                                            '12 Psychology',
                                            '12 Physics',
                                            '12 Scientific Studies',
                                            '12 Scientific Studies (Modifed)'],

                            'HPE':      
                                        [   '07 Health & Physical Education',
                                            '08 Health & Physical Education',
                                            '09 Health & Physical Education',
                                            '10 Health & Physical Education 1',
                                            '10 Health & Physical Education 2',
                                            '10 Aboriginal Careers Exploration',
                                            '10 Soccer Academy (IL)',
                                            '11 Child Studies A',
                                            '11 Child Studies B',
                                            '11 Health & Wellbeing A',
                                            '11 Health & Wellbeing B',
                                            '11 Positive Education',
                                            '11 Outdoor Education A',
                                            '11 Outdoor Education B',
                                            '11 Physical Education A',
                                            '11 Physical Education B',
                                            '12 Child Studies',
                                            '12 Power Cup (Modified)',
                                            '12 Health & Wellbeing',
                                            '12 Health & Wellbeing (Modified)',
                                            '12 SAASTA (IL)',
                                            '12 Child Studies (Modified)',
                                            '12 Sport Health & Physical Activity (IL)',
                                            '12 Outdoor Education',
                                            '12 Sport Health and Physical Activity (Modified)',
                                            '12 Physical Education'
                                            '12 Outdoor Education (Modified)',
                                            '12 Science and Healthy Lifestyle (IL)'],

                            'Food Tech':
                                        [   '07 Food & Nutrition',
                                            '08 Food & Nutrition',
                                            '09 Food & Nutrition',
                                            '09 Food Innovation',
                                            '10 Food & Nutrition',
                                            '10 Food Innovation',
                                            '11 Food and Hospitality Studies',
                                            '11 Food Innovation',
                                            '12 Food & Hospitality Studies',
                                            '12 Food & Hospitality (Modified)',
                                            '12 Food Innovation'],

                            'Digi Tech':
                                        [   '07 Digital Technology',
                                            '07 Digital Products',
                                            '08 Digital Technology',
                                            '08 Digital Products',
                                            '09 Digital Technology',
                                            '09 Digital Products',
                                            '09 Digital Photography',
                                            '10 Digital Technology',
                                            '10 Digital Products',
                                            '10 Digital Photography',
                                            '11 Photography A',
                                            '11 Photography B',
                                            '11 Digital Products',
                                            '11 Digital Technology',
                                            '12 Digital Photography',
                                            '12 Digital Products',
                                            '12 Digital Technology'],
                            'Arts':
                                        [   '07 Dance',
                                            '07 Drama',
                                            '07 Music',
                                            '07 Visual Art',
                                            '08 Dance',
                                            '08 Drama',
                                            '08 Introduction to Media Arts',
                                            '08 Music',
                                            '08 Visual Art',
                                            '09 Dance',
                                            '09 Drama',
                                            '09 Media Arts A - Film & Cinematography',
                                            '09 Media Arts B - Animation',
                                            '09 Music',
                                            '09 Visual Art',
                                            '10 Dance A',
                                            '10 Dance B',
                                            '10 Drama A',
                                            '10 Drama B',
                                            '10 Media Arts: Film & Cinematography',
                                            '10 Media Arts: Animation',
                                            '10 Music A',
                                            '10 Music B',
                                            '10 Specialist Music - Band (IL)',
                                            '10 Visual Arts A',
                                            '10 Visual Arts B',
                                            '11 Creative Arts Music',
                                            '11 Music Experience A',
                                            '11 Music Experience B',
                                            '11 Specialist Music - Band (IL)',
                                            '11 Urban Street & Community Art',
                                            '11 Dance (IL)',
                                            '11 Stage Production (Integrated Learning)',
                                            '11 Art Practical A',
                                            '11 Art Practical B',
                                            '11 Media Film and Animation',
                                            '12 Urban Street & Community Art (Modified)',
                                            '12 Stage Production (Modified)',
                                            '12 Stage Production (IL)',
                                            '12 Urban Street & Community Art (IL)',
                                            '12 Visual Art',
                                            '12 Creative Arts (Music Focus)'],

                            'Design Tech':
                                        [   '07 Design & Technology',
                                            '08 Material Products - Metal',
                                            '08 Material Products - Wood',
                                            '09 Engineering Technology',
                                            '09 Material Products - Metal',
                                            '09 Material Products - Wood',
                                            '10 3D Modelling',
                                            '10 Engineering Technology',
                                            '10 Jewllery Design',
                                            '10 Materials Design with Metal',
                                            '10 Materials Design with Wood',
                                            '10 Introduction to Construction',
                                            '11 Material Solutions (Jewellery)',
                                            '11 Material Solutions (Metalwork)',
                                            '11 Material Solutions (Woodwork)',
                                            '11 Robotic & Electronic Systems A',
                                            '11 Robotic & Electronic Systems B',
                                            '12 Construction Technology',
                                            '12 Material Solutions Metal (Modified)',
                                            '12 Material Solutions Wood (Modified)',
                                            '12 Material Solutions (Metalwork)',
                                            '12 Material Solutions (Furniture Construction)',
                                            '12 Robotic & Electronic Systems',
                                            '12 Wood and Metal (Modified)',
                                            '12 Industry Connections Construction'],
                            'PLP':
                                        [   '11 Personal Learning Plan',
                                            '12 Workplace Practices',
                                            '12 Workplace Practices (Modified)'],
                            'Intervention':
                                        [   '07 Learning Support',
                                            '08 Learning Support',
                                            '09 Learning Support',
                                            '10 Learning Support']
                                    }

# Create tempory database in memory.
conn = sqlite3.connect(':memory:')

### NEEDS OPTIMISING, USE LOOP AND LIST OF SFX YEARS!! ###
### CREATE TABLES ###
for yrLevel in year_levels:
    # Create Database Table
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
yrSS_df = get_subjects("SS")
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
    if 'T1' in r.line or 'T2' in r.line or 'T3' in r.line or 'T4' in r.line:
        r.subject = r.subject + r.line[-3:]
        r.num_classes = r.num_classes / 2
        r.line = r.line[:-3]
    return r

full_subjects_df = full_subjects_df.apply(lambda row: remove_terms_hpe(row), axis=1)

print(full_subjects_df)

# Split into Semesters and strip off Semester Codes
semester_1_df = full_subjects_df[full_subjects_df.line.str.contains('S1')]
semester_1_df['line'] = semester_1_df['line'].str.replace("S1 ", "")
semester_2_df = full_subjects_df[full_subjects_df.line.str.contains('S2')]
semester_2_df['line'] = semester_2_df['line'].str.replace("S2 ", "")

### OUTPUT ###

# Location
workbook = xlsxwriter.Workbook('projected_allocation_creator\Subject Allocations.xlsx')

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
        # semester_sheet.write('A' + str(line_start + max_line_length), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 11, 'bold': True, 'bottom': True}))
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