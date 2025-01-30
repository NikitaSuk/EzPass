# Password Manager

A simple command-line password manager written in Python. This tool allows users to store, generate, retrieve, delete, and update passwords for different websites.

## Features

- **Store passwords**: Manually enter and save passwords.
- **Generate passwords**: Create strong, random passwords.
- **Retrieve passwords**: View saved passwords.
- **Delete passwords**: Remove stored passwords.
- **Update passwords**: Replace old passwords with new randomly generated ones.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/password-manager.git
   ```
2. Navigate to the project directory:
   ```sh
   cd password-manager
   ```
3. Run the script:
   ```sh
   python password_manager.py
   ```

## Usage

When you run the script, you will see the following menu:

```
Welcome to the password manager!

Options:
- 'own'  : Enter your own password
- 'gen'  : Generate a random password
- 'get'  : Retrieve a saved password
- 'del'  : Delete a password
- 'cha'  : Change a stored password
- 'q'    : Quit the program
```

### Commands

- **own**: Manually add a password.
- **gen**: Generate and save a random password.
- **get**: Retrieve a password.
  - `one` - Retrieve a password for a specific website.
  - `all` - Display all stored passwords.
- **del**: Delete a stored password.
- **cha**: Change a password with a newly generated one.
- **q**: Quit the program.

## Example

1. **Add a password manually**:
   ```
   Enter where this password is for: GitHub
   Enter the password: mysecurepassword
   Password for GitHub was saved successfully.
   ```

2. **Generate a password**:
   ```
   Enter where this password is for: Twitter
   Password for Twitter was generated successfully.
   ```

3. **Retrieve a password**:
   ```
   Enter where this password is for: GitHub
   GitHub : mysecurepassword
   ```

## Requirements

- Python 3.x

## Security Considerations

⚠️ **Passwords are stored in plaintext (`passwords.txt`). For better security, consider encrypting stored data.**

