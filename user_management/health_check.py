from pymongo import MongoClient
from pymongo.errors import  ServerSelectionTimeoutError

def check_mongo_connection():
    try:
        # Connect to MongoDB server
        client = MongoClient('mongodb://Admin1:Zaamo%401234@4.224.241.87:18210', serverSelectionTimeoutMS=5000)  # Adjust URI

        # Check the server info to verify connection
        client.server_info()  # If the server cannot be reached, this will raise an exception
        
        print("Connected to MongoDB successfully!")

        db = client['users']
        
        # Check if 'users' collection exists
        collections = db.list_collection_names()
        if 'users' in collections:
            print("Connected to MongoDB successfully and 'users' collection exists!")
        else:
            print("Connected to MongoDB, but 'users' collection does not exist.")




    except ServerSelectionTimeoutError as e:
        print(f"Error: Could not connect to MongoDB (timeout) - {e}")
    

if __name__ == "__main__":
    check_mongo_connection()
