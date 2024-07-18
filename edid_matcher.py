import pandas as pd

# Import files
edsas_output = pd.read_csv("edsas_files/Output.csv")
daymap_output = pd.read_csv("edsas_files/daymap_students.csv")

# Remove unwanted columns
edsas_output.drop(["Name",
                   "Sex",
                   "Admin YL",
                   "Census YL",
                   "Roll Class",
                   "Room"],
                   axis=1,
                   inplace=True)

daymap_output.drop(["StudentID",
                    "Logon",
                    "PhoneMob",
                    "Address1",
                    "Address2",
                    "PostCode",
                    "Town",
                    "State",
                    "Title",
                    "Group",
                    "Active",
                    "DOB",
                    "Indiginous",
                    "GlobalID",
                    "EDID",
                    "SACEID",
                    "StudentFullName"],
                    axis=1,
                    inplace=True)

# Convert student names to proper text
daymap_output["Surname"] = daymap_output["Surname"].str.title()
daymap_output["Firstname"] = daymap_output["Firstname"].str.title()
daymap_output["House"] = daymap_output["House"].str.title()

# print(daymap_output)

# Rename Columns
daymap_output.rename(columns={"StudentCode": "Student ID", "Form": "Home Group", "CoreClass": "Roll Class"}, inplace=True)

# Merge to get final dataframe
full_df = pd.merge(daymap_output, edsas_output, how='left', on="Student ID")

# Filter out into different year levels and change the year
year7 = full_df[full_df['Roll Class'].str.contains('7') & ~full_df['Roll Class'].str.contains('SWD')]
year7["Year"] = 8
year8 = full_df[full_df['Roll Class'].str.contains('8') & ~full_df['Roll Class'].str.contains('SWD')]
year8["Year"] = 9
year9 = full_df[full_df['Roll Class'].str.contains('9') & ~full_df['Roll Class'].str.contains('SWD')]
year9["Year"] = 10
year10 = full_df[full_df['Roll Class'].str.contains('10') & ~full_df['Roll Class'].str.contains('SWD')]
year10["Year"] = 11
year11 = full_df[full_df['Roll Class'].str.contains('11') & ~full_df['Roll Class'].str.contains('SWD')]
year11["Year"] = 12
yearSWD = full_df[full_df['Roll Class'].str.contains('SWD') & ~full_df['Roll Class'].str.contains('12')]
yearSWD["Year"] = yearSWD["Year"] + 1
yearSWD["Roll Class"] = "SWD"

year7.to_csv("edsas_files/year8.csv")
year8.to_csv("edsas_files/year9.csv")
year9.to_csv("edsas_files/year10.csv")
year10.to_csv("edsas_files/year11.csv")
year11.to_csv("edsas_files/year12.csv")
yearSWD.to_csv("edsas_files/yearSWD.csv")
# print(yearSWD)
