"""
Read in main page of Staffing Sheet
"""

import pandas as pd

staffing_sheet = pd.read_excel("staffingsheet\staffing_sheet.xlsx")


print(staffing_sheet)