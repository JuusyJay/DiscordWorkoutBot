import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv('MONGODB_URI')

client = pymongo.MongoClient(URI)
db = client['workoutDB']
collection = db['user_accounts']