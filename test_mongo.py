
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://priyanka_db_user:echo2025@userinfo.bzjqkz1.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)