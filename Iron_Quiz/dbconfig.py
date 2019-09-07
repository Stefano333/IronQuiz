import os
import mysql.connector as mariadb

config = {
    'user': 'ste',
    'password': 'ste',
    'host': 'localhost',
    'database': 'IronDB',
    'raise_on_warnings': True
}


def get_query(query: str) -> dict:
    try:
        db = mariadb.connect(**config)
        cursor = db.cursor()
        return cursor.execute(query)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


if __name__ == "__main__":
    db_host = os.environ.get('DB_HOST')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')

    try:
        db = mariadb.connect(**config)
        print("connected to database {0}".format(config['database']))

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        db.close()
        print('connection closed')
