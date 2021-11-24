import pandas as pd

# Subjects from Timetabler
yr7_subjects = pd.read_csv("code_check_csvs/7_sof_export.csv")
yr8_subjects = pd.read_csv("code_check_csvs/8_sof_export.csv")
yr9_subjects = pd.read_csv("code_check_csvs/9_sof_export.csv")
yr10_subjects = pd.read_csv("code_check_csvs/10_sof_export.csv")
yrSS_subjects = pd.read_csv("code_check_csvs/ss_sof_export.csv")
# Concat into one Dataframe
all_subjects = pd.concat([yr7_subjects, yr8_subjects, yr9_subjects, yr10_subjects, yrSS_subjects]).reset_index(drop=True)
# Remove Unwanted Columns
all_subjects.drop(all_subjects.iloc[:, 0:1], inplace=True, axis=1)
all_subjects.drop(all_subjects.iloc[:, 2:], inplace=True, axis=1)
all_subjects.dropna(inplace=True)  # Remove incomplete Data

# Rename column headings
all_subjects.rename(columns={'Name': 'sub_name', 'Code ': 'sub_code'}, inplace=True)
# Export once for manual checking
# all_subjects.to_csv("All Subjects.csv", index=False)

# Uncomment to Check to ensure columns needed are present if errors
# print(all_subjects)

# EDSAS Subjects and Codes Export
edsas_subjects = pd.read_csv("code_check_csvs/edsas_export.csv")
# Tidy up EDSAS Subject Export
edsas_subjects.drop(edsas_subjects.iloc[:, 1:2], inplace=True, axis=1)
edsas_subjects.drop(edsas_subjects.iloc[:, 2:], inplace=True, axis=1)
edsas_subjects.dropna(inplace=True)  # Remove incomplete data

# Rename Column Headings
edsas_subjects.rename(columns={'Subject Code': 'sub_code', 'Subject Name': 'sub_name'}, inplace=True)

# Uncomment to Check to ensure columns needed are present if errors
# print(edsas_subjects)

# Remove the Class Codes
remove_codes = ["A", "B", "1", "2"]
for row in all_subjects.itertuples():
    for code in remove_codes:
        # if the codes listed above are found modify the name and code
        if row.sub_name[-1:] == code:
            # To get the codes which don't have a " " at the start slicing properly
            all_subjects.at[row.Index, 'sub_code'] = row.sub_code[:-len(code)]
            all_subjects.at[row.Index, 'sub_name'] = row.sub_name[:-1]
        else:
            pass

# Remove spaces and Core Group Codes at the end of the Subject Name
for row in all_subjects.itertuples():
    if row.sub_name[-1:] == " ":
        all_subjects.at[row.Index, 'sub_name'] = row.sub_name[:-1]
    elif row.sub_name[-1:] in ["L", "O", "P", "E"]:
         all_subjects.at[row.Index, 'sub_name'] = row.sub_name[:-2]
    else:
        pass

# Remove Year Level at the start of the name
for row in all_subjects.itertuples():

    if row.sub_name[0:2] in ["07", "08", "09", "10", "11", "12"]:
        all_subjects.at[row.Index, 'sub_name'] = row.sub_name[3:]

# Drop Duplicates
all_subjects.drop_duplicates(inplace=True)
# print(all_subjects)

# Compare codes in Timetabler to codes in EDSAS, Get list of codes not in EDSAS
# Merge the two dataframes together using left join, finding all the codes which exist in EDSAS
# Gets names of each subject as sub_name_x (from sof files) and sub_name_y (EDSAS) and drop all subjects that have data
# in both columns just keeping NaN in sub_name_y (EDSAS) this indicates that the code does not exist in EDSAS
missing_subjects = all_subjects.merge(edsas_subjects, on='sub_code', how='left')
missing_subjects = missing_subjects[missing_subjects['sub_name_y'].isnull()]
missing_subjects.drop(['sub_name_y'], axis=1, inplace=True)
# print(missing_subjects)

# Compare Subject Names in Timetabler to Names in EDSAS, Get list of Subjects which need a name change
# ignoring Missing Codes
incorrect_names = []
for row in all_subjects.itertuples():
    # Stupid EDSAS with Capital letters for Subject Names...
    if row.sub_name.upper() not in edsas_subjects['sub_name'].values \
            and row.sub_code in edsas_subjects['sub_code'].values:
        incorrect_names.append((row.sub_code, row.sub_name,))
    else:
        pass

# Output to CSV Files
missing_subjects.rename(columns={'sub_code': 'Subject Code', 'sub_name_x': 'Subject Name'}, inplace=True)
missing_subjects.to_csv('edsas_missing_codes.csv', index=False)

incorrect_names_df = pd.DataFrame.from_records(incorrect_names, columns=['sub_code', 'sub_name'])
incorrect_names_df.rename(columns={'sub_code': 'Subject Code', 'sub_name': 'Subject Name'}, inplace=True)
incorrect_names_df.to_csv('edsas_rename.csv', index=False)

print("Completed!")
