import pathlib

DATABASE_NAME = 'medical_analysis.sqlite'
DATABASE_PATH = f'{pathlib.Path().resolve()}/medical_analysis.sqlite'

ANALYSIS_VALUE_TYPE_TABLE_CREATION = (
    "CREATE TABLE IF NOT EXISTS analysis_value_type (\n"
    "id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
    "name TEXT NOT NULL,\n"
    "abbreviation TEXT\n"
    ");\n")

LABORATORY_TABLE_CREATION = (
    "CREATE TABLE IF NOT EXISTS laboratory (\n"
    "id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
    "name TEXT NOT NULL\n"
    ");\n")

UNITS_TABLE_CREATION = (
    "CREATE TABLE IF NOT EXISTS units (\n"
    "id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
    "name TEXT NOT NULL\n"
    # "is_main INTEGER NOT NULL\n"
    ");\n")

UNITS_CONVERSION_TABLE_CREATION = (
    "CREATE TABLE IF NOT EXISTS units_conversion (\n"
    "id_first INTEGER,\n"
    "id_second INTEGER,\n"
    "coefficient REAL NOT NULL,\n"
    "FOREIGN KEY (id_first) REFERENCES units (id),\n"
    "FOREIGN KEY (id_second) REFERENCES units (id)\n"
    ");\n")

ANALYSIS_VALUE_TABLE_CREATION = (
    "CREATE TABLE IF NOT EXISTS analysis_value (\n"
    "id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
    "lab_id INTEGER NOT NULL,\n"
    "analysis_type_id INTEGER NOT NULL,\n"
    "is_result_numeric INTEGER NOT NULL,\n"
    "result_text TEXT,\n"
    "result_value REAL,\n"
    # "is_reference_numeric INTEGER NOT NULL,\n"
    "reference TEXT,\n"
    "lower_limit REAL,\n"
    "upper_limit REAL,\n"
    "time_stamp TEXT NOT NULL,\n"
    "unit_id INTEGER,\n"
    "FOREIGN KEY (lab_id) REFERENCES laboratory (id),\n"
    "FOREIGN KEY (analysis_type_id) REFERENCES analysis_value_type (id),\n"
    "FOREIGN KEY (unit_id) REFERENCES units (id)\n"
    ");\n")

STEPS_TABLE_CREATION = (
    "CREATE TABLE IF NOT EXISTS steps_wellbeing (\n"
    "id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
    "timestamp TEXT NOT NULL,\n"
    "steps INTEGER NOT NULL\n"
    ");\n")

TABLES_QUERIES_LIST = [
    LABORATORY_TABLE_CREATION,
    ANALYSIS_VALUE_TYPE_TABLE_CREATION,
    ANALYSIS_VALUE_TABLE_CREATION,
    UNITS_TABLE_CREATION,
    UNITS_CONVERSION_TABLE_CREATION,
    STEPS_TABLE_CREATION
]

TABLES_LIST = [
    "laboratory",
    "analysis_value_type",
    "analysis_value",
    "units",
    "units_conversion",
    "steps_wellbeing"
]
