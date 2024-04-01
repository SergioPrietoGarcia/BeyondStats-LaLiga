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
y se interactúa sobre la web scrapeando las diferentes pestañas que recogen las distintas posiciones
ocupadas en el campo (porteros, defensas, centrocampistas y delanteros) por los jugadores y su 
correspondiente equipo para cada uno de los más de 500 jugadores de La Liga.
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



    ## --- PASO 2. Diseñamos la función que lleve a cabo el web scraping

"""
En la web de Beyond Stats apartado de "Estadisticas Avanzadas", se almacenan 4 tablas
que recopilan estadísticas de los jugadores en función de su posición.

    # TABLAS_PORTEROS
    # TABLAS_DEFENSAS
    # TABLAS_CENTROCAMPISTAS
    # TABLAS_DELANTEROS

En primer lugar, crearemos un DataFrame que almacene el nombre del seleccionable y el HTML 
que almacena la información del botón que deseamos pulsar en cada momento.

En segundo lugar, diseñamos una función que clique sobre un apartado de POSICIÓN
y realice el scrapeo página por página de todos los jugadores. A continuación, la función 
organiza los datos y devuelve TRES LISTAS con la misma LONGITUD: PLAYERS, TEAMS, POSITION.
"""

# Codigo HTML de los botones de los apartados de posiciones
seleccionables = {
'sel_portero' : '//li[@class="styled__Item-sc-d9k1bl-3 VNATM" and text()="Porteros"]',
'sel_defensa' : '//li[@class="styled__Item-sc-d9k1bl-3 VNATM" and text()="Defensas"]',
'sel_mediocentro' : '//li[@class="styled__Item-sc-d9k1bl-3 VNATM" and text()="Centrocampistas"]',
'sel_delantero' : '//li[@class="styled__Item-sc-d9k1bl-3 VNATM" and text()="Delanteros"]'
}

 # Creamos un diccionario con dos claves: seleccionables y html
sel_ordenado = {
    "Seleccionables" : list(seleccionables.keys()),
    "HTML" : list(seleccionables.values())
}

# DataFrame con dos columnas, "Seleccionables" y "HTML"
df_sel = pd.DataFrame(sel_ordenado)


# Utilizamos un identificador único para localizar el botón de siguiente página
pagina_siguiente = 'div[class="styled__PaginationArrow-sc-1c62lz0-5 hMjvPL"]'

# FUNCIÓN: "scrap_pos_players()"
def scrap_pos_players(sel_pos):
    # Buscamos el botón del seleccionable
    boton_pos = driver.find_element(By.XPATH, sel_pos)

    # Hacemos clic en el botón del seleccionable equipo
    driver.execute_script("arguments[0].click();", boton_pos)

    time.sleep(3) # Pequeño tiempo de espera

    # Buscamos el numero de la pagina maxima en el correspondiente equipo
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    banner_paginas = soup.find("div", {'class':"styled__PaginationContainer-sc-jnnmjf-8 jLYUYE"}).find_all("p", {'class':"styled__TextStyled-sc-1mby3k1-0 dLyMQu"})
    pag_max = int([elemento.text for elemento in banner_paginas][-1]) # Extraer numero maximo de paginas 

    # Listas vacías para almacenar el resultado de los bucles
    tabla_players = [] 
    claves = []
    players = []
    teams = []

    # Realizamos x iteraciones para avanzar x páginas
    for i in range(1,pag_max+1):

        # Establecemos un tiempo de espera entre pagina y pagina
        time.sleep(3)  # Tardamos 2 segundos para que de tiempo a cargar la pagina  

        # Almacenamos el HTML de la Pagina x en la variable html_content
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Buscamos la tabla donde se almacenan los datos y añadimos a la lista "tabla_players"
        tabla = soup.find('div', class_ = 'styled__Container-sc-jnnmjf-0 styled__StatsTab-sc-jnnmjf-7 ixLvXA fWaRES')
        tabla_players.append(tabla)

        if i < pag_max:
            # Hacemos clic en el botón de siguiente página
            boton_siguiente = driver.find_element(By.CSS_SELECTOR, pagina_siguiente)
            driver.execute_script("arguments[0].click();", boton_siguiente) # Funciona mejor que boton_siguiente.click()

    # Usar el método join para combinar los elementos de la lista en una sola cadena
    tabla_players_str = "".join([str(tag) for tag in tabla_players])
    tabla_players_html = BeautifulSoup(tabla_players_str, "html.parser")

    # Itera sobre las filas de la tabla
    for fila in tabla_players_html.find_all('tr'):

        # Filtra la clave unica del jugador
        # Busca la etiqueta <a> dentro de la fila
        a_tag = fila.find('a', class_='link')
        if a_tag is not None:
            # Obtiene el atributo href que contiene la clave única del jugador
            clave_id = a_tag.get("href").split("/")[-1]
            claves.append(clave_id)

        # Encuentra la celda que contiene el nombre del jugador
        celda_nombre = fila.find('td', class_='styled__TdStyled-sc-57jgok-4 iPYsfW')
        if celda_nombre:
            nombre_jugador = celda_nombre.get_text(strip=True)
            #print(nombre_jugador)
            players.append(nombre_jugador)

        # Encuentra la celda que contiene el nombre del equipo
        a = fila.find('td', class_ = 'styled__TdStyled-sc-57jgok-4 iBOaCu')
        if a:
            p = a.find('a', class_='link')
            if p:
                celda_equipo = p.find("p", class_ = 'styled__TextStyled-sc-1mby3k1-0 bzvXlU').get_text(strip = True)
                #print(celda_equipo)
                teams.append(celda_equipo)
            else:
                #print("Sin equipo")
                teams.append("Sin equipo")

    # Utilizamos una expresión regular para encontrar la palabra entre comillas después de text()=
    # que se encuentra en el string que almacene el codigo HTML del seleccionable, para despues
    # usar ese string filtrado como posición del jugador correspondiente
    pos = re.search(r'text\(\)="([^"]+)"', sel_pos).group(1)
    position = [pos for _ in range(len(players))]

    time.sleep(3)

    return(claves, players,teams, position)


    ## --- PASO 3. Ejecutamos la función y creamos el DataFrame final

start_time = time.time() # Inicio del tiempo de ejecución

# Creamos un dataframe vacio
posicion_jugadores = pd.DataFrame(columns = ["ID", "Jugador", "Equipo", "Posicion"])

# Creamos un bucle que vaya scrapeando los jugadores, el equipo y la
# posicion de la web para posteriormente introducirlos en su correspondiente columna
claves = []
jugadores = []
equipos = []
posiciones = []
for i in range(0, len(df_sel)):
    name_pos = df_sel.iloc[i, 0].split("_")[1]
    scrapeo_jugadores = scrap_pos_players(df_sel.iloc[i, 1])
    claves.append(scrapeo_jugadores[0])
    jugadores.append(scrapeo_jugadores[1])
    equipos.append(scrapeo_jugadores[2])
    posiciones.append(scrapeo_jugadores[3])

# Introducimos todas las listas en una única lista para cada lista
posicion_jugadores["ID"] = [elemento for sublist in claves for elemento in sublist]    
posicion_jugadores["Jugador"] = [elemento for sublist in jugadores for elemento in sublist]
posicion_jugadores["Equipo"] = [elemento for sublist in equipos for elemento in sublist]
posicion_jugadores["Posicion"] = [elemento for sublist in posiciones for elemento in sublist]

print(posicion_jugadores.head(15))

end_time = time.time() # Final del tiempo de ejecución
execution_time = (end_time - start_time)/60
print("Tiempo de ejecución:", execution_time, "minutos")
# Tiempo de ejecución de 2 minutos

# Introducir DataFrame en un .txt
posicion_jugadores.to_csv("C:\\SQLData\\BeyondStats\\index_equipo_posicion.txt", sep=';', index=False)



driver.quit() # Cerramos el navegador









