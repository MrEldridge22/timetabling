"""
Read in main page of staffing Sheet
"""
from numpy import full
import pandas as pd

"""
TODO:
- Mostly Working, needs to drop where there are blanks to be nans?
- Also need to stack on top of each other, Original on top change on the bottom
"""


def read_in_staffing_sheet(staffing_sheet_df):
    """
    Function to read in Staffing Sheets from Excel and create dataframes in the same format to then compare for changes
    
    Parameters:
        staffing_sheet_df: Pandas Dataframe of the Raw Excel File
        
    Returns:
        dataframe: Panads Dataframe of sorted Data
    """
    # Rename Columns and drop rows 1 and 2
    staffing_sheet_df.drop([0, 1], inplace=True)
    mapping = {
                staffing_sheet_df.columns[0]: 'staff',
                staffing_sheet_df.columns[1]: 'care',
                staffing_sheet_df.columns[2]: 'load',
                staffing_sheet_df.columns[3]: 'line1',
                staffing_sheet_df.columns[4]: 'line2',
                staffing_sheet_df.columns[5]: 'line3',
                staffing_sheet_df.columns[6]: 'line4',
                staffing_sheet_df.columns[7]: 'line5',
                staffing_sheet_df.columns[8]: 'line6',
                staffing_sheet_df.columns[9]: 'line7'
            }
    staffing_sheet_df.rename(columns=mapping, inplace=True)

    # Number of Rows per staff member and empty list to store data
    rows_per_staff = 4
    current_row = 1
    unpacked_list = [0] * 22
    full_list = []
    notes_filter_list = ["Principal", "B1", "B2", "B3", "B4", "B5", "ECT", "Leader"]

    for row in staffing_sheet_df.itertuples():
        # First row of staff block
        if current_row == 1:
            unpacked_list[1] = row.staff
            unpacked_list[8] = str(row.line1)
            unpacked_list[10] = str(row.line2)
            unpacked_list[12] = str(row.line3)
            unpacked_list[14] = str(row.line4)
            unpacked_list[16] = str(row.line5)
            unpacked_list[18] = str(row.line6)
            unpacked_list[20] = str(row.line7)
        
        elif current_row == 2:
            unpacked_list[2] = row.staff
            unpacked_list[6] = row.care
            unpacked_list[3] = row.load
            if not any(x in str(row.line1) for x in notes_filter_list):
                unpacked_list[8] = str(unpacked_list[8]) + " " + str(row.line1)
            if not any(x in str(row.line2) for x in notes_filter_list):
                unpacked_list[10] = str(unpacked_list[10]) + " " + str(row.line2)
            if not any(x in str(row.line3) for x in notes_filter_list):
                unpacked_list[12] = str(unpacked_list[12]) + " " + str(row.line3)
            if not any(x in str(row.line4) for x in notes_filter_list):   
                unpacked_list[14] = str(unpacked_list[14]) + " " + str(row.line4)
            if not any(x in str(row.line5) for x in notes_filter_list):   
                unpacked_list[16] = str(unpacked_list[16]) + " " + str(row.line5)
            if not any(x in str(row.line6) for x in notes_filter_list):   
                unpacked_list[18] = str(unpacked_list[18]) + " " + str(row.line6)
            if not any(x in str(row.line7) for x in notes_filter_list):   
                unpacked_list[20] = str(unpacked_list[20]) + " " + str(row.line7)
        
        elif current_row == 3:
            unpacked_list[0] = row.staff
            unpacked_list[7] = row.care
            unpacked_list[4] = row.load

        elif current_row == 4:
            unpacked_list[9] = str(row.line1)
            unpacked_list[11] = str(row.line2)
            unpacked_list[13] = str(row.line3)
            unpacked_list[15] = str(row.line4)
            unpacked_list[17] = str(row.line5)
            unpacked_list[19] = str(row.line6)
            unpacked_list[21] = str(row.line7)

            # Reset Current row for next teacher and append to main list
            current_row = 0
            full_list.append(unpacked_list)
            unpacked_list = [0] * 22
        
        # Increment current row
        current_row = current_row + 1

    subject_allocation_df = pd.DataFrame(full_list, columns=['code',
                                                        'firstname',    
                                                        'lastname',
                                                        'proposed_load',
                                                        'actual_load',
                                                        'notes',
                                                        'care', 'care_room',
                                                        'line1_class', 'line1_room',
                                                        'line2_class', 'line2_room',
                                                        'line3_class', 'line3_room',
                                                        'line4_class', 'line4_room',
                                                        'line5_class', 'line5_room',
                                                        'line6_class', 'line6_room',
                                                        'line7_class', 'line7_room'])
    subject_allocation_df.sort_values('lastname', inplace=True)
    subject_allocation_df.drop(columns=["proposed_load", "actual_load", "notes"], inplace=True)

    return subject_allocation_df

# Read in Staffing Sheets and put into consistent format!
modified_df = read_in_staffing_sheet(pd.read_excel('staffing_sheet_output\Subject Allocations Changed.xlsx'))
original_df = read_in_staffing_sheet(pd.read_excel('staffing_sheet_output\Subject Allocations.xlsx'))

changes_df = pd.concat([original_df, modified_df]).drop_duplicates(keep=False)
changes_df.to_csv("staffing_sheet_output\Changes.csv")