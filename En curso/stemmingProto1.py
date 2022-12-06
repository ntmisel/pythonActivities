import nltk
from nltk import SnowballStemmer

spanishstemmer = SnowballStemmer('spanish')
# https://medium.com/qu4nt/reducir-el-n%C3%BAmero-de-palabras-de-un-texto-lematizaci%C3%B3n-y-radicalizaci%C3%B3n
# -stemming-con-python-965bfd0c69fa
# text = "Soy un texto que pide a gritos que lo procesen. Por eso yo canto,
# tú cantas, ella canta, nosotros cantamos, cantáis, cantan"
# tokens = normalize(text) # crear una lista de tokens
# stems = [spanishstemmer.stem(token) for token in tokens] print(stems)

from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import nltk
from collections import Counter
from nltk.corpus import stopwords
import string
import json

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

        stems = [spanishstemmer.stem(token) for token in  sinDuplicados]
        stemsSinDuplicados = []
        for a in stems:
            if a not in stemsSinDuplicados:
                if len(a) > 1:
                    stemsSinDuplicados.append(a)
        stemsSinDuplicados.sort()

        conteo = []
        for i in range(len(sinDuplicados)):
            x = sinDuplicados[i]
            d = Counter(sinPuntuacion)
            conteo.append([x, d[x]])

        direccionURL[link] = conteo


    else:
        print("Error de url en la conexion: " + link)
        print(datos.status_code)
print("Palabras:")
print(sinDuplicados)
print("Palabras - Con raices:")
print(stems)
print("Con raices sin duplicados:")
print(stemsSinDuplicados)