A simple command-line password manager built with Python. This tool allows users to store, generate, retrieve, delete, and update passwords for different websites.

Features

🔐 Store Your Own Passwords: Manually enter and save passwords.

🔑 Generate Secure Passwords: Automatically create strong passwords.

📜 Retrieve Passwords: View saved passwords for specific websites.

🗑 Delete Passwords: Remove saved passwords.

🔄 Change Passwords: Update stored passwords with a new generated one.

Installation

Clone the repository:

git clone https://github.com/your-username/password-manager.git

Navigate into the directory:

cd password-manager

Run the script:

python password_manager.py

Usage

Upon running the script, you'll be presented with a menu:

Welcome to the password manager!

If you would like to enter your own password, type 'own'.
If you would like a password generated for you, type 'gen'.
If you would like to get a password, type 'get'.
If you would like to delete a specific password, type 'del'.
If you would like to change a specific password, type 'cha'.
If you would like to quit, type 'q'.

Commands

``: Manually add a password.

``: Generate and save a random password.

``: Retrieve passwords.

one - Retrieve a password for a specific website.

all - Display all stored passwords.

``: Delete a stored password.

``: Change a password with a newly generated one.

``: Quit the program.

Example

Add a password manually:

Enter where this password is for: GitHub
Enter the password: mysecurepassword
Password for GitHub was generated successfully.

Generate a password:

Enter where this password is for: Twitter
Password for Twitter was generated successfully.

Retrieve a password:
