from flask import Flask, render_template, redirect, url_for, request, session, json
import pymongo 
from pymongo import MongoClient
import sys
import json
import requests
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import http.client 
from pprint import pprint
import plotly.plotly as py
import plotly.graph_objs as go
from flask import Markup
import re                  ## import regular expression

client = MongoClient('localhost', 27017) ## pymongo uses Mongoclient for connecting to a MongoDB instance


global user_data

app = Flask(__name__)


@app.route('/', methods=['GET'])  ## URL '/' is bound to fpage() function
def fpage():
    
   return render_template('FirstPage.html')

@app.route('/FirstPage', methods=['GET'])  
def firstpage():
    
   return render_template('FirstPage.html')

@app.route('/SecondPage', methods=['GET'])
def SecondPage():
	
    return render_template('SecondPage.html')

@app.route('/SecondPage', methods=['POST'])
def Second_Page():

    return render_template('SecondPage.html')

	
@app.route('/ThirdPage', methods=['GET'])
def ThirdPage():
  	
   return render_template('ThirdPage.html')

@app.route('/ThirdPage', methods=['POST'])
def Third_Page():

   global user_data
   
   user_data = {}  ## JSON data
   
   ## extracting Data from SecondPage.html and storing it into user_data
 
   user_data['pro_name'] = request.form['pro_name']      
   user_data['Tagname'] = request.form['Tagname']
   user_data['Attack_Vector'] = request.form['Attack_Vector']
   injection = user_data['Attack_Vector']
   user_data['API_Type'] = request.form['API_Type']
   user_data['protocol'] = request.form['protocol']
   api = user_data['API_Type']

   return render_template('ThirdPage.html', api = api) ## posting value of API Type on ThirdPage.html


@app.route('/FourthPage', methods=['GET'])
def FourthPage():
   
   return render_template('FourthPage.html')

@app.route('/FourthPage', methods=['POST'])
def Fourth_Page():
   global user_data
 
  ## extracting Data from ThirdPage.html and storing it into user_data 
   user_data['usrtxt'] = request.form['usrtxt']
   user_data['apidata'] = request.form['apidata']
   return render_template('FourthPage.html')


@app.route('/Settings', methods=['GET'])
def Settings_1():
   
   return render_template('Settings.html')
POST
@app.route('/Settings', methods=['POST'])
def Settings():
   global user_data
   global injection
   user_data['header'] = request.form['header']
  
   db = client["Cyber1"]   ## connection to database
   response = db.collection

   ## code for generating a unique scan_id
   temp = db.response.find().sort( [("_id", -1)] ).limit(1)  ## find previous scan_id from database
   for doc in temp:
        scan_id = str(int(doc['scan_id']) + 1)      ## increase scan_id by 1

   user_data['scan_id'] = scan_id
   
   
   print(scan_id)
   print(user_data['scan_id'])
   
   ## making HTTP POST request and posting user_data. It will run run() function from client.py file
   requests.post('http://127.0.0.1:8003/run', data=user_data)  

   return render_template('Settings.html')


@app.route('/Summary', methods=['GET','POST'])
def Summary():
   
   L = []
   db = client["Cyber1"]     ## connecting to database Cyber1
   response = db.collection  ## connection to collection response
   scanID = db.response.distinct("scan_id")  ## find all scan_ids
   
## code for sending data related to scan_id to summary.html page
   for s in scanID:
       c = db.response.find({'scan_id':s}).limit(1)       
       for document in c: 
           L.append(document)
   return render_template('Summary.html',L=L)

@app.route('/Report', methods=['GET'])
def Report():
    
   return render_template('Report.html')

@app.route('/Help', methods=['GET'])
def Help():
    
   return render_template('api.html')
   


@app.route('/Piechart', methods=['GET','POST'])
def Piechart():
   db = client["Cyber1"]   ## connection to database
   response = db.collection
   c1=0
   c2=0
   c3=0
   c4=0
   c5=0
   a1 = [0] * 20
   a2 = [0] * 20
   a3 = [0] * 20
   a4 = [0] * 20
   a5 = [0] * 20
   global L1
   L1=[]
   global check
   check = {}
   check['scan_id'] = request.form.getlist('scanid')
   value1 = check['scan_id']
   k = 0
   for i in value1:
      print(i)
      doc = db.response.find({"scan_id":i})
      for j in doc:
         n=0
         cnt = j['cnt']
         while n < cnt:
            rc = j['API'][n]['Response_Code']
            rcs = str(rc)
            if rcs[0] == "1" :
                c1=c1+1
                a1[k] = a1[k] + 1
            if rcs[0] == "2" :
                c2=c2+1
                a2[k] = a2[k] + 1
            if rcs[0] == "3" :
                c3=c3+1
                a3[k] = a3[k] + 1
            if rcs[0] == "4" :
                c4=c4+1
                a4[k] = a4[k] + 1
            if rcs[0] == "5" :
                c5=c5+1
                a5[k] = a5[k] + 1
                 
            n = n+1
            
         L1.append(j['Injection_Type'])
      k = k + 1
      
   for i in range(len(L1)):
      print(L1[i])
         

   global labels
   labels = []   
   labels = ["1xx","2xx","3xx","4xx","5xx"]
   values = [c1,c2,c3,c4,c5]
   global values1
   values1 = []
   values1 = [a1,a2,a3,a4,a5]
   colors = [ "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA","#ABCDEF", "#DDDDDD", "#ABCABC","#FEDCBD"  ]
   for i in range(len(values)):
      print(values[i])
   
      
   return render_template('Piechart.html', set=zip(values, labels, colors ))
  
@app.route('/Report1', methods=['GET'])
def Report1get():
    
   return render_template('Report1.html')
   
   
@app.route('/Report1', methods=['POST'])
def Report1():
   db = client["Cyber1"]
   response = db.collection
   
   global check
   value1 = check['scan_id']
   value2 = request.form['value2']
   L2 = []
  
   for i in value1:
     
      doc = db.response.find({"scan_id":i})
      out = {}
      for j in doc:
         n=0
         rjson1 = []
         cnt = j['cnt'] 
         out['scan_id'] = j['scan_id']
         out['Project_Name'] = j['Project_Name']
         out['Date'] = j['DateTime']
         while n < cnt:
            rc = j['API'][n]['Response_Code']
            rcs = str(rc)
            if rcs[0] == value2[0]:
               
               rjson1.append({'Tagid': j['API'][n]['Tagid'],'Request': j['API'][n]['Request'], 'Response_Code':j['API'][n]          
['Response_Code'],'Response': j['API'][n]['Response'],})
            n = n+1
         out['Responses'] = rjson1
        
         L2.append(out)

   
   return render_template('Report1.html',L2 =L2, value2 = value2)


@app.route('/Columnchart', methods=['GET','POST'])
def Columnchart():
   global labels
   global values1
   global L1
   return render_template('Columnchart.html', set = zip(labels,values1), L1=L1)

if (__name__ == "__main__"):
	app.run(port = 8006)
