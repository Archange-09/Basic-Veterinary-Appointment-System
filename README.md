#  Basic Veterinary Appointment System

A desktop-based management tool for veterinary clinics to schedule appointments, manage pet records, and store client data using a local database.

##  Features
* **Appointment Scheduling:**
* **Patient Records:** Maintain a database of pet names, breeds, and medical history.
* **Client Management:** Store owner contact information linked to their pets.
* **Database Integration:** Uses SQL to store all records locally and securely.

##  Getting Started

### Prerequisites
Make sure you have Python installed on your system and the required database

The original database was deleted :<

**Reconstructed Schema:**

```
-- Create the Database
CREATE DATABASE IF NOT EXISTS vet_reserve;
USE vet_reserve;

-- 1. Owners Table
CREATE TABLE owners (
    OwnerID INT(11) NOT NULL AUTO_INCREMENT,
    Name VARCHAR(50),
    Contact_Info VARCHAR(50),
    Address VARCHAR(80),
    PRIMARY KEY (OwnerID)
);

-- 2. Pets Table (Depends on Owners)
CREATE TABLE pets (
    PetID INT(11) NOT NULL AUTO_INCREMENT,
    Name VARCHAR(50),
    OwnerID INT(11),
    Species VARCHAR(50),
    Breed VARCHAR(50),
    Age INT(11),
    PRIMARY KEY (PetID),
    FOREIGN KEY (OwnerID) REFERENCES owners(OwnerID)
);

-- 3. Appointments Table (Depends on Pets)
CREATE TABLE appointments (
    AppointmentID INT(11) NOT NULL AUTO_INCREMENT,
    PetID INT(11),
    Date DATETIME,
    Reason VARCHAR(80),
    Status VARCHAR(12),
    PRIMARY KEY (AppointmentID),
    FOREIGN KEY (PetID) REFERENCES pets(PetID)
);
```
