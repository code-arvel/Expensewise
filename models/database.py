from pymongo import MongoClient


client = MongoClient(
    "mongodb+srv://marvel12:Marvelous2468@cluster0.ah9zmm6.mongodb.net/?appName=Cluster0"
)

db = client['expensewise_db']

users_collection = db['users']
expenses_collection = db['expenses']
budgets_collection = db['budgets']