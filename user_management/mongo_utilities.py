from pymongo import MongoClient
from user_management.settings import MONGO_CLIENT

class MongoConn:

    client = None
    db = None

    def get_mongo_client(self):
        
        if self.client is None:
            self.client = MongoClient(MONGO_CLIENT.get('url'))
            self.db = self.client[MONGO_CLIENT.get('db')]
        
        return self.db

    def close_connection(self):

        if self.client:
            self.client.close()
            self.client = None
            self.db = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()
    
    def insert_data(self, post, collection_name):
        
        try:
            db = self.get_mongo_client()
            result = db.collection[collection_name].insert_one(post)

            return result.acknowledged
        
        except Exception as e:
            print(str(e))

    def fetch_data(self, get, collection_name, timeout_off = False):
        db = self.get_mongo_client()
        
        if not timeout_off:
            results = db.collection[collection_name].find(get)
        
        else:
            results = db.collection[collection_name].find(get,no_cursor_timeout=True)
        
        return results
    
    def fetch_one(self, filter, collection_name, **kwargs):
        db = self.get_mongo_client()
        result = db.collection[collection_name].find_one(filter, **kwargs)

        return result
        
    def update_data(self, filter_query, update_query, collection_name, upsert=False):
        db = self.get_mongo_client()
        results = db.collection[collection_name].update_one(filter_query, update_query, upsert=upsert)
        
        return results

    def delete_data(self, query, collection_name):
        db = self.get_mongo_client()
        result = db.collection[collection_name].delete_one(query)  
        
        return result.deleted_count > 0