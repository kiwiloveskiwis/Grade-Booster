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
if "yuanyiz2" in __file__:
    app.config['MYSQL_DATABASE_USER'] = 'yuanyiz2_root'
    app.config['MYSQL_DATABASE_PASSWORD'] = '12345root'
    app.config['MYSQL_DATABASE_DB'] = 'yuanyiz2_baseless'
    app.config['SECRET_KEY'] = 'whatever'
elif(sys.platform == 'linux' or sys.platform == 'darwin'):
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
    app.config['MYSQL_DATABASE_DB'] = 'baselessdata_db'
    app.config['SECRET_KEY'] = 'whatever'
    SSLify(app)
# else:
#     app.config['MYSQL_DATABASE_USER'] = 'tianyu'
#     app.config['MYSQL_DATABASE_PASSWORD'] = '515253'
#     app.config['MYSQL_DATABASE_DB'] = 'project'
#     app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


def get_data_from_sql(q, commit=False):
    conn = mysql.get_db(); 
    cur = conn.cursor()
    if(type(q) == str): cur.execute(q)
    else: cur.execute(q[0], q[1:])

    data = cur.fetchall()
    if(commit): conn.commit()
    return data

@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    global ac_cache
    search = request.args.get('q_course').upper()
    regex_ = re.compile('.*' + '\s*'.join([i for i in search]) + '.*')

    if ac_cache == None:
        q = "SELECT DISTINCT subject, number FROM `course`"
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
        if(len(parts) == 1): return redirect('/get_subject?subject=%s'%parts[0].strip())
        sbj, number = parts[0].strip(), parts[1].strip()
    except:
        course_info=None
    return redirect('/course?subject=%s&number=%s'%(sbj, number))

@app.route('/explore')
def explore():
    return render_template("explore.html", pageType='explore')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    return render_template("profile.html", pageType='account')

####### Fav_course #######

@app.route('/fav_course', methods=['GET'])
def fav_course():
    # check_user_login()
    if 'user' not in session: flash('SIGN IN FIRST!', 'error'); return redirect('/')
    items = get_data_from_sql(query.get_favorite(session['user']))
    is_fav = [True] * len(items)
    return render_template("tableview.html", pageType='account', items=items, is_fav=is_fav, edit=True)

@app.route('/fav_course/add', )
def insert_table():
    if 'user' not in session: flash('SIGN IN FIRST!', 'error'); return redirect('/')
    sub = request.args.get('sub', default=None)
    num = request.args.get('num', default=None)
    newsub = request.args.get('newsub', default=None)
    newnum = request.args.get('newnum', default=None)

    if not newsub or not newnum: # Not Update => Insert
        q = query.insert_favorite(email=session['user'], course_sub=sub, course_num=num)
        get_data_from_sql(q, commit=True)
    else:
        isValid = get_data_from_sql(query.valid_course_not_in_fav(newsub, newnum, session['user']))
        if isValid:
            q = query.update_favorite(email=session['user'], old_course_sub=sub, old_course_num=num, new_course_sub=newsub, new_course_num=newnum) # update
            get_data_from_sql(q, commit=True)
        else:
            flash('Invalid Course Subject or Number!', 'error');
    return redirect(request.referrer if request.referrer else '/fav_course')

@app.route('/fav_course/del', )
def delete_table():
    if 'user' not in session: flash('SIGN IN FIRST!', 'error'); return redirect('/')
    sub = request.args.get('sub', default=None)
    num = request.args.get('num', default=None)
    q = query.remove_favorite(email=session['user'], course_sub=sub, course_num=num)
    get_data_from_sql(q, commit=True)
    return redirect(request.referrer if request.referrer else '/fav_course')


###############################

@app.route('/signUp', methods=['POST'])
def signUp():
    _email = request.form['email']
    _password = request.form['password']
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
    session.pop('user', None)
    return redirect('/')


############## End of SignUp ############
############## Course information ############

@app.route('/getall')
def getall():
    q = "SELECT subject, ROUND(AVG(overall_gpa), 2) as avg_gpa FROM course GROUP BY subject"
    data = get_data_from_sql(q)

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
    course_list = get_data_from_sql(query.get_subject(subject))

    if 'user' in session:
        fav_list = { (_[0],_[1]) for _ in get_data_from_sql(query.get_favorite(session['user'])) }
        is_fav = [(_[0],_[1]) in fav_list for _ in course_list]
    else:
        is_fav = [False] * len(course_list)
    return render_template('tableview.html', items=course_list, is_fav=is_fav, edit=False) 
 
@app.route('/course_info')
def course_info():
    subject = request.args.get('subject', None)
    number = request.args.get('number', None)
    title = request.args.get('title', None)

    q = "SELECT MIN(subject), min(number), min(crn), min(title), SUM(ap), SUM(a), SUM(am), SUM(bp), SUM(b), SUM(bm), SUM(cp), SUM(c), SUM(cm), \
        SUM(dp), SUM(d), SUM(dm), SUM(f), SUM(w), instructor, semester FROM `raw` \
        WHERE subject = '%s' AND number = %s  GROUP BY semester, instructor" % (subject, number)
    course_info = get_data_from_sql(q)
    # print(course_info)
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
    title = request.args.get('title', \
         get_data_from_sql(query.find_course_instructor(subject, number))[0][0])
    is_fav = False

    if 'user' in session:
        q = """
            SELECT *
            FROM favorite 
            where EMAIL = '{email}' AND COURSE_SUB = '{subject}' AND COURSE_NUM = '{number}'
            """.format(email = session['user'], subject=subject, number=number)
        data=get_data_from_sql(q)
        if(data): is_fav = True
        print(is_fav)
    return render_template('course_detail.html', subject=subject, number=number, title=title, is_fav=is_fav)

############## Bipartite Graph ##############

@app.route('/graph')
def graph():
    json_data = json.load(open('static/config.json','r'))
    json_data = json.dumps(json_data)
    # print (json_data)
    # json_data = jsonify(json_data)
    return render_template("graph.html", pageType='graph', json_data=json_data)

@app.route('/graph_objects')
def graph_objects():

    course_info = get_data_from_sql("""SELECT DISTINCT instructor, subject, number 
        from raw 
        WHERE subject="CS" AND instructor is not Null 
        """)
    inst2course, course2inst = query.advance_fun2(course_info)
    d = { 'data': {}, 'errors': [] }
    for inst,course in inst2course.items():
        d['data'][inst] = {
            'name': inst,
            'type': 'group0',
            'depends': course,
            'dependedOnBy': [],
            'docs': 'Sounds good...'
        }
    for course,inst in course2inst.items():
        d['data'][course] = {
            'name': course,
            'type': 'group1',
            'depends': [],
            'dependedOnBy': inst,
            'docs': 'Sounds Good...'
        }
    return json.dumps(d)

############## Main ##############

@app.route('/')
def main():
    return render_template('index.html', pageType='index')

if __name__ == "__main__":

    if(sys.platform=='linux'): app.run(host='0.0.0.0', port=80, use_reloader=True, threaded=True)
    else: app.run(debug=True, port=5001)
