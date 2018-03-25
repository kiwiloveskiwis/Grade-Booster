from flask import Flask, Response, render_template, json, request, redirect, abort, session, jsonify
from flaskext.mysql import MySQL
import json
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


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q_course')
    print(search)
    # query = db_session.query(Course.title).filter(Course.title.like('%' + str(search) + '%'))
    # TODO: replace below with above
    results = ['CS411', 'CS543'] # just to check the autocompletion works
    return jsonify(matching_courses=results)

@app.route('/search', methods=['POST', 'GET'])
def search():
    search_q = request.form['q']
    # TODO: replace below with search from db
    print("You just searched", search_q)
    return main();


@app.route('/explore')
def explore():
    cursor = mysql.connect().cursor()
    # TODO: replace below with random search from db
    cursor.execute("SELECT * from `Gene`")
    data = cursor.fetchone()
    print(data)
    return render_template("explore.html", pageType='explore')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    return render_template("index.html", pageType='account')

@app.route('/fav_course', methods=['POST', 'GET'])
def fav_course():
    # TODO: replace below with actual db search
    items = [['hey', 'how are you', '4.0']]
    # cur = g.db.execute('select title, text from entries order by id desc')
    # items = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template("fav_course.html", pageType='account', items=items)

@app.route('/signUp', methods=['POST'])
def signUp():
    _email = request.form['email']
    _password = request.form['password']
    print(_email, _password)
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

@app.route('/')
def main():
    return render_template('index.html', pageType='index')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
