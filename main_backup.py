import pandas as pd

# Subjects from Timetabler
yr7_subjects = pd.read_csv("7Codes.csv")
yr8_subjects = pd.read_csv("8Codes.csv")
yr9_subjects = pd.read_csv("9Codes.csv")
yr10_subjects = pd.read_csv("10Codes.csv")
yrSS_subjects = pd.read_csv("SSCodes.csv")
# Concat into one Dataframe
all_subjects = pd.concat([yr7_subjects, yr8_subjects, yr9_subjects, yr10_subjects, yrSS_subjects]).reset_index(drop=True)
# Export once for manual checking
# all_subjects.to_csv("All Subjects.csv", index=False)

# EDSAS Codes
edsas_subjects = pd.read_csv("EDSASCodes.csv")

# Tidy up the Class name and Class Codes
remove_codes = [" A", " B", " P", " E", " L", "L1", "L2", " O", " 1", " 2"]
# Iterate over all the subjects
for row in all_subjects.itertuples():
    for code in remove_codes:
        # if the codes listed above are found modify the name and code
        if row.sub_name[-2:] == code:
            # To get the codes which don't have a " " at the start slicing properly
            if code[0] == " ":
                all_subjects.at[row.Index, 'sub_code'] = row.sub_code[:-(len(code) - 1)]
                all_subjects.at[row.Index, 'sub_name'] = row.sub_name[:-2]
            else:
                all_subjects.at[row.Index, 'sub_code'] = row.sub_code[:-len(code)]
                all_subjects.at[row.Index, 'sub_name'] = row.sub_name[:-3]
        else:
            pass

# Drop Duplicates
all_subjects.drop_duplicates(inplace=True)
# print(all_subjects)

# Compare codes in Timetabler to codes in EDSAS, Get list of codes not in EDSAS
missing_subjects = []
for row in all_subjects.itertuples():
    if row.sub_code not in edsas_subjects['sub_code'].values:
        # Remove Year Level Numbers from subject name
        if row.sub_name[0:2] in ["07", "08", "09", "10", "11", "12"]:
            missing_subjects.append((row.sub_code, row.sub_name[3:],))
        else:
            missing_subjects.append((row.sub_code, row.sub_name,))


# Compare Subject Names in Timetabler to Names in EDSAS, Get list of Subjects which need a name change
# ignoring Missing Codes
incorrect_names = []
for row in all_subjects.itertuples():
    # Stupid EDSAS with Capital letters for Subject Names...
    if row.sub_name[3:].upper() not in edsas_subjects['sub_name'].values \
            and row.sub_code in edsas_subjects['sub_code'].values:
        if row.sub_name[0:2] in ["07", "08", "09", "10", "11", "12"]:
            incorrect_names.append((row.sub_code, row.sub_name[3:],))
        else:
            incorrect_names.append((row.sub_code, row.sub_name,))

# Output to CSV Files
missing_sub_df = pd.DataFrame.from_records(missing_subjects, columns=['sub_code', 'sub_name'])
missing_sub_df.rename(columns={'sub_code': 'Subject Code', 'sub_name': 'Subject Name'}, inplace=True)
missing_sub_df.to_csv('edsas_missing_codes.csv', index=False)

incorrect_names_df = pd.DataFrame.from_records(incorrect_names, columns=['sub_code', 'sub_name'])
incorrect_names_df.rename(columns={'sub_code': 'Subject Code', 'sub_name': 'Subject Name'}, inplace=True)
incorrect_names_df.to_csv('edsas_rename.csv', index=False)

print("Completed!")
