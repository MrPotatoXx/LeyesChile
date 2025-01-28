import pandas as pd
import requests
import os
import time
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed

carpeta_destino = './descargas'

if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

csv_file = './enlaces_descarga.csv'
df = pd.read_csv(csv_file)


def obtener_nombre_archivo(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    nombre_archivo = params.get('nombrearchivo', ['archivo'])[0]
    return nombre_archivo + '.pdf'


def limpiar_nombre_archivo(nombre):
    caracteres_invalidos = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in caracteres_invalidos:
        nombre = nombre.replace(char, '_')
    return nombre

def descargar_pdf(url, max_reintentos=3):
    nombre_archivo = obtener_nombre_archivo(url)
    nombre_archivo_limpio = limpiar_nombre_archivo(nombre_archivo)

    for intento in range(max_reintentos):
        try:
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code == 200:
                ruta_pdf = os.path.join(carpeta_destino, nombre_archivo_limpio)
                with open(ruta_pdf, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=4096):
                        if chunk:
                            f.write(chunk)
                time.sleep(2)
                return f'{ruta_pdf} descargado correctamente.'
            else:
                print(f'Error al descargar {nombre_archivo_limpio}: {response.status_code}')
        except Exception as e:
            print(f'Error al descargar {nombre_archivo_limpio} en intento {intento + 1}: {str(e)}')

        print(f'Reintentando descarga de {nombre_archivo_limpio} (Intento {intento + 1}/{max_reintentos})...')
        time.sleep(5)

    return f'Error al descargar {nombre_archivo_limpio} después de {max_reintentos} reintentos.'

def descargar_todos_los_archivos(df, max_workers=3):
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(descargar_pdf, row['Enlace']) for index, row in df.iterrows()]
            for future in as_completed(futures):
                print(future.result())
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario.")
        executor.shutdown(wait=False)
        raise

max_hilos = 20

try:
    descargar_todos_los_archivos(df, max_workers=max_hilos)
except KeyboardInterrupt:
    print("Descarga cancelada por el usuario.")

print("Descarga completada.")
