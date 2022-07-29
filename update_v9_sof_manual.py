import pandas as pd
from getpass import getpass
import pymssql

password = getpass("Enter the SQL Database password for the user itstaff: ")

# Use Pymssql to connect to database
conn = pymssql.connect(server='SHS-SQL-14', user='SHSWIN\itstaff', password=password, database='DayT')

# Query to get all the current students subjects
query = '''SELECT student.[Student ID] AS StudentID
		    ,studentpe.[School Year Level] AS YearLevel
		    ,sch_cd.[Subject Code] AS SubjectCode
		    ,sch_cd.[Academic Period] AS AcademicPeriod
        FROM [DayT].[dbo].[SCHOOCD] sch_cd
        INNER JOIN [DayT].[dbo].[STUDECOU] student ON sch_cd.[Class Number] = student.[Class Number]
        INNER JOIN [DayT].[dbo].[STUDEPE1] studentpe ON student.[Student ID] = studentpe.[Student ID]
        WHERE sch_cd.[Academic Period] IS NOT NULL
            AND [School Year Level] < '12'
            AND sch_cd.[Subject Code] NOT IN ('LLI', 'PHON', 'LSUP', 'SOC SKILLS', 'FLOCARE')
            AND sch_cd.[Subject Code] NOT LIKE '%TEAL%'
            AND sch_cd.[Subject Code] NOT LIKE '%LNSP'
        ORDER BY StudentID ASC'''

# Get the data
cur = conn.cursor(as_dict=True)
cur.execute(query)
data = cur.fetchall()
db_data_df = pd.DataFrame(data)
db_data_df.drop_duplicates(keep='last', inplace=True)

db_data_df.sort_values(by=['StudentID', 'AcademicPeriod', 'SubjectCode'], inplace=True)

# Remove Core Group Letters
core_group_list = ["7MTHL", "7MTHO", "7MTHE", "7MTHP",
                    "7HUML", "7HUMO", "7HUME", "7HUMP",
                    "7ENGL", "7ENGO", "7ENGE", "7ENGP",
                    "7SCIL", "7SCIO", "7SCIE", "7SCIP",
                    "8MTHL", "8MTHO", "8MTHE", "8MTHP",
                    "8HUML", "8HUMO", "8HUME", "8HUMP",
                    "8ENGL", "8ENGO", "8ENGE", "8ENGP",
                    "8SCIL", "8SCIO", "8SCIE", "8SCIP",
                    "9MTHL", "9MTHO", "9MTHE", "9MTHP",
                    "9HUML", "9HUMO", "9HUME", "9HUMP",
                    "9ENGL", "9ENGO", "9ENGE", "9ENGP",
                    "9SCIL", "9SCIO", "9SCIE", "9SCIP",
                    "0MTHL", "0MTHO", "0MTHE", "0MTHP",
                    "0HUML", "0HUMO", "0HUME", "0HUMP",
                    "0ENGL", "0ENGO", "0ENGE", "0ENGP",
                    "0SCIL", "0SCIO", "0SCIE", "0SCIP",
                    ]

sorted_data_list = []
# Explode the Data across columns and revert Core Classes Back to Straight Subjects
for student_id in db_data_df['StudentID'].unique():
    temp_list = [student_id, db_data_df.loc[db_data_df['StudentID'] == student_id]['YearLevel'].iloc[0]]
    for row in db_data_df.loc[db_data_df['StudentID'] == student_id].itertuples():
        if row.SubjectCode[-1].isdigit():
            temp_list.append(row.SubjectCode[:-1])
        elif row.SubjectCode in core_group_list and row.SubjectCode[:-1] not in temp_list:
            temp_list.append(row.SubjectCode[:-1])
        elif row.SubjectCode not in temp_list and row.SubjectCode not in core_group_list:
            temp_list.append(row.SubjectCode)
        else:
            pass
    
    sorted_data_list.append(temp_list)

# Put into Dataframe
final_df = pd.DataFrame([x if isinstance(x, list) else [x] for x in sorted_data_list])

columns_list = ["StudentID", "Year"]
# Rename Columns
for i in range(1, len(final_df.columns) - 1):
    columns_list.append("Pref " + str(i))
final_df.columns = columns_list

# Export to CSV
final_df[final_df['Year'] == '07'].to_csv("student_choices_csv\Year 7.csv")
final_df[final_df["Year"] == '08'].to_csv("student_choices_csv\Year 8.csv")
final_df[final_df["Year"] == '09'].to_csv("student_choices_csv\Year 9.csv")
final_df[final_df["Year"] == '10'].to_csv("student_choices_csv\Year 10.csv")
final_df[final_df["Year"] == '11'].to_csv("student_choices_csv\Year 11.csv")
final_df.to_csv("student_choices_csv\All.csv")