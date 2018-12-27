# © Robert Geil 2018
import tkinter as tk
from tkinter import filedialog
import scraper

bg_color = "lightblue"
width = 600
height = 600
large_font = ("Verdana", 50, "bold")
mid_font = ("Verdana", 20, "bold")
small_font = ("Verdana", 15, "bold")
# This dictionary maps from languages to hex value colors, based on GitHub's color scheme for 
# each programming language
color_map = {
    "Python":"#3572A5",
    "JavaScript":"#f1e05a",
    "Java":"#b07219",
    "C#":"#178600",
    "C++":"#f34b7d",
    "HTML":"#e34c26",
    "CSS":"#563d7c",
    "C":"#555555",
    "Ruby":"#701516",
    "Go":"#375eab",
    "PHP":"#4F5D95"
}

class SelectPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.configure(height=height, width=width, bg=bg_color)
        label = tk.Label(self, text="Project Liner", bg=bg_color, font=large_font, justify="center")
        label.place(relx=0.5, rely=0.1, anchor="n")
        description = tk.Label(self, 
            text="This project determines the amount and language of code written in different projects. Both local projects\
             as well as those hosted on GitHub can be measured. Select which type of project you would like to analyze", 
            bg=bg_color, 
            font=("Verdana", 20),
            wraplength=400, justify="center")
        description.place(relx=0.5, rely=0.3, anchor="n")

        github = tk.Button(self, text="GitHub", highlightbackground = bg_color, command=lambda: controller.show_frame(GitHubEntry))
        github.place(relx=0.35, rely=0.6, anchor="n")

        local = tk.Button(self, text="Local", highlightbackground = bg_color, command=lambda: controller.show_frame(LocalEntry))
        local.place(relx=0.65, rely=0.6, anchor="n")

        end = tk.Button(self, text="Quit", command=lambda:exit(0), highlightbackground=bg_color)
        end.place(relx=0.8, rely=0.8, anchor="center")

class GitHubEntry(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.configure(height=height, width=width, bg=bg_color)
        label = tk.Label(self, text="Project Liner", bg=bg_color, font=large_font, justify="center")
        label.place(relx=0.5, rely=0.1, anchor="n")
        description = tk.Label(self, 
            text="Enter a GitHub username and a (public) project. While the program is designed to have "+
            "minmal impact on GitHub's servers, any rate limiting is accepted by the end user",
            bg=bg_color, 
            font=("Verdana", 20),
            wraplength=400, justify="center")
        description.place(relx=0.5, rely=0.3, anchor="n")


        # GitHub username, project input boxes
        uprompt=tk.Label(self, text="Username", bg=bg_color, font=small_font)
        uprompt.place(relx=0.3, rely=0.55, anchor="center")
        self.username = tk.Entry(self, width=20, highlightbackground=bg_color)
        self.username.place(relx=0.3, rely=0.6, anchor="center")

        self.project = tk.Entry(self, width=20, highlightbackground=bg_color)
        self.project.place(relx=0.7, rely=0.6, anchor="center")
        pprompt=tk.Label(self, text="Project", bg=bg_color, font=small_font)
        pprompt.place(relx=0.7, rely=0.55, anchor="center")
        # Submit button
        sub = tk.Button(self, text="Get Lines", command=self.get_distribution, highlightbackground=bg_color)
        sub.place(relx=0.75, rely=0.65, anchor="center")
        # Navigation buttons
        back = tk.Button(self, text="Back", command=self.page_back, highlightbackground=bg_color)
        back.place(relx=0.1, rely=0.1, anchor="center")
        end = tk.Button(self, text="Quit", command=lambda:exit(0), highlightbackground=bg_color)
        end.place(relx=0.8, rely=0.8, anchor="center")

    def page_back(self):
        self.username.delete(0, "end")
        self.project.delete(0, "end")
        self.controller.show_frame(SelectPage)

    def get_distribution(self):
        u = self.username.get()
        p = self.project.get()
        print("Getting project {} from user {}".format(p, u))

class LocalEntry(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.configure(height=height, width=width, bg=bg_color)
        label = tk.Label(self, text="Project Liner", bg=bg_color, font=large_font, justify="center")
        label.place(relx=0.5, rely=0.1, anchor="n")

        select = tk.Button(self, text="Select Directory", command=self.get_directory, highlightbackground=bg_color)
        select.place(relx=0.5, rely=0.6, anchor="center")

        # Navigation buttons
        back = tk.Button(self, text="Back", command=self.page_back, highlightbackground=bg_color)
        back.place(relx=0.1, rely=0.1, anchor="center")
        end = tk.Button(self, text="Quit", command=lambda:exit(0), highlightbackground=bg_color)
        end.place(relx=0.8, rely=0.8, anchor="center")

    def page_back(self):
        self.controller.show_frame(SelectPage)
    def get_directory(self):
        dir = filedialog.askdirectory()
        if dir != "":
            print(dir)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Project Liner")
        self.config(bg=bg_color, width=width, height=height)
        self.resizable(False, False)
        container = tk.Frame(self)
        container.grid()

        self.frames = {}

        for F in [SelectPage, GitHubEntry, LocalEntry]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SelectPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = Application()
    app.lift()
    app.mainloop()