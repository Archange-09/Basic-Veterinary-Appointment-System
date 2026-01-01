import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry as tkDateEntry
from mysql.connector import Error, connect
from datetime import datetime

class DataEntry:
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
        
        self.root.title("Basic Veterinary Appointment System")
        self.style = ttk.Style(self.root)
        self.root.tk.call("source", "forest/forest-light.tcl")
        self.style.theme_use("forest-light")  # Default theme
    
        # Title label at the top of the window
        main_title_label = ttk.Label(self.root, text="Basic Veterinary Appointment System", font=("Arial", 24, "bold"))
        main_title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.frame = ttk.Frame(self.root, width=600, height=400)
        self.frame.grid(row=1, column=0)

        self.widgets_frame = ttk.LabelFrame(self.frame, text="Details", width=400, height=200)
        self.widgets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        # Title label for the details frame
        details_title_label = ttk.Label(self.widgets_frame, text="Details", font=("Arial", 12, "bold"))
        details_title_label.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="nsew")

        self.table_frame = ttk.Frame(self.frame)
        self.table_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Create a new frame for the search bar
        self.search_frame = ttk.Frame(self.root)
        self.search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ne")  # Positioned on the top left

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

        # Search Entry Field
        self.search_entry = ttk.Entry(self.search_frame, font=("Arial", 12,), width=32)
        handle_placeholder(self.search_entry, "Owner ID/Owner Name/Pet Name")
        self.search_entry.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="ew")

        # Search Button
        search_button = ttk.Button(self.search_frame, text="Search", command=self.search_by_id_or_name)
        search_button.grid(row=0, column=1, padx=5, pady=(10, 5), sticky="ew")

        owner_label = ttk.Label(self.widgets_frame, text="Owner Info.", font=("Arial", 12, "bold"))
        owner_label.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="nsew", columnspan=2)

        self.name_entry = ttk.Entry(self.widgets_frame, font=("Arial", 12))
        handle_placeholder(self.name_entry, "Name")
        self.name_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.contact_entry = ttk.Entry(self.widgets_frame, font=("Arial", 12))
        handle_placeholder(self.contact_entry, "Contact Info")
        self.contact_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.address_entry = ttk.Entry(self.widgets_frame, font=("Arial", 12))
        handle_placeholder(self.address_entry, "Address")
        self.address_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")


        self.create_separator(3, 0, columnspan=2, pady=(10, 5))

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

        self.reason_entry = ttk.Entry(self.widgets_frame, font=("Arial", 12))
        handle_placeholder(self.reason_entry, "Reason")
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
        
        # Upload Button
        upload_button = ttk.Button(self.widgets_frame, text="Add Reservation", command=self.add_reservation)
        upload_button.grid(row=15, column=0, columnspan=1, padx=5, pady=(10, 5), sticky="ew")

        # Button to show reservations
        show_reservations_button = ttk.Button(self.widgets_frame, text="Show Reservations", command=self.show_reservations)
        show_reservations_button.grid(row=15, column=1, columnspan=2, padx=5, pady=(10, 5), sticky="ew")

        # Create a button to clear the table
        clear_table_button = ttk.Button(self.widgets_frame, text="Clear Table", command=self.clear_table)
        clear_table_button.grid(row=16, column=0, columnspan=1, padx=5, pady=(10, 5), sticky="nsew")

        '''
        # Delete
        delete_reservation_button = ttk.Button(self.widgets_frame, text="Delete Reservation", command=self.delete_reservation)
        delete_reservation_button.grid(row=17, column=0, columnspan=1, padx=5, pady=(10, 5), sticky="ew")
        '''

        # Button to update reservation
        update_reservation_button = ttk.Button(self.widgets_frame, text="Update Reservation", command=self.update_reservation)
        update_reservation_button.grid(row=16, column=1, columnspan=1, padx=5, pady=(10, 5), sticky="ew")

        self.create_separator(17, 0, columnspan=2, pady=(10, 5))
        
        self.table_frame = ttk.Frame(self.frame)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        columns = (
            "OwnerID", "Owner Name", "Address", "Contact Info",
            "Pet Name", "Species", "Breed", "Reason", "Date", "Status"
        )

        self.reservations_treeview = ttk.Treeview(self.table_frame, columns=columns, show='headings', selectmode="browse")

        # Define column headings
        for col in columns:
            self.reservations_treeview.heading(col, text=col)

        # Set column widths
        column_widths = (48, 100, 110, 120, 70, 80, 100, 130, 130, 80)  # Updated width for the "Date" column
        for idx, col in enumerate(columns):
            self.reservations_treeview.column(col, width=column_widths[idx], anchor="center")


        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.reservations_treeview.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure Treeview
        self.reservations_treeview.configure(yscrollcommand=scrollbar.set)
        self.reservations_treeview.pack(expand=True, fill="both")

        # Configure tags for alternate row colors
        self.reservations_treeview.tag_configure("oddrow", background="light Gray", font=("Arial",10))  
        self.reservations_treeview.tag_configure("evenrow", background="#FFFFFF", font=("Arial",10))  


    def add_reservation(self):
        try:
            # Retrieve values from the entry fields
            owner_name = self.name_entry.get()
            contact_info = self.contact_entry.get()
            address = self.address_entry.get()
            pet_name = self.petname_entry.get()
            pet_age = int(self.age.get())
            species = self.species_combobox.get()
            breed = self.breed_entry.get()
            reason = self.reason_entry.get()
            date = self.date_picker.get()
            hour = int(self.hour_spinbox.get())
            minute = int(self.minute_spinbox.get())
            ampm = self.ampm_combobox.get()
            status = self.status_combobox.get()

            # Convert 12-hour format to 24-hour format
            if ampm == "PM" and hour != 12:
                hour += 12  # Add 12 hours for PM except for 12 PM
            elif ampm == "AM" and hour == 12:
                hour = 0  # Convert 12 AM (midnight) to 0

            # Format the time in 24-hour format with seconds as 00
            appointment_time = f"{hour:02d}:{minute:02d}:00"

            # Combine the date and time for the appointment
            appointment_datetime = f"{date} {appointment_time}"

            # Convert the selected appointment date and time to a datetime object
            appointment_datetime = datetime.strptime(appointment_datetime, "%Y-%m-%d %H:%M:%S")

            # Check if the appointment time is in the past
            if appointment_datetime < datetime.now():
                messagebox.showwarning("Invalid Time", "Please select a future date and time.")
                return  # Stop further execution if the time is in the past

            # Insert owner information into the Owners table
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO Owners (Name, Contact_Info, Address) VALUES (%s, %s, %s)",
                           (owner_name, contact_info, address))
            owner_id = cursor.lastrowid  # Get the ID of the newly inserted owner

            # Insert pet information into the Pets table
            cursor.execute("INSERT INTO Pets (Name, OwnerID, Species, Breed, Age) VALUES (%s, %s, %s, %s, %s)",
                           (pet_name, owner_id, species, breed, pet_age))
            pet_id = cursor.lastrowid  # Get the ID of the newly inserted pet

            # Insert appointment information into the Appointments table
            cursor.execute("INSERT INTO Appointments (PetID, Date, Reason, Status) VALUES (%s, %s, %s, %s)",
                           (pet_id, appointment_datetime, reason, status))

            # Commit changes and close cursor
            self.db.commit()
            cursor.close()

            # Display a popup message confirming the successful reservation addition
            messagebox.showinfo("Reservation Added", "Reservation has been successfully added!")
        except Error as e:
            print(f"Error adding reservation: {e}")
    
    def show_reservations(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT 
                    Owners.OwnerID AS OwnerID, Owners.Name AS OwnerName, Owners.Address, Owners.Contact_Info,
                    Pets.Name AS PetName, Pets.Species, Pets.Breed,
                    Appointments.Reason, DATE_FORMAT(Appointments.Date, '%Y-%m-%d %h:%i %p') AS Date, Appointments.Status
                FROM Owners
                INNER JOIN Pets ON Owners.OwnerID = Pets.OwnerID
                INNER JOIN Appointments ON Pets.PetID = Appointments.PetID
            """)


            rows = cursor.fetchall()

            # Clear existing items in the table
            for item in self.reservations_treeview.get_children():
                self.reservations_treeview.delete(item)

            # Populate the table with fetched data
            for idx, row in enumerate(rows):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.reservations_treeview.insert("", "end", values=row, tags=(tag,))

            cursor.close()
        except Error as e:
            print(f"Error fetching data: {e}")


    def update_reservation(self):
        try:
            selected_item = self.reservations_treeview.selection()[0]  
            values = self.reservations_treeview.item(selected_item)['values']  
            owner_id = values[0]  

            # Fetch the original values from the database
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT 
                    Pets.PetID,
                    Owners.OwnerID,
                    Owners.Name, Owners.Contact_Info, Owners.Address,
                    Pets.Name, Pets.Age, Pets.Species, Pets.Breed,
                    Appointments.Reason, Appointments.Date, Appointments.Status
                FROM Owners
                INNER JOIN Pets ON Owners.OwnerID = Pets.OwnerID
                INNER JOIN Appointments ON Pets.PetID = Appointments.PetID
                WHERE Owners.OwnerID = %s
            """, (owner_id,))
            original_values = cursor.fetchone()

            # Compare original values with updated values
            updated_values = (
                self.name_entry.get(),
                self.contact_entry.get(),
                self.address_entry.get(),
                self.petname_entry.get(),
                int(self.age.get()) if self.age.get().isdigit() else 0,
                self.species_entry.get(),
                self.breed_entry.get(),
                self.reason_entry.get(),
                self.date_picker.get(),
                int(self.hour_spinbox.get()) if self.hour_spinbox.get().isdigit() else 0,
                int(self.minute_spinbox.get()) if self.minute_spinbox.get().isdigit() else 0,
                self.status_combobox.get()
            )

            # Check for placeholder values ('HH', 'MM') before converting to int
            if updated_values[9] == 0 or updated_values[10] == 0:
                messagebox.showwarning("Invalid Time", "Please enter valid hour and minute values.")
                return  # Stop execution if the hour or minute is not valid

            # Construct updated appointment date and time
            updated_appointment_date = f"{updated_values[8]} {updated_values[9]:02d}:{updated_values[10]:02d}:00"

            # Update owner details
            cursor.execute("""
                UPDATE Owners 
                SET Name = %s, Contact_Info = %s, Address = %s
                WHERE OwnerID = %s
            """, (updated_values[0], updated_values[1], updated_values[2], original_values[1]))

            # Update pet details
            cursor.execute("""
                UPDATE Pets 
                SET Name = %s, Age = %s, Species = %s, Breed = %s
                WHERE PetID = %s
            """, (updated_values[3], updated_values[4], updated_values[5], updated_values[6], original_values[0]))

            # Update appointment details
            cursor.execute("""
                UPDATE Appointments 
                SET Date = %s, Reason = %s, Status = %s
                WHERE PetID = %s
            """, (updated_appointment_date, updated_values[7], updated_values[11], original_values[0]))

            self.db.commit()
            cursor.close()

            messagebox.showinfo("Reservation Updated", "Reservation has been successfully updated!")
            self.show_reservations()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a reservation to update.")
        except Error as e:
            print(f"Error updating reservation: {e}")

    '''
    def delete_reservation(self):
        try:
            selected_item = self.reservations_treeview.selection()[0]  # Get the selected item from the Treeview
            values = self.reservations_treeview.item(selected_item)['values'] 
            owner_id = values[0]  

            confirmation = messagebox.askokcancel(
                "Confirm Deletion",
                "Are you sure you want to delete this reservation?", icon ='warning'
            )
            
            if confirmation:
                cursor = self.db.cursor()

                # Get PetIDs associated with the OwnerID
                cursor.execute("SELECT PetID FROM Pets WHERE OwnerID = %s", (owner_id,))
                pet_ids = [pet[0] for pet in cursor.fetchall()]

                # Delete appointments related to the pets
                for pet_id in pet_ids:
                    cursor.execute("DELETE FROM Appointments WHERE PetID = %s", (pet_id,))

                # Delete pets associated with the OwnerID
                cursor.execute("DELETE FROM Pets WHERE OwnerID = %s", (owner_id,))

                # Delete the owner
                cursor.execute("DELETE FROM Owners WHERE OwnerID = %s", (owner_id,))

                self.db.commit()
                cursor.close()

                # Remove the selected item from the Treeview
                self.reservations_treeview.delete(selected_item)
                messagebox.showinfo("Reservation Deleted", "Reservation has been successfully deleted!")
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a reservation to delete.")
        except Error as e:
            print(f"Error deleting reservation: {e}")
    '''
    def search_by_name(self):
        try:
            search_name = self.name_entry.get()  # Get the name to search from the entry field
            cursor = self.db.cursor()

            # Perform a SELECT query to retrieve reservations based on the provided name
            cursor.execute("""
                SELECT 
                    Owners.OwnerID AS OwnerID, Owners.Name AS OwnerName, Owners.Address, Owners.Contact_Info,
                    Pets.Name AS PetName, Pets.Species, Pets.Breed,
                    Appointments.Reason, Appointments.Date, Appointments.Status
                FROM Owners
                INNER JOIN Pets ON Owners.OwnerID = Pets.OwnerID
                INNER JOIN Appointments ON Pets.PetID = Appointments.PetID
                WHERE Owners.Name LIKE %s
            """, (f'%{search_name}%',))

            rows = cursor.fetchall()

            # Clear existing items in the table
            for item in self.reservations_treeview.get_children():
                self.reservations_treeview.delete(item)

            # Populate the table with fetched data
            for idx, row in enumerate(rows):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.reservations_treeview.insert("", "end", values=row, tags=(tag,))

            cursor.close()
        except Error as e:
            print(f"Error searching data: {e}")

    def search_by_id_or_name(self):
        try:
            search_term = self.search_entry.get()
            cursor = self.db.cursor()

            # Check if the search term is a number (owner ID)
            if search_term.isdigit():
                cursor.execute("""
                    SELECT 
                        Owners.OwnerID AS OwnerID, Owners.Name AS OwnerName, Owners.Address, Owners.Contact_Info,
                        Pets.Name AS PetName, Pets.Species, Pets.Breed,
                        Appointments.Reason, Appointments.Date, Appointments.Status
                    FROM Owners
                    INNER JOIN Pets ON Owners.OwnerID = Pets.OwnerID
                    INNER JOIN Appointments ON Pets.PetID = Appointments.PetID
                    WHERE Owners.OwnerID = %s
                """, (int(search_term),))
            else:  # Assume it's a name
                cursor.execute("""
                    SELECT 
                        Owners.OwnerID AS OwnerID, Owners.Name AS OwnerName, Owners.Address, Owners.Contact_Info,
                        Pets.Name AS PetName, Pets.Species, Pets.Breed,
                        Appointments.Reason, Appointments.Date, Appointments.Status
                    FROM Owners
                    INNER JOIN Pets ON Owners.OwnerID = Pets.OwnerID
                    INNER JOIN Appointments ON Pets.PetID = Appointments.PetID
                    WHERE Owners.Name LIKE %s OR Pets.Name LIKE %s
                """, (f'%{search_term}%', f'%{search_term}%'))

            rows = cursor.fetchall()

            # Clear existing items in the table
            for item in self.reservations_treeview.get_children():
                self.reservations_treeview.delete(item)

            # Populate the table with fetched data
            for idx, row in enumerate(rows):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.reservations_treeview.insert("", "end", values=row, tags=(tag,))

            cursor.close()
        except Error as e:
            print(f"Error searching data: {e}")


    def clear_table(self):
        self.reservations_treeview.delete(*self.reservations_treeview.get_children())


    def create_separator(self, row, column, columnspan=2, padx=(20, 10), pady=10, sticky="ew"):
        separator = ttk.Separator(self.widgets_frame)
        separator.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady, sticky=sticky)
        return separator
    
    def toggle_row_colors(self, event):
        for idx, item in enumerate(self.treeview.get_children()):
            tag = "oddrow" if idx % 2 == 0 else "evenrow"
            if tag == "oddrow":
                self.treeview.item(item, tags=(tag,), background="light gray")  
            else:
                self.treeview.item(item, tags=(tag,), background="#FFFFFF")  # White

    def species_selection_changed(self, event):
        selected_species = self.species_combobox.get()
        if selected_species == "--Insert Others--":
            # Reset to the default value or choose a different action if needed
            self.species_combobox.set("Species")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataEntry(root)
    root.mainloop()