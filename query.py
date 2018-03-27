def insert_favorite(email, course_id):
    return """
        INSERT INTO favorite (EMAIL, COURSE_ID)
        SELECT * FROM (SELECT '{email}', '{course_id}') AS TMP
        WHERE NOT EXISTS (
	    SELECT * FROM favorite WHERE EMAIL = '{email}' AND COURSE_ID = '{course_id}'
        ) LIMIT 1""".format(email = email, course_id = course_id)

def update_favorite(email, old_course_id, new_course_id):
    return """
        UPDATE favorite
        SET COURSE_ID = '{new_course_id}'
        WHERE EMAIL = '{email}' AND COURSE_ID = '{old_course_id}'
    """.format(email=email, old_course_id=old_course_id, new_course_id=new_course_id)

def remove_favorite(email, course_id):
    return """
        DELETE FROM favorite
        WHERE EMAIL = '{email}' AND COURSE_ID = '{course_id}'
    """.format(email=email, course_id=course_id)

def aggregate_sections_grade(subject_name, subject_number):
    return """
        SELECT SUM(ap) as ap, SUM(a) as a, SUM(am) as am, SUM(bp) as bp, SUM(b) as b, \
               SUM(bm) as bm, SUM(cp) as cp, SUM(c) as c, SUM(cm) as cm, SUM(dp) as dp, \
               SUM(d) as d, SUM(dm) as dm, SUM(f) as f, SUM(w) as w, instructor, semester
        FROM raw
        WHERE `subject`='{subject_name}' AND number='{subject_number}'
        GROUP BY instructor, semester, `subject`, number
    """.format(subject_name = subject_name, subject_number = subject_number)
