from suds.client import Client

from .models import TRM
import time
from datetime import datetime, timedelta

WSDL_URL = 'https://www.superfinanciera.gov.co/SuperfinancieraWebServiceTRM/TCRMServicesWebService/TCRMServicesWebService?WSDL'
date = time.strftime('%Y-%m-%d')

def trm_search(date):
    try:
        client = Client(WSDL_URL, location=WSDL_URL, faults=True)
        trm =  client.service.queryTCRM(date)
    except Exception as e:
        return str(e)
    if trm[5]:
        return date, trm[4]
    return False, False

def data_trm():
    current_date = datetime.now()
    while True:
        try:
            query_date = current_date.strftime('%Y-%m-%d')
            trm_date = TRM.objects.get(date=query_date)
        except:
            trm_date, trm_value = trm_search(current_date.strftime('%Y-%m-%d'))
            if trm_date is not False and trm_value is not False:
                print(trm_date)
                trm, created = TRM.objects.get_or_create(date=trm_date, value=trm_value)
        current_date -= timedelta(days=1)

def data_fill(period=365):
    initial_date = datetime.now() - timedelta(days=period)
    final_date = datetime.now()
    while initial_date < final_date:
        query_date = initial_date.strftime('%Y-%m-%d')
        try:
            trm_date = TRM.objects.get(date=query_date)
            if trm_date.value == 643.42:
                trm_date.delete()
        except:
            trm_date, trm_value = trm_search(query_date)
            if trm_date is not False and trm_value is not False and trm_value != 643.42:
                print("{}={}".format(trm_date, trm_value))
                trm, created = TRM.objects.get_or_create(date=trm_date, value=trm_value)

        initial_date += timedelta(days=1)

def daily_update():
    data_fill(10)
    