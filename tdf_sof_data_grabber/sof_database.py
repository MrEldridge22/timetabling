import sqlite3
import pandas as pd


def import_sfx_data(sfx, conn):
    """
    Imports Students Options File V9 Data into a Database
    
    Parameters:
    sof: Path to Student Options File
    conn: sqlite3 Database Connection
    
    Returns:
    None
    """
    
    # Read data into Dataframe
    subjects_df = pd.json_normalize(sfx, record_path=['Subjects'])

    # Drop all Columns Except SubjectID, Code and Name
    for col in subjects_df.columns:
        if col not in ["SubjectID", "Code", "Name"]:
            subjects_df.drop([col], inplace=True, axis=1)

    # Write to Database
    subjects_df.to_sql('sfx_subjects', conn, if_exists='append', index=False)


def import_edsas_codes(edsas_file, conn):
    """
    Import EDSAS Subjects into database
    
    Parameters
    edsas_file: Excel File Export from EDSAS
    conn: sqlite Database Connection"""

    # Read Excel file into Datafame
    edsas_subjects_df = pd.read_excel(edsas_file)

    # Remove all Unwanted Columns
    for col in edsas_subjects_df.columns:
        if col not in ["Subject Code", "Subject Name", "Status"]:
            edsas_subjects_df.drop([col], inplace=True, axis=1)

    # Filter out all Old Subjects and only get Active ones, O code in EDSAS
    edsas_subjects_df = edsas_subjects_df[edsas_subjects_df.Status == "O"]
    # Drop Status Column
    edsas_subjects_df.drop(["Status"], inplace=True, axis=1)
    # Rename Columns
    edsas_subjects_df.rename(columns={"Subject Code": "SubjectCode", "Subject Name": "SubjectName"}, inplace=True)

    # Write to Database
    edsas_subjects_df.to_sql('edsas_subjects', conn, if_exists='append', index=False)



def create_sof_tables(conn):
    """
    Create all the database tables needed for the sof scripts
    
    Parameters:
    conn: sqlite3 Database Connection
    
    Returns:
    None
    """

    conn.execute(
        '''
        CREATE TABLE sfx_subjects(
        SubjectID TEXT NOT NULL PRIMARY KEY,
        Code TEXT NOT NULL,
        Name TEXT NOT NULL
        );'''
    )

    conn.execute(
        '''
        CREATE TABLE edsas_subjects(
        SubjectID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        SubjectCode TEXT NOT NULL,
        SubjectName TEXT NOT NULL
        );'''
    )