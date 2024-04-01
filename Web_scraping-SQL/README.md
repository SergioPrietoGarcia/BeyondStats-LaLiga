# Web Scraping y almacenamiento en base de datos SQL

En esta carpeta se puede observar el código que ejecuta el web scraping sobre la web de estadísticas de La Liga "Beyond Stats".

Existen dos opciones para ejecutar estos scripts:

  1. Tener un servidor y una base de datos creada en SQL Server y completar y ejecutar únicamente el script de **exe-preparacion.py** con las claves necesarias para acceder a la base de datos SQL.
  2. Ejecutar por separado el script '**indice-posicion.py**' y '**Scrap_Stats-LaLiga.py**', almacenando los conjuntos de estadísticas en 6 archivos .txt. El primer script extrae los nombres de  los jugadores, sus claves identificadoras únicas, sus respectivos equipos y sus posiciones de juego en el campo. El segundo script se encarga de extraer las estadísticas de cada uno de los conjuntos de recopilación de estadísticas de la web.
