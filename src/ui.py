import tkinter as tk
from tkinter import messagebox
from encryption import encrypt_password, decrypt_passwords
import random
import string

class PasswordManagerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("400x500")
        
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        tk.Label(main_frame, text="Website:").pack(pady=5)
        self.website_entry = tk.Entry(main_frame, width=40)
        self.website_entry.pack(pady=5)
        
        tk.Label(main_frame, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(main_frame, width=40, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(main_frame, text="Add Password", command=self.add_password).pack(pady=10)
        tk.Button(main_frame, text="Generate Password", command=self.generate_password).pack(pady=5)
        tk.Button(main_frame, text="Show Passwords", command=self.show_passwords).pack(pady=5)
        
        self.password_list = tk.Text(main_frame, height=15, width=40)
        self.password_list.pack(pady=10)
        
    def add_password(self):
        website = self.website_entry.get()
        password = self.password_entry.get()
        
        if website and password:
            encrypt_password(website, password)
            messagebox.showinfo("Success", "Password added successfully!")
            self.website_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter both website and password")
            
    def generate_password(self):
        length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        
    def show_passwords(self):
        self.password_list.delete(1.0, tk.END)
        passwords = decrypt_passwords()
        if not passwords:
            self.password_list.insert(tk.END, "No passwords saved yet.\n")
        else:
            for website, password in passwords:
                self.password_list.insert(tk.END, f"Website: {website}\nPassword: {password}\n\n")

def main():
    root = tk.Tk()
    app = PasswordManagerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 