from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext

# Create TOS
TOS = Tk()
TOS.title("Terms of Service")
TOS.geometry("500x400")
TOS.grid_columnconfigure(0, weight=1)

title_tos = Label(TOS, text="Terms of Service", font=("Courier", 20, "bold"))
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
content_tos = Label(tos_labelframe, text=f.read())
content_tos.pack(pady=5, padx=5)

# Configure canvas to scrollable region
tos_canvas.create_window((0, 0), window=tos_labelframe, anchor="nw")
tos_canvas.configure(scrollregion=tos_canvas.bbox("all"))

# Configure canvas scrolling
tos_labelframe.bind("<Configure>", lambda e: tos_canvas.configure(scrollregion=tos_canvas.bbox("all")))
tos_canvas.bind_all("<MouseWheel>", lambda e: tos_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

# Buttons at end of service
agree_button = ttk.Button(tos_labelframe, text="Agree")
#agree_button.grid(padx=5, sticky=W, row=2, column=0)
agree_button.pack(side=LEFT, padx=5)

disagree_button = ttk.Button(tos_labelframe, text="Disagree")
#disagree_button.grid(padx=5, row=2, column=1, sticky=E)
disagree_button.pack(side=RIGHT, padx=5)

# Run mainloop
TOS.mainloop()