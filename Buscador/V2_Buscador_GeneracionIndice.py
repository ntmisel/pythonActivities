import requests
from bs4 import BeautifulSoup
import nltk
from collections import Counter
from nltk.corpus import stopwords
import string
import json
import time

start = time.time()
direccionURL = {}

# 1 Lectura de URLS
try:
    with open("urls2.txt", 'r') as f:
        lineas = f.readlines()
        lineas = list(map(lambda l: l.rstrip('\n'), lineas))

except FileNotFoundError:
    print('El archivo especificado no existe.')
print(lineas)

cantidadUrls = 0
for link in lineas:
    # 2 Estados de respuesta HTTP 200
    start2 = time.time()
    stop_words = set(stopwords.words('spanish'))
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/50.0.2661.102 Safari/537.36'}
    datos = requests.get(link, headers=headers)

    # 3 Preprocesamiento (Tokenización, Conversión de minusculas, Filtrado de stopwords, Signos de puntuación,
    # Eliminación de espacios,  Eliminación de duplicados y Ordenamiento)
    if datos.status_code == 200:
        stup = BeautifulSoup(datos.text, 'lxml')
        cuerpo = stup.body;
        cuerpo = cuerpo.get_text()
        cuerpo = cuerpo.strip()
        tokens = nltk.word_tokenize(cuerpo)

        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        sinStopwords = []
        for r in tokens:
            if r not in stop_words:
                sinStopwords.append(r)

        sinPuntuacion = []
        for r in sinStopwords:
            for j in r:
                if j in string.punctuation:
                    r = r.replace(j, "")
            sinPuntuacion.append(r)

        for r in sinPuntuacion:
            if r == "":
                sinPuntuacion.remove(r)

        sinDuplicados = []
        for item in sinPuntuacion:
            if item not in sinDuplicados:
                if len(item) > 1:
                    sinDuplicados.append(item)

        sinDuplicados.sort()
        print(" ")
        cantidadUrls = cantidadUrls + 1
        print(cantidadUrls)
        print("URL :" + link)

        conteo = []
        for i in range(len(sinDuplicados)):
            x = sinDuplicados[i]
            d = Counter(sinPuntuacion)
            conteo.append([x, d[x]])

        direccionURL[link] = conteo
        end2 = time.time()
        total = end2 - start2  # Tiempo de cada url

        print("Tiempo trasnscurrido de URL")
        print(total)

    else:
        print("Error de url en la conexion: " + link)
        print(datos.status_code)

end = time.time()
tiempoTotal = end - start

print("Tiempo trasnscurrido total del programa")
print(tiempoTotal)

# 4 Generación de inidice
f = open("indice2.txt", 'w', encoding='utf-8')
f.write(json.dumps(direccionURL, ensure_ascii=False))
f.close()
