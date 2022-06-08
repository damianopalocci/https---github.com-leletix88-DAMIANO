from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import pandas as pd
import pyodbc
from .fix_fatturati import main as mainfatt
import telepot
from sqlalchemy.engine import URL, create_engine
bot = telepot.Bot('5167065973:AAHfDG_qyMBRNQR-r_EuK2q1E9u5GEMnSm4')

api_magazzino = Blueprint('api_magazzino', __name__)


def ffordine(ordine):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""
        select COMTES.ID  as id, PERSONE.DESCR1 AS cliente , COMTES.ANNDOC as anno
        from COMTES
        LEFT JOIN CLIENTI ON CLIENTI.ID= COMTES.IDCLIENTE
        LEFT JOIN PERSONE ON PERSONE.ID = CLIENTI.IDPERSONA
        where COMTES.id = {ordine} and COMTES.ANNDOC = YEAR(getdate())

        """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data) > 0:
        data['cliente'] = data['cliente'].str.strip()
    return data


def fo(ordine):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""
        select COMTES.ID  as id, PERSONE.DESCR1 AS cliente , COMTES.ANNDOC as anno ,COMTES.NUMDOC numero ,
		 cast(cast(COMTES.DATDOC  as datetime) as date) as data_documento,
		 cast(cast(COMTES.DATCNF  as datetime) as date) as data_conferma
        from COMTES
        LEFT JOIN CLIENTI ON CLIENTI.ID= COMTES.IDCLIENTE
        LEFT JOIN PERSONE ON PERSONE.ID = CLIENTI.IDPERSONA
        where COMTES.NUMDOC = {ordine} and COMTES.ANNDOC = YEAR(getdate())
        """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data) > 0:
        data['cliente'] = data['cliente'].str.strip()
        return data
    else:
        return False


def allview():
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""
	select SAM.COMTESGST.IDMASTER AS ID,SAM.COMTESGST .mag_status AS STATO ,
	PERSONE.DESCR1 AS CLIENTE , COMTES.NUMDOC,
	 cast(cast(COMTES.DATCNF  as datetime) as date) as data_conferma
        from SAM.COMTESGST 
        left join COMTES on COMTES.id = sam.COMTESGST.idmaster
        left join CLIENTI on CLIENTI.ID = COMTES.IDCLIENTE
        LEFT JOIN PERSONE ON PERSONE.ID = CLIENTI.IDPERSONA
        where COMTES.STATO <>'F'  and SAM.COMTESGST.mag_status <>3
        """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data) > 0:
        return data
    else:
        return False


def chk_if_closed(idcomtes, cliente):
    cliente = cliente.replace("'", "")
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""
    SELECT TOP 1 (FATTES.ID) 
    FROM FATRIG
    LEFT JOIN FATTES ON FATTES.ID = FATRIG.IDFAT
    WHERE DesCli = '{cliente}' AND ANNDOC=2022 AND  DESCR LIKE '%{idcomtes}%'
        """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data) > 0:
        return True
    else:
        return False


def find_stato(id):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""
        select top 1 id
        from SAM.COMTESGST
        where sam.comtesgst.idmaster = {id}
        """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data) > 0:
        return True
    else:
        return False


def insert_new(id, stato):
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f""" 
            INSERT INTO SAM.COMTESGST (idmaster, mag_status)
            VALUES ({id}, '{stato}');
            """
        cursor.execute(q)
        engine.commit()
        return '200'
    except:
        return '400'


def update_status(id, stato):
    x = find_stato(id)
    if x == True:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f""" 
            UPDATE SAM.COMTESGST
            SET mag_status = '{stato}'
            where sam.comtesgst.idmaster = {id}
            """
        cursor.execute(q)
        engine.commit()
        return '200'
    else:
        insert_new(id, stato)


@api_magazzino.route('/')
def home():
    try:
        return {'msg': 'ok'}
    except TemplateNotFound:
        abort(404)


def fimagecode(codice):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""
 
    select (SELECT TOP 1 SAMXX_PORTALS.dbo.vw_portal_ImgAttGen.FILENAME 
    FROM SAMXX_PORTALS.dbo.vw_portal_ImgAttGen
    WHERE DESCR LIKE '%{codice}%' AND CODICEAPP ='ECOM' AND  TIPO='D') as fname ,
    (SELECT TOP 1 SAM.articoGST.codori
    FROM SAM.articoGST
    LEFT JOIN SAMA1.DBO.ARTICO ON SAMA1.DBO.ARTICO.ID = SAM.articoGST.idartico
    WHERE SAMA1.DBO.ARTICO.CODICE ='{codice}') as codori
        """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data) > 0:
        return data
    else:
        return False


def bot_message(cliente, stato):
    msg = '📦 STATO ORDINE/MAGAZZINO 📦\n\n'
    msg += f'🧑🏻 CLIENTE 🧑🏻\n'
    msg += f'{cliente}\n\n'
    msg += f'🖖🏻 STATO 🖖🏻\n'
    msg += f'{stato}\n'
    msg += '\n'
    bot.sendMessage(-627048914, msg)


def all_to_fix_order(ordine):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""

        select SAM.COMTESGST.IDMASTER AS ID,SAM.COMTESGST .mag_status AS STATO ,PERSONE.DESCR1 AS CLIENTE , COMTES.NUMDOC
        from SAM.COMTESGST 
        left join COMTES on COMTES.id = sam.COMTESGST.idmaster
        left join CLIENTI on CLIENTI.ID = COMTES.IDCLIENTE
        LEFT JOIN PERSONE ON PERSONE.ID = CLIENTI.IDPERSONA
        where SAM.COMTESGST .mag_status <>3 

        """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data) > 0:
        data['cliente'] = data['cliente'].str.strip()
    return data


@api_magazzino.route('/find_ordine/<id>')
def find_ordine(id):
    try:
        import os
        data = fo(id)
        return data.to_json(orient='records')
    except:
        return {}


@api_magazzino.route('/stat_mag/<id>/<stato>', methods=['GET', 'POST'])
def stat_mag(id, stato):
    ordine = ffordine(id)
    if len(ordine) > 0:
        cliente = ordine['cliente'][0]
    if stato == '0':
        update_status(id, 0)
        stato = 'In fase di preparazione'
    if stato == '1':
        update_status(id, 1)
        stato = 'Packaging'
    if stato == '2':
        update_status(id, 2)
        stato = 'In attesa spedizione'
    if stato == '3':
        update_status(id, 3)
        stato = 'Spedito'
    txt = f"""
                <div style="font-size :11px">
                <p><strong><span style="color: rgb(209, 72, 65);">Stato Ordini</span></strong></p>
                <p><strong>Numero Ordine</strong> : {id}</p>
                <p><strong>Cliente</strong> : {cliente}</p>
                <p><strong>Stato</strong> : {stato}</p>
                </div>
            """
    bot_message(cliente, stato)
    return txt


@api_magazzino.route('/get_all_status')
def get_all_status():
    try:
        import os
        data = allview()
        mainfatt()
        return data.to_json(orient='records')
    except:
        return {}
