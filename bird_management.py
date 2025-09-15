import sqlite3
import csv
from tabulate import tabulate
from menu import *

connection = sqlite3.connect("bird.db")
cursor = connection.cursor()


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


def register_user():
    """
    Register a new user account, including:
    1. username
    2. email
    3. password
    4. user_type
    """
    conn = sqlite3.connect('bird.db')
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
    conn = sqlite3.connect('bird.db')
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


def create_bird_detail_table():
    """
    Create a table for storing bird details.
    """
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS bird_details (
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


def add_bird_details():
    """
    Add details of a new bird to the database.
    """
    try:
        conn = sqlite3.connect('bird.db')
        cursor = conn.cursor()

        name = input("Enter bird name: ").strip()
        bio_name = input("Enter biological name: ").strip()
        origin = input("Enter origin: ").strip()
        habitat = input("Enter habitat: ").strip()
        diet = input("Enter diet: ").strip()
        conservation_status = input("Enter conservation status (extinct/not extinct): ").strip()
        description = input("Enter description: ").strip()

        cursor.execute('''
        INSERT INTO bird_details (name, bio_name, origin, habitat, diet, conservation_status, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, bio_name, origin, habitat, diet, conservation_status, description))

        conn.commit()
        print(f"Bird '{name}' added successfully.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Warning: 'conservation_status' must be 'extinct' or 'not extinct'.")
    finally:
        conn.close()


def update_bird_by_name():
    """
    Update details of an existing bird in the database.
    """
    conn = sqlite3.connect('bird.db')
    cursor = conn.cursor()

    name = input("Enter the name of the bird to edit: ").strip()
    cursor.execute("SELECT * FROM bird_details WHERE LOWER(name) = LOWER(?)", (name.lower(),))
    bird = cursor.fetchone()

    if not bird:
        choice = input(f"Bird '{name}' not found. Do you want to add it as a new bird? (T/F): ").strip().upper()
        if choice == 'T':
            bio_name = input("Enter biological name: ").strip()
            diet = input("Enter diet: ").strip()
            conservation_status = input("Enter conservation status (extinct/not extinct): ").strip()
            habitat = input("Enter habitat: ").strip()
            origin = input("Enter origin: ").strip()
            description = input("Enter description: ").strip()

            add_bird_details(
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

    print(f"\nEditing details for bird: {bird}")
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
        sql = f"UPDATE bird_details SET {', '.join(updated_fields)} WHERE LOWER(name) = ?"
        new_values.append(name.lower())

        cursor.execute(sql, new_values)
        conn.commit()
        print(f"Bird '{name}' details updated successfully.")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        conn.close()


def remove_bird_by_name():
    """
    Remove a bird from the database by its name.
    """
    conn = sqlite3.connect('bird.db')
    cursor = conn.cursor()

    name = input("Enter the name of the bird to be removed from table: ").strip()

    cursor.execute("SELECT * FROM bird_deatils WHERE LOWER(name) = LOWER(?)", (name.lower(),))
    bird = cursor.fetchone()

    if not bird:
        print(f"Bird '{name}' does not exist in the database.")
        conn.close()
        return

    print(f"Bird {bird} exist in the database")
    confirm = input(f"Are you sure you want to delete '{name}'? (T/F): ").strip().upper()

    if confirm == 'T':
        try:
            cursor.execute("DELETE FROM bird_deatils WHERE LOWER(name) = LOWER(?)", (name.lower(),))
            conn.commit()
            print(f"Bird '{name}' deleted successfully.")
        except Exception as e:
            print(f"ERROR occurred while deleting: {e}")
    else:
        print("Deletion canceled.")

    conn.close()  


def view_bird_by_name():
    """
    View details of a specific bird by its name.
    """
    conn = sqlite3.connect('bird.db')
    cursor = conn.cursor()

    name = input("Enter the name of the bird to view from table: ").strip()
    
    cursor.execute("SELECT * FROM bird_deatils WHERE LOWER(name) = LOWER(?)", (name.lower(),))
    bird = cursor.fetchone()

    if not bird:
        print(f"No bird named '{name}' found in the database.")
    else:
        column_names = [desc[0].capitalize() for desc in cursor.description]
        table = [bird]

        print(f"\n Details for bird '{name}':")
        print(tabulate(table, headers=column_names, tablefmt="fancy_grid"))

    conn.close()
   

def view_bird_details_table():
    """
    View all bird details from the database.
    """
    conn = sqlite3.connect('bird.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bird_details")
    birds = cursor.fetchall()

    if not birds:
        print("No bird records found in the database.")
    else:
        column_names = [desc[0].capitalize() for desc in cursor.description]

        print("\n All Bird Records:")
        print(tabulate(birds, headers=column_names, tablefmt="fancy_grid"))

    conn.close()


def export_bird_data_to_csv():
    """
    Export bird data to a CSV file.
    """
    conn = sqlite3.connect('bird.db')
    cursor = conn.cursor()

    print("\n Export Bird Data to CSV")
    print("1. Export a specific bird by name")
    print("2. Export all birds")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        name = input("Enter the bird name to export: ").strip()

        cursor.execute("SELECT * FROM bird_deatils WHERE LOWER(name) = LOWER(?)", (name.lower(),))
        bird = cursor.fetchone()

        if not bird:
            print(f"Bird '{name}' not found in the database.")
        else:
            column_names = [desc[0] for desc in cursor.description]
            filename = f"{name.lower().replace(' ', '_')}_details.csv"

            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerow(bird)

            print(f"Bird '{name}' exported to '{filename}'.")

    elif choice == "2":
        cursor.execute("SELECT * FROM bird_deatils")
        birds = cursor.fetchall()

        if not birds:
            print("No saved bird records found.")
        else:
            column_names = [desc[0] for desc in cursor.description]
            filename = "all_bird_details.csv"

            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerows(birds)

            print(f"All bird records exported to '{filename}'.")

    else:
        print("Invalid choice. Please enter 1 or 2.")

    conn.close()
    

def create_avian_sightings_table():
    """
    Create the avian_sightings table in the database.
    """
    conn = sqlite3.connect('bird.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avian_sightings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bird_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        location TEXT NOT NULL,
        observer TEXT,
        notes TEXT,
        FOREIGN KEY (bird_id) REFERENCES bird_details(id) ON DELETE CASCADE
    );
    ''')

    conn.commit()
    conn.close()
    print("Table 'avian_sightings' created or already exists.")
    

def add_avian_sighting():
    """
    Add a new avian sighting to the database.
    """
    conn = sqlite3.connect('bird.db')
    cursor = conn.cursor()

    bird_name = input("Enter bird name: ").strip()

    cursor.execute("SELECT id FROM bird_details WHERE LOWER(name) = LOWER(?)", (bird_name.lower(),))
    result = cursor.fetchone()

    if not result:
        print(f"Bird '{bird_name}' does not exist in the bird_details table. Cannot add sighting.")
        conn.close()
        return

    bird_id = result[0]

    date = input("Enter sighting date (YYYY-MM-DD): ").strip()
    location = input("Enter location: ").strip()
    observer = input("Enter observer name (optional): ").strip()
    notes = input("Additional notes (optional): ").strip()

    try:
        cursor.execute('''
            INSERT INTO avian_sightings (bird_id, date, location, observer, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (bird_id, date, location, observer or None, notes or None))

        conn.commit()
        print(f"Sighting of '{bird_name}' added successfully.")

    except Exception as e:
        print(f"Failed to add sighting: {e}")

    finally:
        conn.close()


def view_avian_sightings_by_bird_name():
    """
    View avian sightings for a specific bird by its name.
    """
    conn = sqlite3.connect('bird.db')
    cursor = conn.cursor()

    bird_name = input("Enter the bird name to view its sightings: ").strip()

    cursor.execute('''
        SELECT a.id, b.name, a.date, a.location, a.observer, a.notes
        FROM avian_sightings a
        JOIN bird_deatils b ON a.bird_id = b.id
        WHERE LOWER(b.name) = LOWER(?)
        ORDER BY a.date DESC
    ''', (bird_name.lower(),))

    sightings = cursor.fetchall()

    if not sightings:
        print(f"No sightings found for bird '{bird_name}'.")
    else:
        print(f"\n Avian Sightings for '{bird_name}':")
        headers = ["Sighting ID", "Bird Name", "Date", "Location", "Observer", "Notes"]
        print(tabulate(sightings, headers=headers, tablefmt="fancy_grid"))

    conn.close()


def update_avian_sighting_by_bird_name():
    """
    Update an existing avian sighting in the database.
    """
    conn = sqlite3.connect('bird.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    bird_name = input("Enter the bird name to update a sighting for: ").strip()

    cursor.execute("SELECT id FROM bird_details WHERE LOWER(name) = LOWER(?)", (bird_name.lower(),))
    bird = cursor.fetchone()

    if not bird:
        print(f"Bird '{bird_name}' not found in the database.")
        conn.close()
        return

    bird_id = bird[0]

    cursor.execute("""
        SELECT id, date, location, observer, notes
        FROM avian_sightings
        WHERE bird_id = ?
        ORDER BY date DESC
    """, (bird_id,))
    sightings = cursor.fetchall()

    if not sightings:
        print(f"No sightings found for bird '{bird_name}'.")
        conn.close()
        return

    print(f"\n Sightings for '{bird_name}':")
    headers = ["Sighting ID", "Date", "Location", "Observer", "Notes"]
    print(tabulate(sightings, headers=headers, tablefmt="fancy_grid"))

    try:
        sighting_id = int(input("Enter the Sighting ID to update: ").strip())
    except ValueError:
        print("Invalid ID Given.")
        conn.close()
        return

    cursor.execute("SELECT date, observer, notes FROM avian_sightings WHERE id = ? AND bird_id = ?", (sighting_id, bird_id))
    result = cursor.fetchone()

    if not result:
        print("Sighting for input bird is not found.")
        conn.close()
        return

    current_date, current_observer, current_notes = result

    print(f"\n Current Date: {current_date}")
    print(f"Current Observer: {current_observer}")
    print(f"Current Notes:\n{current_notes or '—'}")

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


def view_sightings_for_all_birds():
    """
    View all avian sightings from the database.
    """
    conn = sqlite3.connect('bird.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM avian_sightings")
    birds = cursor.fetchall()

    if not birds:
        print("No bird records found in the database.")
    else:
        column_names = [desc[0].capitalize() for desc in cursor.description]

        print("\n Records of All Birds:")
        print(tabulate(birds, headers=column_names, tablefmt="fancy_grid"))

    conn.close()


def view_all_birds_existing_in_db():
    """
    View all bird names from the database.
    """
    conn = sqlite3.connect('bird.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM bird_details")
    bird_names = cursor.fetchall()

    if not bird_names:
        print("No bird names found.")
    else:
        bird_names_with_slno = [(i+1, name[0]) for i, name in enumerate(bird_names)]

        print("\n Names of all Birds saved in the Database:")
        print(tabulate(bird_names_with_slno, headers=["Sl. No.", "Bird Name"], tablefmt="fancy_grid"))

    conn.close()


def main():
    """
    Main function to run the Avian Management System.
    """
    print("\n-----WELCOME TO AVIAN MANAGEMENT SYSTEM------\n")

    user_exist = input("Are you a registered user? (T/F): ").strip().lower()

    if user_exist == 'f':
        want_to_register = input("Do you want to register? (T/F): ").strip().lower()
        if want_to_register == 't':
            register_user()
        else:
            print("\n Thank you for visiting!")
            exit()
    else:
        user = login_user()  
        if user:
            user_type = user[4].lower()
            if user_type == 'student':
                student_menu()
            elif user_type == 'researcher':
                researcher_menu()
            else:
                common_user_menu()


def student_menu():
    """
    Student menu for avian management system.
    """
    
    print("\n Please choose an option below:")
    print("1. View all saved avian species")
    print("2. View detailed information for all avians")
    print("3. View details for a specific bird")
    print("4. View sightings for a specific bird")
    print("5. View sightings for all birds")
    print("6. Add a new avian sighting")
    print("7. Export avian details to CSV")
    print("0. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 7.")

    if choice == 1:
        view_all_birds_existing_in_db()
    elif choice == 2:
        view_bird_details_table()
    elif choice == 3:
        view_bird_by_name()
    elif choice == 4:
        view_avian_sightings_by_bird_name()
    elif choice == 5:
        view_sightings_for_all_birds()
    elif choice == 6:
        update_avian_sighting_by_bird_name()
    elif choice == 7:
        export_bird_data_to_csv()
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
    print("3. View details for a specific bird")
    print("4. View sightings for a specific bird")
    print("5. View sightings for all birds")
    print("6. Add a new avian sighting") 
    print("7. Update avian detail for a specific bird")   
    print("8. Update avian sighting for a specific bird")
    print("9. Remove specific bird information")
    print("10. Export avian details to CSV")
    print("0. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 10.")

    if choice == 1:
        view_all_birds_existing_in_db()
    elif choice == 2:
        view_bird_details_table()
    elif choice == 3:
        view_bird_by_name()
    elif choice == 4:
        view_avian_sightings_by_bird_name()
    elif choice == 5:
        view_sightings_for_all_birds()
    elif choice == 6:
        add_avian_sighting()
    elif choice == 7:
        update_bird_by_name()
    elif choice == 8:
        update_avian_sighting_by_bird_name()
    elif choice == 9:
        remove_bird_by_name()
    elif choice == 10:
        export_bird_data_to_csv()
    elif choice == 0:
        print("Exiting the menu.")
        exit()
    else:
        print("Invalid choice. Please select a valid option.")


def common_user_menu():
    """
    Menu for common users in the avian management system.
    """
    print("\n Please choose an option below:")
    print("1. View all saved avian species")
    print("2. View detailed information for all avians")
    print("3. View details for a specific bird")
    print("4. View sightings for a specific bird")
    print("5. View sightings for all birds")
    print("6. Export avian details to CSV")
    print("0. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 7.")

    if choice == 1:
        view_all_birds_existing_in_db()
    elif choice == 2:
        view_bird_details_table()
    elif choice == 3:
        view_bird_by_name()
    elif choice == 4:
        view_avian_sightings_by_bird_name()
    elif choice == 5:
        view_sightings_for_all_birds()
    elif choice == 6:
        export_bird_data_to_csv()    
    elif choice == 0:
        print("Exiting the menu.")
        exit()
    else:
        print("Invalid choice. Please select a valid option.")    

  
if __name__ == "__main__":
    main()