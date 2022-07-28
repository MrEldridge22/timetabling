import pandas as pd

# Read in Data
edsas_data = pd.read_csv('ttd_files\Current Subjects.csv')

# Year 9
year9_df = edsas_data[edsas_data['YearLevel'] == 9]
# Duplicate just the full year subjects
year9_fullyear_grid2_df = year9_df[year9_df['AcademicPeriod'] == 0]

# Modify the values to match gridlines in Student Options
# print(year9_df.pivot('StudentID', columns=['1, 2'] values='SubjectCode'))