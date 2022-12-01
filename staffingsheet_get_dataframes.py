import pandas as pd

# Line structures
mainstream_lines_dict = {
                        "Monday":       ["Line 6", "Line 4", "Care", "Line 3", "Line 3", "PD",      "Line 5"],
                        "Tuesday":      ["Line 7", "Line 7", "Care", "Line 6", "Line 6", "Line 2",  "Line 1"],
                        "Wednesday":    ["Line 4", "Line 4", "Care", "Line 5", "Line 3", "Line 2",  "PLT"],
                        "Thursday":     ["Line 2", "Line 2", "Care", "Line 1", "Line 1", "Line 6",  "Line 7"],
                        "Friday":       ["Line 1", "Line 7", "Care", "Line 5", "Line 5", "Line 4",  "Line 3"]
                        }

swd_lines_dict = {
                        "Monday":       ["Line 4", "Line 7", "Care", "Line 3", "Line 3", "PD",      "Line 5"],
                        "Tuesday":      ["Line 4", "Line 7", "Care", "Line 6", "Line 6", "Line 2",  "Line 1"],
                        "Wednesday":    ["Line 4", "Line 6", "Care", "Line 5", "Line 3", "Line 2",  "PLT"],
                        "Thursday":     ["Line 4", "Line 7", "Care", "Line 1", "Line 1", "Line 6",  "Line 2"],
                        "Friday":       ["Line 4", "Line 7", "Care", "Line 5", "Line 5", "Line 1",  "Line 3"]}

# Index is the lesson number for the day
mainstream_lines_df = pd.DataFrame(data=mainstream_lines_dict, index=   ["L1", "L2", "CG", "L3", "L4", "L5", "L6"])
swd_lines_df = pd.DataFrame(data=swd_lines_dict, index=                 ["L1", "L2", "CG", "L3", "L4", "L5", "L6"])


def get_df(conn, faculty=None):
    """
    Get a Dataframe of Subject Allocations based on faculty
   
    Parameters:
        conn : Database Connection object
        faculty : str (Default None)

    Returns:
        subject_allocation_df : pd.dataframe
    """
    # Pull out data in Human Readable Format and into Dataframe
    # Check to see if faculty has been supplied
    if faculty is None:
        sql_query = pd.read_sql_query('''
                                        SELECT d.name AS day,
                                            p.name AS lesson,
                                            t.first_name,
                                            t.last_name,
                                            t.code,
                                            t.proposed_load,
                                            t.actual_load,
                                            t.notes,
                                            c.name AS subject,
                                            r.name AS room,
                                            rc.name as roll_class,
                                            f.code AS faculty,
                                            c.class_id AS id
                                        FROM timetable tt
                                        INNER JOIN periods p ON tt.period_id = p.period_id
                                        INNER JOIN days d ON p.day_id = d.day_id
                                        INNER JOIN teachers t ON tt.teacher_id = t.teacher_id
                                        INNER JOIN classes c ON tt.class_id = c.class_id
                                        INNER JOIN rooms r ON tt.room_id = r.room_id
                                        INNER JOIN roll_classes rc ON tt.roll_class_id = rc.roll_class_id
                                        INNER JOIN faculties f ON c.faculty_id = f.faculty_id
                                        ORDER BY t.last_name ASC;
                                        ''',
                                        conn)
    else:
        sql_query = pd.read_sql_query('''
                                        SELECT d.name AS day,
                                            p.name AS lesson,
                                            t.first_name,
                                            t.last_name,
                                            t.code,
                                            t.proposed_load,
                                            t.actual_load,
                                            t.notes,
                                            c.name AS subject,
                                            r.name AS room,
                                            rc.name as roll_class,
                                            f.code AS faculty,
                                            c.class_id AS id
                                        FROM timetable tt
                                        INNER JOIN periods p ON tt.period_id = p.period_id
                                        INNER JOIN days d ON p.day_id = d.day_id
                                        INNER JOIN teachers t ON tt.teacher_id = t.teacher_id
                                        INNER JOIN classes c ON tt.class_id = c.class_id
                                        INNER JOIN rooms r ON tt.room_id = r.room_id
                                        INNER JOIN roll_classes rc ON tt.roll_class_id = rc.roll_class_id
                                        LEFT JOIN faculties f ON f.faculty_id = c.faculty_id
                                        WHERE t.code IN (SELECT t.code
                                                            FROM teachers t
                                                            INNER JOIN timetable tt ON tt.teacher_id = t.teacher_id
                                                            INNER JOIN classes c ON c.class_id = tt.class_id
                                                            INNER JOIN faculties f ON f.faculty_id = c.faculty_id
                                                            WHERE f.code = (?)
                                                        )
                                        ORDER BY t.last_name ASC;
                                    ''',
                                    conn, params=(faculty, ))

    # Put into dataframe
    tt_df = pd.DataFrame(sql_query)
    # print(tt_df)
    tt_df.replace(r" \(Modified\)","", inplace=True, regex=True)
    # Sort data out to calculate which subjects are on which line and put into a dataframe with one entry of each
    teacher_data_list = []
    # Iterates over the tt_df dataframe finding corresponding line for each daily lesson and put into a list if the lesson is found.
    for row in tt_df.itertuples(index=False):
        if row.faculty != "SpEd":    # Special Ed Run different line structure, this splits it into correct lines, this is the mainstream sorter
            for i, line_num in mainstream_lines_df[row.day].items():
                # If the subject is found in that day, get the corresponding line which is the cell value, exclude Personal Development from results also
                if row.lesson == i and row.subject.find("Personal Development") == -1:  # Found a Subject on a line!
                    # 12 Extra Class - Modify the Name
                    if row.roll_class == '12X' and line_num == "Line 4":
                        subject = row.roll_class + " " + row.subject.split(" ", 1)[1] + " " + row.day[0] + row.lesson[1]
                        teacher_data_list.append([row.id, row.code, row.first_name, row.last_name, row.proposed_load, row.actual_load, row.notes, subject, row.room, line_num])
                    else:
                        subject = row.roll_class + " " + row.subject
                        teacher_data_list.append([row.id, row.code, row.first_name, row.last_name, row.proposed_load, row.actual_load, row.notes, row.subject, row.room, line_num])
        
        else:    # SWD Lines
            for i, line_num in swd_lines_df[row.day].items():
                # If the subject is found in that day, get the corresponding line which is the cell value, exclude Personal Development from results also
                if row.lesson == i and row.subject.find("Personal Development") == -1:  # Found a Subject on a line!
                    teacher_data_list.append([row.id, row.code, row.first_name, row.last_name, row.proposed_load, row.actual_load, row.notes, row.subject, row.room, line_num])

    # Put list into a dataframe, drop the duplicates
    teacher_data_df = pd.DataFrame(teacher_data_list, columns=['id', 'code', 'firstname', 'lastname', 'proposed_load', 'actual_load', 'notes', 'subject', 'room', 'line'])
    teacher_data_df.drop_duplicates(inplace=True, ignore_index=True)

    # Get the Term based subjects and combine them together.
    teacher_data_df['subject'] = teacher_data_df[['code', 'firstname', 'lastname', 'proposed_load', 'actual_load', 'notes' , 'subject', 'room', 'line']].groupby(['code', 'line'])['subject'].transform(lambda x: '/'.join(x))
    teacher_data_df['room'] = teacher_data_df[['code', 'firstname', 'lastname', 'proposed_load', 'actual_load', 'notes', 'subject', 'room', 'line']].groupby(['code', 'line'])['room'].transform(lambda x: '/'.join(x))
    teacher_data_df.drop(columns=['id'], inplace=True)
    teacher_data_df.drop_duplicates(inplace=True, ignore_index=True)
    # Put all data into one line per staff member ready for export
    # Get list of staff Codes
    staff_codes = teacher_data_df['code'].unique()

    # Create list of lists and put into dataframe ready for export
    full_line_alloc_list = []

    # Iterate through each staff member add their classes and rooms to a blank list based on line numbers
    # Check the dataframe below to ensure classes are going in the correct spots
    # Semester data will appear first, then term based subjects
    for code in staff_codes:
        flattened_list = [0] * 22
        for row in teacher_data_df.loc[teacher_data_df["code"] == code].itertuples():
            flattened_list[0] = row.code
            flattened_list[1] = row.firstname
            flattened_list[2] = row.lastname
            flattened_list[3] = row.proposed_load
            flattened_list[4] = row.actual_load
            flattened_list[5] = row.notes
            
            # Put classes into lines else put into care class slot
            if row.line[-1].isnumeric():
    
                # Get Term Based Subjects or Combined classes as these contain a /
                if "/" in row.subject:
                    # Combined and Term based Classes
                    split_subject = row.subject.split('/')
                    year = split_subject[0].split(" ", 1)[0] + " / " + split_subject[1].split(" ", 1)[0]
                    
                    # Catch one teacher teaching 2 12X Classes and put them on seperate lines in Excel
                    if "12X" in row.subject:
                        subject = split_subject[0].split(" ", 1)[1] + "\n" + split_subject[1].split(" ", 1)[1]
                    
                    # Don't repeat same subject name
                    elif  split_subject[0].split(" ", 1)[1] == split_subject[1].split(" ", 1)[1]:
                        subject = split_subject[0].split(" ", 1)[1]
                    else:
                        subject = split_subject[0].split(" ", 1)[1] + " / " + split_subject[1].split(" ", 1)[1] 
                        
                    flattened_list[2* int(row.line[-1]) + 6] = year + ' ' + subject
                    flattened_list[2* int(row.line[-1]) + 7] = row.room.split('/')[0]
                
                # Standard Semester Based Single Classes
                else:
                    flattened_list[2* int(row.line[-1]) + 6] = row.subject
                    flattened_list[2* int(row.line[-1]) + 7] = row.room
            
            # Care Classes
            else:
                flattened_list[6] = row.subject
                flattened_list[7] = row.room
        
        # Add to list
        full_line_alloc_list.append(flattened_list)

    # Final dataframe for processing into excel sheet
    subject_allocation_df = pd.DataFrame(full_line_alloc_list, columns=['code',
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

    return(subject_allocation_df)