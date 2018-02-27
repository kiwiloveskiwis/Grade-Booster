from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'baselessdata_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
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


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * from `Gene`")
        data = cursor.fetchone()
        print(data)
        pass
        # _name = request.form['inputName']
        # _email = request.form['inputEmail']
        # _password = request.form['inputPassword']

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

    except Exception as e:
        return json.dumps({'error':str(e)})


if __name__ == "__main__":
    app.run()