import mysql.connector
from datetime import datetime
import webbrowser

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

cnx = mysql.connector.connect(
    user='root', password='1234',
    host='192.168.1.22', port=33066,
    database='departiculares_spider'
)

c1 = cnx.cursor()
c1.execute("SELECT url FROM anuncis WHERE actiu=1 AND veure_mes_tard=0")
myresult = c1.fetchall()

for x in myresult:
  webbrowser.open(x[0])

c1.close()

cnx.close()