from flask import Flask, jsonify,request
import uuid
import jwt
from flask_mysqldb import MySQL
from flask_cors import CORS,cross_origin
import pymysql
import mysql.connector
from flaskext.mysql import MySQL
from roleauth import authmiddleware
from middlewareauth import jwtmiddleware


app = Flask(__name__)
CORS(app)
authmiddleware(app)
jwtmiddleware(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Krishna@1234'
app.config['MYSQL_DATABASE_DB'] = 'student'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/home",methods=["GET"])
def home():
    return "hello"

@app.route('/add_student', methods=['POST'])
def add_student():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        _json= request.json
        id= _json['id']
        name=_json['name']
        rollno=_json['rollno']
        subject=_json['subject']
        if id and name and rollno and subject and request.method == 'POST':
            sqlquery = "INSERT INTO studentdetail(id,name,rollno, subject) VALUES(%s,%s,%s,%s)"
            bindData = (id,name,rollno,subject)
            cursor.execute(sqlquery , bindData)
            conn.commit()
            respone = jsonify("student added successfully!")
            respone.status_code = 200
            return respone
        else:
            return ("not valid arguments")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/students',methods=['GET'])
def studentdetail():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT id,name,rollno,subject FROM studentdetail")
        studentdetailRows = cursor.fetchall()
        respone = jsonify(studentdetailRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print (e)
    finally:
        cursor.close()
        conn.close()

@app.route('/student',methods=['GET'])
def student():
    id = request.args.get('id')
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT id,name,rollno,subject FROM studentdetail WHERE id =%s",id)
        studentdetailRow=cursor.fetchone()
        respone=jsonify(studentdetailRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/update_student',methods=['PUT'])
def update_student():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        _json= request.json
        id= _json['id']
        name=_json['name']
        rollno=_json['rollno']
        subject=_json['subject']
        if id and name and rollno and subject and request.method == 'PUT':
            sqlQuery = "UPDATE studentdetail SET name=%s, rollno=%s, subject=%s WHERE id=%s"
            bindData = (name, rollno, subject,id )
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify("student updated successfully!")
            respone.status_code = 200
            return respone
        else:
            return ("not valid argument")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/deletestudent',methods=['DELETE'])
def delete_student():
    id = request.args.get('id')
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM studentdetail WHERE id =%s",(id))
        conn.commit()
        respone = jsonify('student deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

app.config['SECRET_KEY']="bcfc6ceab8bc4491b6a73da7f3b47c00"

@app.route('/login', methods=['POST'])
def login():
    # Perform necessary authentication and validation checks
    username = 'chirali'
    password = 'chirali1234'

    # Check if the credentials are valid
    if check_credentials(username, password):
        # Generate the JWT bearer token
        token = generate_token(username)
        return jsonify({'token': token})

    # Return an error message if the credentials are invalid
    return jsonify({'message': 'Invalid username or password'}), 401

def check_credentials(username, password):
    # Implement your authentication logic here
    # This can involve checking against a database, external service, or other methods
    # Return True if the credentials are valid, otherwise return False
    if username == 'chirali' and password == 'chirali1234':
        return True
    return False

def generate_token(username,role):
    # Create the payload for the token
    payload = {'username': username, 'role': role}

    # Generate the JWT bearer token
    token = jwt.encode(payload, 'bcfc6ceab8bc4491b6a73da7f3b47c00', algorithm='HS256')

    # Return the token
    app.config['SECRET_KEY']
    return token

token = generate_token('chirali', 'admin')
print("admin token",token)

token1 = generate_token('krisha' , 'user')
print("user token",token1)

token2 = generate_token('charmi','mediator')
print("mediatior token",token2)

if __name__ == '__main__':
    app.run(debug=True)

app.run()