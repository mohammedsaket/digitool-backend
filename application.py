
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from flask import flash,Flask,jsonify,request,Response
# from flask_cors import CORS

# app= Flask(__name__)
# CORS(app)
# @app.route('/')
# def welcome():
#     result=jsonify({'msg':"Welcome"})
#     result.status_code=200
#     return result

# scope = ['https://spreadsheets.google.com/feeds',
#          'https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name('tool_key.json', scope)
# client = gspread.authorize(creds)

# @app.route('/data')
# def data():

#     sheet = client.open('data').sheet1

#     company_data = sheet.get_all_records()
#     result=jsonify(company_data)
#     result.status_code=200
#     return result

# #sheet_login = client.open('login').sheet1

# #company_login = sheet_login.get_all_records()

# @app.route('/validate',methods=['POST'])
# def validate():
#     try:
#         sheet_login = client.open('login').sheet1
#         company_login = sheet_login.get_all_records()
#         _json=request.json
#         email=_json['username']
#         password=_json['password']
#         if email and request.method=='POST':
#             loc=-1
#             for i in range(len(company_login)):
#                 if (email == company_login[i]['email']):
#                     loc = i
#             if (loc > -1):
#                 if company_login[loc]['password'] == password:
#                     result = jsonify({"msg":'Login Successfully',"data":company_login[loc]})
#                     result.status_code = 200
#                     return result

#             else:
#                 result = jsonify({"msg":'Login Failed'})
#                 result.status_code = 403
#                 return result
#     except Exception as e:
#         result=jsonify({'msg':str(e)})
#         result.status_code=500
#         return result



import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import flash,Flask,jsonify,request,Response
from flask_cors import CORS
from bson.json_util import loads, dumps

import pymongo
import ssl
import json

app= Flask(__name__)
CORS(app)

client = pymongo.MongoClient("mongodb+srv://test:test@cluster0.hdcch.mongodb.net/digitool?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)

db = client.get_database('digitool')
ListCollection = db.ListData
LoginCollection = db.LoginData
@app.route('/')
def welcome():
    result=jsonify({'msg':"Welcome"})
    result.status_code=200
    return result

@app.route('/data')
def data():

    l = []
    cursor = ListCollection.find()
    for record in cursor:
    
        l.append(dumps(record))
   
    result=jsonify(l)
    result.status_code=200
    return jsonify(l)

@app.route('/validate',methods=['POST'])
def validate():
    try:
        
        
        _json=request.json
        email=_json['username']
        password=_json['password']
        if email and request.method=='POST':
    
            cursor = LoginCollection.find()
            for record in cursor:
                
                if (record['email'] == email and record['pwd'] == password):
                    result = jsonify({"msg":'Login Successfully'})
                    result.status_code = 200
                    return result

            else:
                result = jsonify({"msg":'Login Failed'})
                result.status_code = 403
                return result
    except Exception as e:
        result=jsonify({'msg':str(e)})
        result.status_code=500
        return result
