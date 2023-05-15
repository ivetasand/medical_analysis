from utils.constants.database import DATABASE_PATH, TABLES_QUERIES_LIST
from utils.database.database import DbConnector


class DbInterface:
    def __init__(self):
        self.db_connector = DbConnector(DATABASE_PATH, TABLES_QUERIES_LIST)

    def insert_data(self, data):
        """
        insert data to database
        :return:
        """
        for record in data:
            self.db_connector.insert_lab(record[0])
            lab_id = self.db_connector.select_lab_id_by_name(record[0])

            self.db_connector.insert_analysis_value_type(record[1])
            analysis_value_type_id = \
                self.db_connector.select_analysis_value_type_id_by_name(
                    record[1])

            if record[2] == 1:
                self.db_connector.insert_unit(record[-1])
                unit_id = self.db_connector.select_unit_id_by_name(record[-1])
                new_set = (lab_id, analysis_value_type_id, *record[2:-1],
                           unit_id)
            else:
                new_set = (lab_id, analysis_value_type_id, *record[2:])

            self.db_connector.insert_analysis_value(new_set)
        return True

    def fetch_data(self, desired_type=None):
        """
        Select data from database
        :param desired_type by default selects all analysis types.
        If equal to name of the analysis, then selects all data for analysis.
        :return: data
        """
        if desired_type is None:
            return self.db_connector.select_all_analysis_types()
        return self.db_connector.select_analysis_info_by_type(desired_type)


data_sample_new = [("laboratory_name", "analysis_value_type_name", "is_numeric",
                    "result_text", "result_value", "unit", "limit_is_numeric",
                    "reference", "upper_limit", "lower_limit", "time_stamp"),
                   (), ()
                   ]

data_sample_for_testing = \
    [
        ("днком", "ВПЧ типы 51,56", 0, "не обнаружено",
         0, "не обнаружено", "2022-01-27", "unit_name1"),
        ("гемотест", "витамин А", 1, 0.5, 1, 0.2, 0.8, "2023-05-14",
         "unit_name2")
    ]

# ("laboratory_id", "analysis_value_type_id", "is_numeric",
#         "result_text", "result_value", "unit", "limit_is_numeric",
#         "reference", "upper_limit", "lower_limit", "time_stamp")

interface = DbInterface()
# interface.insert_data(data_sample_for_testing)
# print(interface.fetch_data())
print(interface.fetch_data("витамин А"))
