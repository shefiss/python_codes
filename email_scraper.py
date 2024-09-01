from bs4 import BeautifulSoup
import requests
import re
import time as t
import progressbar

def returnMails(url):
    responce = requests.get(url)
    soup = BeautifulSoup(responce.content, 'html.parser')
    soup = str(soup)
    mail = re.findall(
        r'[a-zA-Z0-9.]{2,60}@[a-zA-Z0-9S]+\.com|[a-zA-Z0-9.]{5,60}@[a-zA-Z0-9S]+\.cz|[a-zA-Z0-9.]{5,60}@[a-zA-Z0-9S]+\.eu',
        soup)
    mail2 = re.findall(r'(?<=mailto:).{5,60}(?=")', soup)
    mail.extend(mail2)

    return mail


url = input("URL: ")
responce = requests.get(url)
soup = BeautifulSoup(responce.content, 'html.parser')

pattern = r"^.*//.*$"

countstring = 0
i = 0
mailsArr = []
switch = False

for link in soup.find_all('a'):
    #print("=", end="") - check if its loading
    countstring+=1
    t.sleep(.02)

with progressbar.ProgressBar(max_value=countstring) as bar:

    #code for the url it self

    mailsArr.extend(returnMails(url))

    for link in soup.find_all('a'):
        l = link.get('href')

        try:
            if re.match(pattern, l):
                mailsArr.extend(returnMails(l))

        except:
            continue
            print("error")
        i+=1
        bar.update(i)

print("DONE")
for x in set(mailsArr):
    print(x)

yesno = input("Print to a text file? Y/N: ")

if yesno == "Y":
    path = input("Path: ")
    try:
        with open(path, 'a') as f:
            for m in mailsArr:
                f.write(m)
                f.writelines("\n")

    except:
        print("Something went wrong!")