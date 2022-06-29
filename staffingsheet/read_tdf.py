import xml.etree.ElementTree as ET
import pandas as pd

tdf = ET.parse('staffingsheet\TTDS2-2022.tdf9')

root = tdf.getroot()

subject_allocation_df = pd.DataFrame(columns=['code',
                                                'firstname',    
                                                'lastname',
                                                'care', 'care_loc',
                                                'line1_class', 'line1_loc',
                                                'line2_class', 'line2_loc',
                                                'line3_class', 'line3_loc',
                                                'line4_class', 'line4_loc',
                                                'line5_class', 'line5_loc',
                                                'line6_class', 'line6_loc',
                                                'line7_class', 'line7_loc'])


# Grab Teacher UUID, Code and Name
for teacher_all in root.findall(".//{http://www.timetabling.com.au/TDV9}Teachers/{http://www.timetabling.com.au/TDV9}Teacher"):   
    teacher_id = teacher_all.find('.{http://www.timetabling.com.au/TDV9}TeacherID').text
    teacher_code = teacher_all.find('.{http://www.timetabling.com.au/TDV9}Code').text
    firstname = teacher_all.find('.{http://www.timetabling.com.au/TDV9}FirstName').text
    lastname = teacher_all.find('.{http://www.timetabling.com.au/TDV9}LastName').text
    # print("{0}: {1} {2}".format(code, firstname, lastname))
    