from flask import Flask, Response, render_template, json, request, redirect, abort, session, jsonify, flash
from flaskext.mysql import MySQL
import simplejson as json
import sys
from werkzeug import generate_password_hash, check_password_hash
from flask_sslify import SSLify
import re

import query

mysql = MySQL()
app = Flask(__name__)
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

@app.route('/autocomplete', methods=['GET', 'POST'])
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

@app.route('/search', methods=['GET'])
def search():
    search_q = request.args['q'].upper()
    parts = re.split('(\d.*)', search_q)
    try:
        sbj, number = parts[0].strip(), parts[1].strip()
        print("You just searched", sbj, number)
        # q = ["SELECT * FROM `raw` WHERE subject = (%s) AND number = (%s)", sbj, number]
        # print(q)
        course_info = get_data_from_sql(query.aggregate_sections_grade(sbj, number))
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


@app.route('/tableview')
def tableview():
    # Subject, Number, Title, GPA,
    items = [['CS', '411', 'Database', '4.0'],
             ['CS', '412', 'Introduction to Data Mining', '4.0']]
    is_fav = [False,
              True]
    # is_fav = ['False',
    #           'True']
    return render_template("tableview.html", pageType='tableview', items=items, is_fav=is_fav)


####### Fav_course #######
@app.route('/fav_course', methods=['GET'])
def fav_course():
    # TODO: replace below with actual db search
    # items = [['CS', '411', '4.0']]
    q = query.get_favorite(session['user'])
    items = get_data_from_sql(q)
    print (items)
    # cur = g.db.execute('select title, text from entries order by id desc')
    # items = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template("fav_course.html", pageType='account', items=items)

@app.route('/fav_course/add/<course_id>', )
def insert_table(course_id):
    replace_id = request.args.get('replace', default=None)
    if(not replace_id): # insert
        print ("fav insert", course_id, replace_id)
        q = query.insert_favorite(email=session['user'], course_id=course_id)
    else:
        print ("fav replace", course_id, replace_id)
        q = query.update_favorite(email=session['user'], old_course_id=replace_id, new_course_id=course_id) # update
    print (q)
    # get_data_from_sql(q)
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute(q)
    conn.commit()
    # cursor.fetchall()
    return redirect('/fav_course')

@app.route('/fav_course/del/<course_id>', )
def delete_table(course_id):
    q = query.remove_favorite(email=session['user'], course_id=course_id)
    # get_data_from_sql(q)
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute(q)
    conn.commit()
    return redirect('/fav_course')


###############################

@app.route('/signUp', methods=['POST'])
def signUp():
    _email = request.form['email']
    _password = request.form['password']
    cur, conn = None, None
    error = None
    try:
        # validate the received values
        if _email and _password:
            conn = mysql.get_db()
            cur = conn.cursor()
            # check user existence first
            q = "SELECT * FROM tbl_user WHERE email=\"{}\";".format(_email)
            cur.execute(q)
            data = cur.fetchall()

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
        else:
            session['user'] = _email
            session['uname'] = _email.split("@")[0]
        return redirect('/')

    except Exception as e:
        print ("Error:", e)
        abort(401)

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
            'avg_gpa': float(emp[1])
        }
        empList.append(empDict)

    return json.dumps(empList)

@app.route('/get_subject')
def get_subject():
    subject = request.args.get('subject', None)
    cursor = mysql.connect().cursor()
    # cursor.execute("SELECT * FROM course WHERE subject= %s", subject)
    # course_list = cursor.fetchall()

    # return render_template('course_list.html', course_list=course_list)
    cursor.execute("SELECT DISTINCT subject,number,title FROM raw WHERE subject=%s", subject)
    course_list = cursor.fetchall()
    print (course_list)
    is_fav = [False] * len(course_list)
    return render_template('tableview.html', items=course_list, is_fav=is_fav) 
 
@app.route('/course_info')
def course_info():
    subject = request.args.get('subject', None)
    number = request.args.get('number', None)
    title = request.args.get('title', None)

    q = "SELECT subject, number, crn, title, SUM(ap), SUM(a), SUM(am), SUM(bp), SUM(b), SUM(bm), SUM(cp), SUM(c), SUM(cm), \
        SUM(dp), SUM(d), SUM(dm), SUM(f), SUM(w), instructor, semester FROM `raw` \
        WHERE subject = '%s' AND number = %s AND title LIKE '%s%%' GROUP BY semester, instructor" % (subject, number, title)
    course_info = get_data_from_sql(q)
    print(q)
    empList = []
    for emp in course_info:
        empDict = {
            'subject': emp[0], 'number': emp[1], 'crn': emp[2], 'title': emp[3],
            'ap': emp[4], 'a': emp[5], 'am': emp[6], 
            'bp': emp[7], 'b': emp[8], 'bm': emp[9],
            'cp': emp[10], 'c': emp[11], 'cm': emp[12],
            'dp': emp[13], 'd': emp[14], 'dm': emp[15], 
            'f': emp[16], 'w': emp[17],
            'instructor': emp[18], 'semester': emp[19]
        }
        empList.append(empDict)

    return json.dumps(empList)

@app.route('/course')
def course():
    subject = request.args.get('subject', None)
    number = request.args.get('number', None)
    title = request.args.get('title', None)

    return render_template('course_detail.html', subject=subject, number=number, title=title)

@app.route('/')
def main():
    return render_template('index.html', pageType='index')

if __name__ == "__main__":

    if(sys.platform=='linux'): app.run(host='0.0.0.0', port=80, use_reloader=True, threaded=True)
    else: app.run(debug=True, port=5001)
