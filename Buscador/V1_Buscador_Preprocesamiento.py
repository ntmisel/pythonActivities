import requests
from bs4 import BeautifulSoup
import nltk
from collections import Counter
from nltk.corpus import stopwords
import string

stop_words = set(stopwords.words('spanish'))
link= 'https://es.wikipedia.org/wiki/Ciudad_del_Vaticano#:~:text=La%20Ciudad%20del%20Vaticano%2C%E2%80%8B,ciudad%20de%20Roma%2C%20en%20Italia'
#link = 'https://www.unam.mx/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
datos = requests.get(link, headers=headers)



if datos.status_code == 200:
    stup = BeautifulSoup(datos.text, 'lxml')
    cuerpo = stup.body;
    cuerpo = cuerpo.get_text()
    cuerpo = cuerpo.strip()
    tokens = nltk.word_tokenize(cuerpo)

    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    lista=[]
    for r in tokens:
        if r not in stop_words:
            lista.append(r)

    palabras=[]
    for r in lista:
        for j in r:
            if j in string.punctuation:
                r = r.replace(j, "")
        palabras.append(r)

    for r in palabras:
        if r == "":
            palabras.remove(r)

    result = []
    for item in palabras:
        if item not in result:
            if len(item) > 1:
                result.append(item)


    result.sort()
    # Catidadad de cada palabra
    for i in range(len(result)):
        x = result[i]
        d = Counter(palabras)
        print('"{}"       se a repetido "{}" veces'.format(x, d[x]))
else:
    print("Error")
