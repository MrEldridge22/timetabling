import pandas as pd

# Line structures
mainstream_lines_dict = {"Monday": ["Line 6", "Line 4", "Care", "Line 3", "Line 3", "PD", "Line 5"],
                "Tuesday": ["Line 7", "Line 7", "Care", "Line 6", "Line 6", "Line 2", "Line 1"],
                "Wednesday": ["Line 4", "Line 4", "Care", "Line 5", "Line 3", "Line 2", "PLT"],
                "Thursday": ["Line 2", "Line 2", "Care", "Line 1", "Line 1", "Line 6", "Line 7"],
                "Friday": ["Line 1", "Line 7", "Care", "Line 5", "Line 5", "Line 4", "Line 3"]}

swd_lines_dict = {"Monday": ["Line 4", "Line 7", "Care", "Line 3", "Line 3", "PD", "Line 5"],
                "Tuesday": ["Line 4", "Line 7", "Care", "Line 6", "Line 6", "Line 2", "Line 1"],
                "Wednesday": ["Line 4", "Line 6", "Care", "Line 5", "Line 3", "Line 2", "PLT"],
                "Thursday": ["Line 4", "Line 7", "Care", "Line 1", "Line 1", "Line 6", "Line 2"],
                "Friday": ["Line 4", "Line 7", "Care", "Line 5", "Line 5", "Line 1", "Line 3"]}

# Index is the lesson number for the day
mainstream_lines_df = pd.DataFrame(data=mainstream_lines_dict, index=["L1", "L2", "CG", "L3", "L4", "L5", "L6"])
swd_lines_df = pd.DataFrame(data=swd_lines_dict, index=["L1", "L2", "CG", "L3", "L4", "L5", "L6"])


def get_df(conn, faculty=None):
    """
    Get a Dataframe of Subject Allocations based on faculty
   
    Parameters
    ----------
    conn : Database Connection object
    faculty : str (Default None)

    Returns
    -------
    subject_allocation_df : pd.dataframe
    """
    # Pull out data in Human Readable Format and into Dataframe
    # Check to see if faculty has been supplied
    if faculty is None:
        sql_query = pd.read_sql_query('''SELECT 
                                        d.name AS day, p.name as lesson, t.first_name, t.last_name, t.code, c.name as subject, f.code as faculty, r.name as room
                                        FROM timetable tt
                                        INNER JOIN periods p ON tt.period_id = p.period_id
                                        INNER JOIN days d ON p.day_id = d.day_id
                                        INNER JOIN classes c ON tt.class_id = c.class_id
                                        INNER JOIN faculties f ON c.faculty_id = f.faculty_id
                                        INNER JOIN rooms r ON tt.room_id = r.room_id
                                        INNER JOIN teachers t ON tt.teacher_id = t.teacher_id
                                        ORDER BY t.last_name ASC;''',
                                        conn)
    else:
        sql_query = pd.read_sql_query('''SELECT 
                                        d.name AS day, p.name as lesson, t.first_name, t.last_name, t.code, c.name as subject, f.code as faculty, r.name as room
                                        FROM timetable tt
                                        INNER JOIN periods p ON tt.period_id = p.period_id
                                        INNER JOIN days d ON p.day_id = d.day_id
                                        INNER JOIN classes c ON tt.class_id = c.class_id
                                        INNER JOIN faculties f ON c.faculty_id = f.faculty_id
                                        INNER JOIN rooms r ON tt.room_id = r.room_id
                                        INNER JOIN teachers t ON tt.teacher_id = t.teacher_id
                                        WHERE f.code = (?)
                                        ORDER BY t.last_name ASC;''',
                                        conn, params=(faculty, ))

    tt_df = pd.DataFrame(sql_query)

    # Sort data out to calculate which subjects are on which line and put into a dataframe with one entry of each
    teacher_data_list = []
    # Iterates over the tt_df dataframe finding corresponding line for each daily lesson and put into a list if the lesson is found.
    for row in tt_df.itertuples(index=False):
        if row.faculty != "SpEd":    # Special Ed Run different line structure, this splits it into correct lines
            for i, line_num in mainstream_lines_df[row.day].iteritems():
                # If the subject is found in that day, get the corresponding line which is the cell value, exclude Personal Development from results also
                if row.lesson == i and row.subject.find("Personal Development") == -1:  # Found a Subject on a line!
                    teacher_data_list.append([row.code, row.first_name, row.last_name, row.subject, row.room, line_num])
        else:
            for i, line_num in swd_lines_df[row.day].iteritems():
                # If the subject is found in that day, get the corresponding line which is the cell value, exclude Personal Development from results also
                if row.lesson == i and row.subject.find("Personal Development") == -1:  # Found a Subject on a line!
                    teacher_data_list.append([row.code, row.first_name, row.last_name, row.subject, row.room, line_num])


    # Put list into a dataframe, drop the duplicate
    teacher_data_df = pd.DataFrame(teacher_data_list, columns=['code', 'firstname', 'lastname', 'subject', 'room', 'line'])
    teacher_data_df.drop_duplicates(inplace=True, ignore_index=True)

    # Put all data into one line per staff member ready for export
    # Get list of staff Codes
    staff_codes = teacher_data_df['code'].unique()

    # Create list of lists and put into dataframe ready for export
    full_line_alloc_list = []

    # Iterate through each staff member add their classes and rooms to a blank list based on line numbers
    # Check the dataframe below to ensure classes are going in the correct spots
    for code in staff_codes:
        flattened_list = [0] * 19
        for row in teacher_data_df.loc[teacher_data_df["code"] == code].itertuples():
            flattened_list[0] = row.code
            flattened_list[1] = row.firstname
            flattened_list[2] = row.lastname
            if row.line[-1].isnumeric():
                flattened_list[2* int(row.line[-1]) + 3] = row.subject
                flattened_list[2* int(row.line[-1]) + 4] = row.room
            else:
                flattened_list[3] = row.subject
                flattened_list[4] = row.room
        
        full_line_alloc_list.append(flattened_list)

    # Final dataframe for processing into excel sheet
    subject_allocation_df = pd.DataFrame(full_line_alloc_list, columns=['code',
                                                    'firstname',    
                                                    'lastname',
                                                    'care', 'care_room',
                                                    'line1_class', 'line1_room',
                                                    'line2_class', 'line2_room',
                                                    'line3_class', 'line3_room',
                                                    'line4_class', 'line4_room',
                                                    'line5_class', 'line5_room',
                                                    'line6_class', 'line6_room',
                                                    'line7_class', 'line7_room'])
    subject_allocation_df.sort_values('code', inplace=True)
    
    return(subject_allocation_df)