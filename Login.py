import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry as tkDateEntry
from mysql.connector import Error, connect
from datetime import datetime

class login():
    def __init__(self, root):
        self.root = root
        self.db = self.setup_database()
        self.setup_ui()

    def setup_database(self):
        try:
            # Establish a connection to your MySQL database
            db = connect(
                host="localhost",
                user="root",
                database="vet_reserve"
            )
            return db
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return None
        
    def setup_ui(self):
        
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-light")  # Default theme
    
        # Title label at the top of the window
        main_title_label = ttk.Label(self.root, text="Basic Veterinary Appointment System", font=("Arial", 24, "bold"))
        main_title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.frame = ttk.Frame(self.root, width=600, height=400)
        self.frame.grid(row=1, column=0)

        self.widgets_frame = ttk.LabelFrame(self.frame, text="Existing Account", width=400, height=200)
        self.widgets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.table_frame = ttk.Frame(self.frame)
        self.table_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        def handle_placeholder(entry, placeholder_text):
            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder_text)
                    entry.configure(foreground='grey')

            def on_focus_in(event):
                if entry.get() == placeholder_text:
                    entry.delete(0, 'end')
                    entry.configure(foreground='black')

            entry.insert(0, placeholder_text)
            entry.bind("<FocusOut>", on_focus_out)
            entry.bind("<FocusIn>", on_focus_in)

        owner_label = ttk.Label(self.widgets_frame, text="Owner Info.", font=("Arial", 12, "bold"))
        owner_label.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="nsew", columnspan=2)

        self.search_entry = ttk.Entry(self.widgets_frame, font=("Arial", 12,))
        handle_placeholder(self.search_entry, "Owner ID/Owner Name")
        self.search_entry.grid(row=1, column=0,columnspan=2, padx=(5, 5), pady=(10, 5), sticky="ew")

        # Search
        search_button = ttk.Button(self.widgets_frame, text="Search", command=self.search_owner_by_name_or_id)
        search_button.grid(row=1, column=1, padx=(0, 5), pady=(10, 5), sticky="e")


        self.create_separator(2, 0, columnspan=2, pady=(10, 5))

        pet_label = ttk.Label(self.widgets_frame, text="Pet Info.", font=("Arial", 12, "bold"))
        pet_label.grid(row=4, column=0, padx=5, pady=(10, 5), sticky="nsew", columnspan=2)

        self.petname_entry = ttk.Entry(self.widgets_frame, font=("Arial", 12))
        handle_placeholder(self.petname_entry, "Pet Name")
        self.petname_entry.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        self.age = ttk.Spinbox(
            self.widgets_frame,
            from_=0,
            to=300,
            font=("Arial", 12),
            width=5
        )
        handle_placeholder(self.age, "Age")
        self.age.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        #Species
        species_options = ["Dog", "Cat", "Bird", "Rabbit", "--Insert Others--"]  # Add your desired species options here
        self.species_combobox = ttk.Combobox(self.widgets_frame, values=species_options, font=("Arial", 12))
        self.species_combobox.set("Species")  # Set a default value
        self.species_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.species_combobox.bind("<<ComboboxSelected>>", self.species_selection_changed)      

        #Breed
        self.breed_entry = ttk.Entry(self.widgets_frame, font=("Arial", 12))
        handle_placeholder(self.breed_entry, "Breed")
        self.breed_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        self.create_separator(7, 0, columnspan=2, pady=(10, 5))

        appointment_label = ttk.Label(self.widgets_frame, text="Appointment", font=("Arial", 12, "bold"))
        appointment_label.grid(row=8, column=0, padx=5, pady=(10, 5), sticky="nsew", columnspan=2)

        self.reason_entry = ttk.Combobox(self.widgets_frame, font=("Arial", 12))
        self.reason_entry['values'] = ["Checkup", "Vaccination", "Treatment", "Biochem", "Surgery", "Other"]
        self.reason_entry.set("Reason")  # Set a default value
        self.reason_entry.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        time_label = ttk.Label(self.widgets_frame, text="Date & Time", font=("Arial", 12, "bold"))
        time_label.grid(row=10, column=0, padx=5, pady=(10, 5), sticky="nsew", columnspan=2)

        self.date_picker = tkDateEntry(self.widgets_frame, font=("Arial", 12), width=10, date_pattern="yyyy-MM-dd")
        self.date_picker.grid(row=12, column=0, padx=5, pady=(0, 5), sticky="ew")

        time_frame = ttk.Frame(self.widgets_frame)
        time_frame.grid(row=12, column=1, padx=5, pady=(0, 5), sticky="ew")

        # Time Picker - Hours
        self.hour_spinbox = ttk.Spinbox(time_frame, from_=1, to=12, font=("Arial", 12), width=3)
        handle_placeholder(self.hour_spinbox, "HH")
        self.hour_spinbox.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")

        ttk.Label(time_frame, text=":", font=("Arial", 12)).grid(row=0, column=1, padx=2, pady=5, sticky="ew")

        # Time Picker - Minutes
        self.minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, font=("Arial", 12), width=3)
        handle_placeholder(self.minute_spinbox, "MM")
        self.minute_spinbox.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="ew")

        # AM/PM Picker
        self.ampm_combobox = ttk.Combobox(time_frame, values=["AM", "PM"], font=("Arial", 12), width=5)
        self.ampm_combobox.set("AM")  # Set a default value
        self.ampm_combobox.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.status_combobox = ttk.Combobox(
            self.widgets_frame, values=["Scheduled", "Canceled", "Completed", "Reschedule"],  
            font=("Arial", 12), width=10
        )
        handle_placeholder(self.status_combobox, "Status")
        self.status_combobox.grid(row=13, column=0, columnspan=1, padx=5, pady=(0, 5), sticky="ew")

        self.create_separator(14, 0, columnspan=2, pady=(10, 5))
        
        # Add Button
        add_button = ttk.Button(self.widgets_frame, text="Add Pet and Appointment", command=self.add_pet_with_appointment_to_owner)
        add_button.grid(row=15, column=0, padx=5, pady=(10, 5), sticky="ew")

        # Button to show reservations
        show_reservations_button = ttk.Button(self.widgets_frame, text="Show Reservations", command=self.show_reservations)
        show_reservations_button.grid(row=15, column=1, padx=5, pady=(10, 5), sticky="ew")

    
    def search_owner_by_name_or_id(self):
        try:
            search_text = self.search_entry.get()
            if not search_text:
                messagebox.showwarning("Empty Field", "Please enter Owner Name or Owner ID to search.")
                return

            if self.db:
                with self.db.cursor() as cursor:
                    if search_text.isdigit():
                        cursor.execute("SELECT * FROM Owners WHERE OwnerID = %s", (search_text,))
                    else:
                        cursor.execute("SELECT * FROM Owners WHERE Name LIKE %s", (f"%{search_text}%",))

                    owners = cursor.fetchall()

                    if owners:
                        messagebox.showinfo("Owner Exists", f"Owner with Name/ID: {search_text} already exists.")
                    else:
                        messagebox.showwarning("Owner Not Found", f"No owner found with Name/ID: {search_text}")

        except Error as e:
            print(f"Error searching for owner: {e}")

        
    def add_pet_with_appointment_to_owner(self):
        try:
            # Gather pet details
            owner_name=self.search_entry.get()
            pet_name = self.petname_entry.get()
            pet_age = int(self.age.get())
            species = self.species_combobox.get()
            breed = self.breed_entry.get()

            # Gather appointment details
            reason = self.reason_entry.get()
            date = self.date_picker.get()
            hour = int(self.hour_spinbox.get())
            minute = int(self.minute_spinbox.get())
            ampm = self.ampm_combobox.get()
            status = self.status_combobox.get()

            # Convert time to 24-hour format
            if ampm == "PM" and hour != 12:
                hour += 12
            elif ampm == "AM" and hour == 12:
                hour = 0

            # Combine date and time
            appointment_time = f"{date} {hour:02d}:{minute:02d}:00"

            # Convert to datetime object
            appointment_datetime = datetime.strptime(appointment_time, "%Y-%m-%d %H:%M:%S")

            # Check if appointment time is in the past
            if appointment_datetime < datetime.now():
                messagebox.showwarning("Invalid Time", "Please select a future date and time.")
                return

            if self.db:
                with self.db.cursor() as cursor:
                    # Retrieve the OwnerID based on the owner name
                    cursor.execute("SELECT OwnerID FROM Owners WHERE Name = %s", (owner_name,))
                    result = cursor.fetchone()
                    if result:
                        owner_id = result[0]

                        # Insert new pet for the existing owner
                        cursor.execute("INSERT INTO Pets (Name, OwnerID, Species, Breed, Age) VALUES (%s, %s, %s, %s, %s)",
                                    (pet_name, owner_id, species, breed, pet_age))
                        pet_id = cursor.lastrowid  # Get the ID of the newly inserted pet

                        # Insert appointment for the new pet
                        cursor.execute("INSERT INTO Appointments (PetID, Date, Reason, Status) VALUES (%s, %s, %s, %s)",
                                    (pet_id, appointment_datetime, reason, status))

                        # Commit changes and display success message
                        self.db.commit()
                        messagebox.showinfo("Reservation Added", "Reservation for the new pet has been successfully added!")
                    else:
                        messagebox.showwarning("Owner Not Found", f"No owner found with Name: {owner_name}")

        except Error as e:
            print(f"Error adding pet with appointment: {e}")

    def show_reservations(self):
        if self.db:
            try:
                with self.db.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            Owners.OwnerID AS OwnerID, Owners.Name AS OwnerName, Owners.Address, Owners.Contact_Info,
                            Pets.Name AS PetName, Pets.Species, Pets.Breed,
                            Appointments.Reason, DATE_FORMAT(Appointments.Date, '%Y-%m-%d %h:%i %p') AS Date, Appointments.Status
                        FROM Owners
                        INNER JOIN Pets ON Owners.OwnerID = Pets.OwnerID
                        INNER JOIN Appointments ON Pets.PetID = Appointments.PetID
                    """)
                    reservations = cursor.fetchall()

                # Create a new window for reservations
                reservations_window = tk.Toplevel(self.root)
                reservations_window.title("Reservations")

                # Create a frame in the new window
                table_frame = ttk.Frame(reservations_window)
                table_frame.pack(fill="both", expand=True)

                columns = (
                    "OwnerID", "Owner Name", "Address", "Contact Info",
                    "Pet Name", "Species", "Breed", "Reason", "Date", "Status"
                )

                reservations_treeview = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode="browse")

                # Define column headings
                for col in columns:
                    reservations_treeview.heading(col, text=col)

                # Set column widths
                column_widths = (48, 100, 110, 120, 70, 80, 100, 130, 130, 80)  # Updated width for the "Date" column
                for idx, col in enumerate(columns):
                    reservations_treeview.column(col, width=column_widths[idx], anchor="center")

                # Add a scrollbar
                scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=reservations_treeview.yview)
                scrollbar.pack(side="right", fill="y")
                reservations_treeview.config(yscrollcommand=scrollbar.set)

                    # Configure tags for alternate row colors
                reservations_treeview.tag_configure("oddrow", background="light Gray", font=("Arial", 11))
                reservations_treeview.tag_configure("evenrow", background="#FFFFFF", font=("Arial", 11))

                # Insert fetched data into the treeview with alternating row tags
                for idx, reservation in enumerate(reservations):
                    tags = ('evenrow',) if idx % 2 == 0 else ('oddrow',)
                    reservations_treeview.insert("", "end", values=reservation, tags=tags)

                # Position the Treeview
                reservations_treeview.pack(expand=True, fill="both")

            except Error as e:
                print(f"Error fetching reservations: {e}")

  
    def create_separator(self, row, column, columnspan=2, padx=(20, 10), pady=10, sticky="ew"):
        separator = ttk.Separator(self.widgets_frame)
        separator.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)
        return separator
    
    def species_selection_changed(self, event):
        selected_species = self.species_combobox.get()
        if selected_species == "--Insert Others--":
            # Reset to the default value or choose a different action if needed
            self.species_combobox.set("Species")

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x_offset = (self.root.winfo_screenwidth() - width) // 2
        y_offset = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x_offset}+{y_offset}")


    def on_resize(self, event):
        self.center_window()

if __name__ == "__main__":
    root = tk.Tk()
    app = login(root)
    root.resizable(False, False)
    root.mainloop()
