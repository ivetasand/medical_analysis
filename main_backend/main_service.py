from main_backend.med_service.dnkom import MsDnkom

class Service:

    def __init__(self):
        return

    def get_med_service(self, service, login, password):
        if (service == 'dnkom'):
            service_dnkom = MsDnkom()
            data_dnkom = service_dnkom.authorization(login, password)
            if (data_dnkom != 'Error 2') & (data_dnkom != 'Error 1'):
                return (service_dnkom.parse(data_dnkom))
            else:
                return (data_dnkom)
        elif (service == 'gemotest'):
            service_gemotest = MsGemotest()
            data_gemotest = service_gemotest.authorization(login, password)
            if (data_gemotest != 'Error 2') & (data_gemotest != 'Error 1'):
                return (service_gemotest.parse(data_gemotest))
            else:
                return (data_gemotest)
        else:
            return (0)