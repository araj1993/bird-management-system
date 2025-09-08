# Avian-Management-System

This project file implements the backend logic for an Avian Management System using SQLite as the database with Python as the coding stream. It provides functions for user registration, login, and management of bird details and sightings. The database schema includes tables for users, bird details (avian_details), and bird sightings (avian_sightings). The project supports three user roles: student, researcher, and common user, each with different menu options.

Key features:

 - Database creation and table setup for users, birds, and sightings.
 - User registration and login with role-based access.
 - CRUD operations for bird details and sightings.
 - Exporting bird data to CSV files.
 - Menu-driven command line interface for different user roles.
 - Input validation and error handling for user actions.
 
Each function is designed to interact with the database, handle user input, and display results in a tabular format using the tabulate library. The main function orchestrates the workflow, prompting users to register or log in and then presenting the appropriate menu based on their role.


**Register/Login Flowchart**

<img width="837" height="833" alt="image" src="https://github.com/user-attachments/assets/b1ba20dd-81a6-494d-8b4e-6e8837c8ec86" />


**SQL Schema**

CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT NOT NULL,
    user_type TEXT,
    created_at TIMESTAMP
);

CREATE TABLE avian_details (
    id INTEGER PRIMARY KEY,
    name TEXT,
    bio_name TEXT,
    origin TEXT,
    habitat TEXT,
    diet TEXT,
    conservation_status TEXT
);

CREATE TABLE avian_sighting (
    id INTEGER PRIMARY KEY,
    avian_id INTEGER,
    date TEXT,
    location TEXT,
    observer TEXT,
    notes TEXT,
    FOREIGN KEY (avian_id) REFERENCES avian_details(id)
);


**Entity-Relationship Diagram**

<img width="680" height="347" alt="image" src="https://github.com/user-attachments/assets/913e9a56-4725-4bb2-91a4-ba649a6c6fb2" />

### Feature and Set-up

Features of AMS

 - User registration and management
 - Add and view avian (bird) details
 - Record and track bird sightings

Requirements

 - Python 3.x
 - SQLite3
 
Installation

 - Clone the repository:
    - git clone https://github.com/araj1993/bird-management-system.git
    - cd avian-management-system

Setup the database:

 - Create the database (SQLite3)
 - Run the provided scripts to create tables 

How To Run The Application

  1. Activate python environment (optional)
  2. pip -r requirements.txt (not needed until any specific requirements are mentioned)
  3. **python ./avian_management.py**

## Example of Command Line Interface Design 

**Students***
<img width="1251" height="680" alt="image" src="https://github.com/user-attachments/assets/66a89c6f-cbfe-4048-bb31-425413460059" />
<img width="1053" height="391" alt="image" src="https://github.com/user-attachments/assets/d43bf920-9d82-484a-abbc-1eed57a4595e" />


**Researchers**
<img width="1166" height="649" alt="image" src="https://github.com/user-attachments/assets/d5e0e80e-c464-47fd-a0a0-12b625fb76fe" />
<img width="1173" height="540" alt="image" src="https://github.com/user-attachments/assets/4bebe1eb-8cd5-4c22-9ffe-25ff03def94d" />

**Common Users**
<img width="975" height="780" alt="image" src="https://github.com/user-attachments/assets/8a620b1f-c039-45c1-becf-7c111027d42a" />


