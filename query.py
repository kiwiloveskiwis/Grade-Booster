def get_favorite(email):
    return """
        SELECT * FROM favorite WHERE EMAIL = '{email}';
    """.format(email = email)

def insert_favorite(email, course_id):
    return """
        INSERT INTO favorite (EMAIL, COURSE_ID)
        SELECT * FROM (SELECT '{email}', '{course_id}') AS TMP
        WHERE NOT EXISTS (
	    SELECT * FROM favorite WHERE EMAIL = '{email}' AND COURSE_ID = '{course_id}'
        ) LIMIT 1
        """.format(email = email, course_id = course_id)

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
