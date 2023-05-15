from utils.constants.database import DATABASE_PATH, TABLES_QUERIES_LIST
from utils.database.database import DbConnector


class DbInterface:
    def __int__(self):
        self.db_connector = DbConnector(DATABASE_PATH, TABLES_QUERIES_LIST)

    def insert_data(self):
        '''
        insert data to database
        :return:
        '''
        return

    def fetch_data(self):
        '''
        select data from database
        :return:
        '''
        return


data_sample_new = [("laboratory_name", "analysis_value_type_name", "is_numeric",
                    "result_text", "result_value", "unit", "limit_is_numeric",
                    "reference", "upper_limit", "lower_limit", "time_stamp"),
                   (), ()
                   ]

data_sample_for_testing = \
    [
        ("днком", "ВПЧ типы 51,56", 0, "не обнаружено",
         "LgВПЧ/10^5 эпит.клеток", 0, "не обнаружено", "2022-01-27"),
        ("гемотест", "витамин А", 1, 0.5, "мкг/мл", 1, 0.2, 0.8, "2023-05-14")
    ]
