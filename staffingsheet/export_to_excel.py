import xlsxwriter
import pandas as pd
from datetime import date, datetime

def create_excel(staffing_df):
    """
    :param df Pandas Dataframe:
    :return:
    """
    # Open Workbook and create new sheet
    workbook = xlsxwriter.Workbook('Subject Allocations.xlsx')
    full_sheet = workbook.add_worksheet(name="Whole Staff")
   
    # Heading Information
    heading = "2022 Teaching Staff Sem 2"
    export_from_tdf_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Format Full Sheet
    full_sheet.set_column('A:A', width=11)
    full_sheet.set_column('B:B', width=6)
    full_sheet.set_column('C:C', width=4.5)
    full_sheet.set_column('D:J', width=10)

    # Heading
    full_sheet.merge_range('A1:H1', heading, cell_format=workbook.add_format({'font_name': 'Arial Black', 'font_size': 12, 'bold': True, 'align': "center"}))
    full_sheet.write('I1', export_from_tdf_date, workbook.add_format({'font_name': 'Arial', 'font_size': 8, 'font_color': 'red'}))

    # Line Structures and column Headings
    col_headings = ["Staff Member",
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
    full_sheet.merge_range('A2:B2', "M - 6 4 3 PD 5", cell_format=line_struct_format)
    full_sheet.merge_range('C2:D2', "Tu - 7 6 2 1", cell_format=line_struct_format)
    full_sheet.merge_range('E2:F2', "W - 4 PD 5 3 2", cell_format=line_struct_format)
    full_sheet.merge_range('G2:H2', "Th -  2 1 6 7", cell_format=line_struct_format)
    full_sheet.merge_range('I2:J2', "F - 1 7 5 4 3", cell_format=line_struct_format)
    full_sheet.write('A3', col_headings[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True}))
    full_sheet.write('B3', col_headings[1], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#A6A6A6"}))
    full_sheet.write('C3', col_headings[2], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center"}))
    full_sheet.write('D3', col_headings[3], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#FFC000"}))
    full_sheet.write('E3', col_headings[4], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#8064A2"}))
    full_sheet.write('F3', col_headings[5], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#FF66CC"}))
    full_sheet.write('G3', col_headings[6], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#FF0000"}))
    full_sheet.write('H3', col_headings[7], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#00B050"}))
    full_sheet.write('I3', col_headings[8], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#FFFF00"}))
    full_sheet.write('J3', col_headings[9], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'bold': True, 'align': "center", 'bg_color': "#00B0F0"}))

    # Populate Sheet Data
    start_row = 4   # Row to start writing staffing data in at
    num_rows = 4   # Number of Rows per staff member
    for row in staffing_df.itertuples():
    
        # Name
        full_sheet.write('A' + str(start_row + 0), row.firstname)
        full_sheet.write('A' + str(start_row + 1), row.lastname)
        full_sheet.write('A' + str(start_row + 2), row.code)

        # Care
        if row.care != 0:
            full_sheet.write('B' + str(start_row + 1), row.care[:2], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
            full_sheet.write('B' + str(start_row + 2), row.care_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
        else:
            full_sheet.write('B' + str(start_row + 1), "No", workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
            full_sheet.write('B' + str(start_row + 2), "Care", workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))


        # Load??

        # Line 1
        if row.line1_class != 0:
            try:
                full_sheet.write('D' + str(start_row + 0), row.line1_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('D' + str(start_row + 1), row.line1_class.split(" ",1)[1], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('D' + str(start_row + 2), row.line1_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
            except:
                full_sheet.write('D' + str(start_row + 0), row.line1_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('D' + str(start_row + 2), row.line1_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))


        # Line 2
        if row.line2_class != 0:
            try:
                full_sheet.write('E' + str(start_row + 0), row.line2_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('E' + str(start_row + 1), row.line2_class.split(" ",1)[1], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('E' + str(start_row + 2), row.line2_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
            except:
                full_sheet.write('E' + str(start_row + 0), row.line2_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('E' + str(start_row + 2), row.line2_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))

        # Line 3
        if row.line3_class != 0:
            try:
                full_sheet.write('F' + str(start_row + 0), row.line3_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('F' + str(start_row + 1), row.line3_class.split(" ",1)[1], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('F' + str(start_row + 2), row.line3_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
            except:
                full_sheet.write('F' + str(start_row + 0), row.line3_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('F' + str(start_row + 2), row.line3_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))

        # Line 4
        if row.line4_class != 0:
            try:
                full_sheet.write('G' + str(start_row + 0), row.line4_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('G' + str(start_row + 1), row.line4_class.split(" ",1)[1], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('G' + str(start_row + 2), row.line4_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
            except:
                full_sheet.write('G' + str(start_row + 0), row.line4_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('G' + str(start_row + 2), row.line4_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))

        # Line 5
        if row.line5_class != 0:
            try:
                full_sheet.write('H' + str(start_row + 0), row.line5_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('H' + str(start_row + 1), row.line5_class.split(" ",1)[1], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('H' + str(start_row + 2), row.line5_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
            except:
                full_sheet.write('H' + str(start_row + 0), row.line5_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('H' + str(start_row + 2), row.line5_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))


        # Line 6
        if row.line6_class != 0:
            try:
                full_sheet.write('I' + str(start_row + 0), row.line6_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('I' + str(start_row + 1), row.line6_class.split(" ",1)[1], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('I' + str(start_row + 2), row.line6_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
            except:
                full_sheet.write('I' + str(start_row + 0), row.line6_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('I' + str(start_row + 2), row.line6_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))

        # Line 7
        if row.line7_class != 0:
            try:
                full_sheet.write('J' + str(start_row + 0), row.line7_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('J' + str(start_row + 1), row.line7_class.split(" ",1)[1], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('J' + str(start_row + 2), row.line7_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
            except:
                full_sheet.write('J' + str(start_row + 0), row.line7_class.split(" ",1)[0], workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))
                full_sheet.write('J' + str(start_row + 2), row.line7_room, workbook.add_format({'font_name': 'Arial', 'font_size': 9, 'align': "center"}))


        # Increment start_row for next staff member
        start_row = start_row + num_rows

    # Close the workbook
    workbook.close()
    print("Completed!")