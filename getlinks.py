from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

driver_path = './chromedriver-win64/chromedriver.exe'

service = Service(driver_path)

driver = webdriver.Chrome(service=service)

output_file = 'enlaces_descarga.csv'

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Enlace', 'Título'])

# URL base
url_base = 'https://www.bcn.cl/leychile/consulta/listaresultadosimple?itemsporpagina=50&npagina={}&tipoviene=4&fc_de=&fc_ra=&seleccionado=0&fc_rp=&totalitems=15787&orden=1&fc_pb=&fc_pr=&exacta=0&cadena=&fc_tn=,Ley'

# Recorrer páginas de 1 a 316
for page_num in range(1, 316):
    print(f"Procesando página {page_num}...")

    url = url_base.format(page_num)

    driver.get(url)


    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-body")))
        time.sleep(10)
    except Exception as e:
        print(f"Error al esperar la carga de la página {page_num}: {e}")
        continue

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    cards = soup.find_all('div', class_='card card-body')

    for card in cards:
        links = card.find_all('a', href=True)

        for link in links:
            href = link['href']
            title = link.get('title', 'Sin título')

            if 'Exportar' in href:
                if href.startswith('/'):
                    href = 'https://www.bcn.cl' + href

                print(f"Guardando enlace: {href}, Título: {title}")

                with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([href, title])

driver.quit()

print("Proceso completado.")

