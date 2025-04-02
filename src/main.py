import random
import string
from encryption import encrypt_password, decrypt_passwords, load_key
from cryptography.fernet import Fernet

def get_input():
    user_input = input("What would you like to do? (add, view, edit, tra, q): ")
    return user_input

def add_input():
    print("If you would like to add your own password, type 'own'. If you would like to have a password be generated for you, type 'generate'. If you would like to go back, type 'back'.\n")
    user_input = input("What would you like to do? (own, generate, back): ")
    return user_input

def view_input():
    print("If you would like to get a list of websites you have stored, type 'list'. If you would like to get a password(s), type 'get'. If you would like to go back, type 'back'.\n")
    user_input = input("What would you like to do? (list, get, back): ")
    return user_input

def edit_input():
    print("If you would like to change a specific password, type 'change'. If you would like to move a specific password to trash, type 'remove'. If you would like to go back, type 'back'.\n")
    user_input = input("What would you like to do? (change, remove, back)")
    return user_input

def trash_input():
    print("If you would like to get a list of of websites you have in the trash, type 'look'. If you would like to empty the trash, type 'empty'. If you would like to go back, type 'back'.\n")
    user_input = input("What would you like to do? (look, empty, back) ")
    return user_input()

def password_generator(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def own_password():
    website = input("\nEnter where this password is for: ")
    password = input("\nEnter the password: ")
    encrypt_password(website, password)
    print(f"\nPassword for {website} was stored successfully.\n")

def gen_password():
    website = input("\nEnter where this password is for: ")
    print('')
    password = password_generator()
    encrypt_password(website, password)
    print(f"Password for {website} was generated successfully.\n")

def website_list():
    passwords = decrypt_passwords()
    print('')
    if not passwords:
        print("There are no websites saved")
    else:
        for website, password in passwords:
            print(f"{website}")
    print('')

def get_password():
    website_list()
    website = input("Enter where this password is for from list above: ")
    print('')
    passwords = decrypt_passwords()
    for stored_website, password in passwords:
        if website == stored_website:
            print(f"{website} : {password}\n")

def get_password_list():
    print('')
    passwords = decrypt_passwords()
    for website, password in passwords:
        print(f"{website} : {password}")
    print('')

def change_password_own():
    website_list()
    website = input("Enter which password you would like to change from the list above: ")
    passwords = decrypt_passwords()
    with open('passwords.enc', 'wb') as file:
        for stored_website, password in passwords:
            if website == stored_website:
                new_password = input("\nEnter the password: ")
                print(f"\nPassword for {website} was changed successfully.\n")
                encrypt_password(website, new_password)
            else:
                encrypt_password(stored_website, password)

def change_password_gen():
    website_list()
    website = input("Enter where this password is for from list above: ")
    passwords = decrypt_passwords()
    with open('passwords.enc', 'wb') as file:
        for stored_website, password in passwords:
            if website == stored_website:
                new_password = password = password_generator()
                print(f"\nPassword for {website} was generated successfully.\n")
                encrypt_password(website, new_password)
            else:
                encrypt_password(stored_website, password)

def remove_password():
    website_list()
    website = input("Enter which password you would like to delete from the list above: ")
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
                print(f"\nPassword for {website} was deleted successfully and moved to trash.\n")

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
            print('')
    except FileNotFoundError:
        print("\nTrash is empty.\n")

def restore_one():
    access_trash()
    website = input("Enter which password you would like to restore from the list above: ")
    with open('trash.enc', 'rb') as file:
        trash_lines = file.readlines()
    
    with open('trash.enc', 'wb') as file, open('passwords.enc', 'ab') as passwords_file:
        for line in trash_lines:
            stored_website, encrypted_password = line.strip().split(b':', 1)
            if website != stored_website.decode():
                file.write(line)
            else:
                passwords_file.write(line)
                print(f"\nPassword for {website} was restored successfully.\n")

def restore_all():
    try:
        with open('trash.enc', 'rb') as trash_file, open('passwords.enc', 'ab') as file:
            for line in trash_file:
                stored_website, encrypted_password = line.strip().split(b':', 1)
                file.write(line)
                print(f"\nPassword for {stored_website.decode()} was restored successfully.\n")
        open('trash.enc', 'w').close()
    except FileNotFoundError:
        print("\nTrash is empty.\n")

def empty_one():
    access_trash()
    website = input("Enter which password you would like to delete from the list above: ")
    with open('trash.enc', 'rb') as file:
        trash_lines = file.readlines()
    
    with open('trash.enc', 'wb') as file:
        for line in trash_lines:
            stored_website, encrypted_password = line.strip().split(b':', 1)
            if website != stored_website.decode():
                file.write(line)
            else:
                print(f"\nPassword for {website} was permanently deleted.\n")

def empty_all():
    try:
        with open('trash.enc', 'w') as file:
            file.close()
        print("\nAll passwords in trash were permanently deleted.\n")
    except FileNotFoundError:
        print("\nTrash is empty.\n")

if __name__ == "__main__":
    print("\nWelcome to the password manager!\n")
    print("If you would like to add a password, type 'add'. If you would like to view passwords or websites, type 'view'.")
    print("If you would like to change or remove a password, type 'edit'. If you would like to access the trash, type 'trash'. If you would like to quit, type 'q'.\n")
    
    screen = 0

    while screen == 0:
        user_input = get_input()

        if user_input == "add":
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
            screen = 1
            while screen == 1:
                user_input = view_input()

                if user_input == "list":
                    website_list()
                elif user_input == "get":
                    print("\nIf you would like to get a specific password, type 'one'. If you would like all passwords, type 'all'.\n")
                    user_input = input("What would you like to do? (one, all): ")

                    if (user_input == "one"):
                        get_password()
                        
                    elif (user_input == "all"):
                        get_password_list()

                    elif user_input == "back":
                        screen = 0

        elif user_input == "edit":
            screen = 1
            while screen == 1:
                user_input = edit_input()

                if user_input == "cha":
                    screen = 2
                    while screen == 2:
                        print("\nIf you would like to change a password yourself, type 'own'. If you would like a password generated for you, type 'gen'.\n")
                        user_input = input("What would you like to do? (own, gen): ")
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
            screen == 1
            while screen == 1:
                user_input == trash_input()
            if user_input == "look":
                access_trash()
            elif user_input == "restore":
                screen = 2
                while screen == 2:
                    print("\nIf you would like to restore a specific password, type 'one'. If you would like to restore all passwords, type 'all'.\n")
                    user_input = input("What would you like to do? (one, all): ")
                    if user_input == "one":
                        restore_one()
                    elif user_input == "all":
                        restore_all()
                    elif (user_input == "back"):
                        screen = 1

            elif user_input == "empty":
                screen = 3
                while screen == 3:
                    print("\nIf you would like to restore a specific password, type 'one'. If you would like to restore all passwords, type 'all'.\n")
                    if user_input == "one":
                        empty_one()
                    elif user_input == "all":
                        empty_all()
                    elif (user_input == "back"):
                            screen = 1
            elif user_input == "back":
                screen = 0

        elif user_input == "q":
            print(" ")
            exit()
