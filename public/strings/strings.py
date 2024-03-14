from flask import *
from pymongo import MongoClient
import string

class DB_Details():    
    HOST = '127.0.0.1'
    USER = 'root'
    PASSWORD = 'Pavan@9133'
    DB = 'practice'


client = MongoClient('mongodb://localhost:27017/')

db = client.practice

services = db.services
subservices = db.sub_services
customer = db.customer