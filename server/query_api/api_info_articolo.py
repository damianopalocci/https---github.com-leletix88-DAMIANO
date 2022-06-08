from flask import Blueprint, render_template, abort, request
import codecs
import jinja2
import pyodbc
import pandas as pd

from smtplib import SMTP

from sqlalchemy.engine import URL, create_engine



info_articolo = Blueprint('info_articolo', __name__)


def get_info_artico(codice): 

    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""
        SELECT LTRIM(RTRIM(ARTICO.CODICE)) AS articolo,  LTRIM(RTRIM(GST.codori)) AS codice_ori, 
        LTRIM(RTRIM(CATEGORY.DESCR)) AS categoria,  LTRIM(RTRIM(MARCHE.DESCR)) as marca, 
        LTRIM(RTRIM(ARTICO.DESCR)) AS descrizione,
        (SELECT TOP 1 SAMA1_PORTALS.dbo.vw_portal_ImgAttGen.FILENAME 
        FROM SAMA1_PORTALS.dbo.vw_portal_ImgAttGen
        left join SAMA1.dbo.ARTICO as art on art.id = SAMA1_PORTALS.dbo.vw_portal_ImgAttGen.IDARTICO
        WHERE art.CODICE=ARTICO.CODICE  AND CODICEAPP ='ECOM' AND  TIPO='D') as immagine
        FROM ARTICO
        LEFT OUTER JOIN SAM.articoGST AS GST ON GST.idartico = ARTICO.ID
        LEFT OUTER JOIN CATOMO AS CATEGORY ON CATEGORY.ID = ARTICO.IDCATOMO
        LEFT OUTER JOIN MARCHE ON MARCHE.ID = ARTICO.IDMARCHE
        WHERE ARTICO.CODICE = '{codice}'

        """
    data = pd.read_sql(q, engine).fillna('')
    if len(data) > 0:
        return data
    else:
        return []



def get_data_magaz(codice):
    
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""
        SELECT GIAMAG.QTTGIAI AS giacenza , ANAMAG.DESCR as descrizione
        FROM GIAMAG
        LEFT JOIN LOTSER ON LOTSER.ID = GIAMAG.IDARTICO
        LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
        LEFT JOIN ALLMAG ON ALLMAG.ID = GIAMAG.IDMAG
        LEFT JOIN ANAMAG ON ANAMAG.ID = ALLMAG.IDANAMAG
        WHERE LOTSER.NUMLOT ='00000000000' AND ARTICO.CODICE = '{codice}'
       """
    data = pd.read_sql(q, engine).fillna('')
    if len(data) > 0:
        return data
    else:
        return []

def get_padre_figlio(codice):
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f"""
        SELECT  LTRIM(RTRIM(ARTPADRE.CODICE)) AS padre ,  LTRIM(RTRIM(ARTFIGLI.CODICE)) AS figlio
        FROM EXT_ARTFIGLI
        LEFT JOIN ARTICO AS ARTPADRE ON ARTPADRE.ID = EXT_ARTFIGLI.IDARTICO
        LEFT JOIN ARTICO AS ARTFIGLI ON ARTFIGLI.ID = EXT_ARTFIGLI.IDARTFIGLIO
        WHERE ARTPADRE.CODICE = '{codice}' OR ARTFIGLI.CODICE = '{codice}'
        """
        data = pd.read_sql(q, engine).fillna('')
        if len(data) > 0:
            return data
        else:
            return []
    except:
            return []


def get_statisitiche_art(codice):
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f"""
        SELECT CS_Fatturato.CLIENTE,CS_Fatturato.MESE,CS_Fatturato.ANNO,CS_Fatturato.CODART,CS_Fatturato.QTA,CS_Fatturato.prezzou ,
        CS_FATTURATO.IMPNETTO ,CS_FATTURATO.CategoriaFornitore ,CS_FATTURATO.ZONA ,CS_FATTURATO.NAZIONE,
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
            WHERE PP.DESCR1 = CS_Fatturato.CLIENTE) NOT IN(60,109,74,22,0,105,107)
            AND CODART ='{codice}'
        """
        data = pd.read_sql(q, engine).fillna('')
        if len(data) > 0:
            return data
        else:
            return []
    except: 
        return []


def price_fornitore(codice):
    try:
    
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
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
        return []


def get_nome_fornitore(codice):
    
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f"""
        SELECT PERSONE.DESCR1 AS fornitore
        FROM QUOART
        LEFT JOIN LISFOR ON LISFOR.ID = QUOART.IDLISFOR
        LEFT JOIN FORNITORI ON FORNITORI.ID = LISFOR.IDFOR
        LEFT JOIN PERSONE ON PERSONE.ID = FORNITORI.IDPERSONA
        LEFT JOIN ARTICO ON ARTICO.ID = QUOART.IDARTICO
        WHERE ARTICO.CODICE = '{codice}' AND quoart.tipfor = 'P' AND ARTICO.STAART =  'G'
    """
    data = pd.read_sql(q, engine).fillna('')
    if len(data) > 0:
        return data['fornitore'][0]
    else:
        return []







@info_articolo.route('/find_codice/<codice>', methods=['GET', 'POST'])
def find_articolo(codice):
    try:
        x = get_info_artico(codice)
        if len(x) > 0:
            return x.to_json(orient='records')
        else:
            return {"msg": "errore"}      
    except:
            return []


@info_articolo.route('/find_data_magaz/<codice>', methods=['GET','POST'])
def find_d_m(codice):
    m = get_data_magaz(codice)
    if len(m) > 0:
        return m.to_json(orient='records')
    else:
        return {"msg":"errore"}

@info_articolo.route('/find_padre_figlio/<codice>', methods=['GET','POST'])
def find_p_f(codice):
    p_f = get_padre_figlio(codice)
    if len(p_f) > 0:
        return p_f.to_json(orient='records')
    else:
        return {"msg":"Non ci sono figli correlati"}

@info_articolo.route('/find_static_art/<codice>', methods=['GET','POST'])
def find_s_a(codice):
    try:
        s = get_statisitiche_art(codice)
        if len(s) > 0:
            return s.to_json(orient='records')
        else:
            return {"msg":"errore"}
    except:
        return []


@info_articolo.route('/find_prezzo_base/<codice>', methods=['GET','POST'])
def find_p_b(codice):

    p = price_fornitore(codice)
    n_f = get_nome_fornitore(codice)
    q = {'nome_fornitore' : n_f,'prezzo': p}
    return q

    
    



