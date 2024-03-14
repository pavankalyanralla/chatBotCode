from flask import *
from datetime import datetime,timedelta
from flask_cors import CORS, cross_origin
from flask_restful import Api
import sys
import logging



apiResponse = Flask("Response:::")
urlLog = Flask("URL:::")
requestParams =Flask("Params:::")
exceptionMessage=Flask("Message:::")

class LogRecordings():
    logger = logging.getLogger('')
    logging.basicConfig(
	filename='database/logs/'+datetime.now().strftime("%d-%m-%Y")+'---Log'+'.log',	
	level=logging.INFO,
	format='[%(asctime)s] %(levelname)s from MyIMS: %(message)s')

    def result(self,val):
        return apiResponse.logger.info(val)

    def urlName(self,val):
        return urlLog.logger.info(val)
    
    def request(self,params):
        return requestParams.logger.info(params)
        
    def exceptionMessage(self,params):
        return exceptionMessage.logger.info(params)
