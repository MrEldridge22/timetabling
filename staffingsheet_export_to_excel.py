import math
from datetime import datetime
import random
from constant_values import core_groups
import re

# List of Core Groups, Could this be read in an a csv in the future?
core_groups_list = core_groups

# Colours
principal_color =       '#31869B'
ect_color =             '#92D050'
teacher_leader_color =  '#CCC0DA'
senior_leader_color =   '#009AD0'
coordinator_color =     '#9EC3DA'
other_color =           '#AFD7FF'
shared_class_color =    '#F6FCDC'

# Mapping for Care Class day replacements
day_replacements = {
    "Mon 5": "PD",
    "Mon G": "M",
    "Tue G": "Tu",
    "Wed G": "W",
    "Thu G": "Th",
    "Fri G": "F"
}

# Function to set the cell format for the shared subjects to be different from other subject cells
def highlight_shared_class(workbook, subject_name):
    if [ele for ele in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'] if (ele in str(subject_name))]:
        cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'right': True, 'bg_color': shared_class_color})
    else:
        cell_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'right': True})

    return cell_format


def create_excel_sheet(workbook, staffing_df, sheet_name, heading, fte_load="1200"):
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
    # print(staffing_df)
    # Create new sheet
    sheet = workbook.add_worksheet(name=sheet_name)
    sheet.set_margins(left=0.04, right=0.04, top=0.15, bottom=0.15)
    sheet.freeze_panes(3, 0)
    sheet.repeat_rows(0, 2)
    sheet.set_paper(9)  # A4 Paper Size
    sheet.center_horizontally()
       
    # Heading Information
    export_from_tdf_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sheet.set_footer(f'&8&K808080 Page: &P - Staffing Sheet Created On: {export_from_tdf_date}')

    # Format Full Sheet
    sheet.set_column('A:A', width=11)
    sheet.set_column('B:B', width=6)
    sheet.set_column('C:C', width=4.5)
    sheet.set_column('D:J', width=10)

    # Heading
    sheet.merge_range('A1:J1', heading, workbook.add_format({'font_name': 'Arial Black', 'font_size': 12, 'bold': True, 'align': "center"}))
    # sheet.write('I1', export_from_tdf_date, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'font_color': 'red'}))

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
    sheet.merge_range('E2:F2', "W - 5 3 PD 4 2", cell_format=line_struct_format)
    sheet.merge_range('G2:H2', "Th -  2 1 6 7", cell_format=line_struct_format)
    sheet.merge_range('I2:J2', "F - 1 7 5 4 3", cell_format=line_struct_format)
    sheet.write('A3', col_headings[0], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'bottom': True, 'left': True, 'right': True}))
    sheet.write('B3', col_headings[1], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'align': "center", 'bg_color': "#A6A6A6", 'bottom': True, 'right': True}))
    sheet.write('C3', col_headings[2], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'align': "center", 'bottom': True, 'right': True}))
    sheet.write('D3', col_headings[3], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'align': "center", 'bg_color': "#FFC000", 'bottom': True, 'right': True}))
    sheet.write('E3', col_headings[4], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'align': "center", 'bg_color': "#8064A2", 'bottom': True, 'right': True}))
    sheet.write('F3', col_headings[5], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'align': "center", 'bg_color': "#FF66CC", 'bottom': True, 'right': True}))
    sheet.write('G3', col_headings[6], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'align': "center", 'bg_color': "#FF0000", 'bottom': True, 'right': True}))
    sheet.write('H3', col_headings[7], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'align': "center", 'bg_color': "#00B050", 'bottom': True, 'right': True}))
    sheet.write('I3', col_headings[8], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'align': "center", 'bg_color': "#FFFF00", 'bottom': True, 'right': True}))
    sheet.write('J3', col_headings[9], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'bold': True, 'align': "center", 'bg_color': "#00B0F0", 'bottom': True, 'right': True}))

    # Populate Sheet Data
    start_row = 4   # Row to start writing staffing data in at
    num_rows = 4   # Number of Rows per staff member
    staff_per_page = 11
    page_breaks_list = []

    # Calculate where pagebreaks need to be
    for i in range (1, math.ceil(staffing_df.shape[0] / 11) + 1):
        page_breaks_list.append(i * staff_per_page * num_rows + start_row - 1)
    sheet.set_h_pagebreaks(page_breaks_list)
 
    # Iterate over the data and populate the sheet
    for row in staffing_df.itertuples():
        # Set row heights for subjects to be slightly larger to accomodate long subject names, set_row is 0 indexed, so this affects the 2nd and 3rd row for each teacher
        sheet.set_row(int(start_row + 0), 18)
        sheet.set_row(int(start_row + 1), 18)
        
        # Staff Name
        fte = float(row.proposed_load) / (float(fte_load) * 100)
        sheet.write('A' + str(start_row + 0), row.firstname, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'left': True, 'right': True}))
        sheet.write('A' + str(start_row + 1), row.lastname, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'left': True, 'right': True}))
        
        ### Pick one of the following 2 lines of code, this turns on and off printing the Staff ED ID in the Staffing Sheet ###
        # ON
        # sheet.write('A' + str(start_row + 2), row.code, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'left': True, 'right': True}))
        # OFF
        sheet.write('A' + str(start_row + 2), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'left': True, 'right': True}))
        
        # FTE, turned off until further notice, need to come up with a different way to caluclate FTE
        # Could use FTE from teacher details but this doesn't take into account leadership roles as FTE calculated on teaching load.
        # sheet.write('A' + str(start_row + 3), fte, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'left': True, 'bottom': True, 'right': True, 'num_format': '0.0'}))
        sheet.write('A' + str(start_row + 3), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'left': True, 'bottom': True, 'right': True, 'num_format': '0.0'}))

        # Care Class
        if row.care != 0:
            care_info = re.search(r'(?i)care\s*(.*)', row.care)
            if care_info:
                care_info = care_info.group(1)
            else:
                care_info = ""

            # Replace day codes with appropriate values
            for key, value in day_replacements.items():
                care_info = care_info.replace(key, value)

            sheet.write('B' + str(start_row + 1), row.care[:2], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
            sheet.write('B' + str(start_row + 2), row.care_room, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
            sheet.write('B' + str(start_row + 3), care_info, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))
        else:
            sheet.write('B' + str(start_row + 1), "No", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
            sheet.write('B' + str(start_row + 2), "Care", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
            sheet.write('B' + str(start_row + 3), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))

        # Blank Cells or formatting
        sheet.write('B' + str(start_row + 0), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
        

        # Load
        # Calculates how much underloaded a teacher is and returns 0 if overloaded by minutes
        under_load = round(int(int(row.proposed_load) / 100) - (int(row.actual_load) / 100), 0)
        sheet.write('C' + str(start_row + 0), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
        sheet.write('C' + str(start_row + 1), (int(row.proposed_load) / 100), workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
        sheet.write('C' + str(start_row + 2), (under_load), workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
        sheet.write('C' + str(start_row + 3), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))

        ###Lines###
        free_line_list = []

        ### DEBUG ###
        # print(f"Teacher Code: {row.code} \n Line 1: {row.line1_class} \n Line 2: {row.line2_class} \n Line 3: {row.line3_class} \n Line 4: {row.line4_class} \n Line 5: {row.line5_class} \n Line 6: {row.line6_class} \n Line 7: {row.line7_class} \n\n")

        # Line 1
        if row.line1_class != 0:
            write_line_details(row.line1_class, row.line1_room, 'D', start_row, sheet, workbook, highlight_shared_class(workbook, row.line1_class))
        else:
            free_line_list.append("D")
            
        # Line 2
        if row.line2_class != 0:
            write_line_details(row.line2_class, row.line2_room, 'E', start_row, sheet, workbook, highlight_shared_class(workbook, row.line2_class))
        else:
            free_line_list.append("E")
        
        # Line 3
        if row.line3_class != 0:
            write_line_details(row.line3_class, row.line3_room, 'F', start_row, sheet, workbook, highlight_shared_class(workbook, row.line3_class))
        else:
            free_line_list.append("F")

        # Line 4
        if row.line4_class != 0:
            write_line_details(row.line4_class, row.line4_room, 'G', start_row, sheet, workbook, highlight_shared_class(workbook, row.line4_class))
        else:
            free_line_list.append("G")
        
        # Line 5
        if row.line5_class != 0:
            write_line_details(row.line5_class, row.line5_room, 'H', start_row, sheet, workbook, highlight_shared_class(workbook, row.line5_class))
        else:
            free_line_list.append("H")

        # Line 6
        if row.line6_class != 0:
            write_line_details(row.line6_class, row.line6_room, 'I', start_row, sheet, workbook, highlight_shared_class(workbook, row.line6_class))
        else:
            free_line_list.append("I")
        
        # Line 7
        if row.line7_class != 0:
            write_line_details(row.line7_class, row.line7_room, 'J', start_row, sheet, workbook, highlight_shared_class(workbook, row.line7_class))
        else:
            free_line_list.append("J")

        # print(f"Teacher Code: {row.code}")
        # Fill in Notes into cells
        if row.notes != None:
            # print(f"Teacher Code: {row.code} Free Lines: {free_line_list}")
            free_line = str(random.choice(free_line_list))
            free_line_list.remove(free_line)
            if "Principal" in row.notes:
                notes_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'right': True, 'bottom': True, 'bg_color': principal_color})
            elif any(x in row.notes for x in ["B3", "B4", "B5"]):
                notes_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'right': True, 'bottom': True, 'bg_color': senior_leader_color})
            elif any(x in row.notes for x in ["B1", "B2"]):
                notes_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'right': True, 'bottom': True, 'bg_color': coordinator_color})
            elif "Teacher Leader" in row.notes:
                notes_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'right': True, 'bottom': True, 'bg_color': teacher_leader_color})
            elif "ECT" in row.notes:
                notes_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'right': True, 'bottom': True, 'bg_color': ect_color})
            else:
               notes_format = workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'right': True, 'bottom': True, 'bg_color': other_color}) 
            
            # sheet.write(str(free_line) + str(start_row + 0), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
            sheet.merge_range(str(free_line) + str(start_row + 0) + ':' + str(free_line) + str(start_row + 3), row.notes, notes_format)
            # sheet.write(str(free_line) + str(start_row + 3), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))    

        # Write blanks for other free lines
        for free_line in free_line_list:
            write_blank_cell(str(free_line), start_row, sheet, workbook, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'right': True}))
        
        # Increment start_row for next staff member
        start_row = start_row + num_rows


def write_line_details(subject, room, line_column, start_row, sheet, workbook, cell_format):
    """
    Function to write subjects to cells in worksheet

    Parameters:
        subject: str (subject details)
        room: str (room name)
        line_column: str (Column in Excel for a particular Line)
        start_row: str (Row in Excel to begin writing data in)
        sheet: str (Excel sheet name)
        workbook: xlsxwriter workbook object
        cell_format: dict (xlsxwriting cell format)

    Returns:
        None
    """
    try:
        # Test to get groups
        if str(subject[-2:]) in core_groups_list:
            year = subject.split(" ")[0] + " " + subject.split(" ")[-1]
            subject_name = " ".join(subject.split(" ")[1:-1])
            sheet.write(line_column + str(start_row + 0), year, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
            sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), subject_name, cell_format)
            sheet.write(line_column + str(start_row + 3), room, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))
        
        # Highlight 12X Line 4
        elif "12Extra" in str(subject) and line_column == "G":
            sheet.write(line_column + str(start_row + 0), "12Extra", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
            sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), " ".join(subject.split(" ")[1:]), workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'valign': 'vcenter', 'text_wrap': 'true', 'italic': 'true', 'right': True}))
            sheet.write(line_column + str(start_row + 3), " / ".join(room.split("/")), workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))
        
        # Spaces for combined / term classes
        elif " / " in str(subject):
            if "S" in subject.split(" ")[0]:
                sheet.write(line_column + str(start_row + 0), subject.split(" ")[0], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
                sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), " ".join(subject.split(" ")[1:]), cell_format)
                sheet.write(line_column + str(start_row + 3), " / ".join(room.split("/")), workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))
            else:
                sheet.write(line_column + str(start_row + 0), " ".join(subject.split(" ")[0:3]), workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
                sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), " ".join(subject.split(" ")[3:]), cell_format)
                sheet.write(line_column + str(start_row + 3), " / ".join(room.split("/")), workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))
        
        # Normal Classes
        else:
            sheet.write(line_column + str(start_row + 0), subject.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
            sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), subject.split(" ",1)[1], cell_format)
            sheet.write(line_column + str(start_row + 3), room, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))
    except:
        try:
            sheet.write(line_column + str(start_row + 0), subject.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
            sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), subject.split(" ",1)[1], cell_format)
            sheet.write(line_column + str(start_row + 3), room, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))
        except:
            print("Subject name in incorrect format: " + subject)


def write_blank_cell(line_column, start_row, sheet, workbook, cell_format):
    """
    Write a blank cell to the sheet
    """
    # Blank Cell with Bottom and Side Boarders
    sheet.write(line_column + str(start_row + 0), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'right': True}))
    sheet.merge_range(line_column + str(start_row + 1) + ':' + line_column + str(start_row + 2), " ", cell_format)
    sheet.write(line_column + str(start_row + 3), " ", workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'align': "center", 'bottom': True, 'right': True}))    


def write_workbook(excel_doc):
    """
    Close the excel document once complete
    :param workbook object:
    :return None:
    """
    # Close the workbook
    excel_doc.close()
    print("Staffing Sheet Created!")