import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.core.mail import send_mail

from pubdls.models import Regnum


@shared_task()
def parser():
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
        'ctl00$ContentPlaceHolder1$txtDateFrom': start_date,
        'ctl00$ContentPlaceHolder1$txtDateTo': end_date,
        'ctl00$ContentPlaceHolder1$Button1': 'Запит'
    })
    # regdate_list = []
    regnum_list = []
    # doctype_list = []
    # rpnumber_list = []
    # drugname_list = []
    # serialnum_list = []
    # manufacture_list = []

    while True:
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            soup_rows = soup.select('tr[class$="Row"]')

            for i in range(len(soup_rows)):
                regnum = Regnum.objects.filter(name=str(soup_rows[i].select('td[id$="RegNum"]'))[46:-6])
                if not regnum:
                    reg_number = Regnum.objects.create(
                        reg_num=regnum,
                        reg_date=str(soup_rows[i].select('td[id$="RegDate"]'))[73:-6],
                        doc_type=str(soup_rows[i].select('td[id$="DocTypeName"]'))[51:-6],
                        rp_number=str(soup_rows[i].select('td[id$="RpNumber"]'))[48:-6],
                        drug_name=str(soup_rows[i].select('td[id$="DrugNameAndFormtypeDesc"]'))[63:-6],
                        serial_num=str(soup_rows[i].select('td[id$="SerialNum"]'))[49:-6],
                        manufacture=str(soup_rows[i].select('td[id$="ProducerAndCountry"]'))[58:-6],

                    )
                    regnum_list.append(reg_number)

        print(regnum_list)










