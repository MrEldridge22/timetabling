import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import sqlite3
import xlsxwriter
import json
import pandas as pd
import datetime

# Year Creation and Open File
year = datetime.date.today().year + 1 
main_path_school        = f"V:\\Timetabler\\Current Timetable\\{year}"
student_options_file    = f"\\{year} Year SS Students.sfx"

### Information Needed: ###
# Classes import file:
#
# 1 Contact School Number
# 2 Year
# 3 SACE Stage 1/2
# 4 SACE Subject Code 3 Character SACE Code ie MRS for Material Solutions
# 5 Credits 10 or 20
# 6 Class Number 1-98 (Allocate based on class Suffix??)
# 7 Program Variant A to Z (Not essential)
# 8 Semester 1 or 2
# 9 Teacher Code 3+ Code ie ELDD for David Eldridge
# 10 School Class Code (Not essential but would be nice)
# 11 Results Due J (June) or D (December)
#
# SACE Enrolments File:
# 1 Contact School Number
# 2 SACE Registration Number (Not essential)
# 3 Student Code ie 230000
# 4 Year
# 5 Semester 1/2
# 6 Stage 1 or 2
# 7 SACE Code 3 Character SACE Code
# 8 Credits 10 or 20
# 9 Enrolment Number False If this is not set, a new enrolment is assumed. (Not Essential) - NOT IN OUR FILE!
# 10 Results Due J (June) or D (December)
# 11 Program Variant A to Z (Not Essential) - NOT IN OUR FILE
# 12 Teaching School Number (SACE Number??) The school at which the subject is taught.
# 13 Assessment School Number (SACE Number??) The school at which the subject is assessed.
# 14 Class Number 1-98 (Allocate based on class Suffix??) - Match above??
# 15 Enrolment Status True C (Completed), D or X (Deleted), P (Proposed), E or F (Enrolled), or W (Withdrawn). Must be in upper case. (What's the default??) - NOT IN OUR FILE
# 16 Repeat Indicator False Defaults to 'N' if not set. Set to Y if repeating the subject – only applies to Stage 1 enrolments. (Not Essential)
# 17 School Class Code False Class identifier, unique within the school. Class Code from Timetabler 1MSRJ101A. (Not Essential)
# 18 Stage 1 Grade 1 Char False A, B, C, D or E.  (Not Essential) - NOT IN OUR FILE
# 19 Partial Credits unctionality not yet implemented.  (Not Essential) - NOT IN OUR FILE
# 20 ED ID Applies to EDSAS and Dux.  (Not Essential)

