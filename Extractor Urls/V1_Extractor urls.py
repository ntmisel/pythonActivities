#Jairo Cruz Diaz
#Diana Michelle Perez Rodriguez
import re

file = open("access.log")
line = file.read()
lista_links = [line.split()]
patron = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
urls = re.findall(patron, line)
result = []
for item in urls:
    if item not in result:
        if len(item) > 1:
            result.append(item)

print("URLs")
file = open("urls.txt", 'w')
for u in result:
    print(u)
    file.writelines(u+'\n')

file.close()

