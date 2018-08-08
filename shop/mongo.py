from pymongo import MongoClient



class db_helper():

    db = None

    def __init__(self):
        client = MongoClient("localhost")
        self.db = client.digikala

    def insert_one(self,collection,data):
        id = self.db[collection].insert_one(data)
        return id.inserted_id