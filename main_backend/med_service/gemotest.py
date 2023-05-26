import requests
import json
class MsGemotest:
    def __init__(self):
        return

    # Авторизация на Гемотест. Входные данные: логин и номер телефона.
    # Если пользователь ввел неправильно пароль или логи - Error 1
    # Если у пользователя нет анализов - Error 2
    # Если все успешно - возвращается список с анализами и количество необработанных анализов
    # Пример: [[гемотест, Витамин А], 2] - 1 успешный анализ и 2, которые не удалось обработать
    def authorization(self, login, password):
        user_agent_val = '"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Safari/605.1.15"'
        url = 'https://gemotest.ru/my/#/auth/loginin'

        session = requests.Session()
        r = session.get(url, headers={
            'User-Agent': user_agent_val
        })
        session.headers.update({'Referer': url})
        session.headers.update({'User-Agent': user_agent_val})

        data = {"password": password,
                "phone": login
                }

        response = session.post('https://api2.gemotest.ru/customer/v2/login',
                                headers={
                                    'User-Agent': user_agent_val
                                }, data=data)

        if response.status_code != 200:
            return ('Error 1')
        access_token = \
        json.loads(response.content.decode("utf-8").replace("'", '"'))[
            "access_token"]
        response = session.get("https://gemotest.ru/my/", headers={
            'Authorization': 'Bearer ' + access_token
        })

        response = session.get(
            "https://api2.gemotest.ru/customer/v2/orders_actual?limit=10&offset=0",
            headers={
                'Authorization': 'Bearer ' + access_token
            })
        data = json.loads(response.text)
        # print(response.text)
        orders = data["result"]["orders"]
        if orders is None or orders == [] or orders == "":
            return "Error 2"
        data_json = []
        for order in orders:
            if order['order_status'] == 'Предзаказ' or order['order_status'] == '\u041f\u0440\u0435\u0434\u0437\u0430\u043a\u0430\u0437':
                continue
            order_num = order["order_num"]
            http = 'https://api2.gemotest.ru/customer/v3/order/'
            response = session.post(http + order_num)
            response = session.get(http + order_num, headers={
                'Authorization': 'Bearer ' + access_token
            })

            s = str(response.text)
            i = s.find('"services":[{"id":"')
            while i != -1:
                data_json.append(order["date"])
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
                data_json.append(json.loads(
                    response.content.decode("utf-8").replace("'", '"'))[
                                     "tests"])
                s = s[i:]
                i = s.find('"service":{"id":"')

        print(data_json)
        return (data_json)

    def parse(self, old_list):
        results = []

        for n in range(0, len(old_list), 2):
            for gemo_json in (old_list[n + 1]):
                list_results = []
                list_results.append("гемотест")
                list_results.append(gemo_json["title"])
                gemo_json_value = gemo_json["value"]

                if gemo_json_value.endswith("-"):
                    gemo_json_value = gemo_json_value[:-2]

                if is_numeric(gemo_json_value):
                    list_results.append(1)
                    if (is_numeric(gemo_json_value)) & (
                            is_numeric(
                                gemo_json["reference_range"]["max_value"])) & (
                            is_numeric(
                                gemo_json["reference_range"]["min_value"])):
                        list_results.append(gemo_json_value)
                        if (gemo_json["reference_range"]["max_value"] != "") & (
                                gemo_json["reference_range"][
                                    "min_value"] != ""):
                            list_results.append(
                                gemo_json["reference_range"]["min_value"])
                            list_results.append(
                                gemo_json["reference_range"]["max_value"])
                            list_results.append(old_list[n][:10])
                            list_results.append(gemo_json["unit"])
                    else:
                        list_results.append(gemo_json_value)
                        list_results.append("")
                        list_results.append("")
                        list_results.append(old_list[n][:10])
                        list_results.append(gemo_json["unit"])

                else:
                    list_results.append(0)
                    list_results.append(gemo_json_value)
                    list_results.append(gemo_json["reference_range"]["text"])
                    list_results.append(old_list[n][:10])
                results.append(list_results)
            n += 2
        return (results)
def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

gemotest = MsGemotest()
print(gemotest.parse(gemotest.authorization("79777024573","9sxpfwxf")))
#print(gemotest.parse(gemotest.authorization("79267039809","93079180")))