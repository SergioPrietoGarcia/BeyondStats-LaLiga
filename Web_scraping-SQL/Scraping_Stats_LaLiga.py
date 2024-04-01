from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import re
from bs4 import BeautifulSoup
import time

"""
En este script se realiza web scraping de la web de estadísticas de La Liga, "Beyond Stats".
Para ello, empleando la librería Selenium, se abre el navegador con la url correspondiente
y se interactúa sobre la web scrapeando cada una de las secciones de estadísticas 
(clásicas, eficiencia, disciplina, ataques y defensivas) para cada uno de los más 
de 500 jugadores de La Liga.
"""


    ## --- PASO 1. Abrimos el navegador

# Creamos el driver e iniciamos el navegador en la URL
driver = webdriver.Chrome()
driver.get('https://www.laliga.com/es-GB/estadisticas-avanzadas')

# Aceptamos las coockies
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Aceptar"]')))
boton_aceptar = driver.find_element(By.XPATH, '//button[text()="Aceptar"]')
boton_aceptar.click()

time.sleep(2) # Pequeño tiempo de espera

# Establecer el nivel de zoom al mínimo
driver.execute_script("document.body.style.zoom='65%'")


    ## --- PASO 2. Scrapeamos banner de paginado

"""
Todos los apartados de características contienen el mismo número de jugadores, por lo tanto,
unicamente es necesario scrapear una vez el número total de páginas de jugadores existentes
en la web
"""

# Utilizamos un identificador único para localizar el botón de siguiente página
pagina_siguiente = 'div[class="styled__PaginationArrow-sc-1c62lz0-5 hMjvPL"]'

# Buscamos el numero de la pagina maxima
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')
banner_paginas = soup.find("div", {'class':"styled__PaginationContainer-sc-jnnmjf-8 jLYUYE"}).find_all("p", {'class':"styled__TextStyled-sc-1mby3k1-0 dLyMQu"})
pag_max = int([elemento.text for elemento in banner_paginas][-1]) # Extraer numero maximo de paginas 


    ## --- PASO 3. Diseñamos la función que lleve a cabo el web scraping

"""
En la web de Beyond Stats apartado de "Estadisticas Avanzadas", se almacenan 5 tablas
que recopilan estadísticas de los jugadores.

    # TABLAS_CLASICAS: Estadisticas clásicas de los jugadores
    # TABLAS_EFICIENCIA: Estadísticas relacionadas con la eficiencia de los jugadores
    # TABLAS_DISCIPLINA: Estadisticas relacionadas con la disciplina de los jugadores
    # TABLAS_ATAQUES: Estadisticas de ataque de los jugadores
    # TABLAS_DEFENSIVAS: Estadisticas de defensa de los jugadores

En primer lugar, crearemos un DataFrame que almacene el nombre del seleccionable y el HTML 
que almacena la información del botón que deseamos pulsar en cada momento.

En segundo lugar, diseñamos una función que clique sobre un apartado de características
y realice el scrapeo página por página de todos los jugadores. A continuación, la función 
organiza los datos y devuelve un diccionario con los jugadores como clave y las estadísticas
como valor.
"""

# Codigo HTML de los botones de los apartados de estadísticas
seleccionables = {
'sel_clasicas' : '//li[@class="styled__Item-sc-d9k1bl-3 iEhVUv" and text()="Clásicas"]',
'sel_eficiencia' : '//li[@class="styled__Item-sc-d9k1bl-3 VNATM" and text()="Eficiencia"]',
'sel_disciplina' : '//li[@class="styled__Item-sc-d9k1bl-3 VNATM" and text()="Disciplina"]',
'sel_ataques' : '//li[@class="styled__Item-sc-d9k1bl-3 VNATM" and text()="Ataques"]',
'sel_defensivas' : '//li[@class="styled__Item-sc-d9k1bl-3 VNATM" and text()="Defensivas"]'
}

 # Creamos un diccionario con dos claves: seleccionables y html
sel_ordenado = {
    "Seleccionables" : list(seleccionables.keys()),
    "HTML" : list(seleccionables.values())
}

# DataFrame con dos columnas, "Seleccionables" y "HTML"
sel_ordenado_df = pd.DataFrame(sel_ordenado)


# FUNCIÓN: "scrap_stats_player()"
def scrap_stats_players(sel_stats):

    # Buscamos el botón del seleccionable
    boton_stats = driver.find_element(By.XPATH, sel_stats)

    # Hacemos clic en el botón del seleccionable equipo
    driver.execute_script("arguments[0].click();", boton_stats) 

    tablas_seleccionable = [] # Lista vacía para almacenar los elementos del bucle

    # Realizamos x iteraciones para avanzar x páginas
    for i in range(1,pag_max + 1):

        # Establecemos un tiempo de espera entre pagina y pagina
        time.sleep(4)  # Tardamos 4 segundos para que de tiempo a cargar la pagina  

        # Almacenamos el HTML de la Pagina x en la variable soup
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Hay un problema y es que con "eficiencia" hay un cambio en el html de la tabla. Por lo tanto,
        # vamos a crear un condicionante para cuando scrapeemos el apartado estadístico "Eficiencia"
        caracteristica = re.search(r'text\(\)="([^"]+)"', sel_stats).group(1)
        if caracteristica != "Eficiencia":      
            # Creamos una variable llamada tabla que almacena el html de la tabla de jugadores
            tabla = soup.find('div', class_='styled__Container-sc-jnnmjf-0 styled__StatsTab-sc-jnnmjf-7 ixLvXA fWaRES')  

        else:
            # Creamos una variable llamada tabla que almacena el html de la tabla de jugadores
            tabla = soup.find('div', class_='styled__Container-sc-jnnmjf-0 styled__StatsTab-sc-jnnmjf-7 ixLvXA bgHlbd')


        # Almacenamos los elementos del bucle en la lista vacía creada antes
        tablas_seleccionable.append(tabla)

        # Detenemos el click en el boton de siguiente pagina cuando alcanzamos la última
        if i < pag_max:
            # Hacemos clic en el botón de siguiente página
            boton_siguiente = driver.find_element(By.CSS_SELECTOR, pagina_siguiente)
            driver.execute_script("arguments[0].click();", boton_siguiente) # Funciona mejor que boton_siguiente.click()
            
    # Usar el método join para combinar los elementos de la lista en una sola cadena
    tablas_seleccionable_str = "".join([str(tag) for tag in tablas_seleccionable])
    tablas_seleccionable_html = BeautifulSoup(tablas_seleccionable_str, "html.parser")

    claves = [] # Lista vacía donde se almacenará la clave única del jugador
    jugadores = [] #Lista vacía donde se almacenarán los jugadores
    stats_seleccionable_ = [] # Lista vacía donde se almacenarán las estadísticas

    # Itera sobre las filas de la tabla
    for fila in tablas_seleccionable_html.find_all('tr'):

        # Filtra la clave unica del jugador
        # Busca la etiqueta <a> dentro de la fila
        a_tag = fila.find('a', class_='link')
        if a_tag is not None:
            # Obtiene el atributo href que contiene la clave única del jugador
            clave_id = a_tag.get("href").split("/")[-1]
            claves.append(clave_id)
            #print(clave_id)

        # Filtra la celda que contiene el nombre del jugador
        celda_nombre = fila.find('td', class_='styled__TdStyled-sc-57jgok-4 iPYsfW')
        if celda_nombre:
            nombre_jugador = celda_nombre.get_text(strip=True)
            jugadores.append(nombre_jugador)

        # Filtra todas las celdas de estadísticas
        celdas_stats = fila.find_all('p', class_='styled__TextStyled-sc-1mby3k1-0 ejtpot')
        stats_jugador = [celda.get_text(strip=True) for celda in celdas_stats]
        stats_seleccionable_.append(stats_jugador)

    # Elimina de la lista de stats las lista vacias
    stats_seleccionable = [sublista for sublista in stats_seleccionable_ if len(sublista) > 0]

    # Creacion de tabla de ESTADISTICAS
    seleccionable_stats = {} # Diccionario vacio donde se irán desglosando jugador - estadísticas

    for i, lista in enumerate(stats_seleccionable, start=0):
        # Construir el nombre de la clave
        clave_jugador = claves[i]

        tupla = (jugadores[i], lista)
        
        # Asignar la tupla al diccionario con la clave correspondiente
        seleccionable_stats[clave_jugador] = (tupla[0],) + tuple(tupla[1])

    return(seleccionable_stats)


    
### ERROR A CREAR SELECIONABLE_STATS

"""
Una vez diseñada la función, se ejecuta para cada uno de los apartados estadísticos.
Para ello, se emplea el DataFrame "sel_ordenado_df" que almacena cada uno de los 
botones de los apartados.

Una vez realizado el web scraping mediante la ejecución de la función, se nombra un header 
con el nombre de cada uno de los títulos que recoge un cierto tipo de estadística
y se crea un DataFrame con los resultados para ese apartado de características
"""

start_time = time.time() # Iniciamos el contador del tiempo

###############################
#### ESTADÍSTICAS CLASICAS ####
###############################

clasic_stats = scrap_stats_players(sel_ordenado_df.iloc[0,1])
header = ["ID", "Jugador", "MJ", "PJ", "%PJ", "PC", "%PC",
          "PT", "%PT", "PS", '%PS', 'TA', 
          "TR", "SA", "G", "PR", "GPP",
          "GE"]# Nombre de las columnas
df_clasic_stats  = pd.DataFrame(clasic_stats).transpose()
df_clasic_stats.reset_index(inplace = True)
df_clasic_stats.columns = header
print("ESTADÍSTICAS CLÁSICAS")
print(" ")
print(df_clasic_stats.head(10))


###############################
### ESTADÍSTICAS EFICIENCIA ###
###############################

eficiencia_stats = scrap_stats_players(sel_ordenado_df.iloc[1,1])
header = ["ID", "Jugador", "CL", "ENT", "DUE", "D", "DA", "PC", "PCC", "PLC", "PH", "GPT", 
          "GPTFA", "GPTDA", "GCPI", "GCPD", "CG", "GABP"]# Nombre de las columnas
df_eficiencia_stats = pd.DataFrame(eficiencia_stats).transpose()
df_eficiencia_stats.reset_index(inplace=True)
df_eficiencia_stats.columns = header
print("ESTADÍSTICAS EFICIENCIA")
print(" ")
print(df_eficiencia_stats.head(10))


###############################
### ESTADÍSTICAS DISCIPLINA ###
###############################

disciplina_stats = scrap_stats_players(sel_ordenado_df.iloc[2,1])
header = ["ID", "Jugador", "TA", "TR", "SA", "FDJ", "FR", "FC", "PR", "PCOM", "FPM", "FPT"]# Nombre de las columnas
df_disciplina_stats = pd.DataFrame(disciplina_stats).transpose()
df_disciplina_stats.reset_index(inplace=True)
df_disciplina_stats.columns = header
print("ESTADÍSTICAS DISCIPLINA")
print(" ")
print(df_disciplina_stats.head(10))


###############################
#### ESTADÍSTICAS ATAQUES #####
###############################

ataques_stats = scrap_stats_players(sel_ordenado_df.iloc[3,1])
header = ["ID", "Jugador", "T", "DAP", "ASI", "RE", "RF", "G", "GDDA", "GFDA", "GCPI", "GCPD", "GDP", "CG", "GBP", "GPP"]# Nombre de las columnas
df_ataques_stats = pd.DataFrame(ataques_stats).transpose()
df_ataques_stats.reset_index(inplace=True)
df_ataques_stats.columns = header
print("ESTADÍSTICAS ATAQUES")
print(" ")
print(df_ataques_stats.head(10))


###############################
### ESTADÍSTICAS DEFENSIVAS ###
###############################

defensivas_stats = scrap_stats_players(sel_ordenado_df.iloc[4,1])
header = ["ID", "Jugador", "BLOQ", "INTER", "R", "D", "EE", "EF", "JUH", "DE", "DF", "DAE", "DAF"] # Nombre de las columnas
df_defensivas_stats = pd.DataFrame(defensivas_stats).transpose()
df_defensivas_stats.reset_index(inplace = True)
df_defensivas_stats.columns = header
print("ESTADÍSTICAS DEFENSIVAS")
print(" ")
print(df_defensivas_stats.head(10))


end_time = time.time()
execution_time = (end_time - start_time)/60
print("Tiempo de ejecución:", execution_time, "minutos")

"""
Terminado el scrapeo, se almacenan los resultados en diferentes archivos .txt

EL TIEMPO DE EJECUCIÓN ES DE MÁS O MENOS: 15 MINUTOS
"""

# Escribir cada DataFrame en un archivo txt
clasic_stats = 'C:\\SQLData\\BeyondStats\\clasic_stats.txt'
df_clasic_stats.to_csv(clasic_stats, sep=';', index=False)

eficiencia_stats = 'C:\\SQLData\\BeyondStats\\eficiencia_stats.txt'
df_eficiencia_stats.to_csv(eficiencia_stats, sep=';', index=False)

disciplina_stats = 'C:\\SQLData\\BeyondStats\\disciplina_stats.txt'
df_disciplina_stats.to_csv(disciplina_stats, sep=';', index=False)

ataques_stats = 'C:\\SQLData\\BeyondStats\\ataques_stats.txt'
df_ataques_stats.to_csv(ataques_stats, sep=';', index=False)

defensivas_stats = 'C:\\SQLData\\BeyondStats\\defensivas_stats.txt'
df_defensivas_stats.to_csv(defensivas_stats, sep=';', index=False)



driver.quit() # Cerramos el navegador