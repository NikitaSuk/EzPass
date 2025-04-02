import random
import string
from encryption import encrypt_password, decrypt_passwords

def get_input():
    user_input = input("What would you like to do? (own, gen, get, lis, del, cha, q): ")
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

def website_list():
    passwords = decrypt_passwords()
    print('')
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

def delete_password():
    website_list()
    website = input("Enter which password you would like to delete from the list above: ")
    passwords = decrypt_passwords()
    with open('passwords.enc', 'wb') as file:
        for stored_website, password in passwords:
            if website != stored_website:
                encrypt_password(stored_website, password)
            else:
                print(f"\nPassword for {website} was deleted successfully.\n")

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

if __name__ == "__main__":
    print("\nWelcome to the password manager!\n")
    print("If you would like to enter your own password, type 'own'. If you would like a password generated for you, type 'gen'. If you would like to get a a list of places you have stores, type 'lis'. If you would like to get a password, type 'get'.")
    print("If you would like to delete a specific password, type 'del'. If you would like to change a specific password, type 'cha'. If you would like to quit, type 'q'.\n")
    
    while True:
        user_input = get_input()

        if user_input == "own":
            own_password()

        elif user_input == "gen":
            gen_password()
            
        elif user_input == "lis":
            website_list()

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
            print("\nIf you would like to change a password yourself, type 'own'. If you would like a password generated for you, type 'gen'.\n")
            user_input = input("What would you like to do? (own, gen): ")
            if (user_input == "own"):
                change_password_own()
            elif (user_input == "gen"):
                change_password_gen()
                
        elif user_input == "q":
            print(" ")
            exit()
