import pandas as pd
from database_interaction import slimed_timetable_data
import ast

edsas_days_reference = {
    "Monday": "1M",
    "Tuesday": "2T",
    "Wednesday": "3W",
    "Thursday": "4T",
    "Friday": "5F"
}

edsas_lesson_reference = {
    "L1": "1",
    "L2": "2",
    "L3": "5",
    "L4": "6",
    "L5": "9",
    "L6": "10",
    "CG": "3",
    "PD": "9"
}

line_structure = {
    "['2T10', '4T5', '4T6', '5F1']": "Line 1",
    "['2T9', '3W9', '4T1', '4T2']": "Line 2",
    "['1M5', '1M6', '3W6', '5F10']": "Line 3",
    "['1M2', '3W1', '3W2', '5F9']": "Line 4",
    "['1M10', '3W5', '5F5', '5F6']": "Line 5",
    "['1M1', '2T5', '2T6', '4T9']": "Line 6",
    "['2T1', '2T2', '4T10', '5F2']": "Line 7",
    "['1M2', '2T2', '3W2', '5F2']": "SWD Line 4",
    "['2T1', '3W1', '4T10', '5F9']": "SWD Line 7",
    "['1M3', '1M9', '2T3', '3W3', '4T3', '5F3']": "Care"
}


class LessonMatcher:
    def __init__(self, line_structure):
        self.line_structure = line_structure

    def match_edsas_lessons(self, edsas_lessons):
        key = str(edsas_lessons)
        for full_key, value in self.line_structure.items():
            if all(sub_key in key for sub_key in ast.literal_eval(full_key)):
                return value
        return edsas_lessons

# Rest of the code remains the same


def flatten_to_edsas_lessons(df):
    return (
        df.groupby(["class_code", "code", "subject"])
        .agg(edsas_lessons=pd.NamedAgg(column="edsas_lesson", aggfunc=list))
        .reset_index()
    )

def edcrap(conn):
    tfx_data = slimed_timetable_data(conn)
    
    tfx_data["day"].replace(edsas_days_reference, inplace=True)
    tfx_data["lesson"].replace(edsas_lesson_reference, inplace=True)
    
    tfx_data["edsas_lesson"] = tfx_data["day"] + tfx_data["lesson"]
    tfx_data.drop(["day", "lesson", "id"], axis=1, inplace=True)
    
    edsas_lessons_df = flatten_to_edsas_lessons(tfx_data.copy())
    edsas_lessons_df = edsas_lessons_df.astype(str)
    
    matcher = LessonMatcher(line_structure)
    edsas_lessons_df["edsas_lessons"] = edsas_lessons_df["edsas_lessons"].apply(matcher.match_edsas_lessons)

    edsas_lessons_df.sort_values(by=["class_code"], inplace=True)
    edsas_lessons_df.rename(columns={"code": "Teacher Code", "class_code": "Subject Code", "edsas_lessons": "Line or Lessons"}, inplace=True)

    return edsas_lessons_df
