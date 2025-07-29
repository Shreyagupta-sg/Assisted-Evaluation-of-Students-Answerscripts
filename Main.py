# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "home"
__date__ = "$26 Apr, 2021 6:30:58 PM$"

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import json
import numpy as np
import os
import pandas as pd
import pygal
import pymysql
import random
import requests
import urllib3
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sqlalchemy import create_engine
import urllib.parse as urlparse
from urllib.parse import parse_qs
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'D:/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.secret_key = "1234"
app.password = ""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = ""
        db = "subjectiveanalysis"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    def getuserprofiledetails(self, username):
        strQuery = "SELECT PersonId,Firstname,Lastname,Phoneno,DOB,Age,Address,Recorded_Date FROM personaldetails WHERE Username = '" + username + "' LIMIT 1"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertdoctordetails(self, firstname, lastname, phone, email, address, username, password):
        print('insertdoctordetails::' + username)
        strQuery = "INSERT INTO doctordetails(Firstname, Lastname, Phoneno, Emailid, Address, Username, Password, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (firstname, lastname, phone, email, address, username, password)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def inserthistorydetails(self, PersonId, Question1Id, Question2Id, Question3Id, Question4Id, Question5Id, Question6Id, Result, Percentage):
        print('inserthistorydetails::' + str(PersonId))
        strQuery = "INSERT INTO historydetails(PersonId, Question1Id, Question2Id, Question3Id, Question4Id, Question5Id, Question6Id, Result, Percentage, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (str(PersonId), Question1Id, Question2Id, Question3Id, Question4Id, Question5Id, Question6Id, Result, Percentage)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def insertpersonaldetails(self, firstname, lastname, phone, dob, age, email, address, username, password):
        print('insertpersonaldetails::' + username)
        strQuery = "INSERT INTO personaldetails(Firstname, Lastname, Phoneno, DOB, Age, Emailid, Address, Username, Password, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (firstname, lastname, phone, dob, age, email, address, username, password)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def updatepersonaldetails(self, PersonId, firstname, lastname, phone, dob, age, email, address):
        print('updatepersonaldetails::' + str(PersonId))
        strQuery = "UPDATE personaldetails SET Firstname = '" + str(firstname) + "', Lastname = '" + str(lastname) + "', Phoneno = '" + str(phone) + "', DOB = '" + str(dob) + "', Age = '" + str(age) + "', Emailid = '" + str(email) + "', Address = '" + str(address) + "' WHERE PersonId = '" + str(PersonId) + "' "
        self.cur.execute(strQuery)
        self.con.commit()
        return ""
    def insertquerydetails(self, PersonId, DoctorId, Comments):
        print('insertquerydetails::' + Comments)
        strQuery = "INSERT INTO querydetails(PersonId, DoctorId, Comments, Reply, Recorded_Date) values(%s, %s, %s, '-', now())"
        strQueryVal = (PersonId, DoctorId, Comments)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def updatequerydetails(self, queryId, Comments):
        print('updatequerydetails::' + queryId)
        strQuery = "UPDATE querydetails SET Reply = '" + Comments + "' WHERE QueryId = '" + queryId + "' "
        self.cur.execute(strQuery)
        self.con.commit()
        return ""
    def getpersonaldetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, PersonId FROM personaldetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def getdoctorlogindetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, DoctorId FROM doctordetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def getuserpersonaldetails(self, name):
        strQuery = "SELECT PersonId, Firstname, Lastname, Phoneno, DOB, Age, Emailid, Address, Recorded_Date FROM personaldetails WHERE Username = '" + name + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getquerydetails(self, PersonId):
        strQuery = "SELECT d.Firstname, d.Lastname, q.Comments, q.Reply, q.Recorded_Date FROM querydetails AS q LEFT JOIN doctordetails AS d ON d.DoctorId = q.DoctorId WHERE q.PersonId = '" + str(PersonId) + "' ORDER BY Recorded_Date DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdoctorquerydetails(self, DoctorId):
        strQuery = "SELECT p.Firstname, p.Lastname, q.QueryId, q.Comments, q.Reply, q.Recorded_Date FROM querydetails AS q LEFT JOIN personaldetails AS p ON p.PersonId = q.PersonId WHERE q.DoctorId = '" + str(DoctorId) + "' ORDER BY Recorded_Date DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getvideodetails(self):
        strQuery = "SELECT v.VideoId, v.VideoUrl, c.Name, v.Recorded_Date FROM videodetails AS v LEFT JOIN categorydetails AS c ON c.CategoryId = v.CategoryId "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result    
    def getdoctordetails(self, name):
        strQuery = "SELECT DoctorId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM doctordetails WHERE Username = '" + name + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdoctorlistdetails(self):
        strQuery = "SELECT DoctorId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM doctordetails LIMIT 10 "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result		
    def getuseranswerdetails(self, PersonId):
        strQuery = "SELECT ua.UserAnswerId, ua.QuestionId, q.Question, ua.Answer, ua.Recorded_Date FROM useranswerdetails AS ua LEFT JOIN questiondetails AS q ON q.QuestionId = ua.QuestionId WHERE ua.PersonId = '" + str(PersonId) + "' AND ua.QuestionId IN (1, 2, 3, 4, 5, 6) GROUP BY ua.QuestionId ORDER BY Recorded_Date DESC "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getuseranswerdetailsbyquestionid(self, PersonId, QuestionId):
        strQuery = "SELECT ua.QuestionId, ua.Answer FROM useranswerdetails AS ua WHERE ua.PersonId = '" + str(PersonId) + "' AND ua.QuestionId IN ('" + str(QuestionId) + "') GROUP BY ua.QuestionId ORDER BY Recorded_Date DESC "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getstressdetails(self, id):
        strQuery = "SELECT StressId, Name, Recorded_Date FROM stressdetails WHERE StressId = '" + str(id) + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getanswerdetails(self, Answer, QuestionId):
        strQuery = "SELECT AnswerId, Answer, Category, Recorded_Date FROM answerdetails WHERE Answer = '" + str(Answer) + "' AND QuestionId = '" + str(QuestionId) + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getAnswerDetailsByQuestionId(self, QuestionId, Answer):
        strQuery = "SELECT COUNT(*) AS c FROM answerdetails WHERE QuestionId = '" + str(QuestionId) + "' AND Answer IN (" + str(Answer) + ") "
        print(strQuery)
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertsurveydataset(self, PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19):
        print('insertsurveydataset::' + Email_Address)
        strQuery = "INSERT INTO surverydataset(PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return "" 
    def insertuseranswerdetails(self, PersonId, q1, a1):
        print('insertuseranswerdetails::' + str(PersonId))
        strQuery = "INSERT INTO useranswerdetails(PersonId, QuestionId, Answer, Recorded_Date) values(%s, %s, %s, now())"
        strQueryVal = (PersonId, q1, a1)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return "" 
    def deleteuseranswerdetails(self, PersonId):
        print('deleteuseranswerdetails::' + str(PersonId))
        strQuery = "DELETE FROM useranswerdetails WHERE PersonId = (%s) " 
        strQueryVal = (str(PersonId))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def deletesurveydataset(self, loanId):
        print(loanId)
        strQuery = "DELETE FROM surverydataset WHERE Sno = (%s) " 
        strQueryVal = (str(loanId))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def getsurveydatasetuploadeddetails(self):
        strQuery = "SELECT Sno, PersonId, Timestamp, Email_Address, Name, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Recorded_Date "
        strQuery += "FROM surverydataset "
        strQuery += "ORDER BY Sno DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getgraphdetails(self, dataownername):
        strQuery = "SELECT COUNT(*) AS c, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Attack "        
        strQuery += "FROM kdddataset "        
        strQuery += "GROUP BY Protocol, Service, Flag, Attack "   
        print(strQuery)
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getallprotocoldetails(self):
        strQuery = "SELECT DISTINCT(Protocol) AS Protocol FROM kdddataset"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getkdddatasetdatabyname(self, protocol):
        strQuery = "SELECT Sno, Duration, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Land, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,  s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, Attack "
        strQuery += "FROM kdddataset "
        strQuery += "WHERE Protocol = '" + protocol + "'  "
        strQuery += "ORDER BY Sno DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertanalysisdetails(self, Accuracy, Algorithm):
        print('insertanalysisdetails::' + Algorithm)
        strQuery = "INSERT INTO analysisdetails(Accuracy, Algorithm, Recorded_Date) values(%s, %s, now())"
        strQueryVal = (str(Accuracy).encode('utf-8', 'ignore'), str(Algorithm).encode('utf-8', 'ignore'))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""  
    def getallknndetails(self):
        strQuery = "SELECT sum(Accuracy) as c FROM analysisdetails WHERE Algorithm = 'KNN'"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result  
    def gettaskdetails(self, offset, limit):
        strQuery = "SELECT TaskId, TaskName, Recorded_Date FROM taskdetails LIMIT %s OFFSET %s"        
        strQueryVal = (limit, offset)
        self.cur.execute(strQuery, strQueryVal)        
        result = self.cur.fetchall()
        print(result)
        return result
    def gethistorydetails(self, PersonId):
        strQuery = "SELECT h.HistoryId, h.PersonId, h.Question1Id AS Answer1, "        
        strQuery += "h.Question2Id AS Answer2, " 
        strQuery += "h.Question3Id AS Answer3, "        
        strQuery += "h.Question4Id AS Answer4, "        
        strQuery += "h.Question5Id AS Answer5, "        
        strQuery += "h.Question6Id AS Answer6, "   
        strQuery += "Result, Percentage, Recorded_Date "      
        strQuery += "FROM historydetails AS h "    
        strQuery += "WHERE h.PersonId = '" + str(PersonId) + "'  "
        strQuery += "ORDER BY h.HistoryId DESC "    
        strQuery += "LIMIT 10 "    
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()
        print(result)
        return result
    def getallkmeansdetails(self):
        strQuery = "SELECT sum(Accuracy) as c FROM analysisdetails WHERE Algorithm = 'K-Means'"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    
@app.route('/', methods=['GET'])
def loadindexpage():
    return render_template('index.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/codeindex', methods=['POST'])
def codeindex():
    username = request.form['username']
    password = request.form['password']
    
    print('username:' + username)
    print('password:' + password)
    
    try:
        if username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getpersonaldetails(username, password)       
                return emps
            res = db_query()
            
            for row in res:
                print(row['c'])
                count = row['c']
                
                if count >= 1:      
                    session['x'] = username;
                    session['UID'] = row['PersonId'];
                    def db_query():
                        db = Database()
                        emps = db.getuserprofiledetails(username)       
                        return emps
                    profile_res = db_query()
                    return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
                else:
                    flash ('Incorrect Username or Password.')
                    return render_template('index.html')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('index.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('index.html')
        
    return render_template('index.html')

@app.route('/usersignin', methods=['GET'])
def usersignin():
    return render_template('usersignin.html')

@app.route('/codeusersignin', methods=['POST'])
def codeusersignin():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    dob = request.form['datepicker1']
    age = request.form['age']
    address = request.form['address']    
    username = request.form['username']
    password = request.form['password']
    
    print('firstname:', firstname)
    print('lastname:', lastname)
    print('phone:', phone)
    print('dob:', dob)
    print('age:', age)
    print('email:', email)
    print('address:', address)
    print('username:', username)
    print('password:', password)
    
    try:
        if firstname is not "" and lastname is not ""  and phone is not "" and phone is not ""  and dob is not "" and age is not "" and address is not "" and username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getpersonaldetails(username, password)       
                return emps
            res = db_query()

            for row in res:
                print(row['c'])
                count = row['c']

                if count >= 1:      
                    flash ('Entered details already exists.')
                    return render_template('usersignin.html')
                else:
                    def db_query():
                        db = Database()
                        emps = db.insertpersonaldetails(firstname, lastname, phone, dob, age, email, address, username, password)    
                        return emps
                res = db_query()
                flash ('Dear Customer, Your registration has been done successfully.')
                return render_template('index.html')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('usersignin.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('usersignin.html')
    
    return render_template('usersignin.html')

@app.route('/userprofile', methods=['GET'])
def userprofile():
    def db_query():
        db = Database()
        emps = db.getuserpersonaldetails(session['x'])       
        return emps
    profile_res = db_query()
    return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/signout', methods=['GET'])
def signout():    
    return render_template('signout.html')

@app.route('/logout', methods=['GET'])
def logout():
    del session['x']
    return render_template('index.html')

@app.route('/uploaddata', methods=['GET'])
def uploaddata():
    return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codeuploaddata', methods=['POST'])
def codeuploaddata(): 
    file = request.files['filepath']
    
    print('filename:' + file.filename)
       
    if 'filepath' not in request.files:
        flash ('Please fill all mandatory fields.')
        return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')
    
    if file.filename != '':

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            filepath = UPLOAD_FOLDER + "/" + file.filename

            print('filepath:' + filepath)
            
            data = pd.read_csv(filepath)
            
            # print info about columns in the dataframe 
            print(data.info()) 
            
            # Dropped all the Null, Empty, NA values from csv file 
            csvrows = data.dropna(axis=0, how='any') 

            count = len(csvrows);
            
            print('Length of Data::', count)

            for i in range(count): 
                
                if i == 0:
                    print(count)
                    
                else:  
                    db = Database()
                    db.insertsurveydataset(session['UID'], str(np.array(csvrows['Timestamp'])[i]), str(np.array(csvrows['Email_Address'])[i]), str(np.array(csvrows['Name'])[i]), str(np.array(csvrows['Q1'])[i]), str(np.array(csvrows['Q2'])[i]), str(np.array(csvrows['Q3'])[i]), str(np.array(csvrows['Q4'])[i]), str(np.array(csvrows['Q5'])[i]), str(np.array(csvrows['Q6'])[i]), str(np.array(csvrows['Q7'])[i]), str(np.array(csvrows['Q8'])[i]), str(np.array(csvrows['Q9'])[i]), str(np.array(csvrows['Q10'])[i]), str(np.array(csvrows['Q11'])[i]), str(np.array(csvrows['Q12'])[i]), str(np.array(csvrows['Q13'])[i]), str(np.array(csvrows['Q14'])[i]), str(np.array(csvrows['Q15'])[i]), str(np.array(csvrows['Q16'])[i]), str(np.array(csvrows['Q17'])[i]), str(np.array(csvrows['Q18'])[i]), str(np.array(csvrows['Q19'])[i])) 

            flash('File successfully uploaded!')
            return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')

        else:
            flash('Allowed file types are .txt')
            return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')
    else:
        flash ('Please fill all mandatory fields.')           
        return render_template('uploaddata.html', sessionValue=session['x'], content_type='application/json')

@app.route('/viewuploadeddata', methods=['GET'])
def viewuploadeddata():
    def db_query():
        db = Database()
        emps = db.getsurveydatasetuploadeddetails()       
        return emps
    profile_res = db_query()
    return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/deletedata', methods=['GET'])
def deletedata():
    parsed = urlparse.urlparse(request.url)
    print(parse_qs(parsed.query)['index'])
    
    loanId = parse_qs(parsed.query)['index']
    print(loanId)
    
    try:
        if loanId is not "": 
            
            db = Database()
            db.deletesurveydataset(loanId[0])
            
            def db_query():
                db = Database()
                emps = db.getsurveydatasetuploadeddetails()    
                return emps
            profile_res = db_query()
            flash ('Dear Customer, Your request has been processed sucessfully!')
            return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/graph', methods=['GET'])
def graph():
    
    def accepteddb_query():
        db = Database()
        emps = db.getgraphdetails(session['x'])       
        return emps
    res = accepteddb_query()
    
    graph = pygal.Line()
    
    graph.title = '% Comparison Graph Between Attacks vs Number of Counts.'
    
    graph.x_labels = ['c', 'de_bytes', 'nc_bytes']
    
    for row in res:
        
        print(row['c'])
        
        graph.add(row['Protocol'] + '-' + row['Service'] + '-' + row['Flag'] + '-' + row['Attack'], [int(row['c']), int(row['de_bytes']), int(row['nc_bytes'])])
        
    graph_data = graph.render_data_uri()
    
    return render_template('graph.html', sessionValue=session['x'], graph_data=graph_data)

@app.route('/searchknn', methods=['GET'])
def searchknn():    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    return render_template('searchknn.html', sessionValue=session['x'], protocolresult=protocolresult, content_type='application/json')

@app.route('/codesearchknn', methods=['POST'])
def codesearchknn():  
    
    protocolname = request.form['protocol']
    
    print('protocolname:' + protocolname)
    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    
    try:
        if protocolname is not "": 
            
            db_connection_str = 'mysql+pymysql://root:' + app.password + '@localhost/anomalydetection?charset=utf8'
            
            db_connection = create_engine(db_connection_str)

            strQuery = "SELECT Sno, Duration, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Land, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,  s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, Attack "
            strQuery += "FROM kdddataset "
            strQuery += "WHERE Protocol = '" + protocolname + "'  "
            strQuery += "ORDER BY Sno DESC "
            strQuery += "LIMIT 10" 
            
            print('Query::', strQuery)
        
            df = pd.read_sql(strQuery, con=db_connection)

            # you want all rows, and the feature_cols' columns
            X = df.iloc[:, 8: 42].values
            y = df.iloc[:, 5: 6].values

            print('X Data::', X)

            # Split into training and test set 
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 

            knn = KNeighborsClassifier(n_neighbors=7) 

            knn.fit(X_train, y_train) 

            # Predict on dataset which model has not seen before 
            y_knn = knn.predict(X_test);

            result = metrics.accuracy_score(y_test, y_knn)

            print("KNN Accuracy :", result); 
            
            algo = 'KNN'
            
            db = Database()
            db.insertanalysisdetails(result, algo) 
            
            def db_query():
                db = Database()
                emps = db.getkdddatasetdatabyname(protocolname)
                return emps
            profile_res = db_query()
            
            return render_template('codesearchknn.html', sessionValue=session['x'], result=profile_res, protocolresult=protocolresult, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('searchknn.html', sessionValue=session['x'])
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('searchknn.html', sessionValue=session['x'])
    
    return render_template('searchknn.html', sessionValue=session['x'])

@app.route('/searchkmeans', methods=['GET'])
def searchkmeans():    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    return render_template('searchkmeans.html', sessionValue=session['x'], protocolresult=protocolresult, content_type='application/json')

@app.route('/codesearchkmeans', methods=['POST'])
def codesearchkmeans():  
    
    protocolname = request.form['protocol']
    
    print('protocolname:' + protocolname)
    
    def db_query():
        db = Database()
        emps = db.getallprotocoldetails()       
        return emps
    protocolresult = db_query()
    
    try:
        if protocolname is not "": 
            
            db_connection_str = 'mysql+pymysql://root:' + app.password + '@localhost/anomalydetection?charset=utf8'
            
            db_connection = create_engine(db_connection_str)

            strQuery = "SELECT Sno, Duration, Protocol, Service, Flag, $nc_bytes AS nc_bytes, de$_bytes AS de_bytes, Land, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,  s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, Attack "
            strQuery += "FROM kdddataset "
            strQuery += "WHERE Protocol = '" + protocolname + "'  "
            strQuery += "ORDER BY Sno DESC "
            strQuery += "LIMIT 10" 
            
            print('Query::', strQuery)
        
            df = pd.read_sql(strQuery, con=db_connection)

            # you want all rows, and the feature_cols' columns
            X = df.iloc[:, 8: 42].values
            y = df.iloc[:, 5: 6].values

            print('X Data::', X)

            kmeans = KMeans(n_clusters=4)
            kmeans.fit(X)

            y_kmeans = kmeans.predict(X)
            
            print("y_kmeans :", y_kmeans); 
            
            result = y_kmeans[0] * 2
            
            algo = 'K-Means'
            
            print("K-Means Accuracy :", result); 
            
            db = Database()
            db.insertanalysisdetails(result, algo) 
            
            def db_query2():
                db = Database()
                emps = db.getkdddatasetdatabyname(protocolname)
                return emps
            profile_res = db_query2()
            
            return render_template('codesearchkmeans.html', sessionValue=session['x'], result=profile_res, protocolresult=protocolresult, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('searchkmeans.html', sessionValue=session['x'])
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('searchkmeans.html', sessionValue=session['x'])
    
    return render_template('searchkmeans.html', sessionValue=session['x'])

@app.route('/comparisongraph', methods=['GET'])
def comparisongraph():
    
    labels = ["KNN ALGORITHM", "K-MEANS ALGORITHM"]
    
    def kmeans_query():
        db = Database()
        emps = db.getallkmeansdetails()       
        return emps
    res = kmeans_query()

    kmeanscount = 0;

    for row in res:
        print(row['c'])
        kmeanscount = row['c']
        
    def knn_query():
        db = Database()
        emps = db.getallknndetails()       
        return emps
    res = knn_query()

    knncount = 0;

    for row in res:
        print(row['c'])
        knncount = row['c']
        
    values = [knncount, kmeanscount]

    return render_template('comparisongraph.html', sessionValue=session['x'], values=values, labels=labels)

@app.route('/quiz', methods=['GET'])
def quiz():
    return render_template('quiz.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz', methods=['POST'])
def codequiz():
    db = Database()
    db.deleteuseranswerdetails(session['UID'])    
    return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_1', methods=['POST'])
def quiz_1():    
    return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_1', methods=['POST'])
def codequiz_1():
    q1 = request.form['one']
    q2 = request.form['two']
    a1 = request.form['a']
    a2 = request.form['b']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_1.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_2', methods=['POST'])
def quiz_2():
    return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_2', methods=['POST'])
def codequiz_2():
    q1 = request.form['three']
    q2 = request.form['four']
    a1 = request.form['c']
    a2 = request.form['d']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_2.html', sessionValue=session['x'], content_type='application/json')

@app.route('/quiz_3', methods=['POST'])
def quiz_3():
    return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codequiz_3', methods=['POST'])
def codequiz_3():
    q1 = request.form['five']
    q2 = request.form['six']
    a1 = request.form['e']
    a2 = request.form['f']
    
    print('q1:', q1)
    print('a1:', a1)
    print('q2:', q2)
    print('a2:', a2)
    
    try:
        if q1 is not "" and a1 is not "" and q2 is not "" and a2 is not "": 
            def db_query1():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q1, a1)    
                return emps
            res2 = db_query1()
            
            def db_query2():
                db = Database()
                emps = db.insertuseranswerdetails(session['UID'], q2, a2)    
                return emps
            res2 = db_query2()
            return redirect(url_for("results"))
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')
    
    return render_template('quiz_3.html', sessionValue=session['x'], content_type='application/json')

@app.route('/results', methods=['GET'])
def results():
     
    def db_query():
        db = Database()
        emps = db.getuseranswerdetails(session['UID'])       
        return emps
    profile_res = db_query()
    
    answer = '';
    questionId = '';    
    questionId1 = '';
    questionId2 = '';
    questionId3 = '';
    questionId4 = '';
    questionId5 = '';
    questionId6 = '';
    
    for row in profile_res:
        
        questionId = row['QuestionId'];
        answer = row['Answer'];
        
        strCheck = checkGrammerandSpelling(answer).split("#")
        
        print('strCheck');
        
        print(strCheck);
         
        check = strCheck[0];
        
        print(check);
        
        finalValue = check;
        
        if len(strCheck) > 1:
        
            finalValue = strCheck[0] + ' (' + strCheck[1] + ')'
        
        print(finalValue);
        
        if questionId == 1:
            
            if 'Grammatical problem: agreement error' == check:
                
                questionId1 = finalValue;
                
            elif 'Spelling mistake' == check:
                
                questionId1 = finalValue;
                
            else:
                
                finalResult = getKeyword(answer);
                   
                answers = "";
                                
                for result in finalResult:

                    print(result)
                    
                    answers += '"' + result + '"' + ','
                
                answers = answers[: len(answers) - 1]
                
                print(answers)
                
                def db_answerquery():
                    db = Database()
                    emps = db.getAnswerDetailsByQuestionId(questionId, answers)       
                    return emps
                answer_res = db_answerquery()
                    
                for row in answer_res:
                    
                    questionId1 = row['c'] * 2 * 10;
            
        elif questionId == 2:
            
            if 'Grammatical problem: agreement error' in check:
                
                questionId2 = finalValue;
                
            elif 'Spelling mistake' in check:
                
                questionId2 = finalValue;
                
            else:
                
                finalResult = getKeyword(answer);
                
                answers = "";
                                
                for result in finalResult:

                    print(result)
                    
                    answers += '"' + result + '"' + ','
                
                answers = answers[: len(answers) - 1]
                
                print(answers)
                
                def db_answerquery():
                    db = Database()
                    emps = db.getAnswerDetailsByQuestionId(questionId, answers)       
                    return emps
                answer_res = db_answerquery()
                    
                for row in answer_res:
                    
                    questionId2 = row['c'] * 2 * 10;
            
        elif questionId == 3:
            
            if 'Grammatical problem: agreement error' in check:
                
                questionId3 = finalValue;
                
            elif 'Spelling mistake' in check:
                
                questionId3 = finalValue;
                
            else:
                
                finalResult = getKeyword(answer);
                
                answers = "";
                                
                for result in finalResult:

                    print(result)
                    
                    answers += '"' + result + '"' + ','
                
                answers = answers[: len(answers) - 1]
                
                print(answers)
                
                def db_answerquery():
                    db = Database()
                    emps = db.getAnswerDetailsByQuestionId(questionId, answers)       
                    return emps
                answer_res = db_answerquery()
                    
                for row in answer_res:
                    
                    questionId3 = row['c'] * 2 * 10;
            
        elif questionId == 4:
            
            if 'Grammatical problem: agreement error' in check:
                
                questionId4 = finalValue;
                
            elif 'Spelling mistake' in check:
                
                questionId4 = finalValue;
                
            else:
                
                finalResult = getKeyword(answer);
                
                answers = "";
                                
                for result in finalResult:

                    print(result)
                    
                    answers += '"' + result + '"' + ','
                
                answers = answers[: len(answers) - 1]
                
                print(answers)
                
                def db_answerquery():
                    db = Database()
                    emps = db.getAnswerDetailsByQuestionId(questionId, answers)       
                    return emps
                answer_res = db_answerquery()
                    
                for row in answer_res:
                    
                    questionId4 = row['c']* 2 * 10;
            
        elif questionId == 5:
            
            if 'Grammatical problem: agreement error' in check:
                
                questionId5 = finalValue;
                
            elif 'Spelling mistake' in check:
                
                questionId5 = finalValue;
                
            else:
                
                finalResult = getKeyword(answer);
                
                answers = "";
                                
                for result in finalResult:

                    print(result)
                    
                    answers += '"' + result + '"' + ','
                
                answers = answers[: len(answers) - 1]
                
                print(answers)
                
                def db_answerquery():
                    db = Database()
                    emps = db.getAnswerDetailsByQuestionId(questionId, answers)       
                    return emps
                answer_res = db_answerquery()
                    
                for row in answer_res:
                    
                    questionId5 = row['c']* 2 * 10;
                
        else:
            
            if 'Grammatical problem: agreement error' in check:
                
                questionId6 = finalValue;
                
            elif 'Spelling mistake' in check:
                
                questionId6 = finalValue;
                
            else:
                
                finalResult = getKeyword(answer);
                
                answers = "";
                                
                for result in finalResult:

                    print(result)
                    
                    answers += '"' + result + '"' + ','
                
                answers = answers[: len(answers) - 1]
                
                print(answers)
                
                def db_answerquery():
                    db = Database()
                    emps = db.getAnswerDetailsByQuestionId(questionId, answers)       
                    return emps
                answer_res = db_answerquery()
                    
                for row in answer_res:
                    
                    questionId6 = row['c'] * 2 * 10;
    
    db = Database()
    db.inserthistorydetails(session['UID'], questionId1, questionId2, questionId3, questionId4, questionId5, questionId6, '', '');
     
    return render_template('results.html', sessionValue=session['x'], result=profile_res, result_1=results, content_type='application/json')

@app.route('/editprofile', methods=['GET'])
def editprofile():
    parsed = urlparse.urlparse(request.url)
    print(parse_qs(parsed.query)['index'])
    
    queryId = parse_qs(parsed.query)['index']
    queryId = queryId[0]
    print(queryId)
    
    def db_query():
        db = Database()
        emps = db.getuserpersonaldetails(session['x'])       
        return emps
    profile_res = db_query()
    
    try:
        if queryId is not "":           
            return render_template('editprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('profile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('profile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    
@app.route('/codeeditprofile', methods=['POST'])
def codeeditprofile():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    dob = request.form['datepicker1']
    age = request.form['age']
    email = request.form['email']
    address = request.form['address']      
    
    print('firstname:', firstname)
    print('lastname:', lastname)
    print('phone:', phone)
    print('email:', email)
    print('address:', address)
    print('dob:', dob)
    print('age:' + age)    
  
    def db_query():
        db = Database()
        emps = db.getuserpersonaldetails(session['x'])       
        return emps
    profile_res = db_query()
            
    try:
        if firstname is not "" and lastname is not ""  and phone is not "" and dob is not "" and age is not "" and email is not "" and address is not "": 
            
            db = Database()                
            db.updatepersonaldetails(session['UID'], firstname, lastname, phone, dob, age, email, address);
    
            flash ('Dear Customer, Your details has been updated successfully.')
            return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')                                                   
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('editprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('editprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    
    return render_template('editprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
	
@app.route('/viewtask', methods=['GET'])
def viewtask():
    
    def db_query():
        db = Database()
        emps = db.gettaskdetails(round(random.uniform(1, 10)), 4)       
        return emps
    profile_res = db_query()
    
    return render_template('viewtask.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/history', methods=['GET'])
def history():
    
    def db_query():
        db = Database()
        emps = db.gethistorydetails(session['UID'])       
        return emps
    profile_res = db_query()
    
    return render_template('history.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

def checkGrammerandSpelling(answer):
        
    response = requests.post('https://api.languagetool.org/v2/check', data={'text': answer, 'language':'en-US'})

    res = json.dumps(response.json(), ensure_ascii=False, indent=2)

    print(res)

    data  = json.loads(res)
        
    comment = '';

    if "matches" in data:

        json_object = data['matches']

        print(json_object)

        if json_object:

            if 'Spelling mistake' == json_object[0]["shortMessage"]:
                
                comment = json_object[0]["shortMessage"] + '#' + json_object[0]["sentence"];
            
            else:
                
                comment = json_object[0]["shortMessage"] + '#' + json_object[0]["message"];
                        
            print("--------------------------------------------------------")
            print(json_object[0]["shortMessage"])
            print(json_object[0]["message"])
            print ("--------------------------------------------------------")
                
    return comment
       
def getKeyword(value):
        
    from nltk import tokenize
    from operator import itemgetter
    import math
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize 
    
    nltk.download('stopwords')
    nltk.download('punkt')

    # Remove stopwords
    stop_words = set(stopwords.words('english'))

    # Step 1 : Find total words in the document
    total_words = value.split()
    total_word_length = len(total_words)

    print(total_word_length)

    # Step 2 : Find total number of sentences
    total_sentences = tokenize.sent_tokenize(value)
    total_sent_len = len(total_sentences)

    print(total_sent_len)

    # Step 3: Calculate TF for each word

    tf_score = {}

    for each_word in total_words:

        each_word = each_word.replace('.', '')

        if each_word not in stop_words:

            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y / int(total_word_length)) for x, y in tf_score.items())

    print(tf_score)

    # Check if a word is there in sentence list
    def check_sent(word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))

    # Step 4: Calculate IDF for each word
    idf_score = {}

    for each_word in total_words:
        each_word = each_word.replace('.', '')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len) / y)) for x, y in idf_score.items())

    print(idf_score)

    # Step 5: Calculating TF*IDF
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()};

    print(tf_idf_score)

    # Get top N important words in the document
    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(), key=itemgetter(1), reverse=True)[:n]) 
        return result

    finalResult = get_top_n(tf_idf_score, 5);

    print(finalResult)
    
    return finalResult;