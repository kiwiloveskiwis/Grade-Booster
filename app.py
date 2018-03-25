from flask import Flask, Response, render_template, json, request, redirect, abort, session, jsonify, flash
from flaskext.mysql import MySQL
import json, sys
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
if(sys.platform == 'linux' or sys.platform == 'darwin'):
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
    app.config['MYSQL_DATABASE_DB'] = 'baselessdata_db'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['SECRET_KEY'] = 'whatever'
else:
    # app.config['MYSQL_DATABASE_USER'] = 'yuanyiz2_root'
    # app.config['MYSQL_DATABASE_PASSWORD'] = '12345root'
    # app.config['MYSQL_DATABASE_DB'] = 'yuanyiz2_baseless'
    pass


mysql.init_app(app)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q_course')
    print(search)
    # query = db_session.query(Course.title).filter(Course.title.like('%' + str(search) + '%'))
    # TODO: replace below with above
    results = ['CS 411', 'CS 543'] # just to check the autocompletion works
    return jsonify(matching_courses=results)

@app.route('/search', methods=['POST', 'GET'])
def search():
    search_q = request.form['q']
    # TODO: replace below with search from db
    print("You just searched", search_q)
    return main();


@app.route('/explore')
def explore():
    # cursor = mysql.connect().cursor()
    # TODO: replace below with random search from db
    # cursor.execute("SELECT * from `Gene`")
    # data = cursor.fetchone()
    # print(data)
    return render_template("explore.html", pageType='explore')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    return render_template("profile.html", pageType='account')

@app.route('/fav_course', methods=['POST', 'GET'])
def fav_course():
    # TODO: replace below with actual db search
    items = [['CS', '411', '4.0']]
    # cur = g.db.execute('select title, text from entries order by id desc')
    # items = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template("fav_course.html", pageType='account', items=items)

@app.route('/signUp', methods=['POST'])
def signUp():
    _email = request.form['email']
    _password = request.form['password']
    cur, conn = None, None
    error = None
    try:
        # validate the received values
        if _email and _password:
            conn = mysql.connect()
            cur = conn.cursor()
            # check user existence first
            q = "SELECT * FROM tbl_user WHERE email=\"{}\";".format(_email)
            print (q)
            cur.execute(q)
            data = cur.fetchall()
            print (data)

            if len(data) == 0: # user not exist: consider as sign up
                _hashed_password = generate_password_hash(_password)
                # print (_hashed_password)

                cur.callproc('sp_createUser', (_email, _hashed_password))
                conn.commit()
                flash('User created successfully!', 'success')

            elif not check_password_hash(data[0][1], _password):
                error = 'Wrong password!'
            else: 
                flash('Logged in successfully.', 'success')
        else: error = 'Enter the required fields!'
        # Not used here: js already checked required fields
        if (error): 
            flash(error, 'error')
            return redirect('/')
        else:
            session['user'] = _email.split("@")[0]
            return redirect('/')

    except Exception as e:
        print ("Error:", e)
        abort(401)
    finally:

        if cur is not None: cur.close() 
        if conn is not None: conn.close()

@app.route('/signOut')
def signOut():
    # if 'user' not in session:
    #     return redirect(url_for('signin'))
    session.pop('user', None)
    return redirect('/')
    # return render_template('index.html', pageType='index')

@app.route('/')
def main():
    return render_template('index.html', pageType='index')

if __name__ == "__main__":
    if(sys.platform=='linux'): app.run(host='0.0.0.0', port=80, use_reloader=True, threaded=True)
    else: app.run(debug=True, port=5001)