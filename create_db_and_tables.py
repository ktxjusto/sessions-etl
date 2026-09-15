import psycopg

def create_db(): 
    try:
        #connect to the default database
        conn = psycopg.connect(
            host = '127.0.0.1',
            user = 'postgres',
            password = '',
            dbname = 'postgres',
            port = '5432',
            autocommit=True
        )

        cursor = conn.cursor()

        print('Connection successful')
        #connect to the new sessions specific database
        cursor.execute("CREATE DATABASE sessions;")
        print("Database sessions created successfully!")

        conn.close()

        print("Connection Closed")

    except Exception as e:
        print(f"Error with database creation: {e}")

def create_table(): 
    try:

        #connect to the new database
        conn = psycopg.connect(
            host = '127.0.0.1',
            user = 'postgres',
            password = '',
            dbname = 'sessions',
            port = '5432',
            autocommit=True
        )

        cursor = conn.cursor()

        print('Connection successful to the sessions')

        # create the tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_session_logs (
                date DATE,
                name VARCHAR(250),
                start_time INTEGER,
                end_time INTEGER
            );
        """)
        print("Table raw_session_logs created successfully!")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enriched_session_logs (
                session_id SERIAL PRIMARY KEY,
                name VARCHAR(250),
                start_time TIMESTAMP,
                end_time TIMESTAMP
            );
        """)
        
        print("Table enriched_session_logs created successfully!")

        conn.close()

        print("Connection Closed")

    except Exception as e:
        print(f"Error with table creation: {e}")

def ddl():
    create_db()
    create_table()
