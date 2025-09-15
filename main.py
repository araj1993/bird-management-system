import os
from avian_management import *

  
def main():
    """
    Main function to run the Avian Management System.
    """
    print("\n-----WELCOME TO AVIAN MANAGEMENT SYSTEM------\n")

    user_exist = input("Are you a registered user? (T/F): ").strip().lower()

    if user_exist == 'f':
        want_to_register = input("Do you want to register? (T/F): ").strip().lower()
        if want_to_register == 't':
            if os.path.exists("avian.db"):
                register_user()
            else:    
                db = input("Database file does not exist. Do you want to create a DataBase? (T/F): ").strip().lower()
                if db == 't':
                    create_db()
                    create_register_user_table()
                    create_avian_detail_table()
                    create_avian_sightings_table()
                    print("Database and user table created successfully. Login and register the user.")    
                    exit()     
        else:
            print("\nExiting.... Thank you for visiting! \n")
            exit()
    elif user_exist == 't':
        if os.path.exists("avian.db") is False:
            db = input("Database file does not exist. Do you want to create a DataBase? (T/F): ").strip().lower()
            if db == 't':
                create_db()
                create_register_user_table()
                create_avian_detail_table()
                create_avian_sightings_table()
                print("Database and user table created successfully. Login and register the user.")    
                exit()
            else:
                exit("\nExiting... \n")              
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
    else:
        print("Invalid input. Please enter 'T' or 'F'.")
        exit()


if __name__ == "__main__":
    main()
