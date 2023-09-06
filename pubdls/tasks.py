from datetime import datetime
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

    regnum_list = []

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        soup_rows = soup.select('tr[class$="Row"]')

        for i in range(len(soup_rows)):
            regnum = Regnum.objects.filter(reg_num=str(soup_rows[i].select('td[id$="RegNum"]'))[46:-6],
                                           rp_number=str(soup_rows[i].select('td[id$="RpNumber"]'))[48:-6],
                                           serial_num=str(soup_rows[i].select('td[id$="SerialNum"]'))[49:-6]
                                           )
            if not regnum:
                date_string = str(soup_rows[i].select('td[id$="RegDate"]'))[73:-6]
                date_object = datetime.strptime(date_string, "%d.%m.%Y")
                new_date_string = date_object.strftime("%Y-%m-%d")

                reg_number = Regnum.objects.create(
                    reg_num=str(soup_rows[i].select('td[id$="RegNum"]'))[46:-6],
                    reg_date=new_date_string,
                    doc_type=str(soup_rows[i].select('td[id$="DocTypeName"]'))[51:-6],
                    rp_number=str(soup_rows[i].select('td[id$="RpNumber"]'))[48:-6],
                    drug_name=str(soup_rows[i].select('td[id$="DrugNameAndFormtypeDesc"]'))[63:-6],
                    serial_num=str(soup_rows[i].select('td[id$="SerialNum"]'))[49:-6],
                    manufacture=str(soup_rows[i].select('td[id$="ProducerAndCountry"]'))[58:-6],
                    notes=str(soup_rows[i].select('td[id$="Notes"]'))[45:-6],

                )
                regnum_list.append(reg_number)
        if len(regnum_list) == 0:
            send_mail(
                'Pub DLS!',
                'Нових розпоряджень нема',
                "alita.v@ukr.net",
                ["alita.avs@gmail.com"],
                fail_silently=False,
            )
        if len(regnum_list) > 0:
            message = [f'|->   {i.drug_name} -- {i.serial_num} -- {i.manufacture}. ' for i in regnum_list]
            send_mail(
                f'Pub DLS! Нових разпоряджень: {len(regnum_list)}',
                f'{"__________________________________________________________________________".join(message)}',
                # f"{[f'|||        {i.drug_name}  -  {i.manufacture}.          ' for i in regnum_list]}",
                "alita.v@ukr.net",
                ["alita.avs@gmail.com"],
                fail_silently=False,
            )

