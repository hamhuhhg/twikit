import sqlite3

def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect('twitter_accounts.db')
        print(f'successful connection with sqlite version {sqlite3.version}')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    """
    try:
        sql_create_accounts_table = """ CREATE TABLE IF NOT EXISTS accounts (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        email text NOT NULL,
                                        password text NOT NULL,
                                        account_type text NOT NULL
                                    ); """
        c = conn.cursor()
        c.execute(sql_create_accounts_table)
    except sqlite3.Error as e:
        print(e)

def main():
    conn = create_connection()

    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
