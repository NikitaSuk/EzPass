import random
import string
from encryption import encrypt_password, decrypt_passwords

def get_input():
    user_input = input("What would you like to do? (own, gen, get, del, cha, q): ")
    return user_input

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

def get_password_list():
    print('')
    passwords = decrypt_passwords()
    for website, password in passwords:
        print(f"{website} : {password}")

def get_password():
    website = input("\nEnter where this password is for: ")
    print('')
    passwords = decrypt_passwords()
    for stored_website, password in passwords:
        if website == stored_website:
            print(f"{website} : {password}")

def delete_password():
    website = input("\nEnter where this password is for: ")
    print('')
    passwords = decrypt_passwords()
    with open('passwords.enc', 'wb') as file:
        for stored_website, password in passwords:
            if website != stored_website:
                encrypt_password(stored_website, password)

def change_password():
    website = input("\nEnter where this password is for: ")
    print('')
    passwords = decrypt_passwords()
    with open('passwords.enc', 'wb') as file:
        for stored_website, password in passwords:
            if website == stored_website:
                new_password = password_generator()
                print(f"Password for {website} was generated successfully.\n")
                encrypt_password(website, new_password)
            else:
                encrypt_password(stored_website, password)

if __name__ == "__main__":
    print("\nWelcome to the password manager!\n")
    print("If you would like to enter your own password, type 'own'. If you would like a password generated for you, type 'gen'. If you would like to get a password, type 'get'.")
    print("If you would like to delete a specific password, type 'del'. If you would like to change a specific password, type 'cha'. If you would like to quit, type 'q'.\n")
    
    while True:
        user_input = get_input()

        if user_input == "own":
            own_password()

        elif user_input == "gen":
            gen_password()
            
        elif user_input == "get":
            print("\nIf you would like to get a specific password, type 'one'. If you would like all passwords, type 'all'.\n")
            user_input = input("What would you like to do? (one, all): ")
            if (user_input == "one"):
                get_password()
            elif (user_input == "all"):
                    get_password_list()

        elif user_input == "del":
            delete_password()

        elif user_input == "cha":
            change_password()
                
        elif user_input == "q":
            exit()
