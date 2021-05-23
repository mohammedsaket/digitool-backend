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
CustomerCollection = db.customerData
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


############## Customer List ####################

@app.route('/customerList')
def CustomerCollectionfunc():
    l = []
    cursor = CustomerCollection.find()
    for record in cursor:
    
        l.append(dumps(record))
   
    result=jsonify(l)
    result.status_code=200
    return jsonify(l)


@app.route('/postCustomerList',methods=['POST'])
def postCustomerList():
    try:
        jsonData=request.json
        CustomerCollection.insert_one(jsonData)
        result = jsonify({"msg":'Data Added'})
        result.status_code = 200
        return result

            
    except Exception as e:
        result=jsonify({'msg':str(e)})
        result.status_code=500
        return result

@app.route('/updateCustomerList',methods=['POST'])
def updateCustomerList():
    try:
        jsonData=request.json
        ID = jsonData['ID']
        del jsonData['ID']
        new_dict = {"$set":jsonData}
        CustomerCollection.update_one({"ID":ID},new_dict)
        result = jsonify({"msg":'Data Updated'})
        result.status_code = 200
        return result

            
    except Exception as e:
        result=jsonify({'msg':str(e)})
        result.status_code=500
        return result

@app.route('/deleteCustomerList',methods=['POST'])
def deleteCustomerList():
    try:
        jsonData=request.json
        ID = jsonData['ID']
        CustomerCollection.delete_one({"ID":ID})
        result = jsonify({"msg":'Data Deleted'})
        result.status_code = 200
        return result

            
    except Exception as e:
        result=jsonify({'msg':str(e)})
        result.status_code=500
        return result

############## Order List ####################

@app.route('/orderList',methods=['POST'])
def orderList():
    jsonData=request.json
    ID = jsonData['ID']
    l = []
    cursor = CustomerCollection.find({"ID":ID})
    for record in cursor:
    
        l.append(dumps(record))
   
    result=jsonify(l)
    result.status_code=200
    return jsonify(l)
## Can use this for Post,Update,Delete
@app.route('/postOrderList',methods=['POST'])
def postOrderList():
    try:
        jsonData=request.json
        ID = jsonData['ID']
        del jsonData['ID']
        new_dict = {"$set":jsonData}
        CustomerCollection.update_one({"ID":ID},new_dict)
        result = jsonify({"msg":'Order Data Updated'})
        result.status_code = 200
        return result

            
    except Exception as e:
        result=jsonify({'msg':str(e)})
        result.status_code=500
        return result

######### Data for Graphs ##########

@app.route('/WebsiteData')
def website_data():

    l = []
    d= {'News':0,'Health':0,'Technology':0,'Business':0,'General':0,'Lifestyle':0,'Others':0 ,'Travel':0,'SEO':0 }
    d1= {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0}
    d2 = {'todo':0,'inprogress':0,'done':0}
    cursor = ListCollection.find()
    cursor1 = CustomerCollection.find()
    wc,cc,oc,r = 0,0,0,0

    for record in cursor:
        wc= wc+1
        # l.append(dumps(record))
        if (record['Niche']!= None):
            if ('news' in record['Niche'].lower()):
                d['News'] = d['News'] +1
            elif ('travel' in record['Niche'].lower()):
                d['Travel'] = d['Travel'] +1
            elif ('health' in record['Niche'].lower()):
                d['Health'] = d['Health'] +1
            elif ('tech' in record['Niche'].lower()):
                d['Technology'] = d['Technology'] +1
            elif ('business' in record['Niche'].lower()):
                d['Business'] = d['Business'] +1
            elif ('general' in record['Niche'].lower()):
                d['General'] = d['General'] +1
            elif ('lifestyle' in record['Niche'].lower() or 'beauty' in record['Niche'].lower() or 'fashion' in record['Niche'].lower()):
                d['Lifestyle'] = d['Lifestyle'] +1
            elif ('seo' in record['Niche'].lower()):
                d['SEO'] = d['SEO'] +1
            else:
                d['Others'] = d['Others'] +1
        if (record['DA']!= None and record['DA'].isnumeric()):
            if (int(record['DA'])<16):
                d1['a'] = d1['a'] +1
            elif (int(record['DA'])<31):
                d1['b'] = d1['b'] +1
            elif (int(record['DA'])<46):
                d1['c'] = d1['c'] +1
            elif (int(record['DA'])<61):
                d1['d'] = d1['d'] +1
            elif (int(record['DA'])<76):
                d1['e'] = d1['e'] +1
            elif (int(record['DA'])<101):
                d1['f'] = d1['f'] +1
    
    for record in cursor1:
        cc = cc+1
        for i in record['Orders']:
            oc = oc +1
            r = r + int(i['Amount'][1:])
            if (i['OrderStatus'] == "In Progress"):
                d2['inprogress'] = d2['inprogress'] +1
            elif (i['OrderStatus'] == "Done"):
                d2['done'] = d2['done'] +1
            else:
                d2['todo'] = d2['todo'] +1        
    d3 = {'wc':wc,'cc':cc,'oc':oc,'r':r}
    result=jsonify({'Niche':d,'DA':d1,'Orders':d2,'details':d3})
    result.status_code=200
    return result
if __name__ == '__main__':
    app.run()
