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

<img width="691" height="836" alt="image" src="https://github.com/user-attachments/assets/57d9bbbf-d6bf-4deb-91f9-bdc4b480e8fb" />
