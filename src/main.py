import random
import string
import os
from encryption import encrypt_password, decrypt_passwords, load_key
from cryptography.fernet import Fernet

def get_input():
    user_input = input("\nWhat would you like to do? (add, view, edit, trash, quit): ")
    return user_input

def add_input():
    user_input = input("\nWhat would you like to do? (own, generate, back): ")
    return user_input

def view_input():
    user_input = input("\nWhat would you like to do? (list, get, back): ")
    return user_input

def edit_input():
    user_input = input("\nWhat would you like to do? (change, remove, back): ")
    return user_input

def trash_input():
    user_input = input("\nWhat would you like to do? (look, restore, empty, back): ")
    return user_input

def password_generator(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def own_password():
    website = input("\nEnter where this password is for: ")
    password = input("\nEnter the password: ")
    encrypt_password(website, password)
    print(f"\nPassword for {website} was stored successfully.")

def gen_password():
    website = input("\nEnter where this password is for: ")
    print('')
    password = password_generator()
    encrypt_password(website, password)
    print(f"Password for {website} was generated successfully.")

def website_list():
    passwords = decrypt_passwords()
    print('')
    if not passwords:
        print("There are no websites saved")
    else:
        for website, password in passwords:
            print(f"{website}")

def get_password():
    website_list()
    website = input("\nEnter where this password is for from list above: ")
    print('')
    passwords = decrypt_passwords()
    for stored_website, password in passwords:
        if website == stored_website:
            print(f"{website} : {password}")

def get_password_list():
    print('')
    passwords = decrypt_passwords()
    for website, password in passwords:
        print(f"{website} : {password}")

def change_password_own():
    website_list()
    website = input("\nEnter which password you would like to change from the list above: ")
    passwords = decrypt_passwords()
    with open('passwords.enc', 'wb') as file:
        for stored_website, password in passwords:
            if website == stored_website:
                new_password = input("\nEnter the password: ")
                print(f"\nPassword for {website} was changed successfully.")
                encrypt_password(website, new_password)
            else:
                encrypt_password(stored_website, password)

def change_password_gen():
    website_list()
    website = input("\nEnter where this password is for from list above: ")
    passwords = decrypt_passwords()
    with open('passwords.enc', 'wb') as file:
        for stored_website, password in passwords:
            if website == stored_website:
                new_password = password = password_generator()
                print(f"\nPassword for {website} was generated successfully.")
                encrypt_password(website, new_password)
            else:
                encrypt_password(stored_website, password)

def remove_password():
    website_list()
    website = input("\nEnter which password you would like to delete from the list above: ")
    passwords = decrypt_passwords()
    with open('passwords.enc', 'wb') as file, open('trash.enc', 'ab') as trash_file:
        for stored_website, password in passwords:
            if website != stored_website:
                encrypt_password(stored_website, password)
            else:
                key = load_key()
                f = Fernet(key)
                encrypted_password = f.encrypt(password.encode())
                trash_file.write(f"{stored_website}:".encode() + encrypted_password + b'\n')
                print(f"\nPassword for {website} was removed successfully and moved to trash.")

def access_trash():
    try:
        with open('trash.enc', 'rb') as file:
            print('')
            for line in file:
                website, encrypted_password = line.strip().split(b':', 1)
                key = load_key()
                f = Fernet(key)
                decrypted_password = f.decrypt(encrypted_password).decode()
                print(f"{website.decode()} : {decrypted_password}")
    except FileNotFoundError:
        print("\nTrash is empty.\n")

def restore_one():
    access_trash()
    website = input("\nEnter which password you would like to restore from the list above: ")
    with open('trash.enc', 'rb') as file:
        trash_lines = file.readlines()
    
    with open('trash.enc', 'wb') as file, open('passwords.enc', 'ab') as passwords_file:
        for line in trash_lines:
            stored_website, encrypted_password = line.strip().split(b':', 1)
            if website != stored_website.decode():
                file.write(line)
            else:
                passwords_file.write(line)
                print(f"\nPassword for {website} was restored successfully.")

def restore_all():
    with open('trash.enc', 'rb') as trash_file, open('passwords.enc', 'ab') as file:
        for line in trash_file:
            stored_website, encrypted_password = line.strip().split(b':', 1)
            file.write(line)
            print(f"\nPassword for {stored_website.decode()} was restored successfully.")
    open('trash.enc', 'w').close()

def empty_one():
    access_trash()
    website = input("\nEnter which password you would like to delete from the list above: ")
    with open('trash.enc', 'rb') as file:
        trash_lines = file.readlines()
    
    with open('trash.enc', 'wb') as file:
        for line in trash_lines:
            stored_website, encrypted_password = line.strip().split(b':', 1)
            if website != stored_website.decode():
                file.write(line)
            else:
                print(f"Password for {website} was permanently deleted.\n")

def empty_all():
    with open('trash.enc', 'w') as file:
        file.close()
    print("\nAll passwords in trash were permanently deleted.\n")

def check_passwords_empty():
    try:
        if os.path.getsize('passwords.enc') == 0:
            print("\nThere are no passwords saved.")
            return True
        return False
    except FileNotFoundError:
        print("\nThere are no passwords saved.")
        return True

def check_trash_empty():
    try:
        if os.path.getsize('trash.enc') == 0:
            print("\nTrash is empty.")
            return True
        return False
    except FileNotFoundError:
        print("\nTrash is empty.")
        return True

if __name__ == "__main__":
    print("\nWelcome to the password manager!\n")
    print("If you would like to add a password, type 'add'. If you would like to view passwords or websites, type 'view'.")
    print("If you would like to change or remove a password, type 'edit'. If you would like to access the trash, type 'trash'.")
    print("If you would like to quit, type 'q'.")
    
    screen = 0

    while screen == 0:
        user_input = get_input()

        if user_input == "add":
            print("\nIf you'd like to add your own password, type 'own'. If you'd like to have a password be generated for you, type 'generate'. If you'd like to go back, type 'back'.")
            screen = 1
            while screen == 1:
                user_input = add_input()

                if user_input == "own":
                    own_password()
                elif user_input == "generate":
                    gen_password()
                elif user_input == "back":
                    screen = 0

        elif user_input == "view":
            if check_passwords_empty():
                continue
            print("\nIf you'd like to get the website(s) you have stored, type 'list'. If you'd like to get your password(s), type 'get'. If you'd like to go back, type 'back'.")
            screen = 1
            while screen == 1:
                user_input = view_input()

                if user_input == "list":
                    website_list()
                elif user_input == "get":
                    print("\nIf you'd like to get a specific password, type 'one'. If you'd like all passwords, type 'all'. If you'd like to go back, type 'back'.")
                    screen = 2
                    while screen == 2:
                        user_input = input("\nWhat would you like to do? (one, all, back): ")

                        if (user_input == "one"):
                            get_password()
                            
                        elif (user_input == "all"):
                            get_password_list()

                        elif user_input == "back":
                            screen = 1

                elif user_input == "back":
                    screen = 0

        elif user_input == "edit":
            if check_passwords_empty():
                continue
            print("\nIf you'd like to change a specific password, type 'change'. If you'd like to move a specific password to trash, type 'remove'. If you'd like to go back, type 'back'.")
            screen = 1
            while screen == 1:
                user_input = edit_input()

                if user_input == "change":
                    print("\nIf you'd like to change a password yourself, type 'own'. If you'd like a password generated for you, type 'generate'. If you'd like to go back, type 'back'.")
                    screen = 2
                    while screen == 2:
                        user_input = input("\nWhat would you like to do? (own, generate, back): ")
                        if (user_input == "own"):
                            change_password_own()
                        elif (user_input == "generate"):
                            change_password_gen()
                        elif (user_input == "back"):
                            screen = 1
                    
                elif user_input == "remove":
                    remove_password()

                elif user_input == "back":
                    screen = 0

        elif user_input == "trash":
            if check_trash_empty():
                continue
            print("\nIf you'd like to get a list of of websites you have in the trash, type 'look'. If you'd like to restore your password(s), type 'restore'. If you'd like to empty the trash, type 'empty'. If you'd like to go back, type 'back'.")
            screen = 1
            while screen == 1:
                user_input = trash_input()

                if user_input == "look":
                    access_trash()

                elif user_input == "restore":
                    print("\nIf you'd like to restore a specific password, type 'one'. If you'd like to restore all passwords, type 'all'. If you'd like go to back, type 'back'.")
                    screen = 2
                    while screen == 2:
                        
                        user_input = input("\nWhat would you like to do? (one, all, back): ")
                        if user_input == "one":
                            restore_one()
                        elif user_input == "all":
                            restore_all()
                            screen = 0
                        elif (user_input == "back"):
                            screen = 1

                elif user_input == "empty":
                    print("\nIf you'd like to delete a specific password, type 'one'. If you'd like to delete all passwords, type 'all'. If you'd like to go back, type 'back'.")
                    screen = 3
                    while screen == 3:

                        user_input = input("\nWhat would you like to do? (one, all, back): ")
                        if user_input == "one":
                            empty_one()
                        elif user_input == "all":
                            empty_all()
                            screen = 0
                        elif (user_input == "back"):
                                screen = 1

                elif user_input == "back":
                    screen = 0

        elif user_input == "quit":
            print(" ")
            exit()
