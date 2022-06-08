from operator import index
import pymongo
import pandas as pd
from bson.objectid import ObjectId
import pyodbc
import time
import datetime
from email import encoders
import codecs
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from skpy import Skype, SkypeChats


def smailtech(mybody):
    import win32com.client as win32
    try:
        outlook = win32.GetActiveObject('Outlook.Application')
    except:
        outlook = win32.Dispatch('Outlook.Application')
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'emanuele.pieroni@micromic.com;d.palocci@micromic.com'
    mail.Subject = f'Aumenti Programmati'

    mail.HTMLBody = mybody  # this field is optional
    # To attach a file to the email (optional):
    #attachment = "Path to the attachment"
    # mail.Attachments.Add(attachment)
    mail.Send()


def send_confirm_email(codice, aumento):
    try:
        # print(lista)
        print("Invio Email conferma a")
        lista = ['emanuele.pieroni@micromic.com',
                 'd.palocci@micromic.com', 'marzia.coccellato@micromic.com']
        hh = f""" <p>Salve</p>
        <p>Vi confermiamo che l'aumento programmato di  <b style="color:red">{aumento}</b> € sul codice  <b style="color:red">{codice}</b> &egrave; stato effettuato correttamente.</p>
        <p>I nuovi prezzi sono gi&agrave; disponibiliti sui portali.</p>
        <p>Saluti</p>
        <p><br></p>"""
        msg = MIMEMultipart('alternative')
        me = 'sistemi@micromic.com'
        cc = 'emanuele.pieroni@micromic.com,d.palocci@micromic.com'
        msg['From'] = me
        msg['Subject'] = f"{codice} - Micromic- Aumento effettuato"
        msg['Bcc'] = ','.join(lista)
        msg['From'] = me
        rcpt = cc.split(",") + lista
        msg.attach(MIMEText(hh, "html"))
        server = SMTP('smtps.aruba.it', 587)
        server.starttls()
        server.login(me, 'Micromic$2021')
        server.sendmail(me, rcpt, msg.as_string())
        server.quit()
        print('email  correttamente')
        return {'msg': 'success'}
    except:
        return {'msg': 'error'}


def send_skype_message(codice):
    try:
        sk = Skype("emanuele.pieroni@micromic.com", "Micromic$2021!")
        MSG = f'Attenzione Variazioni eseguite per il codice {codice}'
        ch = sk.chats["19:b16749b2e9ae46bf990573dd1d810e22@thread.skype"]
        ch.sendMsg(MSG)
        return '200'
    except:
        return '400'


def send_confirm_email_fulldb(codice, db, aumento):
    db = db.to_html(index=False)
    lista = ['emanuele.pieroni@micromic.com',
             'd.palocci@micromic.com', 'marzia.coccellato@micromic.com']
    hh = f'<h1>Aumento di {aumento} € su {codice} effettuato correttamente'
    hh = hh + '<br>'
    hh = hh + db
    msg = MIMEMultipart('alternative')
    me = 'sistemi@micromic.com'
    cc = 'emanuele.pieroni@micromic.com,d.palocci@micromic.com'
    msg['From'] = me
    msg['Subject'] = f"{codice} - Micromic- Aumento effettuato"
    msg['Bcc'] = ','.join(lista)
    rcpt = cc.split(",") + lista
    msg.attach(MIMEText(hh, "html"))
    server = SMTP('smtps.aruba.it', 587)
    server.starttls()
    server.login(me, 'Micromic$2021')
    server.sendmail(me, rcpt, msg.as_string())
    server.quit()
    print('email  correttamente')
    return {'msg': 'success'}


def update_max_min(idlistino, codice, prezzo):
    cnxn = pyodbc.connect(
        'DSN=query; ;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN')
    q = f"""
            UPDATE LISRIG
            set PREZZO = {prezzo} ,PREURO ={prezzo}		
            WHERE IDLISTES = {idlistino} AND  IDARTICO = 	(SELECT TOP 1 LOTSER.ID
            FROM LOTSER
            LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
            WHERE ARTICO.CODICE= '{codice}' AND LOTSER.NUMLOT='00000000000')
            """
    cursor = cnxn.cursor()
    cursor.execute(q)
    cnxn.commit()
    return {'msg': 'success'}


def getmax(idlistino, articolo):
    try:
        cnxn = pyodbc.connect(
            'DSN=query; ;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN')
        q = f"""
        SELECT MAX(PREZZO)* 2.5 as massimo
        FROM LISRIG
        LEFT JOIN LOTSER ON LOTSER.ID = LISRIG.IDARTICO
        LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
        WHERE LOTSER.NUMLOT ='00000000000' AND ARTICO.CODICE ='{articolo}' AND LISRIG.IDLISTES={idlistino}
            """

        data = pd.read_sql(q, cnxn).fillna('')
        return data['massimo'][0]
    except:
        return 0


def getmin(idlistino, articolo):
    try:
        cnxn = pyodbc.connect(
            'DSN=query; ;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN')
        q = f"""
        SELECT MIN(PREZZO) as minimo
        FROM LISRIG
        LEFT JOIN LOTSER ON LOTSER.ID = LISRIG.IDARTICO
        LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
        WHERE LOTSER.NUMLOT ='00000000000' AND ARTICO.CODICE ='{articolo}' AND LISRIG.IDLISTES={idlistino}
            """
        data = pd.read_sql(q, cnxn).fillna('')
        return data['minimo'][0]
    except:
        return 0


def update_impresa(id, prezzo):
    try:
        cnxn = pyodbc.connect(
            'DSN=query; ;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN')
        q = f"""
            UPDATE LISRIG
            set PREZZO = {prezzo} ,PREURO ={prezzo}
            WHERE ID = {id}
            """
        cursor = cnxn.cursor()
        cursor.execute(q)
        cnxn.commit()
        return {'msg': 'success'}
    except:
        return{'msg': 'error'}


def updatestatust(_id):
    try:
        _id = ObjectId(_id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["machine_aumenti"]
        mycol = mydb["programmati"]
        myquery = {"_id": _id}
        newvalues = {"$set": {"elaborato": True}}
        mycol.update_one(myquery, newvalues)
        return {'msg': 'success'}
    except:
        return {'msg': 'error'}


def update_lisrig(id, newprice, _id):
    try:
        uimp = update_impresa(id, newprice)
        umdb = updatestatust(_id)
        msgimp = uimp["msg"]
        msgmdb = umdb["msg"]
        response = {'imp': msgimp, 'mdb': msgmdb}
        return response
    except:
        response = {'imp': 'error', 'mdb': 'error'}
        return response


def get_today(today):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["machine_aumenti"]
    mycol = mydb["programmati"]
    q = {'date': today, 'elaborato': False}
    x = list(mycol.find(q))
    x = pd.DataFrame(x)
    return x


print("- MICROMIC AI - ")
print("Elaborazione aumenti del giorno ....")


today = datetime.date.today().strftime("%d/%m/%Y")

print("Scarico la lista delle righe d'aggiornare")
ellist = get_today(today)
if len(ellist) > 0:
    print("Ci sono Codici da aggiornare ...")
    cod_list = ellist.codice.unique()
    print("Lista dei codici coinvolti :")
    print(cod_list)
    print("Elaborazione aumenti programmati")
    for pcode in cod_list:
        print(pcode)
        dblist = ellist[ellist['codice'] == pcode]
        for i, r in dblist.iterrows():
            _id = r['_id']
            newprice = r['newprice']
            id = r['id_riga_listino']
            aumento = float(r['newprice'] - r['prezzo'])
            aumento = round(aumento, 2)
            response = update_lisrig(id, newprice, _id)
            response['codice'] = r['codice']

        print(f"{pcode} - Aumento effettuato correttamente")
        x = pcode.startswith("VE")
        if x == True:
            print('DEVO AGGIORNARE MINIMO E MASSIMO DEL LISTINO GENERARE VENDING')
            massimo = getmax(2458, pcode)
            minimo = getmin(2458, pcode)
            update_max_min(2457, pcode, massimo)
            update_max_min(1133, pcode, minimo)
        else:
            print('DEVO AGGIORNARE MINIMO E MASSIMO DEL LISTINO GENERARE TRADIZIONALE')
            massimo = getmax(2515, pcode)
            minimo = getmin(2515, pcode)
            update_max_min(1132, pcode, massimo)
            update_max_min(1133, pcode, minimo)

        send_confirm_email(pcode, aumento)
        neset = dblist[["idlistino", "descr_listino",
                        "prezzo", "qta", "newprice"]]
        send_confirm_email_fulldb(pcode, neset, aumento)
        send_skype_message(pcode)
else:
    print("Non ci sono aumenti programmati per oggi ")
    smailtech("👀 Nessun Aumento Programmato per Oggi")
