import sqlite3
import xml.etree.ElementTree as ET
import pandas as pd

# Database setup
try:
    conn = sqlite3.connect(':memory:')
    conn.execute('''CREATE TABLE Student(
            student_id TEXT PRIMARY KEY NOT NULL,
            student_code TEXT NOT NULL
        );''')
    conn.execute('''CREATE TABLE Subject(
            subject_id TEXT PRIMARY KEY NOT NULL,
            subject_code TEXT NOT NULL
        );''')
    conn.execute('''CREATE TABLE Option(
            option_id TEXT PRIMARY KEY NOT NULL,
            subject_id TEXT NOT NULL,
            subgrid_no INT NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
        );''')
    conn.execute('''CREATE TABLE Preference(
            student_id TEXT NOT NULL,
            option_id TEXT NOT NULL,
            PRIMARY KEY (student_id, option_id),
            FOREIGN KEY (student_id) REFERENCES Student(student_id),
            FOREIGN KEY (option_id) REFERENCES Option(option_id)
        );''')
    print("Database Created Sucessfully!")
except:
    print("Database failed to create, exiting!")
    quit()

# Import Data from xml file
sof_file = ET.parse('ttd_files\\2022 Year 9 Students.sof9')
sof_root = sof_file.getroot()

# Import Student Data
sql = ''' INSERT INTO Student(student_id, student_code) VALUES(?,?)'''
for students in sof_root.findall('.//{http://www.timetabling.com.au/S0V9}Students/{http://www.timetabling.com.au/S0V9}Student'):
    student_id = students.find('{http://www.timetabling.com.au/S0V9}StudentID').text
    student_code = students.find('{http://www.timetabling.com.au/S0V9}StudentCode').text
    cur = conn.cursor()
    cur.execute(sql, (student_id, student_code))
    conn.commit()

# Import Subjects
sql = ''' INSERT INTO Subject(subject_id, subject_code) VALUES(?,?)'''
for subject in sof_root.findall('.//{http://www.timetabling.com.au/S0V9}Subjects/{http://www.timetabling.com.au/S0V9}Subject'):
    subject_id = subject.find('{http://www.timetabling.com.au/S0V9}SubjectID').text
    subject_code = subject.find('{http://www.timetabling.com.au/S0V9}SubjectCode').text
    cur = conn.cursor()
    cur.execute(sql, (subject_id, subject_code))
    conn.commit()

# Import Options
sql = ''' INSERT INTO Option(option_id, subject_id, subgrid_no) VALUES(?,?,?)'''
for options in sof_root.findall('.//{http://www.timetabling.com.au/S0V9}Options/{http://www.timetabling.com.au/S0V9}Option'):
    option_id = options.find('{http://www.timetabling.com.au/S0V9}OptionID').text
    subject_id = options.find('{http://www.timetabling.com.au/S0V9}SubjectID').text
    subgrid_number = options.find('{http://www.timetabling.com.au/S0V9}SubgridNo').text
    cur = conn.cursor()
    cur.execute(sql, (option_id, subject_id,  subgrid_number))
    conn.commit()

# Import Preferences
sql = ''' INSERT INTO Preference(student_id, option_id) VALUES(?,?)'''
for preferences in sof_root.findall('.//{http://www.timetabling.com.au/S0V9}Preferences/{http://www.timetabling.com.au/S0V9}Preference'):
    student_id = preferences.find('{http://www.timetabling.com.au/S0V9}StudentID').text
    option_id = preferences.find('{http://www.timetabling.com.au/S0V9}OptionID').text
    cur = conn.cursor()
    cur.execute(sql, (student_id, option_id))
    conn.commit()

# Get the Students codes and preferences by subject code
sql = '''SELECT stu.student_code AS StudentCode, sub.subject_code AS SubjectCode, opt.subgrid_no as SubgridNo
        FROM Preference p
        INNER JOIN Student stu ON p.student_id = stu.student_id
        INNER JOIN Option opt ON p.option_id = opt.option_id
        INNER JOIN Subject sub ON opt.subject_id = sub.subject_id'''
sof_data = pd.read_sql(sql, conn)
# Convert StudentCode (Their ID) to Integer and resort index
sof_data["StudentCode"] = pd.to_numeric(sof_data["StudentCode"])
sof_data["SubgridNo"] = pd.to_numeric(sof_data["SubgridNo"])
sof_data.reset_index(drop=True, inplace=True)
# Reorder columns
sof_data = sof_data[["StudentCode", "SubjectCode", "SubgridNo"]]

edsas_data = pd.read_csv('ttd_files\Current Subjects.csv')
# Rename Columns
edsas_data = edsas_data.rename(columns=
                                    {edsas_data.columns[0]: "SubjectCode",
                                    edsas_data.columns[1]: 'SubgridNo',
                                    edsas_data.columns[2]: 'StudentCode'}
                                )
edsas_data = edsas_data[["StudentCode", "SubjectCode", "SubgridNo"]]

# To change Dataframe, combines both and drops matching data
edsas_data.drop(edsas_data.index[edsas_data['SubgridNo'] == 0.0], inplace=True)
# Change Academic Periods 5 and 6 for 9-11 to Subgrids 1 and 2
edsas_data.loc[edsas_data.SubgridNo == 5.0, 'SubgridNo'] = 1.0
edsas_data.loc[edsas_data.SubgridNo == 6.0, 'SubgridNo'] = 2.0
edsas_data.reset_index(drop=True, inplace=True)

print(sof_data)
print(edsas_data)

# df1.merge(df2, left_on='lkey', right_on='rkey')

# sof_data.merge(edsas_data, left_on='StudentCode', right_on='StudentCode')


print(sof_data.compare(edsas_data))



print("Done!")