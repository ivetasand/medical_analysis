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
import re

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
        item_find_analyzes = soup.findAll('a', class_="results-view-btn ajax-link btn_icon")
        if item_find_analyzes == 0:
            return ("Error 2")
        list_of_jpeg = []

        for i in range(0, len(item_find_analyzes), 1):
            response = session.post('http://results.dnkom.ru/cabinet/patient/login',
                                    data=data)
            if response.url != 'http://results.dnkom.ru/cabinet/patient/main_page':
                return ("Error 1")

            soup = BeautifulSoup(response.text, "html.parser")
            item_new_find_analyzes = soup.findAll('a', class_="results-view-btn ajax-link btn_icon")
            if item_new_find_analyzes == 0:
                return ("Error 2")

            s = str(item_new_find_analyzes[i])
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
                list_of_jpeg.append("Error 3")
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
                list_of_jpeg.append("Error 3")
            strAllData2 = str(item_png[1])
            j = strAllData2.find('src=')
            href3 = ""
            j += 5
            while strAllData2[j] != '"':
                href3 += strAllData2[j]
                j += 1
            if href3.startswith("/cabinet/patient//request_info/"):
                http = 'http://results.dnkom.ru'
                href3 = http + href3
                response = session.post(href3)

                if response.status_code == 200:
                    with open('temp' + str(i) + '.jpeg', 'wb') as f:
                        f.write(response.content)
                else:
                    list_of_jpeg.append('Error 3')
                list_of_jpeg.append(str('temp' + str(i) + '.jpeg'))
        return (list_of_jpeg)



    def parse(self, old_img):
        try:
            result = []
            img = cv2.imread(old_img)
            string_img = pytesseract.image_to_string(img, lang='rus')
            new_string = ''
            i = string_img.find("Репктрация биоматериала: ")
            if i != -1:
                for j in range(i + 25, i + 35, 1):
                    new_string += string_img[j]
                new_date_str = format_date(new_string)

                if new_date_str == "":
                    new_string = ''
                    for j in range(i + 25, i + 34, 1):
                        new_string += string_img[j]
                    new_date_str = format_date(new_string)

                    if new_date_str == "":
                        new_string = ''
                        for j in range(i + 25, i + 33, 1):
                            new_string += string_img[j]
                        new_date_str = format_date(new_string)
            else:
                i = string_img.find("Регистрация биоматериала: ")
                if i != -1:
                    for j in range(i + 26, i + 36, 1):
                        new_string += string_img[j]
                    new_date_str = format_date(new_string)

                    if new_date_str == "":
                        new_string = ''
                        for j in range(i + 26, i + 35, 1):
                            new_string += string_img[j]
                        new_date_str = format_date(new_string)

                        if new_date_str == "":
                            new_string = ''
                            for j in range(i + 26, i + 34, 1):
                                new_string += string_img[j]
                            new_date_str = format_date(new_string)
                else:
                    new_date_str = ""
            if new_date_str == "":
                return []
            ocr = TesseractOCR(n_threads=1, lang="rus+eng")
            img = Image(old_img)
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
                    if df.loc[i, 'Результат'] == None:
                        list_results.append("")
                    else:
                        list_results.append(df.loc[i, 'Результат'])

                    if df.loc[i, 'Реф. значения'] != "":
                        new_ref = parse_range_with_comma(df.loc[i, 'Реф. значения'])
                        if new_ref == ('', ''):
                            new_ref = parse_range_with_dot(df.loc[i, 'Реф. значения'])
                            if new_ref == ('', ''):
                                new_ref = parse_range_without_comma(df.loc[i, 'Реф. значения'])
                    list_results.append(str(new_ref[0]))
                    list_results.append(str(new_ref[1]))
                    list_results.append(new_date_str)
                    if df.loc[i, 'Ед. измерения'] == None:
                        list_results.append("")
                    else:
                        list_results.append(df.loc[i, 'Ед. измерения'])
                    result.append(list_results)
                else:
                    list_results.append(0)
                    if df.loc[i, 'Результат'] == None:
                        list_results.append("")
                    else:
                        list_results.append(df.loc[i, 'Результат'])

                    if df.loc[i, 'Реф. значения'] == None:
                        list_results.append("")
                    else:
                        list_results.append(df.loc[i, 'Реф. значения'])

                    list_results.append(new_date_str)
                    result.append(list_results)

            return (result)
        except:
            return []

def format_date(date_img):
    # Пробуем распарсить дату в разных форматах
    for fmt in ('%d.%m.%Y', '%d.%m%Y', '%d%m.%Y', '%d%m%Y'):
        try:
            dt = datetime.strptime(date_img, fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            pass
    # Если не удалось распарсить дату, возвращаем None
    return ""

def parse_range_with_comma(range_str):
    # Ищем числа в строке с помощью регулярного выражения
    match = re.search(r'\d+,\d+', range_str)
    if not match:
        return ('', '')
    # Заменяем запятую на точку и преобразуем в float
    start = float(match.group(0).replace(',', '.'))
    # Ищем следующее число после первого
    match = re.search(r'\d+,\d+', range_str[match.end():])
    if not match:
        return ('', '')
    # Второе число
    end = float(match.group(0).replace(',', '.'))
    # Возвращаем кортеж из двух чисел
    return (start, end)

def parse_range_with_dot(range_str):
    # Ищем числа в строке с помощью регулярного выражения
    match = re.search(r'\d+,\d+', range_str)
    if not match:
        return ('', '')
    # Заменяем запятую на точку и преобразуем в float
    start = float(match.group(0).replace(',', '.'))
    # Ищем следующее число после первого
    match = re.search(r'\d+,\d+', range_str[match.end():])
    if not match:
        return ('', '')
    # Второе число
    end = float(match.group(0).replace(',', '.'))
    # Возвращаем кортеж из двух чисел
    return (start, end)

def parse_range_without_comma(range_str):
    # Ищем числа в строке с помощью регулярного выражения
    match = re.search(r'\d+', range_str)
    if not match:
        return ('', '')
    # Заменяем запятую на точку и преобразуем в float
    start = float(match.group(0).replace(',', '.'))
    # Ищем следующее число после первого
    match = re.search(r'\d+', range_str[match.end():])
    if not match:
        return ('', '')
    # Второе число
    end = float(match.group(0))
    # Возвращаем кортеж из двух чисел
    return (start, end)
