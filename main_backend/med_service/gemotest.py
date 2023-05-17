import requests
from bs4 import BeautifulSoup
import pytesseract
import cv2
class MsGemotest:

    def __init__(self):
        return

    def authorization(self, login, phone):
        user_agent_val = '"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Safari/605.1.15"'
        url = 'https://gemotest.ru/my/#/auth/loginin'

        session = requests.Session()
        r = session.get(url, headers={
            'User-Agent': user_agent_val
        })
        session.headers.update({'Referer': url})
        session.headers.update({'User-Agent': user_agent_val})

        data = {"password": login,
                "phone": phone
                }

        response = session.post('https://api2.gemotest.ru/customer/v2/login', headers={
            'User-Agent': user_agent_val
        }, data=data)

        if response.status_code != 200:
            return ('Error')
        access_token = json.loads(response.content.decode("utf-8").replace("'", '"'))["access_token"]
        response = session.get("https://gemotest.ru/my/", headers={
            'Authorization': 'Bearer ' + access_token
        })

        response = session.get("https://api2.gemotest.ru/customer/v2/orders_actual?limit=10&offset=0", headers={
            'Authorization': 'Bearer ' + access_token
        })

        s = str(response.text)
        i = s.find('"order_num":"')
        order_num = ""
        i += 13
        while s[i] != '"':
            order_num += s[i]
            i += 1
        http = 'https://api2.gemotest.ru/customer/v3/order/'
        response = session.post(http + order_num)

        response = session.get(http + order_num, headers={
            'Authorization': 'Bearer ' + access_token
        })
        s = str(response.text)
        i = s.find('"services":[{"id":"')
        services_id = ""
        i += 20
        while s[i] != '"':
            services_id += s[i]
            i += 1
        http = 'https://api2.gemotest.ru/customer/v3/order/'
        services_id = http + order_num + "/service/Macro+PRL_" + services_id

        response = session.post(services_id)
        response = session.get(services_id, headers={
            'Authorization': 'Bearer ' + access_token
        })
        if (response.status_code < 200) | (response.status_code > 300):
            return ('Error 2')

        json_text = json.loads(response.content.decode("utf-8").replace("'", '"'))["tests"]

        return (json_text)

gemotest = MsGemotest()
print(gemotest.authorization("93079180", "79267039809"))