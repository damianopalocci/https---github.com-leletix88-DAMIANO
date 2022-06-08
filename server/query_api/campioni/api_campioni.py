import numpy as np
from flask import Blueprint, render_template, abort, jsonify, request, current_app
import pandas as pd
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

api_campioni = Blueprint('api_campioni', __name__)


def get_articolo(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        q = {'_id': id}
        x = mycol.find(q)
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return{}


def get_allcampioni():
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return{}

def getsumtipo():
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        pipe = [{"$group": {"_id": "$tipo", "count": {"$sum": 1}}}]
        x = mycol.aggregate(pipeline=pipe)
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return{}


def addnew(data):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        x = mycol.insert_one(data)
        return {'msg': 200}
    except:
        return{'msg': 500}


def addnew_generic_nota(data):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_note_indagini"]
        x = mycol.insert_one(data)
        return {'msg': 200}
    except:
        return{'msg': 500}

def get_indagine(id):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_indagini"]
        q = {'relid': id}
        x = mycol.find(q)
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return{}

def add_indagine(data):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_indagini"]
        x = mycol.insert_one(data)
        return {'msg': 200}
    except:
         return{'msg': 500}


def get_preventivo(id):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_preventivi"]
        q = {'relid': id}
        x = mycol.find(q)
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return{}

def add_preventivo(data):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_preventivi"]
        x = mycol.insert_one(data)
        return {'msg': 200}
    except:
         return{'msg': 500}


def deleteoneid(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        q = {'_id': id}
        x = mycol.delete_one(q)
        return {'msg': 200}
    except:
        return{'msg': 500}


def deleteoneidcomment(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_note_indagini"]
        q = {'_id': id}
        x = mycol.delete_one(q)
        return {'msg': 200}
    except:
        return{'msg': 500}

def deleteoneid_article(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        q = {'_id': id}
        x = mycol.delete_one(q)
        return {'msg': 200}
    except:
        return{'msg': 500}


def deleteoneidnota_tech(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_note_indagini"]
        q = {'_id': id}
        x = mycol.delete_one(q)
        return {'msg': 200}
    except:
        return{'msg': 500}

def deleteoneidtot_nota(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_note_indagini"]
        q = {'_id': id}
        x = mycol.delete_one(q)
        return {'msg': 200}
    except:
        return{'msg': 500}


def deleteoneidpreventivo(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_preventivi"]
        q = {'_id': id}
        x = mycol.delete_one(q)
        return {'msg': 200}
    except:
        return{'msg': 500}

def deleteoneidindagine(id):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_indagini"]
        q = {'_id': id}
        x = mycol.delete_one(q)
        return {'msg': 200}
    except:
        return{'msg': 500}


def updateoneid(id, data):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        myquery = {"_id": id}
        newvalues = {"$set": data}
        x = mycol.update_one(myquery, newvalues)
        return {'msg': 200}
    except:
        return{'msg': 500}


def upstatus(id, nstato):
    try:
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        myquery = {"_id": id}
        newvalues = {"$set": {'stato': nstato}}
        x = mycol.update_one(myquery, newvalues)
        return {'msg': 200}
    except:
        return{'msg': 500}


def updateoneindagine(id, data):
    try:
        id = ObjectId(id)

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_indagini"]
        myquery = {"_id": id}
        newvalues = {"$set": data}
        x = mycol.update_one(myquery, newvalues)
        return {'msg': 200}
    except:
        return{'msg': 500}


def updateonepreventivo(id, data):
    try:
        id = ObjectId(id)

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_preventivi"]
        myquery = {"_id": id}
        newvalues = {"$set": data}
        x = mycol.update_one(myquery, newvalues)
        return {'msg': 200}
    except:
        return{'msg': 500}


def updateonenote(id, data):
    try:
        id = ObjectId(id)

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_note_indagini"]
        myquery = {"_id": id}
        newvalues = {"$set": data}
        x = mycol.update_one(myquery, newvalues)
        return {'msg': 200}
    except:
        return{'msg': 500}


def get_articolo_note(id):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_note_indagini"]
        q = {'relid': id}
        x = mycol.find(q)
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return{}

def getsumstato(tipo):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        pipe = [{'$match': {'tipo': tipo}},
                {"$group": {"_id": "$stato", "count": {"$sum": 1}}}]
        x = mycol.aggregate(pipeline=pipe)
        x = list(x)
        x = pd.DataFrame(x)
        ndb = []
        for i, r in x.iterrows():
            chk = str(r['_id'])
            if chk == 'Nuovo':
                r['prio'] = 0
            if chk == 'Acquisto Campione':
                r['prio'] = 1
            if chk == 'Verifica Campione':
                r['prio'] = 2
            if chk == 'Richiesta Fattibilità':
                r['prio'] = 3
            if chk == 'Attesa Quotazione':
                r['prio'] = 4
            if chk == 'Valutazione Preventivo':
                r['prio'] = 5
            if chk == 'Attesa Prototipo':
                r['prio'] = 6
            if chk == 'Verifica Tecnica Prototipo':
                r['prio'] = 7
            if chk == 'Produzione':
                r['prio'] = 8
            if chk == 'Standby':
                r['prio'] = 9
            if chk == 'Archiviato':
                r['prio'] = 10
            ndb.append(r)
        ndb = pd.DataFrame(ndb)
        return ndb.to_json(orient='records', default_handler=str)
    except:
        return{}


def gettipostato(tipo, stato):
    try:
        import pymongo
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        q = {'stato': stato, 'tipo': tipo}
        x = mycol.find(q)
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return {'msg': 'error'}


def add_cambio_stato(data):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        q = {'relid': id}
        mycol = mydb["db_action"]
        x = mycol.insert_one(data)
        return {'msg': 200}
    except:
         return{'msg': 500}


def get_change_stato(id):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_action"]
        q = {'id_articolo': id}
        x = mycol.find(q)
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return{}

# INIZIO API


@api_campioni.route('/getcampioni', methods=['GET'])
def getcampioni():
    try:
        import pymongo
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        x = mycol.find()
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return {'msg': 'error'}


@api_campioni.route('/getcampioni/<tipo>', methods=['GET'])
def getcampioni_tipo(tipo):
    try:
        import pymongo
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Micromic"]
        mycol = mydb["db_campioni"]
        q = {'tipo': tipo}
        x = mycol.find(q)
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records', default_handler=str)
    except:
        return {'msg': 'error'}


@api_campioni.route('/getcampioni/getsum', methods=['GET'])
def getcampioni_getsum_tipo():
    try:
        x = getsumtipo()
        return x
    except:
        return {'msg': 'error'}


@api_campioni.route('/getcampioni/getsum/<tipo>', methods=['GET'])
def getcampioni_getsum_stato(tipo):
    try:
        x = getsumstato(tipo)
        return x
    except:
        return {'msg': 'error'}


@api_campioni.route('/getcampioni/<tipo>/<stato>', methods=['GET'])
def get_tipostato(tipo, stato):
    try:
        x = gettipostato(tipo, stato)
        return x
    except:
        return {'msg': 'error'}


@api_campioni.route('/getcampioni/campioni_tot/', methods=['GET'])
def get_all_campioni():
    try:
       
        x = get_allcampioni()
        return x
    except:
        return {'msg': 'error'}


@api_campioni.route('/getcampioni/articolo/<id>', methods=['GET'])
def getarticoloid(id):
    try:
        x = get_articolo(id)
        return x
    except:
        return {'msg': 'error'}


@api_campioni.route('/getcampioni/articolo/note/<id>', methods=['GET'])
def get_note_campioni(id):
    try:
        x = get_articolo_note(id)
        return x
    except:
        return {'msg': 'error'}


@api_campioni.route('/newcampione', methods=['POST'])
def newcampione():
    try:
        data = request.json

        x = addnew(data)
        return x
    except:
        return {'msg': 'error'}


@api_campioni.route('/delete/<id>', methods=['GET'])
def delid(id):
    x = deleteoneid(id)
    return x


@api_campioni.route('/deletecomment/<id>', methods=['GET'])
def deletecm(id):
    x = deleteoneidcomment(id)
    return x

@api_campioni.route('/delete_articolo_tot/<id>', methods=['GET'])
def deletearti(id):
    x = deleteoneid_article(id)
    return x

@api_campioni.route('/delete_note_tech/<id>', methods=['GET'])
def deleteth(id):
    x = deleteoneidnota_tech(id)
    return x

@api_campioni.route('/delete_tot_nota/<id>', methods=['GET'])
def deletetotnota(id):
    x = deleteoneidtotnota(id)
    return x

@api_campioni.route('/deletepreventivo/<id>', methods=['GET'])
def deletepr(id):
    x = deleteoneidpreventivo(id)
    return x

@api_campioni.route('/deleteindagine/<id>', methods=['GET'])
def deleteinda(id):
    x = deleteoneidindagine(id)
    return x


@api_campioni.route('/update/<id>', methods=['POST'])
def uponeid(id):
    data = request.json
    x = updateoneid(id, data)
    return x

@api_campioni.route('/updatestatus/<id>', methods=['POST'])
def updatestatus(id):
    data = request.json
    data = data['stato']
    x = upstatus(id, data)
    return x

@api_campioni.route('/update_indagine/<id>', methods=['POST'])
def uponeindagine(id):
    data = request.json
    del data['_id']
    x = updateoneindagine(id, data)
    return x

@api_campioni.route('/update_note/<id>', methods=['POST'])
def uponenote(id):
    data = request.json
    del data['_id']
    x = updateonenote(id, data)
    return x


@api_campioni.route('/update_preventivo/<id>', methods=['POST'])
def uponepreventivo(id):
    data = request.json
    del data['_id']
    x = updateonepreventivo(id, data)
    return x


@api_campioni.route('/addnewnotagenerica', methods=['POST'])
def addnewnotagenerica():
    data = request.json
    x = addnew_generic_nota(data)
    return x

@api_campioni.route('/getcampioni/articolo/indagine/<id>', methods=['GET'])
def get_indagini(id):
    try:
        x = get_indagine(id)
        return x
    except:
        return {'msg': 'error'}

@api_campioni.route('/add_indagine', methods=['POST'])
def add_indag():
    data = request.json
    now = datetime.now()
    data['data_inserimento'] = now.strftime("%d/%m/%Y %H:%M:%S")
    x = add_indagine(data)
    return x

@api_campioni.route('/getcampioni/articolo/preventivo/<id>', methods=['GET'])
def get_prevent(id):
    try:
        x = get_preventivo(id)
        return x
    except:
        return {'msg': 'error'}

@api_campioni.route('/getcampioni/articolo/change_stato/<id>', methods=['GET'])
def get_chan_stato(id):
    try:
        x = get_change_stato(id)
        return x
    except:
        return {'msg': 'error'}


@api_campioni.route('/add_preventivo', methods=['POST'])
def add_preventiv():
    data = request.json
    x = add_preventivo(data)
    return x


@api_campioni.route('/add_action_stato', methods=['POST'])
def add_change_stato():
    data = request.json
    x = add_cambio_stato(data)
    return x