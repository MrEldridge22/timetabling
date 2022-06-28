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

code_list = []


# Grab Teachers and Teachers ID
for teacher in root.findall(".//{http://www.timetabling.com.au/TDV9}Teachers/{http://www.timetabling.com.au/TDV9}Teacher/{http://www.timetabling.com.au/TDV9}Code"):
    print(teacher)