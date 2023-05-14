import pathlib

DATABASE_NAME = 'medical_analysis.sqlite'
DATABASE_PATH = f'{pathlib.Path().resolve()}/medical_analysis.sqlite'

ANALYSIS_VALUE_TYPE_TABLE_CREATION = (
    "CREATE TABLE IF NOT EXISTS analysis_value_type (\n"
    "id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
    "name TEXT NOT NULL,\n"
    "abbreviation TEXT\n"
    ");\n")

LABORATORY_TABLE_CREATION = ("CREATE TABLE IF NOT EXISTS laboratory (\n"
                             "id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                             "name TEXT NOT NULL\n"
                             ");\n")

# ANALYSIS_ITEM_TABLE_CREATION = ("CREATE TABLE IF NOT EXISTS analysis_item (\n"
#                                 "id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
#                                 "value_type_id INTEGER NOT NULL,\n"
#                                 "FOREIGN KEY (value_type_id) REFERENCES analysis_value_type (id)\n"
#                                 ");\n")

ANALYSIS_VALUE_TABLE_CREATION = ("CREATE TABLE IF NOT EXISTS analysis_value (\n"
                                 "id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                                 "lab_id INTEGER NOT NULL,\n"
                                 "analysis_type_id INTEGER NOT NULL,\n"
                                 "is_result_numeric INTEGER NOT NULL,\n"
                                 "result_text TEXT,\n"
                                 "result_value REAL,\n"
                                 "is_reference_numeric INTEGER NOT NULL,\n"
                                 "reference TEXT,\n"
                                 "upper_limit REAL,\n"
                                 "lower_limit REAL,\n"
                                 "time_stamp TEXT NOT NULL,\n"
                                 "FOREIGN KEY (lab_id) REFERENCES laboratory (id),\n"
                                 "FOREIGN KEY (analysis_type_id) REFERENCES analysis_value_type (id)\n"
                                 ");\n")

TABLES_QUERIES_LIST = [LABORATORY_TABLE_CREATION,
                       ANALYSIS_VALUE_TYPE_TABLE_CREATION,
                       ANALYSIS_VALUE_TABLE_CREATION,
                       # ANALYSIS_ITEM_TABLE_CREATION
                       ]
