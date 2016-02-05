from mechanize import Browser
from bs4 import BeautifulSoup
import csv
import re
import os

mech = Browser()
otsikko = False
          
# Ylikirjoitetaan vanha talennustiedosto, jos sellainen löytyy   
if os.path.isfile('l_data.csv'):
    os.remove('l_data.csv')

def kirjoita_tiedot(data, otsikko):
    with open('l_data.csv', 'a') as f:
        w = csv.DictWriter(f, 'NIMI ALKU LOPPU OSOITE'.split(),extrasaction='ignore')
        if not otsikko: 
             w.writeheader()
        w.writerow(data)
        

# Käydään jokainen ID läpi
for luku in range(1000000,2000000):
    miljoonaluku = str(luku).zfill(7)
    url = "http://www.oera.li/webservices/HRG/HRG.asmx/getHRGHTML?chnr=" + miljoonaluku + "&amt=690&toBeModified=0&validOnly=11000&lang=1&sort=0" 
    page = mech.open(url)
    html = page.read()
    soup = BeautifulSoup(html)
    try:
        nimi = soup.find_all("tbody", align="left")
        pvm = soup.find_all("th", width="11%") # Tämä löytää sekä alun ([0]) että lopun ([1]), joita myöhemmin pitää siistiä
        osoite_taulukko = soup.find_all("table")[5]
        osoite = osoite_taulukko.find_all("th")[-1].text.strip() # Firman osoite
        nimi = nimi[0].find_all("th")[2].text.strip() # Firman nimi
        alku = pvm[0].text.replace("Eintragung", "").strip() # Aloituspäivämäärä
        loppu = pvm[1].text.replace(u"\u00F6", "").replace("Lschung","").strip() # Lopetuspäivämäärä
        print miljoonaluku + " Osuma"
        data = {
                    'NIMI': str(nimi).strip(),
                    'ALKU': str(alku),
                    'LOPPU': str(loppu),
                    'OSOITE': str(osoite.encode("utf-8"))
                }

        kirjoita_tiedot(data, otsikko)
        otsikko = True
    except:
        pass

print "Done."

