import psycopg2, subprocess, os

#make sure postgres server is running
commands = ['sudo service postgresql start', 'sudo service postgresql status']
for command in commands:
    result = subprocess.run(command.split(), capture_output=True, text=True)
    print(result.stdout)
    
if not 'online' in result.stdout:
    raise RuntimeError("postgres service not running")

# Establish a connection to the PostgreSQL server
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    host="localhost",
    password=os.environ['POSTGRES_PW']
)

# Set autocommit to True
conn.autocommit = True

# Open a cursor to perform database operations
cur = conn.cursor()

# Terminate all connections to the "myuz" database
cur.execute("""
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = 'myuz';
""")

# Drop the "myuz" database if it exists
cur.execute("DROP DATABASE IF EXISTS myuz;")

# Create a new "myuz" database
cur.execute("CREATE DATABASE myuz;")

admin_user=os.environ['MYUZ_DB_USER']
admin_pw=os.environ['MYUZ_DB_PW']

# Grant all privileges on the "myuz" database to the "sryan" user
cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE myuz TO {admin_user};")

# Close the cursor and the connection
cur.close()
conn.close()
