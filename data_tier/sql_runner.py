import psycopg2

from downloader import config


def run_sql_file(filename: str):

    db_config = config.config.database

    # Connect to the database
    conn = psycopg2.connect(
        host=db_config.host,
        dbname="postgres",
        user=db_config.user,
        password=db_config.password,
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # SQL script
    with open(filename, "r", encoding="utf-8") as f:
        create_script = f.read()

    # Execute the SQL script
    cur.execute(create_script)

    # Commit changes
    conn.commit()

    # Close communication
    cur.close()
    conn.close()
