def get_subject(subject): # Group By
    return """  
        SELECT DISTINCT subject, number, MIN(title), ROUND(AVG(overall_gpa), 2) FROM course \
        WHERE subject='{subject}' \
        GROUP BY subject, number
        ;
    """.format(subject = subject)


def get_favorite(email): # join 
    return """
        SELECT favorite.course_sub, favorite.course_num, course.title, course.overall_gpa
        FROM favorite INNER JOIN course ON 
        favorite.COURSE_SUB = course.Subject AND favorite.COURSE_NUM = course.NUMBER
        where favorite.EMAIL = '{email}' 
        ;
    """.format(email = email)

def insert_favorite(email, course_sub, course_num):
    return """
        INSERT INTO favorite (EMAIL, COURSE_SUB, COURSE_NUM)
        SELECT * FROM (SELECT '{email}', '{course_sub}', '{course_num}') AS TMP
        WHERE NOT EXISTS (
	    SELECT * FROM favorite WHERE EMAIL = '{email}' \
                AND COURSE_SUB = '{course_sub}' AND COURSE_NUM = '{course_num}'
        ) LIMIT 1""".format(email=email, course_num = course_num, course_sub=course_sub)

def update_favorite(email, old_course_sub, old_course_num, new_course_sub, new_course_num):
    return """
        UPDATE favorite
        SET COURSE_SUB = '{new_course_sub}', COURSE_NUM = '{new_course_num}'
        WHERE EMAIL = '{email}' AND COURSE_SUB = '{old_course_sub}' AND COURSE_NUM = '{old_course_num}'
    """.format(email=email, old_course_sub=old_course_sub, old_course_num=old_course_num, new_course_sub=new_course_sub, new_course_num=new_course_num)

def remove_favorite(email, course_sub, course_num):
    return """
        DELETE FROM favorite
        WHERE EMAIL = '{email}' AND COURSE_SUB = '{course_sub}' AND COURSE_NUM = '{course_num}'
    """.format(email=email, course_sub=course_sub, course_num=course_num)

def aggregate_sections_grade(subject_name, subject_number): # Group By
    return """
        SELECT SUM(ap) as ap, SUM(a) as a, SUM(am) as am, SUM(bp) as bp, SUM(b) as b, \
               SUM(bm) as bm, SUM(cp) as cp, SUM(c) as c, SUM(cm) as cm, SUM(dp) as dp, \
               SUM(d) as d, SUM(dm) as dm, SUM(f) as f, SUM(w) as w, instructor, semester\
        FROM raw
        WHERE `subject`='CS' AND number='411'
        GROUP BY instructor, semester, `subject`, number
    """.format(subject_name = subject_name, subject_number = subject_number)
