import os
import mysql.connector as mariadb
from mysql.connector import errorcode

config = {
    'user': 'ste',
    'password': 'ste',
    'host': 'localhost',
    'database': 'IronDB',
    'raise_on_warnings': True
}


def get_user(user_to_search: str) -> dict:
    successful_query: False
    error = ''  # will store eventual error codes
    added_new_user = True

    get_username_query = '''
        SELECT username
        FROM users
        WHERE username = '{0}';'''.format(user_to_search)
    insert_username_query = '''
        INSERT INTO users(username)
        VALUES('{0}');'''.format(user_to_search)

    try:
        db = mariadb.connect(**config)
        cursor = db.cursor(buffered=True)
        cursor.execute(get_username_query)

        if not cursor.rowcount:
            added_new_user = False
            cursor.execute(insert_username_query)
            db.commit()

        successful_query = True

    except mariadb.Error as err:
        error = err.errno

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        error = err

    finally:
        cursor.close()
        db.close()

        return {'successful_query': successful_query, 'error': error, 'data': added_new_user}


def insert_new_question(question: str, right_answer: str, wrong_answer: str) -> dict:
    successful_query: False
    error = ''  # will store eventual error codes

    insert_new_question_query = '''
    INSERT INTO questions(question, right_answer, wrong_answer) 
    VALUES('{0}','{1}','{2}')
    '''.format(question, right_answer, wrong_answer)

    try:
        db = mariadb.connect(**config)
        cursor = db.cursor()
        cursor.execute(insert_new_question_query)
        db.commit()

        successful_query = True

    except mariadb.Error as err:
        error = err
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            successful_query = False

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            successful_query = False

        else:
            print(err)
            successful_query = False
    finally:
        cursor.close()
        db.close()

        return {'successful_query': successful_query, 'error': error}


def get_current_question() -> dict:
    successful_query: False
    error = ''  # will store eventual error codes
    question_data = {}

    query = '''
    SELECT id, question, right_answer, wrong_answer
    FROM questions
    WHERE answered = FALSE
    LIMIT 1
    '''

    try:
        db = mariadb.connect(**config)
        cursor = db.cursor(buffered=True)
        cursor.execute(query)
        current_answer = cursor.fetchone()

        if cursor.rowcount:
            question_data['id'] = current_answer[0]
            question_data['question'] = current_answer[1]
            question_data['right_answer'] = current_answer[2]
            question_data['wrong_answer'] = current_answer[3]

        successful_query = True

    except mariadb.Error as err:
        error = err
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        cursor.close()
        db.close()

        return {'successful_query': successful_query, 'error': error, 'data': question_data}


def book_answer(username: str, question_id: int) -> bool:
    successful_query: False
    error = ''  # will store eventual error codes

    get_placement_query = '''
    SELECT MAX(placement) AS max_placement
    FROM answering_queue
    WHERE answering_queue_questions_id = {0}
    '''.format(question_id)
    placement = 1

    try:
        db = mariadb.connect(**config)
        cursor = db.cursor(buffered=True)
        cursor.execute(get_placement_query)
        max_placement = cursor.fetchone()[0]

        if cursor.rowcount:
            if max_placement == None:
                placement = 1
            else:
                placement += max_placement

        book_answer_query = '''
            INSERT INTO answering_queue(placement, answering_queue_questions_id, answering_queue_users_username)
            VALUES('{0}', '{1}', '{2}')
            '''.format(placement, question_id, username)

        cursor.execute(book_answer_query)
        db.commit()

        successful_query = True

    except mariadb.Error as err:
        error = err
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        cursor.close()
        db.close()

        return {'successful_query': successful_query, 'error': error}


if __name__ == "__main__":
    db_host = os.environ.get('DB_HOST')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')

    print('''
    db_host: {0}
    db_user: {1}
    db password: {2}
    db name: {3}
    '''.format(db_host, db_user, db_password, db_name))

    try:
        db = mariadb.connect(**config)
        print("connected to database {0}".format(config['database']))

        cursor = db.cursor(buffered=True)
        query = ('''
        SELECT * FROM users;
        ''')

        records = {}

        cursor.execute(query)
        result = cursor.fetchall()
        print("result: {0}, type: {1}".format(result, type(result)))

    except mariadb.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        db.close()
        print('connection closed')
