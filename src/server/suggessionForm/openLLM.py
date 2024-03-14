from flask_restful import Resource, reqparse
from database.queries import DB_Queries
from database.dB_Execute import *
from public.strings.strings import *
from database.queries import *
# from flask_mysqldb import MySQL
from src.server.constants.response import *
from datetime import datetime
import requests
from datetime import datetime, timedelta
# from langchain.llms import OpenAI
from langchain_openai import OpenAI
import os
import re
from langchain_community.llms import OpenAI
from langchain.chains import ConversationChain, LLMChain
from langchain.prompts import PromptTemplate

# from langchain.memory import ConversationBufferWindowMemory

api_key='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'
# api_key = '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'
os.environ['OPENAI_API_KEY'] = api_key

class OpenLLMCheck(Resource):
    def post(self):
        requestData = request.get_json()
        if (not request.get_json()
                or not 'reqDescription' in request.get_json() or requestData['reqDescription'] == ''):
            return emptyDataResponse()
        reqDescription=requestData['reqDescription']
        # Customize the LLM template
        print("1......")
        prompt = PromptTemplate(
            input_variables= reqDescription,
            template="what are the 5 most {input} cities in the world?",
        )
        print("2......", prompt.format(input="Terralogic"))
        
                
        
        
        
        
        
        llm = OpenAI(temperature=0.9)
        summary = llm(str(prompt))
        # summary = llm("Please provide user needs, if user gives"+reqDescription+ "from Terralogic software solutions with warmful greeting.")
        # # response = '\n'.join([line.strip() for line in summary.split('\n\n')])
        # response = re.sub(r'\n\n+', '\n', summary)
        resultJson = {
            'data' : summary
        }
        return resultJson