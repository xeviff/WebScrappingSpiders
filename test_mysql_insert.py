import mysql.connector
from datetime import datetime

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

cnx = mysql.connector.connect(
    user='root', password='1234',
    host='192.168.1.22', port=33066,
    database='departiculares_spider'
)

c1 = cnx.cursor()
c1.execute("INSERT INTO anuncis (titol, url, cerca, data_update, descripcio) VALUES (%s,%s,%s,%s,%s)", 
['prova', 'prova', 'prova', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'prova'])
c1.close()

c2 = cnx.cursor()
c2.execute("INSERT INTO anuncis (titol, url, cerca, data_update, descripcio) VALUES (%s,%s,%s,%s,%s)", 
['prova2', 'prova2', 'prova2', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'prova2'])
c2.close()

cnx.commit()
cnx.close()