from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import pyodbc
import time
import codecs
from flask import Blueprint, render_template, abort, jsonify, request
import pandas as pd

api_newsletter = Blueprint('api_newsletter', __name__)


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


def send_mail(lista):
    try:
        # print(lista)
        lista = ['emanuele.pieroni@micromic.com', 'd.palocci@micromic.com']
        f = codecs.open(
            "../client/component/tools/newsletter/report.html", 'r')
        f = f.read()
        msg = MIMEMultipart('alternative')
        me = 'sistemi@micromic.com'
        cc = 'emanuele.pieroni@micromic.com'
        msg['From'] = me
        msg['Subject'] = "Micromic- Vending News"
        msg['Bcc'] = ','.join(lista)
        msg['From'] = me
        rcpt = cc.split(",") + lista
        msg.attach(MIMEText(f, "html"))
        server = SMTP('smtps.aruba.it', 587)
        server.starttls()
        server.login(me, 'Micromic$2021')
        server.sendmail(me, rcpt, msg.as_string())
        server.quit()
        print('email  correttamente')
        return {'msg': 'success'}
    except:
        return {'msg': 'error'}


def get_lotser(codice):
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f""" 
                select top 1 LOTSER.id as idurl
        from LOTSER
        LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO 
        where LOTSER.NUMLOT='00000000000' and artico.codice ='{codice}'"""
        data = pd.read_sql(q, engine).fillna(0)
        if len(data) > 0:
            return data['idurl'][0]
    except:
        return {'msg': 'error'}


def crea_template(data):
    try:
        import jinja2
        templateLoader = jinja2.FileSystemLoader(
            searchpath="../client/component/tools/newsletter/")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "template_news.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        # this is where to put args to the template renderer
        outputText = template.render(data=data)
        rendHtml = open(
            '../client/component/tools/newsletter/report.html', 'w')
        rendHtml.write(outputText)
        rendHtml.close()
        return True
    except:
        return False


@api_newsletter.route('/generate/', methods=['POST'])
def send_em_agent():
    try:
        mydatacode = request.json
        mydatacode = pd.DataFrame(mydatacode)
        sinistra = ''
        left = 'left'
        right = 'right'
        for i, r in mydatacode.iterrows():
            codice = r['codice'].upper()
            urlid = get_lotser(codice)
            img = r['fname']
            descrizione = r['descrweb']
            marca = r['marca'].upper()
            sinistra += f"""<tr style="border-collapse:collapse">
                              <td align="left" style="Margin:0;padding-top:10px;padding-bottom:10px;padding-left:40px;padding-right:40px">
                                  <!--[if mso]><table style="width:200px" cellpadding="0" cellspacing="0"><tr><td style="width:256px" valign="top"><![endif]-->
                                  <table class="es-left" cellspacing="0" cellpadding="0" align="left" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:{left}">
                                      <tr style="border-collapse:collapse">
                                          <td class="es-m-p0r es-m-p20b" valign="top" align="center" style="padding:0;Margin:0;width:256px">
                                              <table style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-position:center top" width="100%" cellspacing="0" cellpadding="0" role="presentation">
                                                  <tr style="border-collapse:collapse">
                                                      <td align="center" style="padding:0;Margin:0;font-size:0px">                                                          
                                                          <img class="adapt-img" src="{img}" 
                                                          style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="246">
                                                      </td>
                                                  </tr>
                                              </table>
                                          </td>
                                      </tr>
                                  </table>
                                  <!--[if mso]></td><td style="width:20px"></td><td style="width:264px" valign="top"><![endif]-->
                                  <table class="es-right" cellspacing="0" cellpadding="0" align="right" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:{right}">
                                      <tr style="border-collapse:collapse">
                                          <td align="left" style="padding:0;Margin:0;width:264px">
                                              <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                                                  <tr style="border-collapse:collapse">
                                                      <td class="es-m-txt-c" align="left" style="padding:0;Margin:0;padding-bottom:10px;padding-top:20px">
                                                          <h4 style="Margin:0;line-height:31px;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;text-align:center;font-size:26px;color:#43c3a1">&nbsp;{codice}</h4>
                                                      </td>
                                                  </tr>
                                                  <tr style="border-collapse:collapse">
                                                      <td class="es-m-txt-c" align="center" style="padding:0;Margin:0">
                                                          <p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;
                                                          font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:21px;color:#333333;font-size:14px"><strong><em>{descrizione}</em></strong><strong><em>.</em></strong></p>
                                                          <p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:21px;color:#333333;font-size:14px"><strong>MARCA</strong>&nbsp;:&nbsp;<u><em>{marca}</em></u></p>
                                                      </td>
                                                  </tr>
                                                  <tr style="border-collapse:collapse">
                                                      <td align="center" style="padding:0;Margin:0;padding-top:15px;padding-bottom:25px"><span class="es-button-border"
                                                       style="border-style:solid;border-color:#ffffff;background:#e48c1e;border-width:0px;display:inline-block;border-radius:9px;width:auto">
                                                       <a href="http://www.micromic-ricambi.com/Products/{urlid}" class="es-button" target="_blank" style="mso-style-priority:100 !important;text-decoration:none;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;color:#efefef;font-size:18px;border-style:solid;border-color:#e48c1e;border-width:10px 20px;display:inline-block;background:#e48c1e;border-radius:9px;font-family:'comic sans ms', 'marker felt-thin', arial, sans-serif;font-weight:bold;font-style:normal;line-height:22px;width:auto;text-align:center">Buy Now !</a></span></td>
                                                  </tr>
                                              </table>
                                          </td>
                                      </tr>
                                  </table>
                                  <!--[if mso]></td></tr></table><![endif]-->
                              </td>
                          </tr>"""
            if left == 'left':
                left = 'right'
            else:
                left = 'left'
            if right == 'right':
                right = 'left'
            else:
                right = 'right'
        crea = crea_template(sinistra)
        time.sleep(1)
        if crea == True:
            return {'msg': 'success'}
        else:
            return {'msg': 'error'}

    except:
        print("Errore")
        return {}
