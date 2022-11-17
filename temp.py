# Testing purposes file

--- Year SWD Student Options File
        CREATE TABLE settings_SWD(
            id INT PRIMARY KEY NOT NULL,
            DefaultStudentUnits TEXT,
            LinesProposed INT,
            DefaultPeriods INT,
            DefaultCodeLength INT,
            AddSuffixString TEXT,
            SuffixType TEXT,
            Subgrids INT,
            ShowRollClass TEXT,
            ShowYearLevel TEXT,
            ShowHomeGroup TEXT,
            ShowHouse TEXT,
            ShowGender TEXT,
            ShowStudentCode TEXT,
            RestartSuffixOnLineorSubgrid INT,
            AddSubgridNo TEXT,
            AddLineChar TEXT,
            TimetableNotice TEXT,
            TimetableClassesSaved TEXT,
            StudentSpareField1 TEXT,
            OptionSpareField1 TEXT,
            ConvertedFromV9 TEXT,
            ClassCodeComponents TEXT,
            DateModified REAL);
        
        CREATE TABLE lines_SWD(
            LineID TEXT PRIMARY KEY,
            Code TEXT,
            Name TEXT,
            LineTagID TEXT,
            Subgrid INT,
            LineNo INT,
            Classes TEXT);
        
        CREATE TABLE subjects_SWD(
            SubjectID TEXT PRIMARY KEY,
            Code TEXT
            Name TEXT,
            Gender TEXT,
            BOSCode TEXT,
            SpareField TEXT,
            Units INT,
            Subgrids INT,
            ClassSizeMaximum INT,
            CorrespondingLines TEXT,
            SameStudents TEXT,
            SpareField1 TEXT,
            SpareField2 TEXT);

        CREATE TABLE options_SWD(
            OptionID TEXT PRIMARY KEY NOT NULL,
            SubjectID TEXT,
            OptionCode TEXT,
            AlternateCode TEXT,
            AlternateName TEXT,
            Subgrid INT,
            Classes INT,
            Lines INT,
            Teachers INT,
            AutoCreate TEXT,
            PrerequisiteType TEXT,
            FOREIGN KEY (SubjectID) REFERENCES subjects_SWD(SubjectID));

        CREATE TABLE students_SWD(
            StudentID TEXT PRIMARY KEY NOT NULL,
            StudentCode INT NOT NULL,
            FirstName TEXT,
            LastName TEXT,
            MiddleName TEXT,
            PreferredName TEXT,
            Gender TEXT,
            BOSCode TEXT,
            RollClass TEXT,
            YearLevel TEXT,
            House TEXT,
            HomeGroup TEXT,
            SpareField1 TEXT,
            SpareField2 TEXT,
            SpareField3 TEXT,
            Email TEXT,
            Units INT,
            Lock TEXT,
            StudentPreferences JSON);

        CREATE TABLE classes_SWD(
            ClassID TEXT PRIMARY KEY NOT NULL,
            OptionID TEXT,
            LineID TEXT,
            SameID TEXT,
            ClassCode TEXT,
            ClassName TEXT,
            Suffix TEXT,
            RollClassCode TEXT,
            TeacherCode TEXT,
            RoomCode TEXT,
            TagLevel INT,
            LessonNo INT,
            Periods INT,
            Maximum_Class_Size INT,
            Lock TEXT,
            FOREIGN KEY (OptionID) REFERENCES options_SWD(OptionID),
            FOREIGN KEY (LineID) REFERENCES lines_SWD(LineID));