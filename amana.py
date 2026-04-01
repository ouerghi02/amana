import mysql.connector # type: ignore

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="amana_db"
)

cursor = db.cursor()
cursor.execute("SELECT * FROM ma_table")