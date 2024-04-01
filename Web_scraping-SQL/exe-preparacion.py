# EJECUCIÓN DE SCRIPT DE WEB SCRAPING

# Con este script se importan las librerias correspondientes, si no se encuentran
# instaladas se instalan automaticamente.

from claves import password
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import pandas as pd
    from bs4 import BeautifulSoup
    import pyodbc
    import time
    import re
except ImportError as e:
    missing_module = str(e).split("'")[1]
    print(f"La biblioteca {missing_module} no está instalada. Instalando...")
    install(missing_module)


def ejecutar_script(script):
    subprocess.run(["python", script])


def ejecutar_script_sql(file_path, server, database, user, password):
    # Establece la conexión con la base de datos SQL Server
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
    conn = pyodbc.connect(conn_str)

    try:
        # Lee el contenido del archivo .sql
        with open(file_path, "r", encoding="utf-8") as file:
            script_sql = file.read()

        # Ejecuta el script SQL
        cursor = conn.cursor()
        cursor.execute(script_sql)
        conn.commit()
        print("Script SQL ejecutado exitosamente.")
    except Exception as e:
        print(f"Error al ejecutar el script SQL: {str(e)}")
    finally:
        # Cierra la conexión
        conn.close()

if __name__ == "__main__":
    file_path_sql = "C:\\Users\\Lenovo\\Desktop\\Universidad\\Python\\Beyond Stats\\Create-tables.sql"
    file_path_py_1 = "C:\\Users\\Lenovo\\Desktop\\Universidad\\Python\\Beyond Stats\\indice-posicion.py"
    file_path_py_2 = "C:\\Users\\Lenovo\\Desktop\\Universidad\\Python\\Beyond Stats\\Scraping_Stats_LaLiga.py"
    server = "LAPTOP-AALTB412\SQLEXPRESS"
    database = "BeyondStats"
    user = "sa"
    # password = "****************"

    # Ejecutar el script de recopilado de ID, Jugador, Equipo, Posición
    ejecutar_script(file_path_py_1)

    # Ejecutar el script de recopilado de STATS
    ejecutar_script(file_path_py_2)

    # Ejecutar el script SQL para crear las tablas en la base de datos
    ejecutar_script_sql(file_path_sql, server, database, user, password)

    print("Ambos scripts han finalizado su ejecución.")



