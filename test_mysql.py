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
titol = "Piso en Alquiler en Carrer Cervantes de Òdena, Pisos Òdena"
url = "https://www.fotocasa.es/es/alquiler/vivienda/odena/parking-terraza-trastero/176573781/d?tti=3&ppi=3&xtor=AF-10012-[departiculares]-[general]-[NA]-[NA]-[NA]"
c1.execute("SELECT count(*) FROM anuncis WHERE titol = %s AND url = %s", [titol, url])
myresult = c1.fetchone()

if (myresult[0] > 0):
    print("yes fuck")

c1.close()
cnx.close()