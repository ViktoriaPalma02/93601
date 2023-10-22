"""
Import modules.
"""
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext
import tkinter.messagebox
import re
from urllib.request import urlopen
import urllib.request
import validators
from bs4 import BeautifulSoup
import whois
import requests
from textblob import Word, TextBlob
from googlesearch import search
import en_core_web_lg
nlp = en_core_web_lg.load()

def destroy_tos():
    """
    When user agrees to terms, destroy TOS page and make main program available
    """
    tos.destroy()
    user_text.configure(state="normal", bg="#E3E3E3")
    output_text.configure(bg="#E3E3E3")


def disagree_tos():
    """
    When user disagree to terms, make program unavailable
    """
    tkinter.messagebox.showinfo("Disagreeing to TOS",
                                "As you do not agree, this program will remain unavailable to you.")

def more_result():
    """
    When users wants more results
    """
    file = open(r"data\more_info.txt", "r", encoding="utf-8")
    content = file.read()
    output_text.configure(state="normal")
    output_text.insert("insert", "\nSpelling: ")
    output_text.insert("insert", content)
    output_text.configure(state="disabled")


def get_input():
    """
    Gets input from user and begin evaluating input
    """
    #clear textfiles in case user repeats action
    open(r"data\evaluate.txt", "w", encoding="utf-8").close()
    open(r"data\more_info.txt", "w", encoding="utf-8").close()
    open(r"text_files\cross_ref.txt", 'w', encoding="utf-8").close()
    open(r"text_files\html.txt", "w", encoding="utf-8").close()
    open(r"text_files\\tempstore.txt", "w", encoding="utf-8").close()
    open(r"text_files\user_input.txt", "w", encoding="utf-8").close()
    
    #Clear output_text
    output_text.configure(state="normal")
    output_text.delete('1.0', tk.END)
    output_text.configure(state="disabled")
    user_input = user_text.get('1.0', 'end-1c')
    #adds loading
    output_text.configure(state="normal")
    output_text.insert("insert", "Please wait! loading...")
    tkinter.messagebox.showinfo("Received",
         "Your request has been received, press OK to begin processing.\n\nIf the output is left blank after 1 minute, the request most likely failed."
        )
    #check if user_input is url or text
    validate_url = validators.url(user_input)
    if validate_url:
        #evaluate url for domain
        ev_url(user_input)
        #webscrape html
        file_storehtml = open(r"text_files\\html.txt", "w", encoding="utf-8")
        file_storehtml.write(requests.get(user_input, timeout=10).text)
        htmlscrape()
    #user input is text
    else:

        #store user_input to file
        file_store = open(r"text_files\\user_input.txt", "w", encoding="utf-8")
        file_store.write(user_input)
        #check spelling of input
        spell_check(user_input)
    #store userinput url into file
    file_store = open(r"text_files\\user_input.txt", "w", encoding="utf-8")
    file_store.write(user_input)
    #go to similarity function
    similarity(user_input)
    #go to calculate function
    calculate()
    #go to reliablity calculator function
    reliable_calc()
    #go to sentiment function
    sentiment(user_input)


def ev_url(url_input):
    """
    Evaluate domain as registered
    """
    #check url is registered through whois
    try:
        whois.whois(url_input)
    except whois.parser.PywhoisError:
        #store data as 0 for verified domain
        file_evaluate = open(r"data\evaluate.txt", "a", encoding="utf-8")
        file_evaluate.write("0\n")
    else:
        #store data as 1 for contains verified domain
        file_evaluate = open(r"data\evaluate.txt", "a", encoding="utf-8")
        file_evaluate.write("1\n")

def htmlscrape():
    """
    Extract Html elements from user url
    """
    with open (r"text_files\html.txt", encoding="utf-8") as html_file:
        contents = html_file.read()
    #use regexpression to find author name, article id, date and title
    author_name = re.search(r'"citation_author"\s+content=+"([^"]*)"', contents)
    doi_id = re.search(r'"citation_doi"\s+content=+"([^"]*)"', contents)
    article_date = re.search(r'"citation_publication_date"\s+content=+"([^"]*)"', contents)
    article_title = re.search(r'"og:title"\s+content=+"([^"]*)"', contents)

    #exception handling if any of the aforementioned are not found
    try:
        author_name.group(1)
        #store 1 as article contains author name
        html_file = open(r"data\evaluate.txt", "a", encoding="utf-8")
        html_file.write("1\n")
        #store name in more info
        author_info = open(r"data\more_info.txt", "a", encoding="utf-8")
        author_info.write("Author: ")
        author_info.write(author_name.group(1))
        author_info.write('\n')
        print(author_name.group(1))

    except AttributeError:
        #store 0 as article does not contain author name
        html_file = open(r"data\evaluate.txt", "a", encoding="utf-8")
        html_file.write("0\n")
    try:
        doi_id.group(1)
        #store 1 as article cointains article id
        html_file = open(r"data\evaluate.txt", "a", encoding="utf-8")
        html_file.write("1\n")
        #store DOI in more info
        doi_info = open(r"data\more_info.txt", "a", encoding="utf-8")
        doi_info.write("DOI: ")
        doi_info.write(doi_id.group(1))
        doi_info.write('\n')
        print(doi_id.group(1))
    except AttributeError:
        #store 0 as article does not contain article id
        html_file = open(r"data\evaluate.txt", "a", encoding="utf-8")
        html_file.write("0\n")

    try:
        article_date.group(1)
        #store 1 as article cointains date
        html_file = open(r"data\evaluate.txt", "a", encoding="utf-8")
        html_file.write("1\n")
        #store date in more info
        date_info = open(r"data\more_info.txt", "a", encoding="utf-8")
        date_info.write("Article date: ")
        date_info.write(article_date.group(1))
        date_info.write('\n')
        print(article_date.group(1))
    except AttributeError:
        #store 0 as article does not contain date
        html_file = open(r"data\evaluate.txt", "a", encoding="utf-8")
        html_file.write("0\n")
    #will use this for semantic similarity
    try:
        article_title.group(1)
        html_file = open(r"text_files\html.txt", "w", encoding="utf-8")
        html_file.write(article_title.group(1))
    except AttributeError:
        #if article title cannot be found, get article title from title tags instead
        try:
            article_title = re.search(r".*?<title>(.*?)</title>.*", contents)
            article_title.group(1)
            html_file = open(r"text_files\html.txt", "w", encoding="utf-8")
            html_file.write(article_title.group(1))
        except AttributeError:
            output_text.configure(state="normal")
            output_text.delete('1.0', tk.END)
            output_text.insert("insert", "Error cannot read website, input text instead!")



def spell_check(input):
    """
    Evaluate correct spelling of input
    """
    count = 0
    word_list = input.split()
    #get float number of closeness input has to correct spelling
    for i in range(0, len(word_list)):
        ev_word = Word(word_list[i]).spellcheck()
        correct = list(ev_word[0])
        count += correct[1]
    correct_spelling = count/len(word_list)
    #store spelling result to file
    file_spell = open(r"data\evaluate.txt", "a", encoding="utf-8")
    file_spell.write(str(correct_spelling))
    file_spell.write('\n')
    #store spelling to more info 
    spell_percent = f"{correct_spelling:.0%}"
    spell_info = open(r"data\more_info.txt", "a", encoding="utf-8")
    spell_info.write(spell_percent)
    spell_info.write('\n')

def similarity(input):
    """
    Evaluate similarity to other websites
    """
    #google search user_input
    for i in search(input, tld="co.in", num=30, stop=30, pause=2):
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
            file_crossref = open(r"text_files\cross_ref.txt", "w", encoding="utf-8")
            file_crossref.write(text)

            #compare semantic similarity between website and original input
            file1 = open(r"text_files\cross_ref.txt", encoding="utf-8").read()
            doc1 = nlp(file1)
            file2 = open(r"text_files\user_input.txt", encoding="utf-8").read()
            doc2 = nlp(file2)
            compare_file = doc1.similarity(doc2)
            file_tempstore = open(r"text_files\tempstore.txt", "a", encoding="utf-8")
            file_tempstore.write("\n")
            file_tempstore.write(str(compare_file))

    #If cannot webscrape, read null
        except urllib.error.HTTPError:
            file_tempstore=open(r"text_files\tempstore.txt", "a", encoding="utf-8")
            file_tempstore.write("\n")
            file_tempstore.write("null")
            continue


def calculate():
    """
    Calculate total similarity
    """
    total = 0
    line_count = 0
    with open(r"text_files\tempstore.txt", encoding="utf-8") as file_sim:
        lines = file_sim.readlines()[1:]
        for line in lines:
            try:
                num = float(line)
                total += num
                line_count += 1
            except Exception:
                continue
        try:
            sem_total = total/line_count
        except Exception:
            output_text.configure(state="normal")
            output_text.delete('1.0', tk.END)
            output_text.insert("insert", "Error cannot read website, input text instead!")
    #store overall semantic total
    file_sim = open(r"data\evaluate.txt", "a", encoding="utf-8")
    file_sim.write(str(sem_total))


def reliable_calc():
    """
    Reliablity percent
    """
    total =0
    line_count = 0
    #calculate total reliablity after evaluating previous elements
    with open(r"data\evaluate.txt", encoding="utf-8") as data_file:
        lines = data_file.readlines()
        for line in lines:
            num = float(line)
            total += num
            line_count += 1
            reliable_tot = total/line_count
    #show result on output box
    output_text.configure(state="normal")
    output_text.delete('1.0', tk.END)
    output_text.insert("insert", "The reliablity percent of this is: ")
    output_text.insert("insert", "%.f%%" % (100 * reliable_tot))
    output_text.configure(state="disabled")


def sentiment(input):
    """
    Sentiment anaylsis
    """
    global happy_image, angry_image, neutral_image
    anaylsis = TextBlob(input).sentiment
    polarity = anaylsis[0]
    subjectivity = anaylsis[1]
    #show result on output box
    output_text.configure(state="normal")
    output_text.insert("insert", "\nPolarity: ")
    if polarity > 0:
        output_text.insert("insert", "Author views subject matter positively")
        happy_image = tk.PhotoImage(file=r"assets\happy.png")
        happy_image = happy_image.subsample(2)
        output_text.image_create("end", image=happy_image)
    elif polarity < 0:
        output_text.insert("insert", "Author views subject matter negatively")
        angry_image = tk.PhotoImage(file=r"assets\angry.png")
        angry_image = angry_image.subsample(2)
        output_text.image_create("end", image=angry_image)
    else:
        output_text.insert("insert", "Author views subject matter in a neutral manner")
        neutral_image = tk.PhotoImage(file=r"assets\neutral.png")
        neutral_image = neutral_image.subsample(2)
        output_text.image_create("end", image=neutral_image)
    output_text.insert("insert", "\nSubjectivity: ")
    output_text.insert("insert", "%.f%%" % (100 * subjectivity))  
    output_text.configure(state="disabled")


# Make main window
menu = tk.Tk()
menu.title("Fake News Detector")
menu.state('zoomed')
menu.configure(bg="#EAE0D8")
menu.resizable(False, False)
menu.columnconfigure(0, weight=1)


heading_frame = tk.LabelFrame(menu, bg="#22333B")
heading_frame.grid(row=0, column=0, sticky="NSEW")
heading_frame.columnconfigure(0, weight=1)


# Create title of page
title_label = tk.Label(heading_frame, text="Fake News Detector", foreground="#FFFFFF", bg="#22333B", font=
                    ("Verdana", 40, "bold"))
title_label.grid(padx=10, pady=10, column=0, row=0, sticky="NSEW")

# Icon
icon = tk.PhotoImage(file=r"assets\icon.png")
icon = icon.subsample(2)
icon_label = tk.Label(heading_frame, image=icon, bg='#22333B')
icon_label.grid(row=0, column=1, sticky="E")

secondframe = tk.LabelFrame(menu, borderwidth = 0, highlightthickness = 0, bg="#f0f0f0")
secondframe.grid(row=1,column=0, sticky="NSEW")
secondframe.columnconfigure(0, weight=1)

#introductory paragraph
file = open(r"text_files\intro.txt", "r", encoding="utf-8")
userinp_label = ttk.Label(secondframe, text=file.read(), font=("Verdana", 10), justify="center")
userinp_label.grid(row=1, column=0, pady=50)

frame = tk.Frame(menu, bg="#EAE0D8")
frame.grid(row=2, column=0, sticky='nsew',pady=50)

for i in range(3):
    frame.columnconfigure(i, weight=1)

frame.rowconfigure(1, weight=1)
tk.Label(frame, text='Input:', bg='#5E503F', fg="#FFFFFF").grid(row=0, column=0, sticky='nsew', padx=70)
user_text = scrolledtext.ScrolledText(frame, bg="#898989", width=80, font=
                                      ("Verdana"))
user_text.grid(row=1, column=0, padx=70, sticky='w')


user_button = tk.Button(frame, text="More Results", width=20,bg="black", fg="white", command=more_result)
user_button.grid(row=0, column=1)

enter_button = tk.Button(frame, text="Enter", width=10,bg="black", fg="white", command=get_input)
enter_button.grid(row=2, column=1)


tk.Label(frame, text='Output:',bg='#5E503F', fg="#FFFFFF").grid(row=0, column=2, sticky='nsew', padx=70)
output_text = scrolledtext.ScrolledText(frame, bg="#898989", width=80, font=
                                      ("Verdana"))
output_text.grid(row=1, column=2, sticky='e', padx=70)


# Create tos
tos = tk.Toplevel(menu)
tos.title("Terms of Service")

#set window at center
HEIGHT = 400
WIDTH = 500
x = (menu.winfo_screenwidth()//2)-(WIDTH//2)
y = (menu.winfo_screenheight()//2)-(HEIGHT//2)
tos.geometry('{}x{}+{}+{}'.format(WIDTH,HEIGHT,x,y))
# Set the main window as the master for tos
tos.transient(menu)
# Raise tos window above the main window
tos.lift()
tos.grid_columnconfigure(0, weight=1)
#prevent tos from being resized
tos.resizable(False, False)

title_tos = ttk.Label(tos, text="Terms of Service", font=("Verdana", 20, "bold"))
title_tos.grid(row=0, column=0, sticky="NSEW", padx=10, pady=10)

# Create canvas for tos
tos_canvas = tk.Canvas(tos)#, width=tos_width)
tos_canvas.grid(row=1, column=0, sticky="NSEW")

# Create scrollbar for tos
tos_scrollbar = tk.Scrollbar(tos, orient="vertical", command=tos_canvas.yview)
tos_scrollbar.grid(row=1, column=1, sticky="ns")
tos_canvas.configure(yscrollcommand=tos_scrollbar.set)

# Make Labelframe inside canvas
tos_labelframe = ttk.LabelFrame(tos_canvas)
tos_labelframe.pack(fill="both", expand=True, pady=5,padx=5)

# Open textfile and put in tos
file_tos = open(r"tos.txt", "r", encoding="utf-8")
content_tos = ttk.Label(tos_labelframe, text=file_tos.read(), wraplength=400, font=("Verdana", 10))
content_tos.pack(pady=5, padx=5) 

# Configure canvas to scrollable region
tos_canvas.create_window((0, 0), window=tos_labelframe, anchor="nw")
tos_canvas.configure(scrollregion=tos_canvas.bbox("all"))

# Configure canvas scrolling
tos_labelframe.bind("<Configure>", lambda e: tos_canvas.configure(
    scrollregion=tos_canvas.bbox("all")))
tos_canvas.bind_all("<MouseWheel>", lambda e: tos_canvas.yview_scroll(
    int(-1 * (e.delta / 120)), "units"))

# Buttons at end of service
agree_button = ttk.Button(tos_labelframe, text="Agree", command=destroy_tos)
agree_button.pack(side="left", padx=5)

disagree_button = ttk.Button(tos_labelframe, text="Disagree", command=disagree_tos)
disagree_button.pack(side="right", padx=5)

def tos_closed():
    """
    Exit program if user exist TOS without agreeing
    """
    menu.destroy()

tos.protocol("WM_DELETE_WINDOW", tos_closed)

# Run mainloop
menu.mainloop()