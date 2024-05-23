"""
This is the only file that should need changing once bugs are squashed.

This file contains data strucutres for the following:
    Student Options Year Levels
    Core Group List (Put in as Roll Classes in Timetabler)
    School Line Strucutre
    File Path Locations
"""

import pandas as pd

# Student option file year levels
sfx_year_levels = ['07', '08', '09', '10', 'SS', 'SWD']

# Core groups that the school runs
core_groups = [' E', ' P', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8']

# File Paths to sfx and tfx files

# Line structures
mainstream_lines_dict = {
                        "Monday":       ["Line 6", "Line 4", "Care", "Line 3", "Line 3", "Care",    "Line 5"],
                        "Tuesday":      ["Line 7", "Line 7", "Care", "Line 6", "Line 6", "Line 2",  "Line 1"],
                        "Wednesday":    ["Line 4", "Line 4", "Care", "Line 5", "Line 3", "Line 2",  "PLT"],
                        "Thursday":     ["Line 2", "Line 2", "Care", "Line 1", "Line 1", "Line 6",  "Line 7"],
                        "Friday":       ["Line 1", "Line 7", "Care", "Line 5", "Line 5", "Line 4",  "Line 3"]
                        }

# SWD changing to Mainstream lines, maybe temporially???
swd_lines_dict = mainstream_lines_dict
# swd_lines_dict = {
#                         "Monday":       ["Line 6",      "Line 4",       "Care",     "Line 3",       "Line 3",       "Care",         "Line 5"],
#                         "Tuesday":      ["SWD Line 7",  "SWD Line 4",   "Care",     "Line 6",       "Line 6",       "Line 2",       "Line 1"],
#                         "Wednesday":    ["SWD Line 7",  "SWD Line 4",   "Care",     "Line 5",       "Line 3",       "Line 2",       "PLT"],
#                         "Thursday":     ["Line 2",      "Line 2",       "Care",     "Line 1",       "Line 1",       "Line 6",       "Line 7"],
#                         "Friday":       ["Line 1",      "SWD Line 4",   "Care",     "Line 5",       "Line 5",       "SWD Line 7",   "Line 3"]
#                         }

elite_lines_dict = {    
                        "Monday":       ["SWD Line 6", "SWD Line 4", "Care", "SWD Line 3", "SWD Line 3", "Care",        "SWD Line 5"],
                        "Tuesday":      ["SWD Line 7", "SWD Line 4", "Care", "SWD Line 6", "SWD Line 6", "SWD Line 2",  "SWD Line 1"],
                        "Wednesday":    ["SWD Line 7", "SWD Line 4", "Care", "SWD Line 5", "SWD Line 3", "SWD Line 2",  "PLT"],
                        "Thursday":     ["SWD Line 2", "SWD Line 2", "Care", "SWD Line 1", "SWD Line 1", "SWD Line 6",  "SWD Line 7"],
                        "Friday":       ["SWD Line 1", "SWD Line 4", "Care", "SWD Line 5", "SWD Line 5", "SWD Line 7",  "SWD Line 3"]

                    }

minute_loads_dict = {
                        "Monday":       [50, 50, 10, 50, 50, 60, 60],
                        "Tuesday":      [50, 50, 10, 50, 50, 60, 60],
                        "Wednesday":    [50, 50, 30, 50, 50, 50, 00],
                        "Thursday":     [50, 50, 10, 50, 50, 60, 60],
                        "Friday":       [50, 50, 10, 50, 50, 60, 60]
                    }

# Index is the lesson number for the day
mainstream_lines_df = pd.DataFrame(data=mainstream_lines_dict, index=   ["L1", "L2", "CG", "L3", "L4", "L5", "L6"])
swd_lines_df = pd.DataFrame(data=swd_lines_dict, index=                 ["L1", "L2", "CG", "L3", "L4", "L5", "L6"])

term_based_subjects = [
    "07 Design & Technology",
    "07 Drama",
    "07 Dance",
    "07 Digital Products",
    "07 Digital Technology",
    "07 Food & Nutrition",
    "07 Music", 
    "07 Visual Arts",
    "08 Dance",
    "08 Digital Technology",
    "08 Digital Products",
    "08 Drama",
    "08 Food & Nutrition",
    "08 Introduction to Media Arts",
    "08 Material Products - Metal",
    "08 Material Products - Wood",
    "08 Music",
    "08 Visual Arts"
]