from flask import Blueprint, render_template, abort, request
import codecs
import jinja2
import pyodbc
import pandas as pd
import pymongo
from bson.objectid import ObjectId

from smtplib import SMTP

from sqlalchemy.engine import URL, create_engine



utenti = Blueprint('utenti', __name__)

def get_lista_utenti():
    try:
        import pymongo
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["db_login"]
        x = mycol.find()
        x = list(x)
        x = pd.DataFrame(x)
        return x
    except:
        return {'msg': 'errore'}


def deleteone_user(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["db_login"]
        q = {'_id': id}
        x = mycol.delete_one(q)
        return {'msg': 200}
    except:
        return{'msg': 500}


def updateoneuser(id, data):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["db_login"]
        myquery = {"_id": id}
        newvalues = {"$set": data}
        x = mycol.update_one(myquery, newvalues)
        return {'msg': 200}
    except:
        return{'msg': 500}


def add_user(data):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["db_login"]
        x = mycol.insert_one(data)
        return {'msg': 200}
    except:
         return{'msg': 500}



@utenti.route('/find_all_user', methods=['GET','POST'])
def find_user():
    try:
        user = get_lista_utenti()
        if len(user) > 0:
            return user.to_json(orient='records', default_handler=str)
        else:
            return {}
    except:
        return("Errore")


@utenti.route('/delete_one_user/<id>', methods=['GET'])
def delete_u(id):
    x = deleteone_user(id)
    return x


@utenti.route('/update_one_user/<id>', methods=['POST'])
def up_one_u(id):
    data = request.json
    del data['_id']
    x = updateoneuser(id, data)
    return x


@utenti.route('/add_user', methods=['POST'])
def add_u():
    data = request.json
    x = add_user(data)
    return x