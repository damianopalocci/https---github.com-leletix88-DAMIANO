from flask import Blueprint, render_template, abort, request
import codecs
import jinja2
import pyodbc
import pandas as pd

from smtplib import SMTP

from sqlalchemy.engine import URL, create_engine
from query_api.moduli.listini_vendita import list_to_json
from datetime import date
import numpy as np


listini_promozionali = Blueprint('listini_promozionali', __name__)

global current_year, lastone

current_year = date.today().year
lastone = current_year -1  


def getstat(mese,articoli):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create( 
        "mssql+pyodbc", query={"odbc_connect": connection_string}) 
    engine = create_engine(connection_url)
    q=f"""
    SELECT CS_Fatturato.CLIENTE,CS_Fatturato.MESE,CS_Fatturato.ANNO,CS_Fatturato.CODART,CS_Fatturato.QTA,CS_Fatturato.prezzou ,
    CS_FATTURATO.IMPNETTO ,CS_FATTURATO.CategoriaFornitore ,CS_FATTURATO.ZONA ,CS_FATTURATO.NAZIONE,CS_FATTURATO.NAZIONE,CS_FATTURATO.idlistfatt ,
    (select top 1 PERSONE.DESCR1 AS AGENTE 
        FROM AGENTI
        LEFT JOIN PERSONE ON PERSONE.ID = AGENTI.IDPERSONA
        LEFT JOIN CLIENTI ON CLIENTI.IDAGENTE = AGENTI.ID
        LEFT JOIN PERSONE AS PP ON PP.ID = CLIENTI.IDPERSONA
        WHERE PP.DESCR1 = CS_Fatturato.CLIENTE) AS AGENTE ,
    ISNULL((SELECT TOP 1 GST.isVending
    FROM CLIENTI
    LEFT JOIN PERSONE ON PERSONE.ID = CLIENTI.IDPERSONA
    LEFT JOIN SAMA1.SAM.ClientiGST AS gst on gst.idclienti = persone.ID
    where PERSONE.DESCR1 = CS_Fatturato.CLIENTE),0) as isVending ,	
    (select top 1marche.DESCR
    from artico
    left join MARCHE on marche.id = artico.IDMARCHE
    where artico.codice = CS_Fatturato.codart) as MARCA,
    (select top 1 AGENTI.ID AS IDAGENTE 
        FROM AGENTI
        LEFT JOIN PERSONE ON PERSONE.ID = AGENTI.IDPERSONA
        LEFT JOIN CLIENTI ON CLIENTI.IDAGENTE = AGENTI.ID
        LEFT JOIN PERSONE AS PP ON PP.ID = CLIENTI.IDPERSONA
        WHERE PP.DESCR1 = CS_Fatturato.CLIENTE) AS IDAGENTE 
    FROM GSTPIVOT.dbo.CS_Fatturato_new CS_Fatturato 
    WHERE  (CODART NOT LIKE '%TRASPO%' AND CODART <>'VARI' AND CODART <>'DIVERSI' or CODART  IS NULL ) 
    AND  CS_Fatturato.ANNO >YEAR(getdate())-3  AND (select top 1 AGENTI.ID AS IDAGENTE 
    FROM AGENTI
        LEFT JOIN PERSONE ON PERSONE.ID = AGENTI.IDPERSONA
        LEFT JOIN CLIENTI ON CLIENTI.IDAGENTE = AGENTI.ID
        LEFT JOIN PERSONE AS PP ON PP.ID = CLIENTI.IDPERSONA
    WHERE PP.DESCR1 = CS_Fatturato.CLIENTE) NOT IN(60,109,74,22,0,105,107) AND  (CS_Fatturato.MESE <=  MONTH(getdate()) AND CS_Fatturato.MESE>={mese}) AND
    CS_Fatturato.CODART IN {articoli} AND CS_FATTURATO.NAZIONE ='Italia'     
    """
    data = pd.read_sql(q, engine).fillna('')
    return data

def getinfo(listino):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create( 
        "mssql+pyodbc", query={"odbc_connect": connection_string}) 
    engine = create_engine(connection_url)
    q=f"""
        SELECT MONTH(CONVERT(datetime,LISTES.DATINI)) as mese , year(CONVERT(datetime,LISTES.DATINI)) as anno
        FROM LISTES
        WHERE ID = {listino}    
    """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data)>0:
        return data['mese'][0]
def getcodelist(listino):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create( 
        "mssql+pyodbc", query={"odbc_connect": connection_string}) 
    engine = create_engine(connection_url)
    q=f"""
    SELECT ARTICO.CODICE
    FROM LISRIG
    LEFT JOIN LOTSER ON LOTSER.ID = LISRIG.IDARTICO
    LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
    WHERE LISRIG.IDLISTES ={listino}
    """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data)>0:
        return tuple(list(data['CODICE'].str.strip()))

def generate(idlistino):
    meselistino = getinfo(idlistino)
    listcode = getcodelist(idlistino)
    data = getstat(meselistino,listcode)
    ndb = []
    for i,r in data.iterrows():
        if(r['ANNO']==current_year and r['idlistfatt']!=idlistino):        
            pass
        else:
            ndb.append(r.to_dict())
    data = pd.DataFrame(ndb)
    table_fatturato = pd.pivot_table(data, values='IMPNETTO', index=['CODART'],
                        columns=['ANNO'], aggfunc=np.sum, fill_value=0).reset_index().fillna(0)
    table_fatturato['CODART'] = table_fatturato['CODART'].str.strip()
    table_fatturato['difference'] = table_fatturato[current_year] - table_fatturato[lastone]
    table_fatturato['difference'] = table_fatturato['difference']  / table_fatturato[lastone]
    table_fatturato['difference'] =  round(table_fatturato['difference'] *100,2)
    return table_fatturato.fillna(0).to_json(orient='records')



def getlistpromo():
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f"""  
            SELECT ID AS IDLISTINO , CODICE, LTRIM(RTRIM(DESCR)) AS DESCRIZIONE
            FROM LISTES
            WHERE CODICE LIKE '%PROMO%' and OKWEB = -1
            """
        data = pd.read_sql(q,engine)
        return data.to_json(orient='records')
    except:
        return 500

def gedata(id_list):
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f"""  
         SELECT CS_Fatturato.CLIENTE,CS_Fatturato.MESE,CS_Fatturato.ANNO,CS_Fatturato.CODART AS CODICE,CS_Fatturato.QTA ,CS_Fatturato.prezzou ,
        CS_FATTURATO.IMPNETTO ,CS_FATTURATO.CategoriaFornitore ,CS_FATTURATO.ZONA ,CS_FATTURATO.NAZIONE,CS_FATTURATO.NAZIONE,CS_FATTURATO.idlistfatt ,
        (select top 1 PERSONE.DESCR1 AS AGENTE 
            FROM AGENTI
            LEFT JOIN PERSONE ON PERSONE.ID = AGENTI.IDPERSONA
            LEFT JOIN CLIENTI ON CLIENTI.IDAGENTE = AGENTI.ID
            LEFT JOIN PERSONE AS PP ON PP.ID = CLIENTI.IDPERSONA
            WHERE PP.DESCR1 = CS_Fatturato.CLIENTE) AS AGENTE ,
        ISNULL((SELECT TOP 1 GST.isVending
        FROM CLIENTI
        LEFT JOIN PERSONE ON PERSONE.ID = CLIENTI.IDPERSONA
        LEFT JOIN SAMA1.SAM.ClientiGST AS gst on gst.idclienti = persone.ID
        where PERSONE.DESCR1 = CS_Fatturato.CLIENTE),0) as isVending ,	
        (select top 1marche.DESCR
        from artico
        left join MARCHE on marche.id = artico.IDMARCHE
        where artico.codice = CS_Fatturato.codart) as MARCA,
        (select top 1 AGENTI.ID AS IDAGENTE 
            FROM AGENTI
            LEFT JOIN PERSONE ON PERSONE.ID = AGENTI.IDPERSONA
            LEFT JOIN CLIENTI ON CLIENTI.IDAGENTE = AGENTI.ID
            LEFT JOIN PERSONE AS PP ON PP.ID = CLIENTI.IDPERSONA
            WHERE PP.DESCR1 = CS_Fatturato.CLIENTE) AS IDAGENTE 
        FROM GSTPIVOT.dbo.CS_Fatturato_new CS_Fatturato 
        WHERE  CS_Fatturato.idlistfatt = {id_list}
            """
        data = pd.read_sql(q,engine)
        return data
        
def gby(data,field,head):
    ndata  = data.groupby([f'{field}'])['IMPNETTO'].agg('sum').reset_index()
    ndata = ndata.sort_values(by=['IMPNETTO'], ascending=False).head(head)
    return ndata.to_dict(orient='records')




@listini_promozionali.route('/find_list_promo', methods=['GET', 'POST'])
def find_l_p():
    x = getlistpromo()
    if len(x) > 0:
        return x
    else:
        return {"msg": "errore"}      




@listini_promozionali.route('/find_list_promo/<id_list>', methods=['GET', 'POST'])
def find_l_p_idlistino(id_list):
        data = gedata(id_list)

        listino = list_to_json(id_list)
        agenti = gby(data,'AGENTE',10)
        codici = gby(data,'CODICE',5)
        cliente = gby(data,'CLIENTE',5)
        x = {'dbagenti':agenti,'db':data.to_dict(orient='records') ,'dbcodici':codici,'dbclienti':cliente, 'listino' : listino.to_dict(orient='records')}
        if len(x) > 0:
            return x
        else:
            return {"msg": "errore"}



