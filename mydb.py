import psycopg2

database = psycopg2.connect("dbname=djangocrm", user="eyji", password="eyji", host="localhost", port="5432")

cursor = database.cursor()
