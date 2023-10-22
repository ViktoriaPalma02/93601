#This file is made to hold all the code for processing the input
#evaluate.py, spell.py, sem.py, webscraping.py
#note: print statements with * at the start means to delete when using actual thing

#python libraries here
import validators
import whois
import requests
from bs4 import BeautifulSoup
import re
from textblob import Word
from googlesearch import search
from urllib.request import urlopen
import en_core_web_lg
nlp = en_core_web_lg.load()

#functions here
"""
Evaluate domain as registered
"""
def ev_url(url_input):
    try:
        whois.whois(url_input)
    except Exception:
        print("*THIS DOESNT WORK")
        f = open(r"data\evaluate.txt", "a")
        f.write("0\n")
    else: 
        print("*THIS WORKS")
        f = open(r"data\evaluate.txt", "a")
        f.write("1\n")


"""
Extract Html elements from user url
"""

def htmlscrape():
    with open (r"text_files\html.txt", encoding="utf-8") as f:
        contents = f.read()
    author_name = re.search(r'"citation_author"\s+content=+"([^"]*)"', contents)
    doi_id = re.search(r'"citation_doi"\s+content=+"([^"]*)"', contents)
    article_date = re.search(r'"citation_publication_date"\s+content=+"([^"]*)"', contents)
    article_title = re.search(r'"og:title"\s+content=+"([^"]*)"', contents)

    try:
        print(author_name.group(1))
        f = open(r"data\evaluate.txt", "a")
        f.write("1\n")
    except Exception:
        print("does not exist")
        f = open(r"data\evaluate.txt", "a")
        f.write("0\n")
    try:
        print(doi_id.group(1))
        f = open(r"data\evaluate.txt", "a")
        f.write("1\n")
    except Exception:
        print("does not exist")
        f = open(r"data\evaluate.txt", "a")
        f.write("0\n")
    try:
        print(article_date.group(1))
        f = open(r"data\evaluate.txt", "a")
        f.write("1\n")
    except Exception:
        print("does not exist")
        f = open(r"data\evaluate.txt", "a")
        f.write("0\n")
    #will use this for semantic similarity
    try:
        print(article_title.group(1))
        f = open(r"text_files\user_input.txt", "w", encoding="utf-8")
        f.write(article_title.group(1))
    except Exception:
        print("does not exist")
        article_title = re.search(r".*?<title>(.*?)</title>.*", contents)
        print(article_title.group(1))
        f = open(r"text_files\user_input.txt", "w", encoding="utf-8")
        f.write(article_title.group(1))

"""
Evaluate correct spelling of input
"""
def spell_check(input):
    count = 0
    word_list = input.split()
    #get float number of closeness input has to correct spelling
    for i in range(0, len(word_list)):
        ev_word = Word(word_list[i]).spellcheck()
        correct = list(ev_word[0])
        count += correct[1]
    correct_spelling = count/len(word_list)
    print(correct_spelling)
    f = open(r"data\evaluate.txt", "w")
    f.write(str(correct_spelling))

"""
Evaluate similarity to other websites
"""
def similarity(input):
    for i in search(input, tld="co.in", num=15, stop=15, pause=2):
        print("*starting loop")
        try:
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
            file2 = open(r"text_files\user_input.txt", encoding="utf-8").read()
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

"""
Calculate total similarity
"""
def calculate():
    total = 0
    line_count = 0
    with open(r"text_files\tempstore.txt") as f:
        lines = f.readlines()[1:]
        for line in lines:
            print(line)
            if line == "null":
                print("not it")

            else:
                try:
                    num = float(line)
                    total += num
                    line_count += 1
                except:
                    pass

                #print(total)
                #print(line_count)
                sem_total = total/line_count
                #print(sem_total)
    f = open(r"data\evaluate.txt", "a")
    f.write(str(sem_total))

"""
Reliablity percent
"""
def reliable_calc():
    total =0
    line_count = 0
    with open(r"data\evaluate.txt") as f:
        lines = f.readlines()
        for line in lines:
            num = float(line)
            total += num
            line_count += 1
            reliable_tot = total/line_count
            
    print("The reliablity percent of this input is: ", reliable_tot)


#inital user input
print("*Please type somethere here!")
user_input = input()

#evaluate if user inputs url or text
validate_url = validators.url(user_input)
if validate_url: 
    print("This is a url")
    ev_url(user_input)
    #store user input on file for comparison
    #webscrape website    
    f = open(r"text_files\html.txt", "w", encoding="utf-8")
    f.write(requests.get(user_input).text)
    htmlscrape()

else:
    print("not a url")
    #store user input on file for comparison
    f = open(r"text_files\user_input.txt", "w", encoding="utf-8")
    f.write(user_input)
    spell_check(user_input)

#read similarity of code on random goofy ahh
f = open(r"text_files\user_input.txt", "w", encoding="utf-8")
f.write(user_input)
print(user_input)
similarity(user_input)
calculate()
reliable_calc()
