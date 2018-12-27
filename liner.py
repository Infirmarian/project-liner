# © Robert Geil 2018
import tkinter as tk
from tkinter import filedialog
import scraper
import localprog

bg_color = "lightblue"
width = 600
height = 600
large_font = ("Verdana", 35, "bold")
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
    "PHP":"#4F5D95",
    "Swift":"#ffac45"
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
# TODO: make webscraper run on seperate thread to prevent main program from hanging
# TODO: make loading indicator for better user experience
# TODO: make option to scrape through ALL user projects?
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
        sub = tk.Button(self, text="Analyze", command=self.get_distribution, highlightbackground=bg_color)
        sub.place(relx=0.75, rely=0.65, anchor="center")
        # Navigation buttons
        back = tk.Button(self, text="Back", command=self.page_back, highlightbackground=bg_color)
        back.place(relx=0.2, rely=0.8, anchor="center")
        end = tk.Button(self, text="Quit", command=lambda:exit(0), highlightbackground=bg_color)
        end.place(relx=0.8, rely=0.8, anchor="center")

        # Error message
        self.err = tk.Label(self, bg=bg_color, font=small_font, fg="red",text="")
        self.err.place(relx = 0.5, rely = 0.7, anchor="center")

    def clear_entries(self):
        self.username.delete(0, "end")
        self.project.delete(0, "end")
        self.err.config(text="")

    def page_back(self):
        self.clear_entries()
        self.controller.show_frame(SelectPage)

    def get_distribution(self):
        u = self.username.get()
        p = self.project.get()
        if u == "" or p == "":
            self.err.config(text="Username and project cannot be blank")
        else:
            res = scraper.get_language_frequency(u, p)
            if res["ErrorStatus"] == 0:
                self.clear_entries()
                self.controller.display_results(Result, res)
            else:
                self.err.config(text="That user or project doens't seem to exist, or is private. Try again!")
# TODO: improve GUI for selecting path
class LocalEntry(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.configure(height=height, width=width, bg=bg_color)
        label = tk.Label(self, text="Project Liner", bg=bg_color, font=large_font, justify="center")
        label.place(relx=0.5, rely=0.1, anchor="n")
        
        description = tk.Label(self, 
            text="Select a local directory to analyze. Checking the .gitignore button will cause the program to not count those files in the total", 
            bg=bg_color, font=("Verdana", 20), justify="center", wraplength=400)
        description.place(relx=0.5, rely=0.3, anchor="n")

        # Input path
        self.path_input = tk.Entry(self, highlightbackground=bg_color, width=35)
        self.path_input.place(relx=0.45, rely=0.55, anchor="center")
        canvas = tk.Canvas(self, width=25, height=25, highlightbackground=bg_color, bg="#ffdfa5")
        canvas.bind("<Button-1>", self.open_file_dialog)
        canvas.create_oval(5,12,10,17, fill="brown")
        canvas.create_oval(12,12,17,17, fill="brown")
        canvas.create_oval(19,12,24,17, fill="brown")
        canvas.place(relx=0.77, rely=0.55, anchor="center")

        # Option to use .gitignore when found
        self.bool_gitignore = tk.IntVar()
        self.check = tk.Checkbutton(self, bg=bg_color, text="Use .gitignore", variable=self.bool_gitignore)
        self.check.place(relx=0.7, rely=0.6, anchor="center")

        # Button to begin analysis
        select = tk.Button(self, text="Analyze", command=self.analyze, highlightbackground=bg_color)
        select.place(relx=0.5, rely=0.6, anchor="center")

        # Navigation buttons
        back = tk.Button(self, text="Back", command=self.page_back, highlightbackground=bg_color)
        back.place(relx=0.2, rely=0.8, anchor="center")
        end = tk.Button(self, text="Quit", command=lambda:exit(0), highlightbackground=bg_color)
        end.place(relx=0.8, rely=0.8, anchor="center")

        # Error message
        self.err = tk.Label(self, bg=bg_color, font=small_font, fg="red",text="")
        self.err.place(relx = 0.5, rely = 0.7, anchor="center")

    def page_back(self):
        self.controller.show_frame(SelectPage)

    def open_file_dialog(self, event):
        dir = filedialog.askdirectory()
        self.path_input.delete(0,"end")
        self.path_input.insert(0,dir)

    def reset_page(self):
        self.path_input.delete(0,"end")
        self.err.config(text="")

    def analyze(self):
        dir = self.path_input.get()
        res = localprog.get_code_frequency(dir, gitignore=self.bool_gitignore.get())
        if res["ErrorStatus"] != 0:
            print("Error, invalid path")
            self.err.config(text="Please enter a valid path")
        else:
            self.reset_page()
            self.controller.display_results(Result, res)


# Display the results of a project
class Result(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.configure(height=height, width=width, bg=bg_color)

        # Project Title
        self.project_title = tk.Label(self, text="", font=large_font, bg=bg_color)
        self.project_title.place(relx=0.5, rely=0.05, anchor="n")

        # Total lines
        self.lcount = tk.Label(self, text="", font=mid_font, bg=bg_color)
        self.lcount.place(relx=0.5, rely=0.2, anchor="n")

        # Canvas to display proportion bar
        self.bar_width=width-20
        self.bar = tk.Canvas(self, width=self.bar_width, height=100, bg=bg_color, highlightbackground=bg_color)
        self.bar.place(relx =0.5, rely=0.5, anchor="center")

        # Navigation buttons
        self.back = tk.Button(self, text="Back", command=self.page_back, highlightbackground=bg_color)
        self.back.place(relx=0.2, rely=0.8, anchor="center")
        end = tk.Button(self, text="Quit", command=lambda:exit(0), highlightbackground=bg_color)
        end.place(relx=0.8, rely=0.8, anchor="center")

    def display_data(self, data):
        # Configure the back button to jump back to the previous page
        if data["Type"] == "local":
            self.back.config(command=lambda: self.page_back(LocalEntry))
        elif data["Type"] == "GitHub":
            self.back.config(command=lambda: self.page_back(GitHubEntry))

        self.project_title.config(text=data["ProjectTitle"])
        total_lines = sum(data["languages"].values())
        self.lcount.config(text="Total lines: {}".format(total_lines))
        sorted_by_value = sorted(data["languages"].items(), key=lambda kv: kv[1], reverse=True)
        names_to_display = min(4, len(sorted_by_value))
        x_val = 0
        count = 1
        for lan in sorted_by_value:
            mini_width = self.bar_width*lan[1]/total_lines
            self.bar.create_rectangle(x_val, 0, x_val+mini_width, 20, fill=color_map[lan[0]], outline="")

            if count <= names_to_display:
                self.bar.create_oval(count*self.bar_width/(names_to_display+1)-4, 25, 6+count*self.bar_width/(names_to_display+1), 35, fill=color_map[lan[0]], outline="")
                
                self.bar.create_text(count*(self.bar_width)/(names_to_display+1), 45, text=lan[0], font=small_font)
                self.bar.create_text(count*(self.bar_width)/(names_to_display+1), 80, text="{} lines\n({}%)".format(lan[1], round(100*lan[1]/total_lines,1)), font=small_font, justify="center")
            
            x_val += mini_width
            count += 1
        
    def page_back(self, page=SelectPage):
        self.bar.delete("all")
        self.controller.show_frame(page)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Project Liner")
        self.config(bg=bg_color, width=width, height=height)
        self.resizable(False, False)
        container = tk.Frame(self)
        container.grid()

        self.frames = {}

        for F in [SelectPage, GitHubEntry, LocalEntry, Result]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SelectPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    # Specialized display frame function to load data as well
    def display_results(self, cont, data):
        frame = self.frames[cont]
        frame.display_data(data)
        frame.tkraise()

if __name__ == "__main__":
    app = Application()
    app.lift()
    app.mainloop()