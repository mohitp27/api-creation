#doc https://medium.com/@connect.hashblock/creating-an-api-in-flask-with-mysql-a-step-by-step-guide-446f08722057

from flask import Flask, jsonify, Response, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'students'

mysql = MySQL(app)

#print 'hello world'
@app.route('/')
def hello_world():
    return 'Hello world'

#get data
@app.route('/data', methods=['GET'])
def get_data():
    cur =  mysql.connection.cursor()
    cur.execute('''SELECT * FROM student''')
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

#Get data from id
@app.route('/data/<int:id>', methods=['GET'])
def get_data_by_id(id):
    cur =  mysql.connection.cursor()
    cur.execute('''select * from student where id = %s''', (id,))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

#insert data in database
@app.route('/data', methods=['POST'])
def add_new_data():
    cur = mysql.connection.cursor()
    my_id = request.json['id']
    name = request.json['name']
    my_class = request.json['my_class']
    mark = request.json['mark']
    gender = request.json['gender']
    cur.execute('''insert into student (id, name, class, mark, gender) values (%s, %s, %s, %s, %s)''', (my_id, name, my_class, mark, gender))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'Data added successfully'})

#update data in database
@app.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    cur = mysql.connection.cursor()
    name = request.json['name']
    my_class = request.json['my_class']
    mark = request.json['mark']
    gender = request.json['gender']
    cur.execute('''update student set name = %s, class = %s, mark = %s, gender = %s where id = %s ''', (name, my_class, mark, gender, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'Data update successfully'})

#delete data from database
@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    cur = mysql.connection.cursor()
    cur.execute('''delete from student where id = %s ''', (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'Data deleted successfully'})

if __name__ =='__main__':
    app.run(debug=True)
