import pandas as pd
import pyodbc
from sqlalchemy.engine import URL
from sqlalchemy import create_engine



def get_titolo(listino):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q= f""" 
    select DESCR
    from LISTES
    where ID = {listino}
                    """
    data = pd.read_sql(q,engine)
    return(data['DESCR'][0])
def analizza_codice(codice):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q= f""" 
    select ARTICO.CODICE AS codice , LISRIG.QTA , LISRIG.PREZZO
    from LISRIG
    LEFT JOIN LOTSER ON LOTSER.ID = LISRIG.IDARTICO
    LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
    where IDLISTES = {nlistino} AND ARTICO.CODICE ='{codice}'
                    """
    data = pd.read_sql(q,engine)
    return(data)
def listino_cinque(db):
    mycode = {'codice':codice}
    for i,r in appdb.iterrows():       
        if i == 0 :
            prezzo = float(r.PREZZO) *2.5
            mycode['listino'] = prezzo
        if i == 1:
            prezzo = r.PREZZO 
            mycode['Sconto 60'] = prezzo
            mycode['Qta 1'] = int(r.QTA+1)
        if i == 2:
            prezzo = r.PREZZO 
            mycode['Prezzo 1'] = prezzo
            mycode['Qta 2'] = int(r.QTA+1)
        if i == 3:
            prezzo = r.PREZZO 
            mycode['Prezzo 2'] = prezzo
            mycode['Qta 3'] = int(r.QTA+1)
        if i == 4:
            prezzo = r.PREZZO 
            mycode['Prezzo 3'] = prezzo
            mycode['Qta 4'] = int(r.QTA+1)
        if i == 5:
            prezzo = r.PREZZO 
            mycode['Prezzo 4'] = prezzo
            mycode['Qta 5'] = int(r.QTA+1)
        if i == 6:
            prezzo = r.PREZZO 
            mycode['Prezzo 5'] = prezzo
    return mycode
def listino_quattro(db):
    mycode = {'codice':codice}
    for i,r in appdb.iterrows():
       
        if i == 0 :
            prezzo = float(r.PREZZO) *2.5
            mycode['listino'] = prezzo
        if i == 1:
            prezzo = r.PREZZO 
            mycode['Sconto 60'] = prezzo
            mycode['Qta 1'] = int(r.QTA+1)
        if i == 2:
            prezzo = r.PREZZO 
            mycode['Prezzo 1'] = prezzo
            mycode['Qta 2'] = int(r.QTA+1)
        if i == 3:
            prezzo = r.PREZZO 
            mycode['Prezzo 2'] = prezzo
            mycode['Qta 3'] = int(r.QTA+1)
        if i == 4:
            prezzo = r.PREZZO 
            mycode['Prezzo 3'] = prezzo
            mycode['Qta 4'] = int(r.QTA+1)
        if i == 5:
            prezzo = r.PREZZO 
            mycode['Prezzo 4'] = prezzo
    return mycode
def listino_tre(db):
    mycode = {'codice':codice}
    for i,r in appdb.iterrows():
       
        if i == 0 :
            prezzo = float(r.PREZZO) *2.5
            mycode['listino'] = prezzo
        if i == 1:
            prezzo = r.PREZZO 
            mycode['Sconto 60'] = prezzo
            mycode['Qta 1'] = int(r.QTA+1)
        if i == 2:
            prezzo = r.PREZZO 
            mycode['Prezzo 1'] = prezzo
            mycode['Qta 2'] = int(r.QTA+1)
        if i == 3:
            prezzo = r.PREZZO 
            mycode['Prezzo 2'] = prezzo
            mycode['Qta 3'] = int(r.QTA+1)
        if i == 4:
            prezzo = r.PREZZO 
            mycode['Prezzo 3'] = prezzo
       
    return mycode
def listino_due(db):
    mycode = {'codice':codice}
    for i,r in appdb.iterrows():
       
        if i == 0 :
            prezzo = float(r.PREZZO) *2.5
            mycode['listino'] = prezzo
        if i == 1:
            prezzo = r.PREZZO 
            mycode['Sconto 60'] = prezzo
            mycode['Qta 1'] = int(r.QTA+1)
        if i == 2:
            prezzo = r.PREZZO 
            mycode['Prezzo 1'] = prezzo
            mycode['Qta 2'] = int(r.QTA+1)
        if i == 3:
            prezzo = r.PREZZO 
            mycode['Prezzo 2'] = prezzo
       
    return mycode
def listino_uno(db):
    mycode = {'codice':codice}
    for i,r in appdb.iterrows():
       
        if i == 0 :
            prezzo = float(r.PREZZO)*2.5
            mycode['listino'] = prezzo
        if i == 1:
            prezzo = r.PREZZO 
            mycode['Sconto 60'] = prezzo
            mycode['Qta 1'] = int(r.QTA+1)
        if i == 2:
            prezzo = r.PREZZO 
            mycode['Prezzo 1'] = prezzo       

    return mycode
def listino_base(db):
    mycode = {'codice':codice}
    for i,r in appdb.iterrows():
        if i == 0 :
            prezzo = float(r.PREZZO) *2.5
            mycode['listino'] = prezzo
        if i == 1:
            prezzo = r.PREZZO 
            mycode['Sconto 60'] = prezzo   

    return mycode
def listino_zero(db):
    mycode = {'codice':codice}
    for i,r in appdb.iterrows():
        if i == 0 :
            prezzo = float(r.PREZZO) *2.5
            mycode['listino'] = prezzo
            prezzo = r.PREZZO 
            mycode['Sconto 60'] = prezzo   

    return mycode







def list_to_json(idlistino):
    try:
        global nlistino,appdb,d1,codice
        nlistino = idlistino
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q= f""" 
        select ARTICO.CODICE AS codice , LISRIG.QTA , LISRIG.PREZZO ,LISRIG.IDARTICO as idlotser
        from LISRIG
        LEFT JOIN LOTSER ON LOTSER.ID = LISRIG.IDARTICO
        LEFT JOIN ARTICO ON ARTICO.ID = LOTSER.IDARTICO
        where IDLISTES = {nlistino}
                        """
        data = pd.read_sql(q,engine)
        data.codice = data.codice.str.strip()
        unique_cod = data.codice.str.strip().unique()
        newdb =[]
        for codice in unique_cod:
            appdb = analizza_codice(codice)
            lentype = len(appdb)    
            if lentype ==7:
                newdb.append(listino_cinque(appdb))    
            if lentype ==6:
                newdb.append(listino_quattro(appdb))    
            if lentype ==5:
                newdb.append(listino_tre(appdb))
            if lentype ==4:
                newdb.append(listino_due(appdb))
            if lentype ==3:
                newdb.append(listino_uno(appdb))
            if lentype ==2:
                newdb.append(listino_base(appdb))
            if lentype ==1:
                newdb.append(listino_zero(appdb))
        titolo = get_titolo(nlistino).strip()
        newdb = pd.DataFrame(newdb).fillna('')
        return newdb
    except:
        return []

