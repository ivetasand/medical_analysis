from utils.constants.database import DATABASE_PATH, TABLES_QUERIES_LIST
from utils.database.database import DbConnector


class DbInterface:
    def __init__(self):
        self.db_connector = DbConnector(DATABASE_PATH, TABLES_QUERIES_LIST)

    @classmethod
    def __check_if_record_in_db(cls, self, record):
        """
        internal function for checking if this analysis is already been added
        :param self:
        :param record: analysis record
        :return: if record is in db
        """
        print(record)
        check = self.db_connector.select_analysis_info_by_type_name(
            record[1])

        check = [list(ele) for ele in check]
        new_check = []
        for check_item in check:
            check_item = check_item[1:]
            check_item = [i for i in check_item if i is not None]
            new_check.append(check_item)

        return record in new_check

    def insert_analysis_data(self, data):
        """
        insert data to database
        :return: number of analysis that were inserted
        """
        unique_analysis_count = 0
        for record in data:
            if self.__check_if_record_in_db(self, record):
                continue

            unique_analysis_count += 1

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
        return unique_analysis_count

    def fetch_analysis_data(self, desired_type=None):
        """
        Select data from database
        :param desired_type by default selects all analysis types.
        If equal to name of the analysis, then selects all data for analysis.
        :return: data
        """
        if desired_type is None:
            return self.db_connector.select_all_analysis_types()
        return self.db_connector.select_analysis_info_by_type_name(desired_type)

    def fetch_steps_data(self, desired_date=None):
        """
        Select data from database
        :param desired_type by default selects all analysis types.
        If equal to name of the analysis, then selects all data for analysis.
        :return: data
        """
        if desired_date is None:
            return self.db_connector.select_all_steps()
        return self.db_connector.select_steps_by_timestamp(desired_date)

    def insert_steps_data(self, data):
        """
        insert data to database
        :return: number of analysis that were inserted
        """
        # data = [[date, numb], [date, numb]]
        unique_steps_count = 0
        for record in data:
            if self.db_connector.select_steps_by_timestamp(record[0]):
                continue

            unique_steps_count += 1
            self.db_connector.insert_steps(record[1], record[0])
        return unique_steps_count

data_sample_for_testing = \
    [
        # [lab_name, analysis_type_name, is_result_numeric, result_text,
        # reference_text, date]
        ["днком", "ВПЧ типы 51,56", 0, "не обнаружено", "не обнаружено",
         "2022-01-27"],
        # [lab_name, analysis_type_name, is_result_numeric, result_value,
        # reference_lower_value,reference_upper_value, date, units]
        ["гемотест", "витамин А", 1, 0.5, 0.2, 0.8, "2023-05-14",
         "unit_name2"]
    ]

# interface = DbInterface()
# print(interface.insert_data(data_sample_for_testing))
# print(interface.fetch_data())
#
# print(interface.fetch_data("ВПЧ типы 51,56"))
# print(interface.fetch_data("витамин А"))
# print(interface.insert_steps_data([['2023-04-11', 1234], ['2023-04-12', 432]]))
# print(interface.fetch_steps_data('2023-04-11'))