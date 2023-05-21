from main_backend.med_service.dnkom import MsDnkom



class Service:

    def __init__(self):
        return

    def get_med_service(self, service, login, password):
        if (service == 'dnkom'):
            service_dnkom = MsDnkom()
            data_dnkom = service_dnkom.authorization(login, password)
            return (service_dnkom.parse(data_dnkom))
        elif (service == 'gemotest'):
            service_gemotest = MsGemotest()
            data_gemotest = service_gemotest.authorization(login, password)
            return (service_gemotest.parse(data_gemotest))
        else:
            return (0)


