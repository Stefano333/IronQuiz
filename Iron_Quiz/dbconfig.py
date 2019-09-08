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


def get_user(user_to_search: str) -> bool:
    get_username_query = '''
        SELECT username
        FROM users
        WHERE username = '{0}' '''.format(user_to_search)
    insert_username_query = '''
        INSERT INTO users(username)
        VALUES('{0}')'''.format(user_to_search)

    try:
        db = mariadb.connect(**config)
        cursor = db.cursor(buffered=True)
        print('search {0}'.format(user_to_search))
        cursor.execute(get_username_query)

        if not cursor.rowcount:
            print('insert {0}'.format(user_to_search))
            cursor.execute(insert_username_query)
            db.commit()

    except mariadb.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            print('ope')


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
        SELECT * FROM users WHERE username='imperialsoldier3'
        ''')

        records = {}

        # cursor.execute(query)
        cursor.execute("INSERT INTO users(username) VALUES('ciao')")
        db.commit()
        print(cursor.rowcount)

        for id, username in cursor:
            records[id] = username
            print("{0}: {1}".format(id, username))

        if(records):
            for id in records.keys():
                print("{0}: {1}".format(id, records[id]))
        else:
            print("no records")

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
