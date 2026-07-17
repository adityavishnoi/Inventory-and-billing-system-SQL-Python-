import psycopg2

def connection():
    con=psycopg2.connect(
        host="localhost",
        database="ecommerce",
        user="postgres",
        password="",
        port="5432"
    )
    if con:
        print(">>>>>> Connnection Established")
    else:
        print(">>>>>> Connection is not Established")
    return con
conn =connection()
