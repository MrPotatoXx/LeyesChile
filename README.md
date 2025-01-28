
# Repositorio de Leyes de Chile

Este proyecto permite obtener enlaces de leyes de Chile desde el sitio web de la Biblioteca del Congreso Nacional de Chile (https://www.bcn.cl/leychile) y descargar las leyes en formato PDF.

## Estructura del Proyecto

El proyecto cuenta con dos scripts principales:

1. **getlinks.py**: Este script extrae enlaces de descarga de las leyes desde la web.
2. **download.py**: Este script descarga los archivos PDF correspondientes a los enlaces extraídos.

## Requisitos

### Instalación de dependencias

Este proyecto requiere los siguientes paquetes de Python:

- `selenium`
- `beautifulsoup4`
- `pandas`
- `requests`

Puedes instalarlos ejecutando:

```bash
pip install selenium beautifulsoup4 pandas requests
```

Además, necesitarás el driver de Chrome (`chromedriver`) compatible con tu versión de Google Chrome. Puedes descargarlo desde [aquí](https://googlechromelabs.github.io/chrome-for-testing/).

### Configuración del proyecto

* Coloca el archivo `chromedriver.exe` en el directorio `chromedriver-win64/`.


## Uso

### 1. Obtener enlaces de las leyes

Ejecuta el script `getlinks.py` para extraer los enlaces de descarga de las leyes:

```bash
python getlinks.py
```

Este script recorrerá las páginas de la Biblioteca del Congreso Nacional, extraerá los enlaces de las leyes y los almacenará en un archivo CSV llamado `enlaces_descarga.csv`.

### 2. Descargar las leyes en PDF

Una vez que se haya generado el archivo CSV con los enlaces, ejecuta el script `download.py` para descargar los archivos PDF:

```bash
python download.py
```

Este script leerá los enlaces desde el archivo CSV y descargará los archivos en la carpeta `descargas`.

## Personalización

- **Número de páginas**: Puedes ajustar el rango de páginas que el script `getlinks.py` recorre cambiando el valor en el bucle `for` dentro del script.
- **Número de hilos**: El script `download.py` permite ajustar el número de hilos que se utilizan para la descarga concurrente, modificando el valor de `max_hilos`.

## Consideraciones

- Este proyecto utiliza Selenium, por lo que es posible que necesites instalar el driver adecuado para el navegador que estás utilizando.
- En caso de errores al descargar archivos, el script intentará varios reintentos antes de abandonar la descarga.

