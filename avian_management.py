import sqlite3
import csv
import os
from tabulate import tabulate


def create_db():
    """
    Create a SQLite database and establish a connection.
    """
    global connection, cursor
    connection = sqlite3.connect('avian.db')
    cursor = connection.cursor()
    print("Database created successfully.")


def create_register_user_table():
    """
    Create a user registration table with the following fields:
    1. username
    2. email
    3. password
    4. user_type
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_type TEXT CHECK(user_type IN ('researcher', 'common_user', 'student')) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')

    connection.commit()
    connection.close()
    print("successfully created 'users' table.")


def register_user():
    """
    Register a new user account, including:
    1. username
    2. email
    3. password
    4. user_type
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    user_name = input("Enter a username: ").strip()
    email = input("Enter a email: ").strip()
    password = input("Enter the password: ").strip()
    user_type = input("Select a user type from given [Student/Researcher/Common_user]: ").strip()

    try:
        cursor.execute('''
            INSERT INTO users (username, email, password, user_type) 
            VALUES (?, ?, ?, ?)
            ''', (user_name, email, password, user_type)) 
        conn.commit()
        print("User registered successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def login_user():
    """
    Login an existing user with their credentials.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    username_or_email = input("Enter a username or email: ").strip()
    password = input("Enter the password: ").strip()
    user_type = input("Select a user type from given [Student/Researcher/Common_user]: ").lower().strip()

    cursor.execute('''
        SELECT * FROM users
        WHERE (username = ? OR email = ?) AND password = ? AND user_type = ?
        ''', (username_or_email, username_or_email, password, user_type))

    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"Login successful. Welcome, {user[1]}, you are logged in as a {user[4]}.")
        if user_type == 'student':
            student_menu()
        elif user_type == 'researcher':
            researcher_menu()
        elif user_type == 'common_user':
            common_user_menu()
        else:
            print("Check user type.")
        return user
    else:
        print("ERROR: Login Failed!.")
        return None


def create_avian_detail_table():
    """
    Create a table for storing avian details.
    """
    connection = sqlite3.connect('avian.db')
    cursor = connection.cursor()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS avian_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            bio_name TEXT NOT NULL UNIQUE,
            origin TEXT NOT NULL,
            habitat TEXT NOT NULL,
            diet TEXT NOT NULL,
            conservation_status TEXT CHECK(conservation_status IN ('extinct', 'not extinct')) NOT NULL,
            description TEXT NOT NULL)
        ''')
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        connection.close()


def add_avian_details():
    """
    Add details of a new avian to the database.
    """
    try:
        conn = sqlite3.connect('avian.db')
        cursor = conn.cursor()

        name = input("Enter avian name: ").strip()
        bio_name = input("Enter biological name: ").strip()
        origin = input("Enter origin: ").strip()
        habitat = input("Enter habitat: ").strip()
        diet = input("Enter diet: ").strip()
        conservation_status = input("Enter conservation status (extinct/not extinct): ").strip()
        description = input("Enter description: ").strip()

        cursor.execute('''
        INSERT INTO avian_details (name, bio_name, origin, habitat, diet, conservation_status, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, bio_name, origin, habitat, diet, conservation_status, description))

        conn.commit()
        print(f"avian '{name}' added successfully.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Warning: 'conservation_status' must be 'extinct' or 'not extinct'.")
    finally:
        conn.close()


def update_avian_by_name():
    """
    Update details of an existing avian in the database.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    name = input("Enter the name of the avian to edit: ").strip()
    cursor.execute("SELECT * FROM avian_details WHERE LOWER(name) = LOWER(?)", (name.lower(),))
    avian = cursor.fetchone()

    if not avian:
        choice = input(f"avian '{name}' not found. Do you want to add it as a new avian? (T/F): ").strip().upper()
        if choice == 'T':
            bio_name = input("Enter biological name: ").strip()
            diet = input("Enter diet: ").strip()
            conservation_status = input("Enter conservation status (extinct/not extinct): ").strip()
            habitat = input("Enter habitat: ").strip()
            origin = input("Enter origin: ").strip()
            description = input("Enter description: ").strip()

            add_avian_details(
                name=name,
                bio_name=bio_name,
                diet=diet,
                conservation_status=conservation_status,
                habitat=habitat,
                origin=origin,
                description=description
            )
        else:
            print("Update Cancelled!.")
        conn.close()
        return

    print(f"\nEditing details for avian: {avian}")
    print("Leave blank to keep the current value.\n")
    
    new_bio_name = input("New biological name: ").strip()
    new_diet = input("New diet: ").strip()
    new_conservation_status = input("New conservation status (extinct/not extinct): ").strip()
    new_habitat = input("New habitat: ").strip()
    new_description = input("New description: ").strip()

    updated_fields = []
    new_values = []

    if new_bio_name:
        updated_fields.append("bio_name = ?")
        new_values.append(new_bio_name)
    if new_diet:
        updated_fields.append("diet = ?")
        new_values.append(new_diet)
    if new_conservation_status in ['extinct', 'not extinct']:
        updated_fields.append("conservation_status = ?")
        new_values.append(new_conservation_status)
    elif new_conservation_status:
        print("Conservation status must be 'extinct' or 'not extinct'.")
    if new_habitat:
        updated_fields.append("habitat = ?")
        new_values.append(new_habitat)
    if new_description:
        updated_fields.append("description = ?")
        new_values.append(new_description) 

    if not updated_fields:
        print("No fields to update.")
        conn.close()
        return

    try:
        sql = f"UPDATE avian_details SET {', '.join(updated_fields)} WHERE LOWER(name) = ?"
        new_values.append(name.lower())

        cursor.execute(sql, new_values)
        conn.commit()
        print(f"avian '{name}' details updated successfully.")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        conn.close()


def remove_avian_by_name():
    """
    Remove a avian from the database by its name.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    name = input("Enter the name of the avian to be removed from table: ").strip()

    cursor.execute("SELECT * FROM avian_details WHERE LOWER(name) = LOWER(?)", (name.lower(),))
    avian = cursor.fetchone()

    if not avian:
        print(f"avian '{name}' does not exist in the database.")
        conn.close()
        return

    print(f"avian {avian} exist in the database")
    confirm = input(f"Are you sure you want to delete '{name}'? (T/F): ").strip().upper()

    if confirm == 'T':
        try:
            cursor.execute("DELETE FROM avian_details WHERE LOWER(name) = LOWER(?)", (name.lower(),))
            conn.commit()
            print(f"avian '{name}' deleted successfully.")
        except Exception as e:
            print(f"ERROR occurred while deleting: {e}")
    else:
        print("Deletion canceled.")

    conn.close()  


def view_avian_by_name():
    """
    View details of a specific avian by its name.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    name = input("Enter the name of the avian to view from table: ").strip()
    
    cursor.execute("SELECT * FROM avian_details WHERE LOWER(name) = LOWER(?)", (name.lower(),))
    avian = cursor.fetchone()

    if not avian:
        print(f"No avian named '{name}' found in the database.")
    else:
        column_names = [desc[0].capitalize() for desc in cursor.description]
        table = [avian]

        print(f"\n Details for avian '{name}':")
        print(tabulate(table, headers=column_names, tablefmt="fancy_grid"))

    conn.close()
   

def view_avian_details_table():
    """
    View all avian details from the database.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM avian_details")
    avians = cursor.fetchall()

    if not avians:
        print("EMPTY TABLE !!. No avian records found in the database.")
    else:
        column_names = [desc[0].capitalize() for desc in cursor.description]

        print("\n All avian Records:")
        print(tabulate(avians, headers=column_names, tablefmt="fancy_grid"))

    conn.close()
    

def export_avian_data_to_csv():
    """
    Export avian data to a CSV file.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    print("\n Export avian Data to CSV")
    print("1. Export a specific avian by name")
    print("2. Export all avians")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        name = input("Enter the avian name to export: ").strip()

        cursor.execute("SELECT * FROM avian_details WHERE LOWER(name) = LOWER(?)", (name.lower(),))
        avian = cursor.fetchone()

        if not avian:
            print(f"avian '{name}' not found in the database.")
        else:
            column_names = [desc[0] for desc in cursor.description]
            filename = f"{name.lower().replace(' ', '_')}_details.csv"

            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerow(avian)

            print(f"avian '{name}' exported to '{filename}'.")

    elif choice == "2":
        cursor.execute("SELECT * FROM avian_details")
        avians = cursor.fetchall()

        if not avians:
            print("No saved avian records found.")
        else:
            column_names = [desc[0] for desc in cursor.description]
            filename = "all_avian_details.csv"

            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerows(avians)

            print(f"All avian records exported to '{filename}'.")

    else:
        print("Invalid choice. Please enter 1 or 2.")

    conn.close()
    

def create_avian_sightings_table():
    """
    Create the avian_sightings table in the database.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avian_sightings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        avian_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        location TEXT NOT NULL,
        observer TEXT,
        notes TEXT,
        FOREIGN KEY (avian_id) REFERENCES avian_details(id) ON DELETE CASCADE
    );
    ''')

    conn.commit()
    conn.close()
    print("Table 'avian_sightings' created successfully.")
    

def add_avian_sighting():
    """
    Add a new avian sighting to the database.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    avian_name = input("Enter avian name: ").strip()

    cursor.execute("SELECT id FROM avian_details WHERE LOWER(name) = LOWER(?)", (avian_name.lower(),))
    result = cursor.fetchone()

    if not result:
        print(f"avian '{avian_name}' does not exist in the avian_details table. Cannot add sighting.")
        conn.close()
        return

    avian_id = result[0]

    date = input("Enter sighting date (YYYY-MM-DD): ").strip()
    location = input("Enter location: ").strip()
    observer = input("Enter observer name (optional): ").strip()
    notes = input("Additional notes (optional): ").strip()

    try:
        cursor.execute('''
            INSERT INTO avian_sightings (avian_id, date, location, observer, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (avian_id, date, location, observer or None, notes or None))

        conn.commit()
        print(f"Sighting of '{avian_name}' added successfully.")

    except Exception as e:
        print(f"Failed to add sighting: {e}")

    finally:
        conn.close()


def view_avian_sightings_by_avian_name():
    """
    View avian sightings for a specific avian by its name.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    avian_name = input("Enter the avian name to view its sightings: ").strip()

    cursor.execute('''
        SELECT a.id, b.name, a.date, a.location, a.observer, a.notes
        FROM avian_sightings a
        JOIN avian_details b ON a.avian_id = b.id
        WHERE LOWER(b.name) = LOWER(?)
        ORDER BY a.date DESC
    ''', (avian_name.lower(),))

    sightings = cursor.fetchall()

    if not sightings:
        print(f"No sightings found for avian '{avian_name}'.")
    else:
        print(f"\n Avian Sightings for '{avian_name}':")
        headers = ["Sighting ID", "avian Name", "Date", "Location", "Observer", "Notes"]
        print(tabulate(sightings, headers=headers, tablefmt="fancy_grid"))

    conn.close()


def update_avian_sighting_by_avian_name():
    """
    Update an existing avian sighting in the database.
    """
    conn = sqlite3.connect('avian.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    avian_name = input("Enter the avian name to update a sighting for: ").strip()

    cursor.execute("SELECT id FROM avian_details WHERE LOWER(name) = LOWER(?)", (avian_name.lower(),))
    avian = cursor.fetchone()

    if not avian:
        print(f"avian '{avian_name}' not found in the database.")
        conn.close()
        return

    avian_id = avian[0]

    cursor.execute("""
        SELECT id, date, location, observer, notes
        FROM avian_sightings
        WHERE avian_id = ?
        ORDER BY date DESC
    """, (avian_id,))
    sightings = cursor.fetchall()

    if not sightings:
        print(f"No sightings found for avian '{avian_name}'.")
        conn.close()
        return

    print(f"\n Previous sightings for '{avian_name}':")
    headers = ["Sighting ID", "Date", "Location", "Observer", "Notes"]
    print(tabulate(sightings, headers=headers, tablefmt="fancy_grid"))

    try:
        sighting_id = int(input("Enter the Sighting ID to update: ").strip())
    except ValueError:
        print("Invalid ID Given.")
        conn.close()
        return

    cursor.execute("SELECT date, observer, notes FROM avian_sightings WHERE id = ? AND avian_id = ?", (sighting_id, avian_id))
    result = cursor.fetchone()

    if not result:
        print("Sighting for input avian is not found.")
        conn.close()
        return

    current_date, current_observer, current_notes = result

    new_date = input("Enter a new date to append (YYYY-MM-DD), or press Enter to skip: ").strip()
    new_observer = input("Enter a new observer name to append, or press Enter to skip: ").strip()
    new_note = input("Enter new note to append, or press Enter to skip: ").strip()

    updated_date = f"{current_date} | {new_date}" if new_date else current_date
    updated_observer = f"{current_observer} | {new_observer}" if new_observer else current_observer
    updated_notes = f"{current_notes}\n---\n{new_note}" if new_note else current_notes

    cursor.execute("""
        UPDATE avian_sightings
        SET date = ?, observer = ?, notes = ?
        WHERE id = ?
    """, (updated_date, updated_observer, updated_notes, sighting_id))

    conn.commit()
    conn.close()

    print("\n Sighting updated successfully.")


def view_sightings_for_all_avians():
    """
    View all avian sightings from the database.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM avian_sightings")
    avians = cursor.fetchall()

    if not avians:
        print("No avian records found in the database.")
    else:
        column_names = [desc[0].capitalize() for desc in cursor.description]

        print("\n Records of All avians:")
        print(tabulate(avians, headers=column_names, tablefmt="fancy_grid"))

    conn.close()


def view_all_avians_existing_in_db():
    """
    View all avian names from the database.
    """
    conn = sqlite3.connect('avian.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM avian_details")
    avian_names = cursor.fetchall()

    if not avian_names:
        print("No avian names found.")
    else:
        avian_names_with_slno = [(i+1, name[0]) for i, name in enumerate(avian_names)]

        print("\n Names of all avians saved in the Database:")
        print(tabulate(avian_names_with_slno, headers=["Sl. No.", "avian Name"], tablefmt="fancy_grid"))

    conn.close()

def student_menu():
    """
    Student menu for avian management system.
    """
    
    print("\n Please choose an option below:")
    print("1. View all saved avian species")
    print("2. View detailed information for all avians")
    print("3. View details for a specific avian")
    print("4. View sightings for a specific avian")
    print("5. View sightings for all avians")
    print("6. Add a new avian sighting")
    print("7. Export avian details to CSV")
    print("0. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 7.")
        return

    if choice == 1:
        view_all_avians_existing_in_db()
    elif choice == 2:
        view_avian_details_table()
    elif choice == 3:
        view_avian_by_name()
    elif choice == 4:
        view_avian_sightings_by_avian_name()
    elif choice == 5:
        view_sightings_for_all_avians()
    elif choice == 6:
        update_avian_sighting_by_avian_name()
    elif choice == 7:
        export_avian_data_to_csv()
    elif choice == 0:
        print("Exiting the menu.")
        exit()
    else:
        print("Invalid choice. Please select a valid option.")


def researcher_menu():
    """
    Researcher menu for avian management system.
    """
    print("\n Please choose an option below:")
    print("1. View all saved avian species")
    print("2. View detailed information for all avians")
    print("3. View details for a specific avian")
    print("4. View sightings for a specific avian")
    print("5. View sightings for all avians")
    print("6. Add new avian details")
    print("7. Add a new avian sighting")
    print("8. Update avian detail for a specific avian")
    print("9. Update avian sighting for a specific avian")
    print("10. Remove specific avian information")
    print("11. Export avian details to CSV")
    print("0. Exit")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 10.")
        return

    if choice == 1:
        view_all_avians_existing_in_db()
    elif choice == 2:
        view_avian_details_table()
    elif choice == 3:
        view_avian_by_name()
    elif choice == 4:
        view_avian_sightings_by_avian_name()
    elif choice == 5:
        view_sightings_for_all_avians()
    elif choice == 6:
        add_avian_details()    
    elif choice == 7:
        add_avian_sighting()
    elif choice == 8:
        update_avian_by_name()
    elif choice == 9:
        update_avian_sighting_by_avian_name()
    elif choice == 10:
        remove_avian_by_name()
    elif choice == 11:
        export_avian_data_to_csv()
    elif choice == 0:
        print("Exiting the menu.")
        exit()
    else:
        print("Invalid choice. Please select a valid option.")
        print("Invalid choice. Please select a valid option.")


def common_user_menu():
    """
    Menu for common users in the avian management system.
    """
    print("\n Please choose an option below:")
    print("1. View all saved avian species")
    print("2. View detailed information for all avians")
    print("3. View details for a specific avian")
    print("4. View sightings for a specific avian")
    print("5. View sightings for all avians")
    print("6. Export avian details to CSV")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 7.")
        return

    if choice == 1:
        view_all_avians_existing_in_db()
    elif choice == 2:
        view_avian_details_table()
    elif choice == 3:
        view_avian_by_name()
    elif choice == 4:
        view_avian_sightings_by_avian_name()
    elif choice == 5:
        view_sightings_for_all_avians()
    elif choice == 6:
        export_avian_data_to_csv()    
    elif choice == 0:
        print("Exiting the menu.")
        exit()
    else:
        print("Invalid choice. Please select a valid option.")    
  
