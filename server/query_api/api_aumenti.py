import imp
import json
import numpy as np
from flask import Blueprint, render_template, abort, jsonify, request, current_app
import pandas as pd
import pyodbc
import jinja2
import codecs
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from flask_mail import Mail, Message
from sqlalchemy.engine import URL, create_engine

api_aumenti = Blueprint('api_aumenti', __name__)

inc = [{'id': 2515, 'descrizione': 'test'},
       {'id': 2458, 'descrizione': 'test1'}]
inc = pd.DataFrame(inc)
idlist = list(inc['id'])
idlist = tuple(idlist)


listini_esclusi = [{'id': 2457, 'descrizione': 'Vending Generale'},
                   {'id': 1132, 'descrizione': 'Tradizionale Generale'},
                   {'id': 1133, 'descrizione': 'Minimi'},
                   {'id': 2773, 'descrizione': 'Top vending'}]


def rtome_tuble(data):
    data = pd.DataFrame(data)
    data = list(data['id'])
    data = tuple(data)
    return data


def insert_db(data):
    try:
        import pymongo
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["machine_aumenti"]
        mycol = mydb["programmati"]
        x = mycol.insert_many(data)
        return {'msg': 'success'}
    except:
        return {'msg': 'errore'}


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


def ck_listini(codice):
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f""" 
        select *
        from LISRIG
        left join lotser on LOTSER.id = LISRIG.IDARTICO
        left join artico on artico.id = LOTSER.IDARTICO
        where IDLISTES IN (2458,2515) AND ARTICO.codice='{codice}'
        """
        data = pd.read_sql(q, engine).fillna(0)
        cnxn.close()
        llist = list(data['IDLISTES'])
        if 2515 in llist and 2458 in llist:
            x = getlistaemail('misto')
            return x['lista'][0]
        elif 2515 in llist:
            x = getlistaemail('tradizionale')
            return x['lista'][0]
        elif 2458 in llist:
            x = getlistaemail('vending')
            return x['lista'][0]
        else:
            x = getlistaemail('errorlist')
            return x['lista'][0]
    except:
        x = getlistaemail('errorlist')
        return x['lista'][0]


def info_artico(codice, lista_inclusioni):
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f"""
                SELECT ARTICO.CODICE AS codice ,ARTICO.DESCR AS descrizione, artico.STAART as stato, ARTICO.ID as id, LOTSER.ID as id_artico_vendita, gst.codori as cod_originale,
                marche.DESCR as marca ,(select MIN(PREZZO)
                from LISRIG
                LEFT JOIN LOTSER ON LOTSER.ID = LISRIG.IDARTICO
                LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
                WHERE  LOTSER.NUMLOT='00000000000' AND ARTICO.CODICE='{codice}' AND LISRIG.IDLISTES  IN {lista_inclusioni}) as prezzo ,
                (select MAX(PREZZO)
                from LISRIG
                LEFT JOIN LOTSER ON LOTSER.ID = LISRIG.IDARTICO
                LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
                WHERE  LOTSER.NUMLOT='00000000000' AND ARTICO.CODICE='{codice}' AND LISRIG.IDLISTES  IN {lista_inclusioni})*2.5 as prezzo_max
                FROM ARTICO
                LEFT JOIN LOTSER ON LOTSER.IDARTICO = ARTICO.ID
                LEFT JOIN MARCHE ON MARCHE.ID = ARTICO.IDMARCHE
                LEFT JOIN SAM.articoGST AS GST ON GST.idartico = ARTICO.ID
                WHERE ARTICO.CODICE ='{codice}' AND LOTSER.NUMLOT='00000000000'

            """
        data = pd.read_sql(q, engine).fillna('')
        return data
    except:
        return []


def get_img(codice):
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f"""
         select  TOP 1  SAMA1_PORTALS.dbo.vw_portal_ImgAttGen.FILENAME  as fname
         FROM SAMA1_PORTALS.dbo.vw_portal_ImgAttGen
         left join SAMA1.dbo.ARTICO as art on art.id = SAMA1_PORTALS.dbo.vw_portal_ImgAttGen.IDARTICO
         WHERE art.CODICE='{codice}'  AND CODICEAPP ='ECOM' AND  TIPO='D'

            """
        data = pd.read_sql(q, engine).fillna('')
        if len(data) > 0:
            urlimg = 'http://www.micromic-ricambi.com/Content/attachments/' + \
                data['fname'][0]
            return urlimg
        else:
            return ''
    except:
        return ''


def price_fornitore(codice):
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f"""

              SELECT top 1 QUOART.PRBASE as quotazione , PSCON1 as sconto1 ,PSCON2 as sconto2 ,PSCON3 as sconto3
            FROM QUOART
            LEFT JOIN ARTICO ON ARTICO.ID = QUOART.IDARTICO
            where ARTICO.CODICE='{codice}' and quoart.tipfor = 'P'

            """
        data = pd.read_sql(q, engine).fillna('')
        if len(data) > 0:
            pbase = data['quotazione'][0]
            sconto1 = data['sconto1'][0]
            sconto2 = data['sconto2'][0]
            sconto3 = data['sconto3'][0]
            if sconto1 > 0:
                sconto1 = (sconto1/100) * pbase
                pnetto = pbase - sconto1
            else:
                pnetto = pbase
            if sconto2 > 0:
                sconto2 = (sconto2/100) * pnetto
                pnetto = pnetto - sconto2
            if sconto3 > 0:
                sconto3 = (sconto3/100) * pnetto
                pnetto = pnetto - sconto3
            pnetto = round(pnetto, 3)
            return pnetto
        else:
            return 0
    except:
        return '500'


def listini_coinvolti(listini_esclusi, codice):
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f"""

            select LISRIG.ID AS id_riga_listino , LISTES.ID as idlistino , LISTES.DESCR as descr_listino , LISRIG.PREZZO as prezzo , LISRIG.QTA as qta
            from LISRIG
            LEFT JOIN LOTSER ON LOTSER.ID = LISRIG.IDARTICO
            LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
            LEFT JOIN LISTES ON LISTES.ID = LISRIG.IDLISTES
            WHERE  LOTSER.NUMLOT='00000000000' AND ARTICO.CODICE='{codice}' AND LISRIG.IDLISTES NOT IN {listini_esclusi}

                """

        data = pd.read_sql(q, engine).fillna('')
        return data
    except:
        return '500'


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()


def elaborate(data, codice):
    try:
        if len(data) > 0 and str(data) != '500':
            ulr_image = get_img(codice)
            costo = price_fornitore(codice)
            data.loc[data.index[0], 'costo'] = costo
            data['codice'] = data['codice'].str.strip()
            data['descrizione'] = data['descrizione'].str.strip()
            data['marca'] = data['marca'].str.strip()
            moltiplicatore = data['prezzo'][0] - data['costo'][0]
            moltiplicatore = round(moltiplicatore / data['costo'][0], 3)
            data.loc[data.index[0], 'ricarico'] = moltiplicatore
            data.loc[data.index[0], 'ulr_image'] = ulr_image
            result = data.loc[0]
            result = result.to_dict()
            result = json.dumps(result, default=np_encoder)
            return result
    except:
        return {'msg': 'errore'}


def send_mail(lista, codice):
    try:
        #lista = ['emanuele.pieroni@micromic.com', 'd.palocci@micromic.com']
        msg = MIMEMultipart('alternative')
        f = codecs.open(
            "../client/component/tools/variazione_prezzi/report.html", 'r')
        f = f.read()
        msg = Message(f"{codice} - MicromicAI-Programmazione Aumento Codice", sender='sistemi@micromic.com',
                      bcc=lista)
        msg.html = f
        with current_app.app_context():
            mail = Mail()
            mail.send(msg)

        return {'msg': 'success'}
    except:
        return {'msg': 'error'}


def crea_template(codice, descrizione, codori, img, marca, aumento, data):
    templateLoader = jinja2.FileSystemLoader(
        searchpath="../client/component/tools/variazione_prezzi/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "template_mail_aumenti.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(codice=codice, descrizione=descrizione, codori=codori, img=img,
                                 aumento=aumento, marca=marca, data=data)  # this is where to put args to the template renderer
    rendHtml = open(
        '../client/component/tools/variazione_prezzi/report.html', 'w')
    rendHtml.write(outputText)
    rendHtml.close()


listini_esclusi = rtome_tuble(listini_esclusi)


@api_aumenti.route('/info/listini/<codice>')
def take_listini(codice):
    try:
        data = listini_coinvolti(listini_esclusi, codice)
        if len(data) > 0:
            return data.to_json(orient='records')
        else:
            return {}
    except:
        print("Errore")
        return {}


@api_aumenti.route('/elaboratelist/', methods=['POST'])
def elaborate_list():
    try:
        data = request.json
        data = pd.DataFrame(data)
        codice = data['codice'][0]
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data['date'] = data['date'].dt.strftime('%d/%m/%Y')
        data = data.to_dict(orient='records')
        tryinsert = insert_db(data)
        if tryinsert['msg'] == 'success':
            return {'msg': 'success'}
        else:
            return {'msg': 'error'}
    except:
        return {'msg': 'error'}


@api_aumenti.route('/send_agent_email/', methods=['POST'])
def send_em_agent():
    try:
        import datetime
        data = request.json
        codice = data['codice']
        mailist = ck_listini(codice)
        cr_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
        cr_date = cr_date.strftime("%d-%m-%Y")
        crea_template(data['codice'], data['descrizione'], data['cod_originale'],
                      data['ulr_image'], data['marca'], data['aumento'], cr_date)
        import time
        time.sleep(1)
        send_mail(mailist, data['codice'])
        return {'msg': 'success'}
    except:
        print("Errore")
        return {}


@api_aumenti.route('/info/<codice>')
def g_aumenti_codice(codice):
    try:
        data = info_artico(codice, idlist)
        if len(data) > 0:
            data = elaborate(data, codice)
            return data
        else:
            return {}
    except:
        print("Errore")
        return {}
