from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext

# Make main window
menu = Tk()
menu.title("Fake News Detector")
menu.state('zoomed')
menu.grid_columnconfigure(0, weight=1)
menu.configure(bg="#EAE0D5")

# Create title of page
title_label = Label(menu, text="Fake News Detector", foreground="#22333B", bg="#EAE0D5", font=("Helvetica", 40, "bold"))
title_label.grid(padx=10, pady=10, column=0, row=0)

# Icon
icon = PhotoImage(file="assets/icon.png")
icon = icon.subsample(2)
icon_label = Label(menu, image=icon, bg='#EAE0D5')
icon_label.grid(row=0, column=0, sticky=NW)

# Subheading
file = open(r"text_files/intro_text.txt", "r")
userinp_label = Label(menu, text=file.read(), font=("Helvetica", 10))
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

# User input and output
user_text = scrolledtext.ScrolledText(user_labelframe)
user_text.grid(row=1, column=0, sticky=NSEW)

output_text = scrolledtext.ScrolledText(user_labelframe)
output_text.grid(row=1, column=1, sticky=NSEW)

user_text.configure(state="disabled", bg="#898989")
output_text.configure(state="disabled", bg="#898989")

# Enter button for input
enter_button = Button(menu, text="Enter", justify=CENTER)
enter_button.grid(row=4, column=0, sticky=W, padx=20, pady=5)

menu.mainloop()