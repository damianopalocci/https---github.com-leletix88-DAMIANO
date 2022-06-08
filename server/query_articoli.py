import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps

class Articoli:
    def __init__(self, codice, loro_codice, descrizione):
        self.codice = codice
        self.loro_codice = loro_codice
        self.descrizione = descrizione

    def find_by_id(id):
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Monitoring"]
        mycol = mydb["articoli"]
        x = mycol.find_one({'_id':id})    
        return dumps(x)       

    def getall():
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Monitoring"]
        mycol = mydb["articoli"]
        x = mycol.find({})    
        return dumps(x)
        
    def insert_new(data):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Monitoring"]
        mycol = mydb["articoli"]
        x = mycol.insert_one(data)
        return x  

    def delete_articolo(id):
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Monitoring"]
        mycol = mydb["articoli"]
        x = mycol.delete_one({'_id':id})
        return x   

    def update_articolo(id, data):
        del data['_id']
        id = ObjectId(id)
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Monitoring"]
        mycol = mydb["articoli"]
        myquery = {'_id':id} 
        newvalues = { "$set": data }
        x = mycol.update_one(myquery,newvalues)
        return x   

