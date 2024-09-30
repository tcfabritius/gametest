import mysql.connector
from geopy import distance


connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='user',
         password='user',
         autocommit=True
         )


iso_country = "FI"
cursor = connection.cursor()
cursor.execute("SELECT ident, name FROM airport WHERE iso_country = %s ORDER BY RAND() LIMIT 10;", (iso_country,))
taulukko = cursor.fetchall()
print(taulukko)

