import requests
from bs4 import BeautifulSoup
import pytesseract
import cv2
from img2table.document import Image
#from PIL import Image
from img2table.ocr import TesseractOCR
from datetime import datetime
import pandas as pd
import os



class MsDnkom:

    def __init__(self):
        return

    # Авторизация на ДНКом. Входные данные: логин и пароль.
    # Если пользователь ввел неправильно пароль или логи - Error 1
    # Если у пользователя нет анализов - Error 2
    # Если все успешно - возвращается список с анализами и количество необработанных анализов
    # Пример: [[днком, Витамин А], 2] - 1 успешный анализ и 2, которые не удалось обработать
    def authorization(self, login, password):
        user_agent_val = '"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Safari/605.1.15"'

        session = requests.Session()
        session.headers.update(
            {'Referer': 'http://results.dnkom.ru/cabinet/patient/login'})
        session.headers.update({'User-Agent': user_agent_val})

        form_build_id = session.cookies.get('form_build_id', domain=".dnkom.ru")
        data = {'login': str(login),
                'password': str(password),
                'currentURL': 'cabinet / patient / login',
                'redirectUrl': 'cabinet / patient / main_page',
                'form_build_id': form_build_id,
                'form_id': 'patient_login_form',
                'op': 'Войти',
                'User-Agent': user_agent_val
                }

        response = session.post('http://results.dnkom.ru/cabinet/patient/login',
                                data=data)
        if response.url != 'http://results.dnkom.ru/cabinet/patient/main_page':
            return ("Error 1")

        soup = BeautifulSoup(response.text, "html.parser")
        item_find_analyzes = []
        item_find_analyzes.append(
            soup.findAll('a', class_="results-view-btn ajax-link btn_icon"))
        if item_find_analyzes == 0:
            return ("Error 2")

        list_of_png = []
        for i in range(0, len(item_find_analyzes), 1):
            s = str(item_find_analyzes[i])
            j = s.find(" href=")
            href = ""
            j += 7
            while s[j] != '"':
                href += s[j]
                j += 1
            http = 'http://results.dnkom.ru/'
            href = http + href
            response = session.post(href)

            soupB = BeautifulSoup(response.text, "html.parser")
            items_find_img = soupB.findAll('a',
                                           class_="request-results-btn btn_icon")
            if items_find_img == 0:
                list_of_png.append("Error 3")
            strAllData = str(items_find_img[0])
            j = strAllData.find(' href=')
            href2 = ""
            j += 7
            while strAllData[j] != '"':
                href2 += strAllData[j]
                j += 1
            http = 'http://results.dnkom.ru'
            href2 = http + href2
            response = session.post(href2)

            soupB = BeautifulSoup(response.text, "html.parser")
            item_png = soupB.findAll('img')
            if item_png == 0:
                list_of_png.append("Error 3")
            strAllData2 = str(item_png[1])
            j = strAllData2.find('src=')
            href3 = ""
            j += 5
            while strAllData2[j] != '"':
                href3 += strAllData2[j]
                j += 1
            http = 'http://results.dnkom.ru'
            href3 = http + href3
            response = session.post(href3)
            #print(response.content)
            if response.status_code == 200:
                with open('temp' + str(i) + '.jpeg', 'wb') as f:
                    f.write(response.content)
            else:
                list_of_png.append('Error 3')
            list_of_png.append(str('temp' + str(i) + '.jpeg'))
        return (list_of_png[0])

    def parse(self, old_img):
        try:
            result = []
            img = cv2.imread(old_img)
            string_img = pytesseract.image_to_string(img, lang='rus')
            print(string_img)
            new_string = ''

            i = string_img.find("Репктрация биоматериала: ")
            if i != -1:
                for j in range(i + 25, i + 35, 1):
                    new_string += string_img[j]
                date_obj = datetime.strptime(new_string, '%d.%m.%Y')
                new_date_str = date_obj.strftime('%Y-%m-%d')
            else:
                i = string_img.find("Регистрация биоматериала: ")
                if i != -1:
                    for j in range(i + 26, i + 36, 1):
                        new_string += string_img[j]
                    date_obj = datetime.strptime(new_string, '%d.%m.%Y')
                    new_date_str = date_obj.strftime('%Y-%m-%d')
                else:
                    new_date_str = ""

            ocr = TesseractOCR(n_threads=1, lang="rus+eng")
            img = Image(old_img)
            #print(img)
            # Table identification
            img_tables = img.extract_tables(ocr=ocr,
                                            implicit_rows=False,
                                            borderless_tables=False,
                                            min_confidence=10
                                            )

            df = img_tables[0].df
            df = pd.DataFrame(df.values[1:], columns=df.values[0])
            df.columns = ['Показатель', 'Результат', 'Ед. измерения',
                          'Реф. значения']
            for i in range(0, len(df), 1):
                list_results = []
                list_results.append("днком")
                list_results.append(df.loc[i, 'Показатель'])

                def is_numeric(value):
                    try:
                        float(value)
                        return True
                    except ValueError:
                        return False

                df["Результат"] = df["Результат"].str.replace(",", ".")
                if is_numeric(df.loc[i, 'Результат']):
                    list_results.append(1)
                else:
                    list_results.append(0)

                list_results.append(df.loc[i, 'Результат'])

                # разбиваем строку на подстроки по символу "-"
                parts = df.loc[i, 'Реф. значения'].split("-")
                # проверяем количество полученных подстрок
                if len(parts) >= 2 and len(parts) <= 15:
                    # извлекаем первые две подстроки
                    first_part = parts[0][:-1]
                    second_part = parts[1][1:]
                    list_results.append(1)
                    list_results.append(df.loc[i, 'Реф. значения'])
                    list_results.append(first_part.replace(",", "."))
                    list_results.append(second_part.replace(",", "."))
                else:
                    parts = df.loc[i, 'Реф. значения'].split("—")
                    # проверяем количество полученных подстрок
                    if len(parts) >= 2 and len(parts) <= 15:
                        # извлекаем первые две подстроки
                        first_part = parts[0][:-1]
                        second_part = parts[1][1:]
                        list_results.append(df.loc[i, 'Реф. значения'])
                        list_results.append(first_part.replace(",", "."))
                        list_results.append(second_part.replace(",", "."))
                        list_results.append(new_date_str)
                        list_results.append(df.loc[i, 'Ед. измерения'])
                    else:
                        list_results.append(df.loc[i, 'Реф. значения'])
                        list_results.append(new_date_str)

                result.append(list_results)

            return (result)
        except:
            return False
dnkom = MsDnkom()
print(dnkom.parse(dnkom.authorization("89264702030", "Asdfghq1")))
#print(dnkom.parse("temp0.jpeg"))
