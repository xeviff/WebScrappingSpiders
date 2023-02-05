#coding: utf-8
import requests
import json
from bs4 import BeautifulSoup
import re
from time import sleep
import webbrowser
import mysql.connector
from datetime import datetime

cnx = mysql.connector.connect(
    user='root', password='1234',
    host='192.168.1.22', port=33066,
    database='departiculares_spider'
)

class Anunci:
    def __init__(self, json_text, preu_capturat):
        json_tree = json.loads(json_text, strict=False)
        self.titol = json_tree['name']
        self.descripcio = json_tree['description']
        self.url = json_tree['url']
        self.preu = preu_capturat

    def te_altura(self):
        regex = ".*.tic(o|\s|\.).*"
        compilador = re.compile(regex, re.IGNORECASE)
        atico = compilador.match(desc)
        regex = ".*d.plex.*"
        compilador = re.compile(regex, re.IGNORECASE)
        duplex = compilador.match(desc)
        return atico or duplex

    def te_piscina(self):
        regex = ".*pi(c|s|z)*ina.*"
        compilador = re.compile(regex, re.IGNORECASE)
        te = compilador.match(desc)
        return te

    def te_parquing(self):
        regex = ".*p.r(qu|k)in.*"
        compilador = re.compile(regex, re.IGNORECASE)
        te = compilador.match(desc)
        return te

    def te_traster(self):
        regex = ".*traster.*"
        compilador = re.compile(regex, re.IGNORECASE)
        te = compilador.match(desc)
        return te

    def es_chalet(self):
        regex = ".*(chalet|casa).*"
        compilador = re.compile(regex, re.IGNORECASE)
        te = compilador.match(titol)
        return te


cerca = "parquing_altura"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}
base_url = "https://www.departiculares.com/alquiler/barcelona&priceMax=1000"

def tractar_anunci(anunci):
    c0 = cnx.cursor()
    c0.execute("SELECT count(*) FROM anuncis WHERE titol=%s", [anunci.titol])
    existance_count = c0.fetchone()
    if existance_count[0] > 0:
        print("--- Preexistent ---")
    else:
        c1 = cnx.cursor()
        c1.execute("INSERT INTO anuncis (titol, preu, url, cerca, data_update, descripcio) VALUES (%s,%s,%s,%s,%s,%s)", [anunci_seleccionat.titol, anunci_seleccionat.preu, anunci_seleccionat.url, cerca, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), anunci_seleccionat.descripcio])
        c1.close()
        cnx.commit()
        print("--- Guardat a BD ---")
    c0.close()
    

pagina = 1
pagina_horitzo = 2
while pagina < pagina_horitzo:
    print("Aranya visitant pàgina " + str(pagina))
    cua_url = ""
    if pagina > 1:
        cua_url = "&page=" + str(pagina)
    url = base_url + cua_url

    respuesta = requests.get(url, headers=headers)
    soup = BeautifulSoup(respuesta.text, features="lxml")
    resultats = soup.find('ul', class_="list-results")
    if resultats is not None:
        resultats_item = resultats.find_all('li', class_="list-result-item")
        anuncis_list = []

        for resultat_item in resultats_item:
            preu_txt = resultat_item.find('p', class_="details-price")
            preu = -1
            if preu_txt is not None:
                preu = int(preu_txt.text.strip().replace('.', '').replace('€', ''))

            if preu > 400:
                res_json = resultat_item.find('script', type='application/ld+json')
                anunci = Anunci(res_json.string, preu)
                titol = anunci.titol
                desc = anunci.descripcio

                if anunci.te_parquing():
                    anuncis_list.append(anunci)

        for anunci_seleccionat in anuncis_list:
            print("** Anunci **")
            print("Títol: " + anunci_seleccionat.titol)
            print("Descripció: " + anunci_seleccionat.descripcio)
            print("Url: ")
            print(anunci_seleccionat.url)
            if anunci_seleccionat.preu > 0:
                print("Preu: " + str(anunci_seleccionat.preu))
            print("************")
            tractar_anunci(anunci_seleccionat)

        resultats = soup.find('ul', class_="pager")
        resultats_item = resultats.find_all('a')
        for resultat_item in resultats_item:
            paginador = resultat_item.text
            if paginador.isnumeric():
                pagina_horitzo = int(paginador)

        print("setejat horitzo a " + str(pagina_horitzo))

        pagina = pagina + 1
        print("fent una pausa...")
        sleep(10)

    else:
        print("sembla que no hi ha res a tractar")
        pagina = pagina + 1

print("Fi de recorregut")
cnx.close()