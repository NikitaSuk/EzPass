import random
import string

def get_input():
    user_input = input("What would you like to do? (own, gen, get, del, cha, q): ")
    return user_input

def password_generator(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

if __name__ == "__main__":
    print("\nWelcome to the password manager!\n")
    print("If you would like to enter your own password, type 'own'. If you would like a password generated for you, type 'gen'. If you would like to get a password, type 'get'.")
    print("If you would like to delete a specific password, type 'del'. If you would like to change a specific password, type 'cha'. If you would like to quit, type 'q'.\n")
    
    while True:
        user_input = get_input()

        if user_input == "own":
            website = input("\nEnter where this password is for: ")
            password = input("\nEnter the password: ")
            with open("passwords.txt", "a") as passwords:
                passwords.write(f"{website} : {password}\n")
            print(f"\nPassword for {website} was generated successfully.\n")

        elif user_input == "gen":
            website = input("\nEnter where this password is for: ")
            password = password_generator()
            with open("passwords.txt", "a") as passwords:
                passwords.write(f"{website} : {password}\n")
            print(f"\nPassword for {website} was generated successfully.\n")

        elif user_input == "get":
            print('')
            with open("passwords.txt", "r") as passwords:
                print(passwords.read())

        elif user_input == "del":
            website = input("\nEnter where this password is for: ")
            with open("passwords.txt", "r") as passwords:
                lines = passwords.readlines()

            with open("passwords.txt", "w") as passwords:
                for line in lines:
                    if website not in line:
                        passwords.write(line)

        elif user_input == "cha":
            website = input("Enter where this password is for: ")
            with open("passwords.txt", "r") as passwords:
                lines = passwords.readlines()
            with open("passwords.txt", "w") as passwords:
                for line in lines:
                    if website in line:
                        password = password_generator()
                        passwords.write(f"{website} : {password}\n")
                    else:
                        passwords.write(line)
                
        elif user_input == "q":
            exit()
