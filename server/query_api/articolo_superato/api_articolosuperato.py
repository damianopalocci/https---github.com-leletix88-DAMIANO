from flask import Blueprint, render_template, abort, request
import codecs
import jinja2
import pyodbc
import pandas as pd
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from sqlalchemy.engine import URL, create_engine

from smtplib import SMTP


articolo_superato = Blueprint('articolo_superato', __name__)


def get_info_artico(articolo):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""
        select top 1(SELECT TOP 1 SAMA1_PORTALS.dbo.vw_portal_ImgAttGen.FILENAME 
    FROM SAMA1_PORTALS.dbo.vw_portal_ImgAttGen
       left join SAMA1.dbo.ARTICO as art on art.id = SAMA1_PORTALS.dbo.vw_portal_ImgAttGen.IDARTICO
         WHERE art.CODICE='{articolo}'  AND CODICEAPP ='ECOM' AND  TIPO='D') as fname ,
        (SELECT TOP 1 SAM.articoGST.codori
        FROM SAM.articoGST
        LEFT JOIN SAMA1.DBO.ARTICO ON SAMA1.DBO.ARTICO.ID = SAM.articoGST.idartico
        WHERE SAMA1.DBO.ARTICO.CODICE ='{articolo}') as codori,
         (SELECT TOP 1 SAMA1.DBO.ARTICO.DESCR
        FROM SAMA1.DBO.ARTICO
        WHERE SAMA1.DBO.ARTICO.CODICE ='{articolo}') as descrizione ,
		 (SELECT TOP 1 marche.DESCR as marca
        FROM SAMA1.DBO.ARTICO
		left join SAMA1.DBO.MARCHE as marche on marche.id = SAMA1.DBO.ARTICO.IDMARCHE
        WHERE SAMA1.DBO.ARTICO.CODICE ='{articolo}') as marca,
        (SELECT TOP 1 SAM.articoGST.descrweb
        FROM SAM.articoGST
        LEFT JOIN SAMA1.DBO.ARTICO ON SAMA1.DBO.ARTICO.ID = SAM.articoGST.idartico
        WHERE SAMA1.DBO.ARTICO.CODICE ='{articolo}') as descrweb
        """
    data = pd.read_sql(q, engine).fillna('')
    if len(data) > 0:
        data['fname'] = " http://www.micromic-ricambi.com/Content/attachments/" + data['fname']
        return data
    else:
        return []


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
            x = getlistaemail('tradizionale')
            return x['lista'][0]
    except:
        lista = ['emanuele.pieroni@micromic.com', 'd.palocci@micromic.com']
        return lista


def crea_template(codice, descrizione, note, codori, fname, marca):
    templateLoader = jinja2.FileSystemLoader(
        searchpath="../client/component/tools/articoli_superati/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "template.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(codice=codice, descrizione=descrizione, codori=codori, fname=fname,
                                 note=note, marca=marca)  # this is where to put args to the template renderer
    rendHtml = open(
        '../client/component/tools/articoli_superati/report.html', 'w')
    rendHtml.write(outputText)
    rendHtml.close()


def send_mail(lista):
    try:
        # print(lista)
        #lista = ['emanuele.pieroni@micromic.com','d.palocci@micromic.com' ]
        msg = MIMEMultipart('alternative')
        f = codecs.open(
            "../client/component/tools/articoli_superati/report.html", 'r')
        f = f.read()
        me = 'sistemi@micromic.com'
        cc = 'emanuele.pieroni@micromic.com'
        msg['From'] = me
        msg['Subject'] = "Micromic-AI Articolo Superato"
        msg['Bcc'] = ','.join(lista)
        msg['From'] = me
        rcpt = cc.split(",") + lista
        msg.attach(MIMEText(f, "html"))
        server = SMTP('smtps.aruba.it', 587)
        server.starttls()
        server.login(me, 'Micromic$2021')
        server.sendmail(me, rcpt, msg.as_string())
        server.quit()
        return {'msg': 0}
    except:
        return {'msg': 2}


@articolo_superato.route('/find_articolo/<articolo>', methods=['GET', 'POST'])
def find_articolo(articolo):
    x = get_info_artico(articolo)
    if len(x) > 0:
        return x.to_json(orient='records')


@articolo_superato.route('/send_email', methods=['GET', 'POST'])
def send_email():

    try:

        data = request.json

        if data:
            _codice = str(data['codice']).strip().upper()
            try:
                _note = str(data['note']).strip()
            except:
                _note = ''
            _codori = str(data['data']['codori']).strip()
            _marca = str(data['data']['marca']).strip()
            _descrizione = str(data['data']['descrizione']).strip()
            _fname = str(data['data']['fname']).strip()
            _lista = ck_listini(_codice)
            crea_template(_codice, _descrizione, _note,
                          _codori, _fname, _marca)
            import time
            time.sleep(1)
            send_mail(_lista)

            return ({'msg': 0})

        else:
            return ({'msg': 2})
    except:
        return ({'msg': 2})
