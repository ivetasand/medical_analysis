from main_backend.med_service.dnkom import MsDnkom
from main_backend.med_service.gemotest import MsGemotest

class Service:

    def __init__(self):
        return

    def get_med_service(self, service, login, password):
        if (service == 'dnkom'):
            service_dnkom = MsDnkom()
            data_dnkom = service_dnkom.authorization(login, password)
            count_error = 0
            result_list = []
            for i in range(0, len(data_dnkom)):
                if (data_dnkom[i] == 'Error 1'):
                    return "Error 1"
                elif (data_dnkom[i] == 'Error 2'):
                    return "Error 2"
                elif (data_dnkom[i] == 'Error 3'):
                    count_error += 1
                    continue
                else:
                    parse_data = service_dnkom.parse(data_dnkom[i])
                    if parse_data != False:
                        result_list = result_list + (
                            service_dnkom.parse(data_dnkom[i]))
                    else:
                        count_error += 1
                        continue
            result_list.append(count_error)
            return (result_list)
        elif (service == 'gemotest'):
            service_gemotest = MsGemotest()
            data_gemotest = service_gemotest.authorization(login, password)
            count_error = 0
            result_list = []
            for i in range(0, len(data_gemotest)):
                if (data_gemotest[i] == 'Error 1'):
                    return "Error 1"
                elif (data_gemotest[i] == 'Error 2'):
                    return "Error 2"
                elif (data_gemotest[i] == 'Error 3'):
                    count_error += 1
                    continue
                else:
                    parse_data = service_gemotest.parse(data_gemotest[i])
                    if parse_data != False:
                        result_list = result_list + (
                            service_gemotest.parse(data_gemotest[i]))
                    else:
                        count_error += 1
                        continue
            result_list.append(count_error)
            return (result_list)
        else:
            return (0)