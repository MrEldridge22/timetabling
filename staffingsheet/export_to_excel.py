import math
from datetime import datetime
from unittest import findTestCases

# List of Core Groups, Could this be read in an a csv in the future?
core_groups_list = [' L', 'L1', ' E', 'E1', ' P', 'P1', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6']


def create_excel_sheet(workbook, staffing_df, fte_load, sheet_name):
    """
    Creates the various sheets on the excel document
    
    Parameters
    workbook: (excel workbook object):
    staffing_df: Pandas Dataframe:
    fte_load: Str (FTE load from tdf)
    sheet_name: Str (Sheet Name to be created)
    
    Returns
    None:
    """

    # Create new sheet
    sheet = workbook.add_worksheet(name=sheet_name)
    sheet.set_margins(left=0.04, right=0.04, top=0.15, bottom=0.15)
    sheet.freeze_panes(3, 0)
    sheet.repeat_rows(0, 2)
   
    # Heading Information
    heading = "2022 Teaching Staff Sem 2"
    export_from_tdf_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Format Full Sheet
    sheet.set_column('A:A', width=11)
    sheet.set_column('B:B', width=6)
    sheet.set_column('C:C', width=4.5)
    sheet.set_column('D:J', width=10)

    # Heading
    sheet.merge_range('A1:H1', heading, workbook.add_format({'font_name': 'Arial Black', 'font_size': 12, 'bold': True, 'align': "center"}))
    sheet.write('I1', export_from_tdf_date, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'font_color': 'red'}))

    # Line Structures and column Headings
    col_headings = ["Staff",
                    "Care",
                    "Load",
                    "Line 1",
                    "Line 2",
                    "Line 3",
                    "Line 4",
                    "Line 5",
                    "Line 6",
                    "Line 7"]
    line_struct_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'italic': True, 'align': "center"})
    sheet.merge_range('A2:B2', "M - 6 4 3 PD 5", cell_format=line_struct_format)
    sheet.merge_range('C2:D2', "Tu - 7 6 2 1", cell_format=line_struct_format)
    sheet.merge_range('E2:F2', "W - 4 PD 5 3 2", cell_format=line_struct_format)
    sheet.merge_range('G2:H2', "Th -  2 1 6 7", cell_format=line_struct_format)
    sheet.merge_range('I2:J2', "F - 1 7 5 4 3", cell_format=line_struct_format)
    sheet.write('A3', col_headings[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'bottom': True, 'left': True, 'right': True}))
    sheet.write('B3', col_headings[1], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#A6A6A6", 'bottom': True, 'right': True}))
    sheet.write('C3', col_headings[2], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bottom': True, 'right': True}))
    sheet.write('D3', col_headings[3], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#FFC000", 'bottom': True, 'right': True}))
    sheet.write('E3', col_headings[4], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#8064A2", 'bottom': True, 'right': True}))
    sheet.write('F3', col_headings[5], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#FF66CC", 'bottom': True, 'right': True}))
    sheet.write('G3', col_headings[6], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#FF0000", 'bottom': True, 'right': True}))
    sheet.write('H3', col_headings[7], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#00B050", 'bottom': True, 'right': True}))
    sheet.write('I3', col_headings[8], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#FFFF00", 'bottom': True, 'right': True}))
    sheet.write('J3', col_headings[9], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#00B0F0", 'bottom': True, 'right': True}))

    # Populate Sheet Data
    start_row = 4   # Row to start writing staffing data in at
    num_rows = 4   # Number of Rows per staff member
    staff_per_page = 11
    page_breaks_list = []

    # Calculate where pagebreaks need to be
    for i in range (1, math.ceil(staffing_df.shape[0] / 11) + 1):
        page_breaks_list.append(i * staff_per_page * num_rows + start_row - 1)
    sheet.set_h_pagebreaks(page_breaks_list)

    subject_cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'right': True})
    
    # Iterate over the data and populate the sheet
    for row in staffing_df.itertuples():
        # Set row heights for subjects to be slightly larger to accomodate long subject names, set_row is 0 indexed, so this affects the 2nd and 3rd row for each teacher
        sheet.set_row(int(start_row + 0), 18)
        sheet.set_row(int(start_row + 1), 18)
        
        # Staff Name
        fte = float(row.proposed_load) / float(fte_load)
        sheet.write('A' + str(start_row + 0), row.firstname, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'left': True, 'right': True}))
        sheet.write('A' + str(start_row + 1), row.lastname, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'left': True, 'right': True}))
        sheet.write('A' + str(start_row + 2), row.code, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'left': True, 'right': True}))
        sheet.write('A' + str(start_row + 3), fte, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'left': True, 'bottom': True, 'right': True, 'num_format': '0.0'}))

        # Care Class
        if row.care != 0:
            sheet.write('B' + str(start_row + 1), row.care[:2], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
            sheet.write('B' + str(start_row + 2), row.care_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
        else:
            sheet.write('B' + str(start_row + 1), "No", workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
            sheet.write('B' + str(start_row + 2), "Care", workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
        # Blank Cells or formatting
        sheet.write('B' + str(start_row + 0), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
        sheet.write('B' + str(start_row + 3), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'bottom': True, 'right': True}))

        # Load
        # Calculates how much underloaded a teacher is and returns 0 if overloaded by minutes
        under_load = max(0, (int(row.proposed_load) - int(row.actual_load)))
        sheet.write('C' + str(start_row + 0), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
        sheet.write('C' + str(start_row + 1), (int(row.proposed_load) / 100), workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
        sheet.write('C' + str(start_row + 2), (under_load / 100), workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
        sheet.write('C' + str(start_row + 3), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'bottom': True, 'right': True}))

        ###Lines###
        # Line 1
        if row.line1_class != 0:
            write_line_details(row.line1_class, row.line1_room, 'D', start_row, sheet, workbook, subject_cell_format)
        else:
            write_blank_cell('D', start_row, sheet, workbook, subject_cell_format)
            
        # Line 2
        if row.line2_class != 0:
            write_line_details(row.line2_class, row.line2_room, 'E', start_row, sheet, workbook, subject_cell_format)
        else:
            write_blank_cell('E', start_row, sheet, workbook, subject_cell_format)
        
        # Line 3
        if row.line3_class != 0:
            write_line_details(row.line3_class, row.line3_room, 'F', start_row, sheet, workbook, subject_cell_format)
        else:
            write_blank_cell('F', start_row, sheet, workbook, subject_cell_format)

        # Line 4
        if row.line4_class != 0:
            write_line_details(row.line4_class, row.line4_room, 'G', start_row, sheet, workbook, subject_cell_format)
        else:
            write_blank_cell('G', start_row, sheet, workbook, subject_cell_format)
        
        # Line 5
        if row.line5_class != 0:
            write_line_details(row.line5_class, row.line5_room, 'H', start_row, sheet, workbook, subject_cell_format)
        else:
            write_blank_cell('H', start_row, sheet, workbook, subject_cell_format)

        # Line 6
        if row.line6_class != 0:
            write_line_details(row.line6_class, row.line6_room, 'I', start_row, sheet, workbook, subject_cell_format)
        else:
            write_blank_cell('I', start_row, sheet, workbook, subject_cell_format)
        
        # Line 7
        if row.line7_class != 0:
            write_line_details(row.line7_class, row.line7_room, 'J', start_row, sheet, workbook, subject_cell_format)
        else:
            write_blank_cell('J', start_row, sheet, workbook, subject_cell_format)

        # Increment start_row for next staff member
        start_row = start_row + num_rows
    

def write_line_details(subject, room, line_column, start_row, sheet, workbook, cell_format):
    """
    Function to write subjects to cells in worksheet

    """
    try:
        # Test to get groups
        if str(subject[-2:]) in core_groups_list:
            year = subject.split(" ")[0] + " " + subject.split(" ")[-1]
            subject_name = " ".join(subject.split(" ")[1:-1])
            sheet.write(line_column + str(start_row + 0), year, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
            sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), subject_name, cell_format)
            sheet.write(line_column + str(start_row + 3), room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'bottom': True, 'right': True}))
        
        # Highlight 12X Line 4
        elif "12X" in str(subject) and line_column == "G":
            sheet.write(line_column + str(start_row + 0), " ".join(subject.split(" ")[0:3]), workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
            sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), " ".join(subject.split(" ")[3:]), workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'italic': 'true', 'right': True}))
            sheet.write(line_column + str(start_row + 3), " / ".join(room.split("/")), workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'bottom': True, 'right': True}))
        
        # Spaces for combined / term classes
        elif " / " in str(subject):
            sheet.write(line_column + str(start_row + 0), " ".join(subject.split(" ")[0:3]), workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
            sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), " ".join(subject.split(" ")[3:]), cell_format)
            sheet.write(line_column + str(start_row + 3), " / ".join(room.split("/")), workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'bottom': True, 'right': True}))
        
        # Normal Classes
        else:
            sheet.write(line_column + str(start_row + 0), subject.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
            sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), subject.split(" ",1)[1], cell_format)
            sheet.write(line_column + str(start_row + 3), room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'bottom': True, 'right': True}))
    except:
        try:
            sheet.write(line_column + str(start_row + 0), subject.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
            sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), subject.split(" ",1)[1], cell_format)
            sheet.write(line_column + str(start_row + 3), room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'bottom': True, 'right': True}))
        except:
            print("Subject name in incorrect format: " + subject)


def write_blank_cell(line_column, start_row, sheet, workbook, cell_format):
    """
    Write a blank cell to the sheet
    """
    # Blank Cell with Bottom and Side Boarders
    sheet.write(line_column + str(start_row + 0), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'right': True}))
    sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), " ", cell_format)
    sheet.write(line_column + str(start_row + 3), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center", 'bottom': True, 'right': True}))    


def write_workbook(excel_doc):
    """
    Close the excel document once complete
    :param workbook object:
    :return None:
    """
    # Close the workbook
    excel_doc.close()
    print("Staffing Sheet Created!")