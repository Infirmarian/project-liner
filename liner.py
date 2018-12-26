# © Robert Geil 2018
import tkinter as tk
import scraper

bg_color = "lightblue"

def quit_GUI():
    exit(0)
def calculate_lines():
    u = username.get()
    p = project.get()
    print("Getting info about {p} by {u}".format(p=p, u=u))

window = tk.Tk()
window.title("Project Liner")
window.config(width=600,height=600)

# Canvas
canvas = tk.Canvas(window, bg=bg_color, width=window.winfo_reqwidth(), height=window.winfo_reqheight())
# Quit button
end = tk.Button(window, text="Quit", command=quit_GUI, highlightbackground=bg_color)
end.place(relx=0.8, rely=0.8, anchor="center")

title = tk.Label(window, text = "Project Liner", bg=bg_color, font=("Verdana", 50, "bold"))
title.place(relx=0.5, rely=0.1, anchor="n")
description = tk.Label(window, 
    text="Enter a GitHub username and project name to find out the code distribution for that project", 
    bg=bg_color, 
    font=("Verdana", 20),
    wraplength=300, justify="center")
description.place(relx=0.5, rely=0.3, anchor="n")

uprompt = tk.Label(window, text="Enter username", bg=bg_color, font=("Verdana", 15))
uprompt.place(relx=0.3, rely=0.55, anchor="center")
username = tk.Entry(window, width=15, highlightbackground=bg_color)
username.place(relx=0.3, rely=0.6, anchor="center")

pprompt = tk.Label(window, text="Enter project name", bg=bg_color, font=("Verdana", 15))
pprompt.place(relx=0.7, rely=0.55, anchor="center")
project = tk.Entry(window, width=15, highlightbackground=bg_color)
project.place(relx=0.7, rely=0.6, anchor="center")

submit = tk.Button(window, text="Calculate Lines", command=calculate_lines, highlightbackground=bg_color)
submit.place(relx=0.5, rely=0.7, anchor="center")
canvas.pack()




window.lift()
#window.attributes('-topmost',True)
window.mainloop()