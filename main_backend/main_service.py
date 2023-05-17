import main_backend.med_service.dnkom


class Service:

    def __init__(self):
        return

    def get_med_service(self, service, login, password):
        if (service == 'gemotest'):
            main_backend.med_service.dnkom.MsDnkom.authorization(login, password)
        elif (service == 'dnkom'):
            main_backend.med_service.gemotest.authorization(login, password)
        else:
            return (0)


