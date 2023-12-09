import pandas as pd

# Example data
data = {
    "class_code": ["A", "A", "B", "B", "A", "B"],
    "code": ["1", "1", "2", "2", "3", "2"],
    "edsas_lesson": ["Lesson 1", "Lesson 2", "Lesson 3", "Lesson 4", "Lesson 5", "Lesson 6"],
}

df = pd.DataFrame(data)

def g(df):
    return (
        df.groupby(["class_code", "code", "subject"])
        .agg(edsas_lessons=pd.NamedAgg(column="edsas_lesson", aggfunc=list))
        .reset_index()
    )

result = g(df.copy())
print(result)