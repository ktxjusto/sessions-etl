import psycopg
from create_db_and_tables import ddl


#connect to the db server
def connect_to_db(): 
    try:

        conn = psycopg.connect(
            host = '127.0.0.1',
            user = 'postgres',
            password = '',
            dbname = 'sessions',
            port = '5432',
            autocommit=True
        )

        cursor = conn.cursor()

        print('Connection successful')

        return cursor
    except Exception as e:
        print(f"Error with database connection: {e}")

#load the csv data into the staging table
def extract(cursor):
    try:   
        print("Beginning the extaction of the raw csv data into the staging table")
        with open('sessions.csv', 'r') as f, cursor.copy(
            "COPY raw_session_logs (date, name, start_time, end_time) FROM STDIN WITH (FORMAT csv, HEADER true)"
        ) as copy:
            while data := f.read(8192):
                copy.write(data)

        print("Successfully extracted the raw CSV data into the staging table in the DB")

    except Exception as e:
        print(f"Error with the extraction step:{e}")

def transform_and_load(cursor):
    try:
        print("Beginning transform and loading")
        cursor.execute("""
            INSERT INTO enriched_session_logs (name, start_time, end_time)
                SELECT
                    name,
                    date + make_interval(secs => start_time) AS start_time,
                    date + make_interval(secs => end_time) AS end_time
                FROM raw_session_logs
                WHERE start_time IS NOT NULL
                AND end_time IS NOT NULL

                UNION ALL

                SELECT
                    a.name,
                    a.date + make_interval(secs => a.start_time) AS start_time,
                    b.date + make_interval(secs => b.end_time) AS end_time
                FROM raw_session_logs a
                JOIN raw_session_logs b
                ON b.name = a.name
                AND b.date = a.date + INTERVAL '1 day'
                AND a.end_time IS NULL
                AND b.start_time IS NULL
                WHERE a.start_time IS NOT NULL
                AND b.end_time IS NOT NULL;
        """
        )
        print("Successfully transformed and loaded the raw data into the enriched_session_logs table")
    except Exception as e:
        print(f"Error with Transformaions: {e}")

def main():
    ddl()
    cursor = connect_to_db()
    extract(cursor)
    transform_and_load(cursor)
    cursor.close()

if __name__ == "__main__":
    main()
