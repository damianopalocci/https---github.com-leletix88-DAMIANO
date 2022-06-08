from numpy import true_divide
import pandas as pd
from pip import main
import pyodbc
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import codecs
from smtplib import SMTP


# def loginsmtpserver():
#    try:
#        global server
#        print('TENTATIVO LOGIN SMPT')
#        me = 'vendingnews@micromic.com'
#        server = SMTP('smtps.aruba.it', 587)
#        server.starttls()
#        server.login(me, 'Micromic$2021')
#        print('LOGIN AVVENUTO')
#        return server
#    except:
#        print('errore login')


def getlistaemail(tipo):
    try:
        import pymongo
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["Email"]
        q = {'tipo': tipo}
        x = mycol.find(q)
        x = list(x)
        x = pd.DataFrame(x)
        return x
    except:
        return {'msg': 'errore'}


def send_mail(to):
    try:
        msg = MIMEMultipart('alternative')
        f = codecs.open(
            "../client/component/tools/newsletter/report.html", 'r')
        f = f.read()
        me = 'vendingnews@micromic.com'
        msg['From'] = me
        msg['Subject'] = "MicroMic - Novità Vending"
        msg['Bcc'] = 'emanuele.pieroni@micromic.com'
        rcpt = to.split(";")
        server = SMTP('smtps.aruba.it', 587)
        server.starttls()
        me = 'vendingnews@micromic.com'
        server.login(me, 'Micromic$2021')
        msg.attach(MIMEText(f, "html"))
        server.sendmail(me, rcpt, msg.as_string())
        return True
    except:
        return False


def get_vending_list_italia():
    try:
        cnxn = pyodbc.connect(
            'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN')
        q = f"""
        SELECT  PERSONE.DESCR1 AS cliente , gst.isVending as tipo ,
        gst.Mailinglist , gst.Marketing , 
        CLIENTI.Stato , NAZIONI.DESCR as nazione , PERSONE.EMAIL AS email
        FROM CLIENTI
        LEFT JOIN PERSONE ON PERSONE.ID = CLIENTI.IDPERSONA
        LEFT JOIN SAMA1.SAM.ClientiGST AS gst on gst.idclienti = persone.ID
        LEFT JOIN NAZIONI ON NAZIONI.ID = PERSONE.IDNAZIONI
        where CLIENTI.STATO = 'A' AND GST.isVending = -1 AND GST.Marketing ='SI' and  NAZIONI.DESCR ='ITALIA'
            """
        data = pd.read_sql(q, cnxn).fillna('')
        return data['email']
    except:
        return[]


if __name__ == '__main__':
    #lista = ['emanuele.pieroni@micromic.com', 'd.palocci@micromic.com']

    lista = getlistaemail('vending')
    lista = lista['lista'][0]
    for user in lista:
        try:
            tt = send_mail(str(user))
            if tt == True:
                print(f"Email inviata con successo a {user}")
            else:
                print(f"Email fallita a {user}")
        except:
            print(f"Email fallita a {user}")
    print('Elaborazione Terminata')
