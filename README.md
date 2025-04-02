
# EzPass Password Manager

_EzPass Password Manager_ is a lightweight, Python-based application designed to securely manage your passwords. With both a graphical interface (built with Tkinter) and a command-line interface, it offers flexibility for users who prefer either interactive or terminal-based management. The application employs strong encryption using the [cryptography](https://cryptography.io/en/latest/) library (Fernet) to safeguard your stored passwords.

---

## Table of Contents

- [Features](#features)
- [File Structure](#file-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Graphical User Interface (GUI)](#graphical-user-interface-gui)
  - [Command-Line Interface (CLI)](#command-line-interface-cli)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Secure Storage:** Encrypts passwords using Fernet symmetric encryption.
- **Multiple Interfaces:** Choose between a modern Tkinter GUI and a classic command-line interface.
- **Password Generation:** Quickly generate strong, random passwords.
- **Password Management:** Easily add, view, edit, and delete passwords.
- **Trash System:** Moved deleted passwords are stored in a “trash” file for potential restoration.

---

## File Structure

- **`main.py`**  
  Provides a command-line interface with various options for adding, viewing, editing, and deleting passwords.

- **`ui.py`**  
  Implements a Tkinter-based GUI for users who prefer a graphical approach. It includes interactive tabs for adding, viewing, editing, and trash management.

- **`encryption.py`**  
  Handles encryption and decryption operations using Fernet. It is responsible for generating/loading the encryption key and managing the encrypted password files.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/ezpass-password-manager.git
   cd ezpass-password-manager
   ```

2. **Set Up a Virtual Environment (Optional but Recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   Make sure you have Python 3 installed. Then install the required package:

   ```bash
   pip install cryptography
   ```

   _Note: Tkinter is bundled with standard Python distributions. If not, please install it via your package manager._

---

## Usage

### Graphical User Interface (GUI)

To launch the interactive GUI:

```bash
python ui.py
```

The GUI features four interactive tabs:

- **Add Password:**  
  Enter the website and either type in or generate a secure password.

- **View Passwords:**  
  Browse through the saved passwords. Use the search bar to filter by website and toggle visibility to show/hide passwords.

- **Edit Passwords:**  
  Select a website from the list, then update or regenerate the password as needed.

- **Trash:**  
  Manage deleted passwords. Restore accidentally deleted items or permanently remove them.

### Command-Line Interface (CLI)

For users who prefer the terminal, run:

```bash
python main.py
```

Follow the interactive prompts:

1. **Add:**  
   Choose to add your own password or generate one automatically.

2. **View:**  
   List saved websites or display specific passwords.

3. **Edit:**  
   Change an existing password or move a password to the trash.

4. **Trash:**  
   View, restore, or permanently delete trashed passwords.

Each option is designed to guide you through the process with clear instructions, making password management simple and secure.

---

## How It Works

- **Encryption:**  
  All passwords are encrypted before being stored in the `passwords.enc` file. The encryption key is generated once and stored in `secret.key`. This ensures that even if the encrypted file is compromised, the passwords remain secure.

- **Trash Mechanism:**  
  When a password is removed, it is not immediately deleted. Instead, it is moved to a `trash.enc` file, giving you a chance to restore it if needed.

- **User Experience:**  
  Both interfaces offer an interactive experience:
  - The GUI uses modern widgets and tabs for an intuitive workflow.
  - The CLI provides step-by-step instructions and interactive prompts to perform actions.

---

## Contributing

Contributions are welcome! If you have ideas for improvements or have found a bug, feel free to create an issue or submit a pull request on GitHub.

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Create a new Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

_Enjoy using EzPass Password Manager to keep your digital life secure and organized!_

--- 

This README provides a comprehensive overview of the project along with clear, step-by-step instructions on how to install and use the tool, both via GUI and CLI.
