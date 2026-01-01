import tkinter as tk
from tkinter import ttk
from Sign_in import New_Customer
from Login import login
from Table import mesa

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        #creating window part
        self.title("Basic Veterinary Appointment System")
        self.geometry(f"{620}x{730}")
        self.style = ttk.Style(self)
        self.tk.call("source", "forest/forest-light.tcl")
        self.style.theme_use("forest-light")
        # Configure the grid to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #mainframe
        self.main_frame = ttk.Frame(self,)
        self.main_frame.grid(row=0, column=1, sticky="news")
        # Configure the main frame to expand
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        ###########################################################################################################
        # Create a notebook
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=1, sticky="news")
        # Configure the notebook to expand
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.grid_columnconfigure(1, weight=1)
        ###########################################################################################################
        #Sign-in
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Sign-In")
        self.si = New_Customer(tab1)
        
        #Login
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Login")
        self.lg = login(tab2)  # Add the login frame to tab2 instead of tab1

        # Update
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Update")
        self.up = mesa(tab3)  # Add the login frame to tab2 instead of tab1

        # Binding tab change event to a function
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        current_tab = self.notebook.select()
        tab_name = self.notebook.tab(current_tab, "text")
        if tab_name == "Update":
            self.state('zoomed')  # Maximizing window when "Update" tab is selected
        else:
            self.state('normal')

    def set_theme(self, theme_name):
        self.style.theme_use(theme_name)

if __name__ == "__main__":
    app = Main()
    app.mainloop()