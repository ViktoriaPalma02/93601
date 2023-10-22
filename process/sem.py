import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
from googlesearch import search
import spacy
import en_core_web_lg
nlp = en_core_web_lg.load()

#hard code input for now
input = "Elon Musk buy tumblr and reddit"
#input = "New Zealand buys Australlian government as consolation from fending off Emu attack."
f = open(r"process\user_text.txt", "w", encoding="utf-8")
f.write(input)

#google search input online, for 50 URLS
for i in search(input, tld="co.in", num=50, stop=50, pause=2):
    print("starting loop")
    try:
        #webscraping
        url = i
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        #getting rid of html tags
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        f = open(r"text_files\cross_ref.txt", "w", encoding="utf-8")
        f.write(text)
        print("process finished")

        #compare semantic similarity between website and original input
        file1 = open(r"text_files\cross_ref.txt", encoding="utf-8").read()
        doc1 = nlp(file1)
        file2 = open(r"process\user_text.txt", encoding="utf-8").read()
        doc2 = nlp(file2)
        a = doc1.similarity(doc2)
        print(a)
        f = open(r"text_files\tempstore.txt", "a", encoding="utf-8")
        f.write("\n")
        f.write(str(a))

    #If cannot webscrape, read null
    except Exception as error:
        print("an exception has occured!")
        f=open(r"text_files\tempstore.txt", "a", encoding="utf-8")
        f.write("\n")
        f.write("null")
        continue

