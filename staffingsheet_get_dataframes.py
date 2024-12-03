import pandas as pd
from constant_values import mainstream_lines_df, swd_lines_df, minute_loads_dict
from database_interaction import get_full_timetable_data, get_faculty_timetable_data


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
        sql_query = get_full_timetable_data(conn)
    else:
        sql_query = get_faculty_timetable_data(conn, faculty)

    # Put into dataframe
    tt_df = pd.DataFrame(sql_query)
    # print(tt_df)
    # Remove Modified from class names
    tt_df.replace(r" \(Modified\)","", inplace=True, regex=True)
    
    # Sort data out to calculate which subjects are on which line and put into a dataframe with one entry of each
    teacher_data_list = []
    # Iterate over the tt_df dataframe finding corresponding line for each daily lesson and put into a list if the lesson is found.
    for row in tt_df.itertuples(index=False):
        if row.faculty != "SWD":    # Special Ed Run different line structure, this splits it into correct lines, this is the mainstream sorter
            for index, (i, line_num) in enumerate(mainstream_lines_df[row.day].items()):
                # If the subject is found in that day, get the corresponding line which is the cell value
                if row.lesson == i:  # Found a Subject on a line!
                    if (row.roll_class == '12X' or row.roll_class == '12P') and (line_num == "Line 4" or line_num == "Line 3"):
                        subject = "12Extra" + " " + row.subject.split(" ", 1)[1] + " " + row.day[0:3] + row.lesson[1]
                        day = row.day[0:3] + row.lesson[1]
                        teacher_data_list.append([row.id, row.code, row.first_name, row.last_name, row.proposed_load, row.actual_load, row.notes, subject, row.room, line_num, day, minute_loads_dict[row.day][index]])
                    else:
                        subject = row.roll_class + " " + row.subject
                        day = row.day[0:3] + row.lesson[1]
                        teacher_data_list.append([row.id, row.code, row.first_name, row.last_name, row.proposed_load, row.actual_load, row.notes, row.subject, row.room, line_num, day, minute_loads_dict[row.day][index]])
        
        else:    # SWD Lines
            for index, (i, line_num) in enumerate(swd_lines_df[row.day].items()):
                # If the subject is found in that day, get the corresponding line which is the cell value
                if row.lesson == i:  # Found a Subject on a line!
                    # Shorten SWD Subject Names
                    if ("Math" in row.subject):
                        subject = row.subject[0:3] + " Maths"
                    elif ("Society" in row.subject):
                        subject = row.subject[0:3] + " Society and Culture"
                    elif ("Science" in row.subject):
                        subject = row.subject[0:3] + " Science"
                    elif ("Personal Learning Plan" in row.subject):
                        subject = row.subject[0:3] + " PLP"
                    elif ("Research Project" in row.subject):
                        subject = row.subject[0:3] + " RP"
                    elif ("Scien" in row.subject):
                        subject = row.subject[0:3] + " Science"
                    elif ("English" in row.subject):
                        subject = row.subject[0:3] + " English"
                    elif ("Cross" in row.subject):
                        subject = row.subject[0:3] + " Cross Disc."
                    elif ("Health" in row.subject):
                        subject = row.subject[0:3] + " Health"
                    elif ("Business" in row.subject):
                        subject = row.subject[0:3] + " Business Innovation"
                    else:
                        subject = row.subject
                    
                    day = row.day[0:3] + row.lesson[1]

                    teacher_data_list.append([row.id, row.code, row.first_name, row.last_name, row.proposed_load, row.actual_load, row.notes, subject, row.room, line_num, day, minute_loads_dict[row.day][index]])
                    # print(row.roll_class)
    
    
    
    # Put list into a dataframe, drop the duplicates
    teacher_data_df = pd.DataFrame(teacher_data_list, columns=['id', 'code', 'firstname', 'lastname', 'proposed_load', 'actual_load', 'notes', 'subject', 'room', 'line', 'day', 'class_load']) 
    # Correct Loads here
    teacher_data_df['class_load'] = teacher_data_df[['id', 'code', 'firstname', 'lastname', 'proposed_load', 'actual_load', 'notes', 'subject', 'room', 'line', 'day', 'class_load']].groupby(['id', 'code'])['class_load'].transform('sum')
       
    # Remove 12X Class Loads
    teacher_data_df.loc[teacher_data_df['subject'].str.startswith('12Extra'), 'class_load'] = 0

    # Code to catch multiple teachers for one class (permanent swaps/reliefs ect.)
    # Group by Teacher code and id. this gives each class and the days / lesson they are on combined together
    teacher_data_df['day'] = teacher_data_df[['id', 'code', 'firstname', 'lastname', 'proposed_load', 'actual_load', 'notes' , 'subject', 'room', 'line', 'day','class_load']].groupby(['id','code'])['day'].transform(lambda x: ','.join(x))
    teacher_data_df.drop_duplicates(inplace=True, ignore_index=True)
    
    # Filter out those classes with 3 or less lessons, put day code onto class name, flag if shared class for highlighting later.
    for idx, row in teacher_data_df.iterrows():
        # if len(row.day.split(",")) <= 3 and "SWD" not in row.line:
        if len(row.day.split(",")) <= 3:
            teacher_data_df.loc[idx, 'subject'] = row.subject + " " + row.day
            teacher_data_df.loc[idx, 'day'] = True
        # Get SWD swaps
        # elif len(row.day.split(",")) <= 2 and "SWD" in row.line:
        #     teacher_data_df.loc[idx, 'subject'] = row.subject + " " + row.day
        #     teacher_data_df.loc[idx, 'day'] = True
        else:
            teacher_data_df.loc[idx, 'day'] = False
        
    # Remove SWD from SWD Line names
    teacher_data_df.replace({'line': "SWD"}, inplace=True)
    # teacher_data_df['line'].replace(to_replace='SWD', value='', inplace=True)
    
    # Get the Term based subjects and combine them together.
    teacher_data_df['subject'] = teacher_data_df[['code', 'firstname', 'lastname', 'proposed_load', 'actual_load', 'notes' , 'subject', 'room', 'line', 'class_load']].groupby(['code', 'line'])['subject'].transform(lambda x: '/'.join(x))
    teacher_data_df['room'] = teacher_data_df[['code', 'firstname', 'lastname', 'proposed_load', 'actual_load', 'notes', 'subject', 'room', 'line', 'class_load']].groupby(['code', 'line'])['room'].transform(lambda x: '/'.join(x))
    teacher_data_df.drop(columns=['id'], inplace=True)
    teacher_data_df.drop_duplicates(inplace=True, ignore_index=True)
       
    # Get list of staff Codes
    staff_codes = teacher_data_df['code'].unique()
    
    for code in staff_codes:
        term_swap = False
        teacher_subjects = []
        for row in teacher_data_df.loc[teacher_data_df["code"] == code].itertuples():
            teacher_subjects.append(row.subject)

        # Search through using list comprehension and print out a list where True appears when a teacher has a subject which changes lines
        # in the change of term and change the class_load value so it's not doubled up.
        # LIMITIATION: Only 1 line swap subject per staff member!!!
        results = [True if string[-2:] == ("T2" or "T4") and "/" not in string else False for string in teacher_subjects]
        
        if True in results:
            term_subject = next((string for string in teacher_subjects if string[-2:] == ("T1" or "T3")), None)
            if term_subject is not None:
                # print(term_subject)
                teacher_data_df.loc[(teacher_data_df['code'] == code) & (teacher_data_df['subject'] == term_subject), 'class_load'] = 0

    # Calculate Actual Load based on taken Subjects
    sum_of_class_loads = teacher_data_df.groupby('code')['class_load'].sum().fillna(0)
    
    ### Put all data into one line per staff member ready for export ###
    # Create list of lists and put into dataframe ready for export
    full_line_alloc_list = []

    # Iterate through each staff member add their classes and rooms to a blank list based on line numbers
    # Check the dataframe below to ensure classes are going in the correct spots
    # Semester data will appear first, then term based subjects
    staff_codes = teacher_data_df['code'].unique()
    for staff in staff_codes:
        flattened_list = [0] * 22
        for row in teacher_data_df[teacher_data_df["code"] == staff].itertuples():
            flattened_list[0] = staff
            flattened_list[1] = row.firstname
            flattened_list[2] = row.lastname
            flattened_list[3] = row.proposed_load
            flattened_list[4] = row.actual_load
            flattened_list[5] = row.notes

            # Reset Subject variable
            subject = ""
            
            # Put classes into lines else put into care class slot
            if row.line[-1].isnumeric():
    
                # Get Term Based Subjects or Combined classes as these contain a /
                if "/" in row.subject:
                    # List of term
                    terms = ["T1", "T2", "T3", "T4"]

                    # Combined and Term based Classes
                    split_subject = row.subject.split('/')
                    
                    # Fix for SWD Classes
                    if ("S" in split_subject[0].split(" ", 1)[0]):
                        year = split_subject[0].split(" ", 1)[0]
                    else:
                        year = split_subject[0].split(" ", 1)[0] + " / " + split_subject[1].split(" ", 1)[0]
                    
                    # Catch one teacher teaching 2 12X Classes and put them on seperate lines in Excel
                    if "12X" in row.subject:
                        subject = split_subject[0].split(" ", 1)[1] + "\n" + split_subject[1].split(" ", 1)[1]
                    
                    # Filter Term Based Subjects
                    elif any(x in split_subject[0] for x in terms):
                        if (split_subject[0].split(" ")[0:-1] == split_subject[1].split(" ")[0:-1]):
                            subject = (" ".join(split_subject[0].split(" ")[1:-1]) + f" {split_subject[0].split(' ')[-1]}/{split_subject[1].split(' ')[-1]}")
                        # Catch subjects which change year levels or Subjects in term swap over
                        elif (split_subject[0][3:-3] == split_subject[1][3:-3]):
                            subject = f"{split_subject[0][3:-3]} {split_subject[0][-2:]}/{split_subject[1][-2:]}"
                        else:
                            subject = f"{split_subject[0][3:-3]} / {split_subject[1][3:-3]} {split_subject[0][-2:]}/{split_subject[1][-2:]}"
                    
                    # Don't repeat same subject name
                    elif split_subject[0].split(" ", 1)[1] == split_subject[1].split(" ", 1)[1]:
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
        # print(flattened_list)

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
                                                    'line7_class', 'line7_room',])
    subject_allocation_df.sort_values('lastname', inplace=True)
    
    subject_allocation_df['actual_load'] = subject_allocation_df['code'].replace(sum_of_class_loads)

    # print(subject_allocation_df)
    # subject_allocation_df.to_csv("Subject_Allocations.csv", index=False)

    return(subject_allocation_df)