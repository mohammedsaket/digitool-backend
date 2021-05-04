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
