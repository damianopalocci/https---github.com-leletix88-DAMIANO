
from flask import Blueprint, render_template, abort, request
import pymongo
import pyodbc
import pandas as pd

api_dash_agente = Blueprint('api_dash_agente', __name__)


# PREFIX /api_agenti

class Agenti:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["Portals"]
        self.mycol = self.mydb["fulldb"]
    def get_db(id):
        try:
            x = Agenti().mycol.find({'IDAGENTE': id})
            frame = pd.DataFrame(list(x))
            Agenti().myclient.close()
            return frame
        except:
            return {}

    def get_db_vending(id):
        try:
            x = Agenti().mycol.find({"IDAGENTE": id, "isVending": -1})
            frame = pd.DataFrame(list(x))
            Agenti().myclient.close()
            return frame
        except:
            return {}

    def get_db_tradizionale(id):
        try:
            x = Agenti().mycol.find({"IDAGENTE": id, "isVending": 0})
            frame = pd.DataFrame(list(x))
            Agenti().myclient.close()
            return frame
        except:
            return {}

    def get_db_mesi(id):
        try:
            from datetime import datetime
            mnow = datetime.now().month
            x = Agenti().mycol.find({'IDAGENTE': id, 'MESE': mnow})
            frame = pd.DataFrame(list(x))
            Agenti().myclient.close()
            return frame
        except:
            return {}

    def get_db_mesi_s(id, mm):
        try:
            x = Agenti().mycol.find({'IDAGENTE': id, 'MESE': mm})
            frame = pd.DataFrame(list(x))
            Agenti().myclient.close()
            return frame
        except:
            return {}

    def elaborate(db, elemento, tipo):
        try:
            from datetime import date
            ynow = date.today().year
            mnow = date.today().month
            ym1 = date.today().year - 1
            ym2 = date.today().year - 2
            ndb = db.groupby([f'{elemento}', 'ANNO'])[
                f'{tipo}'].sum().reset_index()
            ndb = pd.pivot_table(ndb, values=f'{tipo}', index=[
                f'{elemento}'], columns='ANNO').reset_index()
            ndb = pd.DataFrame(ndb.to_records())
            ndb = ndb.fillna(0)
            if not str(ynow) in ndb.columns:
                ndb[str(ynow)] = 0
            if not str(ynow-1) in ndb.columns:
                ndb[str(ynow-1)] = 0
            if not str(ynow-2) in ndb.columns:
                ndb[str(ynow-2)] = 0
            ndb['difference'] = ndb[str(ynow)] - ndb[str(ynow-1)]
            ndb[f'{elemento}'] = ndb[f'{elemento}'].str.strip()
            ndb = ndb.sort_values(by=['difference'])
            return ndb.drop(columns=['index'])
        except:
            return {}


def get_agent_sum(q):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Portals"]
        mycol = mydb["fulldb"]
        pipe = [{"$match": q}, {"$group": {
            "_id": "$ANNO", "sum": {"$sum": "$IMPNETTO"}}}]
        x = mycol.aggregate(pipeline=pipe)
        x = list(x)
        x = pd.DataFrame(x)
        return x.to_json(orient='records')
    except:
        return{}


@api_dash_agente.route('anno/<id>/<tipo>/<valore>')
def retur_stat_anno(id, tipo, valore):
    try:
        id = int(id)
        tipo = str(tipo)
        valore = str(valore)
        db = Agenti.get_db(id)
        pivotdb = Agenti.elaborate(db, f'{tipo}', f'{valore}')
        return pivotdb.to_json(orient='records')
    except:
        return {}


@api_dash_agente.route('sumquery', methods=['GET', 'POST'])
def sumquery():
    try:
        if request.method == 'POST':
            data = request.json
            x = get_agent_sum(data)
            return x
    except:
        return {}


@api_dash_agente.route('mese/<id>/<tipo>/<valore>')
def retur_stat_mese(id, tipo, valore):
    try:
        id = int(id)
        tipo = str(tipo)
        valore = str(valore)
        db = Agenti.get_db_mesi(id)
        pivotdb = Agenti.elaborate(db, f'{tipo}', f'{valore}')
        return pivotdb.to_json(orient='records')
    except:
        return {}


@api_dash_agente.route('<mese>/<id>/<tipo>/<valore>')
def retur_stat_meses(mese, id, tipo, valore):
    try:
        id = int(id)
        tipo = str(tipo)
        valore = str(valore)
        mese = int(mese)
        db = Agenti.get_db_mesi_s(id, mese)
        pivotdb = Agenti.elaborate(db, f'{tipo}', f'{valore}')
        return pivotdb.to_json(orient='records')
    except:
        return {}


@api_dash_agente.route('vending/<id>/<tipo>/<valore>')
def retur_db_vending(id, tipo, valore):
    try:
        id = int(id)
        tipo = str(tipo)
        valore = str(valore)
        db = Agenti.get_db_vending(id)
        pivotdb = Agenti.elaborate(db, f'{tipo}', f'{valore}')
        return pivotdb.to_json(orient='records', default_handler=str)
    except:
        return {}


@api_dash_agente.route('tradizionale/<id>/<tipo>/<valore>')
def retur_db_tradizionale(id, tipo, valore):
    try:
        id = int(id)
        tipo = str(tipo)
        valore = str(valore)
        db = Agenti.get_db_tradizionale(id)
        pivotdb = Agenti.elaborate(db, f'{tipo}', f'{valore}')
        return pivotdb.to_json(orient='records', default_handler=str)
    except:
        return {}
