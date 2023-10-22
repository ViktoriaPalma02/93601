from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext
import tkinter.messagebox
import validators
import whois
import requests
from bs4 import BeautifulSoup
import re
from textblob import Word, TextBlob
from googlesearch import search
from urllib.request import urlopen
import en_core_web_lg
nlp = en_core_web_lg.load()

"""
 When user agrees to terms, destroy TOS page and make main program available
"""
def destroy_TOS():
    TOS.destroy()
    user_text.configure(state="normal", bg="#E3E3E3")
    output_text.configure(bg="#E3E3E3")

"""
When user disagree to terms, make program unavailable
"""
def disagree_TOS():
    tkinter.messagebox.showinfo("Disagreeing to TOS", "As you do not agree to the TOS, this program will remain unavailable to you.")

"""
Gets input from user and begin evaluating input
""" 
def get_input():
    #clear evaluate and tempstore files
    open(r"data\evaluate.txt", 'w').close()
    open(r"text_files\tempstore.txt", "w").close()
    #Clear output_text
    output_text.configure(state="normal")
    output_text.delete('1.0', tk.END)
    output_text.configure(state="disabled")
    user_input = user_text.get('1.0', 'end-1c')
    print(user_input)
    validate_url = validators.url(user_input)
    if validate_url: 
        print("This is a url")
        ev_url(user_input)
        f = open(r"text_files\html.txt", "w", encoding="utf-8")
        f.write(requests.get(user_input).text)
        htmlscrape()
    else:
        print("not a url")
        f = open(r"text_files\user_input.txt", "w", encoding="utf-8")
        f.write(user_input)
        spell_check(user_input)
    f = open(r"text_files\user_input.txt", "w", encoding="utf-8")
    f.write(user_input)
    print(user_input)
    similarity(user_input)
    calculate()
    reliable_calc()
    sentiment(user_input)

"""
Evaluate domain as registered
"""
def ev_url(url_input):
    try:
        whois.whois(url_input)
    except Exception:
        #print("*THIS DOESNT WORK")
        f = open(r"data\evaluate.txt", "a")
        f.write("0\n")
    else: 
        #print("*THIS WORKS")
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
        author_name.group(1)
        #print(author_name.group(1))
        f = open(r"data\evaluate.txt", "a")
        f.write("1\n")
    except Exception:
        print("does not exist")
        f = open(r"data\evaluate.txt", "a")
        f.write("0\n")
    try:
        doi_id.group(1)
        #print(doi_id.group(1))
        f = open(r"data\evaluate.txt", "a")
        f.write("1\n")
    except Exception:
        print("does not exist")
        f = open(r"data\evaluate.txt", "a")
        f.write("0\n")
    try:
        article_date.group(1)
        #print(article_date.group(1))
        f = open(r"data\evaluate.txt", "a")
        f.write("1\n")
    except Exception:
        #print("does not exist")
        f = open(r"data\evaluate.txt", "a")
        f.write("0\n")
    #will use this for semantic similarity
    try:
        article_title.group(1)
        #print(article_title.group(1))
        f = open(r"text_files\user_input.txt", "w", encoding="utf-8")
        f.write(article_title.group(1))
    except Exception:
        #print("does not exist")
        article_title = re.search(r".*?<title>(.*?)</title>.*", contents)
        article_title.group(1)
        #print(article_title.group(1))
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
    f = open(r"data\evaluate.txt", "a", encoding="utf-8")
    f.write(str(correct_spelling))
    f.write('\n')

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
            try:
                num = float(line)
                total += num
                line_count += 1
            except:
                continue
        sem_total = total/line_count
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
    
    output_text.configure(state="normal")
    output_text.insert(INSERT, "The reliablity percent of this is: ")
    output_text.insert(INSERT, "%.f%%" % (100 * reliable_tot))
    
    output_text.configure(state="disabled")

"""
Sentiment anaylsis
"""
def sentiment(input):
    anaylsis = TextBlob(input).sentiment
    polarity = anaylsis[0]
    subjectivity = anaylsis[1]
    output_text.configure(state="normal")
    output_text.insert(INSERT, "\nPolarity: ")
    output_text.insert(INSERT, "%.f%%" % (100 * polarity))
    output_text.insert(INSERT, "\nSubjectivity: ")
    output_text.insert(INSERT, "%.f%%" % (100 * subjectivity))



# Make main window
menu = Tk()
menu.title("Fake News Detector")
menu.state('zoomed')
menu.grid_columnconfigure(0, weight=1)
menu.configure(bg="#EAE0D5")
#prevent window from being resizeable
menu.resizable(False, False)

# Create title of page
title_label = Label(menu, text="Fake News Detector", foreground="#22333B", bg="#EAE0D5", font=("Verdana", 40, "bold"))
title_label.grid(padx=10, pady=10, column=0, row=0)

# Icon
icon = PhotoImage(file="assets/icon.png")
icon = icon.subsample(2)
icon_label = Label(menu, image=icon, bg='#EAE0D5')
icon_label.grid(row=0, column=0, sticky=NW)

# Subheading
file = open(r"text_files/intro_text.txt", "r")
userinp_label = Label(menu, text=file.read(), font=("Verdana", 10), wrap=1200)
userinp_label.grid(row=1, column=0, pady=5)

# Create label frame
user_labelframe = LabelFrame(menu, pady=5, padx=5, bg="#5E503F")
user_labelframe.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
user_labelframe.rowconfigure(0, weight=1)
user_labelframe.columnconfigure(0, weight=1)
user_labelframe.columnconfigure((0, 1), weight=1)

# Create label for instructions
input_label = Label(user_labelframe, text="Input:", bg="#5E503F", fg="#FFFFFF", font=("bold"))
input_label.grid(row=0, column=0, padx=5, pady=5)

output_label = Label(user_labelframe, text="Output:", bg="#5E503F", fg="#FFFFFF", font=("bold"))
output_label.grid(row=0, column=1, padx=5, pady=5)

# User input 
user_text = scrolledtext.ScrolledText(user_labelframe,font=("Verdana"))
user_text.grid(row=1, column=0, sticky=NSEW)

#input button
user_button = Button(menu, text="Enter", width=10, command=get_input)
user_button.grid(row=3, column=0)

#output
output_text = scrolledtext.ScrolledText(user_labelframe, font=("Verdana"))
output_text.grid(row=1, column=1, sticky=NSEW)

user_text.configure(state="disabled", bg="#898989")
output_text.configure(state="disabled", bg="#898989")

# Create TOS
TOS = Toplevel(menu)
TOS.title("Terms of Service")
#set window at center
height = 400
width = 500
x = (menu.winfo_screenwidth()//2)-(width//2)
y = (menu.winfo_screenheight()//2)-(height//2)
TOS.geometry('{}x{}+{}+{}'.format(width,height,x,y))
# Set the main window as the master for TOS
TOS.transient(menu)  
# Raise TOS window above the main window
TOS.lift()  
TOS.grid_columnconfigure(0, weight=1)
#prevent TOS from being resizeable
TOS.resizable(False, False)

title_tos = Label(TOS, text="Terms of Service", font=("Verdana", 20, "bold"))
title_tos.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

# Create canvas for TOS
tos_canvas = Canvas(TOS)#, width=tos_width)
tos_canvas.grid(row=1, column=0, sticky=NSEW)

# Create scrollbar for TOS
tos_scrollbar = Scrollbar(TOS, orient=VERTICAL, command=tos_canvas.yview)
tos_scrollbar.grid(row=1, column=1, sticky="ns")
tos_canvas.configure(yscrollcommand=tos_scrollbar.set)

# Make Labelframe inside canvas
tos_labelframe = LabelFrame(tos_canvas)
tos_labelframe.pack(fill="both", expand=True, pady=5,padx=5)

# Open textfile and put in TOS
f = open(r"text_files/tos_text.txt", "r")
content_tos = Label(tos_labelframe, text=f.read(), wraplength=400, font=("Verdana", 10))
content_tos.pack(pady=5, padx=5)

# Configure canvas to scrollable region
tos_canvas.create_window((0, 0), window=tos_labelframe, anchor="nw")
tos_canvas.configure(scrollregion=tos_canvas.bbox("all"))

# Configure canvas scrolling
tos_labelframe.bind("<Configure>", lambda e: tos_canvas.configure(scrollregion=tos_canvas.bbox("all")))
tos_canvas.bind_all("<MouseWheel>", lambda e: tos_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

# Buttons at end of service
agree_button = ttk.Button(tos_labelframe, text="Agree", command=destroy_TOS)
#agree_button.grid(padx=5, sticky=W, row=2, column=0)
agree_button.pack(side=LEFT, padx=5)

disagree_button = ttk.Button(tos_labelframe, text="Disagree", command=disagree_TOS)
#disagree_button.grid(padx=5, row=2, column=1, sticky=E)
disagree_button.pack(side=RIGHT, padx=5)

# Run mainloop
menu.mainloop()