from flask import Flask, render_template, json, request, redirect, abort, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'baselessdata_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = 'streamliner18 was here'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/search')
def search():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from `Gene`")
    data = cursor.fetchone()
    print(data)
    return main();

@app.route('/login', methods=['POST'])
def login():
    _email = request.form['email']
    _password = request.form['password']
    print(_email,_password)
    # TODO: Do your thing here
    return redirect('/')

@app.route('/signUp', methods=['POST'])
def signUp():
    _email = request.form['email']
    _password = request.form['password']
    # _name = request.form['name']
    print(_email,_password)
    try:
        # TODO: Convert this query to python
        # SQL: INSERT INTO Users VALUES ({_email}, {_password}, {_name})
        
        # # validate the received values
        # if _name and _email and _password:

        #     # All Good, let's call MySQL

        #     conn = mysql.connect()
        #     _hashed_password = generate_password_hash(_password)
        #     cur = mysql.connection.cursor()
        #     cur.callproc('sp_createUser', (name, email, hashed_password))
        #     data = cur.fetchall()

        #     if len(data) is 0:
        #         conn.commit()
        #         return json.dumps({'message':'User created successfully !'})
        #     else:
        #         return json.dumps({'error':str(data[0])})
        # else:
        #     return json.dumps({'html':'<span>Enter the required fields</span>'})
        session['user'] = user_data_object
        # TODO: Write handling here
    except Exception as e:
        abort(401)


if __name__ == "__main__":
    app.run(debug=True)
