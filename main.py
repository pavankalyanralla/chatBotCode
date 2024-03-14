from flask import Flask, jsonify
from flask import *
from datetime import datetime,timedelta
from flask_cors import CORS, cross_origin
from flask_restful import Api
import sys
#from src.server.login.login import *
import requests
import urllib.request
import logging
from flask_restful import Resource, reqparse
from src.server.errors.errors import errors
from database.dB_Connect import mysql
from public.strings.strings import *
from src.server.TLChatBot.projectEnquiry import *
from src.server.suggessionForm.userFormAndSuggestion import *
from public.logRecordings.logRecordings import LogRecordings

app = Flask(__name__)

# object for restful plugin
poc = Api(app,errors=errors)


# configurations for dB connections
app.config['MYSQL_DATABASE_HOST'] = DB_Details.HOST
app.config['MYSQL_DATABASE_USER'] =  DB_Details.USER
app.config['MYSQL_DATABASE_PASSWORD'] = DB_Details.PASSWORD
app.config['MYSQL_DATABASE_DB'] =  DB_Details.DB


CORS(app)
# Add URL's and function to call

poc.add_resource(addUserFormAndSuggestion,'/api/enquiryFormData')
poc.add_resource(synopsisFromUploadedFile,'/api/enquiryResult')

# TL chatbot
poc.add_resource(ProjectEnquiry,'/chatBot/projectEnquiry')
poc.add_resource(SummaryOnRequirements,'/chatBot/summaryOnRequirements')
poc.add_resource(SendProjectEnquiryEmail,'/chatBot/sendProjectEnquiryEmail')
poc.add_resource(SendCareerEnquiryEmail,'/chatBot/sendCareerEnquiryEmail')
poc.add_resource(SendOthersEmail,'/chatBot/sendOthersEmail')


mysql.init_app(app)

if __name__ == '__main__':
    # mysql.init_app(app)
    app.run(host='0.0.0.0',port=5015, debug=False)