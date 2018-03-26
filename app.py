from flask import Flask, Response, render_template, json, request, redirect, abort, session, jsonify, flash
from flaskext.mysql import MySQL
import json, sys
from werkzeug import generate_password_hash, check_password_hash
from flask_sslify import SSLify
import re


mysql = MySQL()
app = Flask(__name__)
# sslify = SSLify(app)
ac_cache = None

# # MySQL configurations
# if "yuanyiz2" in __file__:
#     app.config['MYSQL_DATABASE_USER'] = 'yuanyiz2_root'
#     app.config['MYSQL_DATABASE_PASSWORD'] = '12345root'
#     app.config['MYSQL_DATABASE_DB'] = 'yuanyiz2_baseless'
# else:
# # if(sys.platform == 'linux' or sys.platform == 'darwin'):
#     app.config['MYSQL_DATABASE_USER'] = 'root'
#     app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#     app.config['MYSQL_DATABASE_DB'] = 'baselessdata_db'
#     # sslify = SSLify(app)
#     SSLify(app)


app.config['MYSQL_DATABASE_USER'] = 'tianyu'
app.config['MYSQL_DATABASE_PASSWORD'] = '515253'
app.config['MYSQL_DATABASE_DB'] = 'project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = 'whatever'

mysql.init_app(app)


def get_data_from_sql(q):
    conn = mysql.connect(); cur = conn.cursor()
    if(type(q) == str): cur.execute(q)
    else: cur.execute(q[0], q[1:])

    data = cur.fetchall()
    conn.close(); cur.close()
    return data

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    global ac_cache
    search = request.args.get('q_course').upper()
    regex_ = re.compile('.*' + '\s*'.join([i for i in search]) + '.*')

    if ac_cache == None: 
        q = "SELECT DISTINCT subject, number FROM `raw`"
        all_data = get_data_from_sql(q)
        ac_cache = [d[0] + ' ' + str(d[1]) for d in all_data]

    results = filter(regex_.match, ac_cache)
    results = [i for i in results][:5]
    return jsonify(matching_courses=results)

@app.route('/search', methods=['POST', 'GET'])
def search():
    search_q = request.form['q'].upper()
    parts = re.split('(\d.*)', search_q)
    try:
        sbj, number = parts[0].strip(), parts[1].strip()
        print("You just searched", sbj, number)
        q = ["SELECT * FROM `raw` WHERE subject = (%s) AND number = (%s)", sbj, number]
        print(q)
        course_info = get_data_from_sql(q)
        print(course_info)
    except:
        course_info=None
    return render_template("course_info.html", pageType='other', course_info=course_info)

@app.route('/explore')
def explore():
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
                flash('Ohhh poor little guy that strays!', 'success')

            elif not check_password_hash(data[0][1], _password):
                error = 'Seems like you forgot your password, so miserable.'
            else: 
                flash('Why come back? Nothing has been updated.', 'success')
        else: error = 'FILL OUT THE FORMS!' # Not used here: js already checked required fields
        
        if (error): flash(error, 'error')
        else:       session['user'] = _email.split("@")[0]

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

@app.route('/getall')
def getall():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT subject, ROUND(AVG(overall_gpa), 2) as avg_gpa FROM course GROUP BY subject")
    data = cursor.fetchall()

    empList = []
    for emp in data:
        empDict = {
            'subject': emp[0],
            'avg_gpa': emp[1]
        }
        empList.append(empDict)

    return json.dumps(empList)

@app.route('/get_subject')
def get_subject():
    subject = request.args.get('subject', None)

    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM course WHERE subject= %s", subject)
    course_list = cursor.fetchall()

    return render_template('course.html', course_list=course_list)

@app.route('/')
def main():
    return render_template('index.html', pageType='index')

if __name__ == "__main__":

    if(sys.platform=='linux'): app.run(host='0.0.0.0', port=80, use_reloader=True, threaded=True)
    else: app.run(debug=True, port=5001)
