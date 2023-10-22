import requests
from bs4 import BeautifulSoup
import spacy
import en_core_web_lg
nlp = en_core_web_lg.load()
import re

#Delete later: inital testing for semantic similarity
#test1 = nlp('this duck is tasty')
#test2 = nlp('this duck is quite ravishing')
#print(test1.similarity(test2))

#userinp = input()
#test1 = nlp(userinp)

#get url and write it to text file 
url = 'https://www.academia.edu/79015428/Where_Airy_Voices_Lead_A_Short_History_of_Immortality'
#url = 'https://helpfulprofessor.com/dramaturgical-analysis/'
#url ="https://en.m.wikipedia.org/wiki/King_asleep_in_mountain"
#url ="https://www.hsph.harvard.edu/nutritionsource/what-should-you-eat/vegetables-and-fruits/"

#USING REQUESTS FOR WEBSCRAPING
f= open("process\webread.txt", "w", encoding="utf-8")
res = requests.get(url)
f.write(res.text)

#read file
with open ("process\webread.txt", encoding="utf-8") as f:
    contents = f.read()

#print author name
author_name = re.search(r'"citation_author"\s+content=+"([^"]*)"', contents)

#print doi name
doi_id = re.search(r'"citation_doi"\s+content=+"([^"]*)"', contents)

#print citation date
article_date = re.search(r'"citation_publication_date"\s+content=+"([^"]*)"', contents)

#pritn article title
article_title = re.search(r'"og:title"\s+content=+"([^"]*)"', contents)

#Will try to have exception handel + function to make code cleaner to use

try:
    author_name.group(1) 
    #print(author_name.group(1))
except:
    print("does not exist")  
try:
    doi_id.group(1)
    #print(doi_id.group(1))
except:
    print("does not exist") 
try:
    print(article_date.group(1))
except:
    print("does not exist") 
try:
    print(article_title.group(1))
except:
    print("does not exist")

#USING BEAUTIFUL SOUP FOR WEBSCRAPING
#page = requests.get('https://www.academia.edu/79015428/Where_Airy_Voices_Lead_A_Short_History_of_Immortality')
#soup = BeautifulSoup(page.text, 'html.parser')
#soup = BeautifulSoup(res.content, 'html5lib') 
#a = soup.prettify()
#f2 = open("process\websoup.txt", "w", encoding="utf-8")
#f2.write(a)

#hardcode input for similarity
testx = ''

#with open("process\webread.txt", encoding="utf-8") as f:
 #   print(test1.similarity(f))
'''
userinp = input()

#checks if input is exactly the same in textfile
with open("process\webread.txt", encoding="utf-8") as f:
    if userinp in f.read():
        print("contains input!")'''