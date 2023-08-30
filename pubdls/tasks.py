import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def quotes_parser():
    start_date = '01-01-2023'
    end_date = '04-01-2023'
    # r = requests.get("http://pub-mex.dls.gov.ua/QLA/DocList.aspx")
    r = requests.post("http://pub-mex.dls.gov.ua/QLA/DocList.aspx", data={
        'ctl00$ScriptManager1': 'ctl00$UpdatePanel1|ctl00$ContentPlaceHolder1$Button1',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '',
        '__VIEWSTATEGENERATOR': '',
        '__EVENTVALIDATION': '',
        'ctl00_Content_fvParams_edtDocDateBegin': start_date,
        'ctl00_Content_fvParams_edtDocDateEnd': end_date,
        'ctl00$ContentPlaceHolder1$Button1': 'Запит'
    })
    pub_date = []
    numb_doc = []
    type_doc = []
    numb_rp = []
    name = []
    sert = []
    manufacturer = []

    while True:
        if r.status_code == 200:
            soup_nav = BeautifulSoup(r.text, 'html.parser')





