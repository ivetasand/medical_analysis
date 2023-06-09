from main_backend.med_service.DNKom import MsDnkom
from main_backend.med_service.gemotest import MsGemotest
from main_backend.wellness_service.googleFit.googleFit import MSGoogleFit

class Service:

    def __init__(self):
        return

    def get_med_service(self, service, login=None, password=None):
        if (service == 'dnkom'):
            service_dnkom = MsDnkom()
            data_dnkom = service_dnkom.authorization(login, password)
            count_error = 0
            result_list = []

            if type(data_dnkom) is str and \
                    (data_dnkom == "Error 1" or data_dnkom == "Error 2"):
                return data_dnkom

            for i in range(0, len(data_dnkom)):
                parse_data = service_dnkom.parse(data_dnkom[i])
                if parse_data == []:
                    count_error += 1
                    continue
                else:
                    result_list = result_list + (
                        service_dnkom.parse(data_dnkom[i]))

            result_list.append(count_error)
            return (result_list)
        elif service == 'gemotest':
            service_gemotest = MsGemotest()
            data_gemotest = service_gemotest.authorization(login, password)
            count_error = 0
            result_list = []
            if type(data_gemotest) is str and \
                    (data_gemotest == "Error 1" or data_gemotest == "Error 2"):
                return data_gemotest
            for i in range(0, len(data_gemotest)):
                if data_gemotest[i] == 'Error 3':
                    count_error += 1
                    continue

            parse_data = service_gemotest.parse(data_gemotest)
            for i in range(len(parse_data)):
                if parse_data[i] == []:
                    count_error += 1
                    continue
                else:
                    result_list.append(parse_data[i])
            result_list.append(count_error)
            return (result_list)
        elif service == 'google_fit':
            service_googlefit = MSGoogleFit()
            service_googlefit.authorization()
        else:
            return (0)
