import pandas as pd
import pyodbc
import numpy as np
from flask import Blueprint, render_template, abort, request
import json
from sqlalchemy.engine import URL, create_engine

api_gen_kit = Blueprint('api_gen_kit', __name__)


def find_subkit(kitlist):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f""" 
    select ARTICO.CODICE , r.QTIMCO  as qta
    from VARDB v
    inner join ridiba r on r.IDVARDB=v.ID
    inner join ARTICO on ARTICO.ID = r.IDARTICO
    inner join ARTICO aa on aa.ID = v.IDARTICO
    where aa.CODICE  = '{kitlist}'
    """
    data = pd.read_sql(q, engine).fillna(0)
    data['CODICE'] = data['CODICE'].str.strip()
    return data


def find_kit():
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f""" 
    
    select DISTINCT ( ARTICO.CODICE)
    from VARDB
    left join ARTICO on ARTICO.ID = VARDB.IDARTICO
    WHERE ARTICO.STAART='G'

    """
    data = pd.read_sql(q, engine).fillna(0)
    data['CODICE'] = data['CODICE'].str.strip()
    return data


def get_real_qta(codice):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f""" 
    
    select SUM(giamag.QTTGIAI) as tot
    from SAMA1.dbo.GIAMAG as giamag
    LEFT OUTER JOIN SAMA1.dbo.AllMag AS alm  On giamag.IDMAG = alm.id 
    LEFT OUTER JOIN SAMA1.dbo.AnaMag AS anm  ON alm.idanamag = anm.id    -- VANO
    left OUTER JOIN LOTSER ON LOTSER.ID = giamag.IDARTICO
    left OUTER JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO    
    WHERE  (IDANAMAG = 61 or IDANAMAG = 58) and ARTICO.CODICE='{codice}'

    """
    data = pd.read_sql(q, engine).fillna(0)
    return data


def get_artico_info(codice):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f""" 

    select TOP 1 QTTORDI ,IMMAGINE, NAZIONI.DESCR AS P_ORIGINE, NETTO
    from ARTICO
    LEFT JOIN NAZIONI ON NAZIONI.ID = ARTICO.IDPAESOR
    WHERE ARTICO.CODICE ='{codice}'

    """
    data = pd.read_sql(q, engine).fillna('')
    return data


def get_me_fornitore(codice):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f""" 

    SELECT ARTICO.CODICE , PERSONE.DESCR1 as fornitore
    FROM QUOART
    LEFT JOIN LISFOR ON LISFOR.ID = QUOART.IDLISFOR
    LEFT JOIN FORNITORI ON FORNITORI.ID = LISFOR.IDFOR
    LEFT JOIN PERSONE ON PERSONE.ID = FORNITORI.IDPERSONA
    LEFT JOIN ARTICO ON ARTICO.ID = QUOART.IDARTICO
    where quoart.tipfor = 'P' AND ARTICO.CODICE = '{codice}'

    """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data) > 0:
        data = data['fornitore'][0]
    else:
        data = ''

    return data


def get_me_price(codice):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f""" 
    select TOP 1 PREZZO
    from LISRIG
    LEFT JOIN LOTSER ON LOTSER.ID = LISRIG.IDARTICO
    LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
    WHERE LOTSER.NUMLOT = '00000000000' and ARTICO.CODICE ='{codice}' AND LISRIG.IDLISTES =2618

    """
    data = pd.read_sql(q, engine).fillna(0)
    if len(data) > 0:
        data = data['PREZZO'][0]
    else:
        data = ''

    return data


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


@api_gen_kit.route('/getkit', methods=['POST', 'GET'])
def getkit():
    data = find_kit()
    codici = data['CODICE'].unique().tolist()
    return json.dumps(codici)


@api_gen_kit.route('/calculatekit', methods=['POST'])
def calculatekit():
    data = request.json
    data = pd.DataFrame(data)
    data = data.astype({"qta": int})
    finaldb = []
    for i, r in data.iterrows():
        subkit = find_subkit(r.kit)
        subkit.qta = subkit.qta * r.qta
        for ii, rr in subkit.iterrows():
            q = {'articolo': rr.CODICE, 'qta': rr.qta}
            finaldb.append(q)
    finaldb = pd.DataFrame(finaldb)
    appdb = finaldb
    finaldb = finaldb.groupby(['articolo']).sum().reset_index()
    enddb = []
    for ii, rr in finaldb.iterrows():
        qtareal = get_real_qta(rr.articolo)
        info = get_artico_info(rr.articolo)
        fornitore = get_me_fornitore(rr.articolo)
        vprice = get_me_price(rr.articolo)
        immagine = get_img(rr.articolo)

        q = {'articolo': rr.articolo, 'qta': rr.qta, 'rgia': int(
            qtareal.tot[0]), 'img': immagine, 'ordinati': info.QTTORDI[0], 'fornitore': fornitore.strip(), 'vprice': vprice ,'p_origine':info.P_ORIGINE[0], 'peso': info.NETTO[0]}
        enddb.append(q)
    enddb = pd.DataFrame(enddb)
    enddb['reo'] = enddb['rgia'] + enddb['ordinati']
    enddb['reo'] = enddb['reo'] - enddb['qta']
    return enddb.to_json(orient='records')
