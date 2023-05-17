import requests
from bs4 import BeautifulSoup
import pytesseract
import cv2
class MsDnkom:

    def __init__(self):
        return

    def authorization(self, login, password):
        user_agent_val = '"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Safari/605.1.15"'

        session = requests.Session()
        r = session.get('http://results.dnkom.ru/cabinet/patient/login', headers={
            'User-Agent': user_agent_val
        })
        session.headers.update({'Referer': 'http://results.dnkom.ru/cabinet/patient/login'})
        session.headers.update({'User-Agent': user_agent_val})

        form_build_id = session.cookies.get('form_build_id', domain=".dnkom.ru")
        data = {'login': str(login),
                'password': str(password),
                'currentURL': 'cabinet / patient / login',
                'redirectUrl': 'cabinet / patient / main_page',
                'form_build_id': form_build_id,
                'form_id': 'patient_login_form',
                'op': 'Войти'
                }

        response = session.post('http://results.dnkom.ru/cabinet/patient/login', data=data)
        if response.url != 'http://results.dnkom.ru/cabinet/patient/main_page':
            return ("Error")

        soup = BeautifulSoup(response.text, "html.parser")
        alldata = soup.findAll('a', class_="results-view-btn ajax-link btn_icon")
        if alldata == 0:
            return ("Error")
        s = str(alldata[0])
        i = s.find(" href=")
        href = ""
        i += 7
        while s[i] != '"':
            href += s[i]
            i += 1
        http = 'http://results.dnkom.ru/'
        href = http + href
        response = session.post(href)

        soupB = BeautifulSoup(response.text, "html.parser")
        alldata1 = soupB.findAll('a', class_="request-results-btn btn_icon")
        if alldata1 == 0:
            return ("Error")
        strAllData = str(alldata1[0])
        i = strAllData.find(' href=')
        href2 = ""
        i += 7
        while strAllData[i] != '"':
            href2 += strAllData[i]
            i += 1
        http = 'http://results.dnkom.ru'
        href2 = http + href2
        response = session.post(href2)

        soupB = BeautifulSoup(response.text, "html.parser")
        alldata2 = soupB.findAll('img')
        if alldata2 == 0:
            return ("Error")
        strAllData2 = str(alldata2[1])
        i = strAllData2.find('src=')
        href3 = ""
        i += 5
        while strAllData2[i] != '"':
            href3 += strAllData2[i]
            i += 1
        http = 'http://results.dnkom.ru'
        href3 = http + href3
        response = session.post(href3)

        if response.status_code == 200:
            with open('temp.png', 'wb') as f:
                f.write(response.content)
        else:
            return ('Error')
        image = cv2.imread("temp.png")
        string = pytesseract.image_to_string(image, lang='rus')
        print(string)

dnkom = MsDNKom()
print(dnkom.authorization("89264702030", "Asdfghq1"))