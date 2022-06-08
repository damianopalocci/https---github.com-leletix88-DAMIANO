import pandas as pd
import pyodbc
import numpy as np
import pymongo
from flask import Blueprint, render_template, abort, request
import json
from sqlalchemy.engine import URL, create_engine
from bson.objectid import ObjectId

lavorazione = Blueprint('lavorazione', __name__)



def find_codice(codice):
    connection_string = 'DSN=query;Description=Database Pivot SAM-s3;UID=SA;PWD=1Password1;APP=Microsoft® Query;WSID=BERLINO;DATABASE=SAMA1;LANGUAGE=us_english;Network=DBMSLPCN'
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    q = f""" 
    SELECT LTRIM(RTRIM(ARTICO.CODICE)) AS articolo,  LTRIM(RTRIM(GST.codori)) AS codice_ori,   LTRIM(RTRIM(MARCHE.DESCR)) as marca, 
    LTRIM(RTRIM(ARTICO.DESCR)) AS descrizione,
    (SELECT TOP 1 SAMA1_PORTALS.dbo.vw_portal_ImgAttGen.FILENAME 
    FROM SAMA1_PORTALS.dbo.vw_portal_ImgAttGen
    left join SAMA1.dbo.ARTICO as art on art.id = SAMA1_PORTALS.dbo.vw_portal_ImgAttGen.IDARTICO
    WHERE art.CODICE=ARTICO.CODICE  AND CODICEAPP ='ECOM' AND  TIPO='D') as immagine
    FROM ARTICO
    left outer JOIN SAM.articoGST AS GST ON GST.idartico = ARTICO.ID
    left outer JOIN CATOMO AS CATEGORY ON CATEGORY.ID = ARTICO.IDCATOMO
    left outer JOIN MARCHE ON MARCHE.ID = ARTICO.IDMARCHE
    WHERE ARTICO.CODICE = '{codice}'
    """
    data = pd.read_sql(q, engine).fillna('')
    return data

def get_lista_code():
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["officina_lavorazioni"]
        x = mycol.find()
        x = list(x)
        x = pd.DataFrame(x)
        return x
    except:
        return {'msg': 'errore'}


def add_code(data):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["officina_lavorazioni"]
        x = mycol.insert_one(data)
        return {'msg': 200}
    except:
         return{'msg': 500}


def deleteone_code(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["officina_lavorazioni"]
        q = {'_id': id}
        x = mycol.delete_one(q)
        return {'msg': 200}
    except:
        return{'msg': 500}

def updateonecode(id, data):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["officina_lavorazioni"]
        myquery = {"_id": id}
        newvalues = {"$set": data}
        x = mycol.update_one(myquery, newvalues)
        return {'msg': 200}
    except:
        return{'msg': 500}


def get_code(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["officina_lavorazioni"]   
        q = {'_id': id}
        x = mycol.find(q)
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return{}


@lavorazione.route('/find_all_code', methods=['GET','POST'])
def find_code():
    try:
        code = get_lista_code()
        if len(code) > 0:
            return code.to_json(orient='records', default_handler=str)
        else:
            return {}
    except:
        return("Errore")


@lavorazione.route('/find_codice/<codice>', methods=['GET', 'POST'])
def find_c(codice):
    try:
        x = find_codice(codice)
        if len(x) > 0:
            return x.to_json(orient='records')
        else:
            return {"msg": "errore"}      
    except:
            return []


@lavorazione.route('/add_code', methods=['POST'])
def add_c():
    data = request.json
    x = add_code(data)
    return x


@lavorazione.route('/delete_one_code/<id>', methods=['GET'])
def delete_art(id):
    x = deleteone_code(id)
    return x


@lavorazione.route('/update_one_code/<id>', methods=['POST'])
def up_one_code(id):
    data = request.json
    del data['_id']
    x = updateonecode(id, data)
    return x
   


@lavorazione.route('/get_codice/<id>', methods=['GET'])
def get_c(id):
    try:
        x = get_code(id)
        return x
    except:
        return []


