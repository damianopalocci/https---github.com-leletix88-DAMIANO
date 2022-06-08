import pandas as pd
import time
import pyodbc
import telepot

from sqlalchemy.engine import URL, create_engine
bot = telepot.Bot('5167065973:AAHfDG_qyMBRNQR-r_EuK2q1E9u5GEMnSm4')


def bot_message(cliente, stato):
    msg = '📦 STATO ORDINE/MAGAZZINO 📦\n\n'
    msg += f'🧑🏻 CLIENTE 🧑🏻\n'
    msg += f'{cliente}\n\n'
    msg += f'🖖🏻 STATO 🖖🏻\n'
    msg += f'{stato}\n'
    msg += '\n'
    bot.sendMessage(-627048914, msg)


def chk_if_exist(ordine):
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f"""
                select COUNT(FATRIG.IDFAT) as count
                from FATRIG 
                left join COMRIG on COMRIG.ID = FATRIG.IDCOMRIG
                left join COMTES on COMTES.ID = COMRIG.IDCOMTES
                where COMTES.ID ={ordine}
                    """
        data = pd.read_sql(q, engine).fillna('')
        value = int(data['count'][0])
        return value
    except:
        return 0


def all_to_fix_order():
    try:
        connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
        q = f"""
         select SAM.COMTESGST.IDMASTER AS ID,SAM.COMTESGST .mag_status AS STATO ,
		PERSONE.DESCR1 AS CLIENTE ,
		COMTES.NUMDOC ,pp.DESCR1 as agente , COMTES.STATO as stacomtes
      from SAM.COMTESGST 
      left join COMTES on COMTES.id = sam.COMTESGST.idmaster
      left join CLIENTI on CLIENTI.ID = COMTES.IDCLIENTE
      LEFT JOIN PERSONE ON PERSONE.ID = CLIENTI.IDPERSONA
	  left join AGENTI on agenti.id= CLIENTI.IDAGENTE
	  left join persone as pp on pp.id = agenti.IDPERSONA
      where SAM.COMTESGST .mag_status <>3 
            """
        data = pd.read_sql(q, engine).fillna('')
        if len(data) > 0:
            data['CLIENTE'] = data['CLIENTE'].str.strip()
            data['agente'] = data['agente'].str.strip()
            return data
        else:
            print("Non esistono elementi")
            return False
    except:
        print("Errore Generare esecuzione")
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


def update_status(id, stato):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    cursor = engine.cursor()
    q = f""" 
        UPDATE SAM.COMTESGST
        SET mag_status = '{stato}'
        where sam.comtesgst.idmaster = {id}
        """
    cursor.execute(q)
    engine.commit()
    print('modificato')
    return '200'


def main():
    try:
        data = all_to_fix_order()
        if False in data:
            pass
        else:
            for i, r in data.iterrows():
                _ordine = r['ID']
                x = chk_if_exist(_ordine)
                x = int(x)
                if x != 0:
                    try:
                        update_status(_ordine, 3)
                        bot_message(r['CLIENTE'], 'Spedito')
                    except:
                        print("errore")
                if r['stacomtes'] == 'E':
                    print(r['stacomtes'])
                    try:
                        update_status(_ordine, 3)
                        bot_message(r['CLIENTE'], 'Spedito')
                    except:
                        print("errore")

            return {'msg': 'ok'}
    except:
        return {'msg': 'error'}
