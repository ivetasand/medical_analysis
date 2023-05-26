import subprocess

from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from main_backend.wellness_service.googleFit.app_decorator import \
    login_required, login_login
import json
import time
from datetime import datetime, timedelta
import os, signal
import requests
from psutil import process_iter
from signal import SIGTERM  # or SIGKILL

app = Flask(__name__)
app.secret_key = "asdjhalksdhakjsdha"
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="47943249643-ga46nc3ivvkedq6tbmv3v125ujesinkq.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={
        'scope': 'email profile https://www.googleapis.com/auth/fitness.activity.write https://www.googleapis.com/auth/fitness.activity.read'},
    # добавить scope из API
    # server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration'
)


@app.route('/')
@login_required
def hello_world():
    # return redirect('/terminate')
    return 'hello'


@login_login
@app.route('/terminate')
def terminate():
    # for conns in proc.connections(kind='inet'):
    # if conns.laddr.port == 8080:
    # print(os.getpid())
    # print(signal.SIGINT)
    # os.kill(os.getpid(), signal.SIGINT)
    #
    # for proc in process_iter():
    #     try:
    #         for conns in proc.connections(kind='inet'):
    #             if conns.laddr.port == 5000:
    #                 proc.send_signal(SIGTERM)
    #     except Exception as e:
    #         continue

    # os.system("killport 5000")

    return



@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get(
        'userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    result_list = authorization(token['access_token'])
    print(result_list)
    r = requests.post("http://127.0.0.1:7000/login_data_post/",
                      data={b'1'}, headers={'User-Agent': 'some cool user-agent'})
    print('oh no')
    # session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


def get_access_token():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    return token['access_token']


def authorization(token):
    OAUTH_TOKEN = token
    # OAUTH_TOKEN = "ya29.a0AWY7Ckmq3eMCwmueAxCXn9kre4tskUBY5A6M18L4arZuWJ5lv5ZmaaXaYCdOhHlof2tWEZEbv6lFVXHysoKvtTaF8wpxD48gi_RcSOgfu70H46_A3dd7cP69yvaTAujUw826vSHj_E_J35St8gR1sVsExzwKaCgYKAfcSARISFQG1tDrpQnAvyFCQD73Cv6TVo55okQ0163"
    APP_SECRET_KEY = "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"
    CLIENT_ID = "47943249643-ga46nc3ivvkedq6tbmv3v125ujesinkq.apps.googleusercontent.com"

    url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"

    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer %s' % OAUTH_TOKEN}

    two_months_ago = datetime.now() - timedelta(days=60)
    body = {
        "aggregateBy": [{
            "dataTypeName": "com.google.step_count.delta",
            "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
        }],
        "bucketByTime": {"durationMillis": 86400000},
        "startTimeMillis": int(
            time.mktime(two_months_ago.timetuple()) / 86400) * 86400 * 1000,
        "endTimeMillis": int(
            time.mktime(time.localtime()) / 86400) * 86400 * 1000

    }
    r = requests.post(url, headers=headers, data=json.dumps(body))
    res = r.content.decode("utf-8")
    parse(res)

    # print(requests.get("https://www.googleapis.com/fitness/v1/users/me/sessions",
    #                    headers=headers).text)
    # start_time = int(time.mktime(two_months_ago.timetuple()) / 86400) * 86400
    # end_time = int(time.mktime(time.localtime()) / 86400) * 86400
    # print(requests.get("https://www.googleapis.com/fitness/v1/users/me/sessions?startTime="+ str(start_time) + '&endTime=' + str(end_time) + '&activityType=72',
    #                   headers=headers).text)
    # print(requests.get("https://www.googleapis.com/fitness/v1/users/me/sessions",
    #                    headers=headers).text)


def parse(res):
    result_googlefit = []
    seq = res.split("\n")
    for i in range(len(seq)):
        # print(seq[i])
        result = []
        if "startTimeMillis" in seq[i]:
            startTimeMillis = int(
                seq[i].strip().split(": ")[1].strip('"').replace('"', '').split(
                    ",")[0])
            if startTimeMillis != "":
                startTimeMillis = datetime.fromtimestamp(
                    startTimeMillis / 1000).strftime('%Y-%m-%d')
                result.append(startTimeMillis)
        if i + 13 < len(seq) and "intVal" in seq[i + 13]:
            intVal = int(seq[i + 13].strip().split(": ")[1].split(",")[0])
            if intVal != "":
                result.append(intVal)
                result_googlefit.append(result)

    new_lst = [sublst for sublst in result_googlefit if sublst]
    # print(result_googlefit)
    return (new_lst)
