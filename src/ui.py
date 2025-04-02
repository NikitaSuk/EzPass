import tkinter as tk
from tkinter import ttk, messagebox
from encryption import encrypt_password, decrypt_passwords, load_key
from cryptography.fernet import Fernet
import random
import string
import os

class PasswordManagerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EzPass Password Manager")
        self.root.geometry("600x700")
        self.root.minsize(800, 600)
        self.root.configure(bg='#f0f0f0')
        
        style = ttk.Style()
        style.configure('TButton', padding=5, font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 10), background='#f0f0f0')
        style.configure('TEntry', padding=5)
        
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(expand=True, fill='both')
        
        title_label = ttk.Label(self.main_frame, text="EzPass Password Manager", 
                              font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill='both', pady=10)
        
        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.edit_tab = ttk.Frame(self.notebook)
        self.trash_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.add_tab, text='Add Password')
        self.notebook.add(self.view_tab, text='View Passwords')
        self.notebook.add(self.edit_tab, text='Edit Passwords')
        self.notebook.add(self.trash_tab, text='Trash')
        
        self.setup_add_tab()
        self.setup_view_tab()
        self.setup_edit_tab()
        self.setup_trash_tab()
        
    def setup_add_tab(self):
        add_frame = ttk.LabelFrame(self.add_tab, text="Add New Password", padding="10")
        add_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        ttk.Label(add_frame, text="Website:").pack(pady=5)
        self.website_entry = ttk.Entry(add_frame, width=40)
        self.website_entry.pack(pady=5)
        
        ttk.Label(add_frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(add_frame, width=40, show="*")
        self.password_entry.pack(pady=5)
        
        button_frame = ttk.Frame(add_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Password", 
                  command=self.add_password).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Generate Password", 
                  command=self.generate_password).pack(side='left', padx=5)
        
    def setup_view_tab(self):
        view_frame = ttk.LabelFrame(self.view_tab, text="View Passwords", padding="10")
        view_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        search_frame = ttk.Frame(view_frame)
        search_frame.pack(fill='x', pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_passwords)
        
        self.password_list = ttk.Treeview(view_frame, columns=('Website', 'Password'), 
                                        show='headings', height=15)
        self.password_list.heading('Website', text='Website')
        self.password_list.heading('Password', text='Password')
        self.password_list.pack(expand=True, fill='both', pady=5)
        
        button_frame = ttk.Frame(view_frame)
        button_frame.pack(pady=5)
        
        self.show_passwords_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(button_frame, text="Show Passwords", 
                       variable=self.show_passwords_var,
                       command=self.toggle_password_visibility).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Refresh", 
                  command=self.refresh_passwords).pack(side='left', padx=5)
        
    def toggle_password_visibility(self):
        self.refresh_passwords()
        
    def refresh_passwords(self):
        for item in self.password_list.get_children():
            self.password_list.delete(item)

        passwords = decrypt_passwords()
        for website, password in passwords:
            if self.show_passwords_var.get():
                self.password_list.insert('', 'end', values=(website, password))
            else:
                self.password_list.insert('', 'end', values=(website, "••••••••"))

        self.edit_website_combo['values'] = [website for website, _ in passwords]
        
    def filter_passwords(self, event=None):
        search_term = self.search_entry.get().lower()
        
        for item in self.password_list.get_children():
            self.password_list.delete(item)
            
        passwords = decrypt_passwords()
        for website, password in passwords:
            if search_term in website.lower():
                self.password_list.insert('', 'end', values=(website, password))
                
    def setup_edit_tab(self):
        edit_frame = ttk.LabelFrame(self.edit_tab, text="Edit Passwords", padding="10")
        edit_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        content_frame = ttk.Frame(edit_frame)
        content_frame.pack(side='left', expand=True, fill='both', padx=5)
        
        ttk.Label(content_frame, text="Select Website:").pack(pady=5)
        self.edit_website_var = tk.StringVar()
        self.edit_website_combo = ttk.Combobox(content_frame, textvariable=self.edit_website_var)
        self.edit_website_combo.pack(pady=5)
        
        ttk.Label(content_frame, text="New Password:").pack(pady=5)
        self.edit_password_entry = ttk.Entry(content_frame, width=40, show="*")
        self.edit_password_entry.pack(pady=5)
        
        button_frame = ttk.Frame(edit_frame)
        button_frame.pack(side='right', fill='y', padx=5)
        
        ttk.Button(button_frame, text="Enter", 
                  command=self.change_password).pack(pady=5)
        ttk.Button(button_frame, text="Generate New Password", 
                  command=self.generate_new_password).pack(pady=5)
        ttk.Button(button_frame, text="Move to Trash", 
                  command=self.move_to_trash).pack(pady=5)
        
    def setup_trash_tab(self):
        trash_frame = ttk.LabelFrame(self.trash_tab, text="Trash", padding="10")
        trash_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        content_frame = ttk.Frame(trash_frame)
        content_frame.pack(side='left', expand=True, fill='both', padx=5)
        
        self.trash_list = ttk.Treeview(content_frame, columns=('Website', 'Password'), 
                                     show='headings', height=15)
        self.trash_list.heading('Website', text='Website')
        self.trash_list.heading('Password', text='Password')
        self.trash_list.pack(expand=True, fill='both', pady=5)
        
        self.show_trash_passwords_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(content_frame, text="Show Passwords", 
                       variable=self.show_trash_passwords_var,
                       command=self.toggle_trash_password_visibility).pack(pady=5)
        
        button_frame = ttk.Frame(trash_frame)
        button_frame.pack(side='right', fill='y', padx=5)
        
        ttk.Button(button_frame, text="Restore Selected", 
                  command=self.restore_selected).pack(pady=5)
        ttk.Button(button_frame, text="Restore All", 
                  command=self.restore_all).pack(pady=5)
        ttk.Button(button_frame, text="Delete Selected", 
                  command=self.delete_selected).pack(pady=5)
        ttk.Button(button_frame, text="Empty Trash", 
                  command=self.empty_trash).pack(pady=5)
        ttk.Button(button_frame, text="Refresh", 
                  command=self.refresh_trash).pack(pady=5)
        
    def toggle_trash_password_visibility(self):
        self.refresh_trash()
        
    def refresh_trash(self):
        for item in self.trash_list.get_children():
            self.trash_list.delete(item)
            
        try:
            with open('trash.enc', 'rb') as file:
                for line in file:
                    website, encrypted_password = line.strip().split(b':', 1)
                    key = load_key()
                    f = Fernet(key)
                    decrypted_password = f.decrypt(encrypted_password).decode()
                    if self.show_trash_passwords_var.get():
                        self.trash_list.insert('', 'end', values=(website.decode(), decrypted_password))
                    else:
                        self.trash_list.insert('', 'end', values=(website.decode(), "••••••••"))
        except FileNotFoundError:
            pass
        
    def add_password(self):
        website = self.website_entry.get()
        password = self.password_entry.get()
        
        if website and password:
            if ' ' in website or ' ' in password:
                messagebox.showerror("Error", "Spaces are not allowed in website or password")
                return
                
            passwords = decrypt_passwords()
            base_website = website
            counter = 2
            while any(w == website for w, _ in passwords):
                website = f"{base_website}{counter}"
                counter += 1
                
            encrypt_password(website, password)
            messagebox.showinfo("Success", f"Password added successfully for {website}!")
            self.website_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.refresh_passwords()
        else:
            messagebox.showerror("Error", "Please enter both website and password")
            
    def generate_password(self):
        length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        
    def change_password(self):
        website = self.edit_website_var.get()
        new_password = self.edit_password_entry.get()
        
        if website and new_password:
            if ' ' in new_password:
                messagebox.showerror("Error", "Spaces are not allowed in password")
                return
            passwords = decrypt_passwords()
            with open('passwords.enc', 'wb') as file:
                for stored_website, password in passwords:
                    if website == stored_website:
                        encrypt_password(website, new_password)
                    else:
                        encrypt_password(stored_website, password)
            messagebox.showinfo("Success", "Password changed successfully!")
            self.edit_password_entry.delete(0, tk.END)
            self.refresh_passwords()
        else:
            messagebox.showerror("Error", "Please select a website and enter a new password")
            
    def generate_new_password(self):
        website = self.edit_website_var.get()
        if website:
            length = 12
            characters = string.ascii_letters + string.digits + string.punctuation
            new_password = ''.join(random.choice(characters) for i in range(length))
            self.edit_password_entry.delete(0, tk.END)
            self.edit_password_entry.insert(0, new_password)
        else:
            messagebox.showerror("Error", "Please select a website first")
            
    def move_to_trash(self):
        website = self.edit_website_var.get()
        if website:
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
            messagebox.showinfo("Success", "Password moved to trash successfully!")
            self.refresh_passwords()
            self.refresh_trash()
        else:
            messagebox.showerror("Error", "Please select a website first")
            
    def restore_selected(self):
        selected = self.trash_list.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a password to restore")
            return
            
        for item in selected:
            website = self.trash_list.item(item)['values'][0]
            with open('trash.enc', 'rb') as file:
                trash_lines = file.readlines()
            
            with open('trash.enc', 'wb') as file, open('passwords.enc', 'ab') as passwords_file:
                for line in trash_lines:
                    stored_website, encrypted_password = line.strip().split(b':', 1)
                    if website != stored_website.decode():
                        file.write(line)
                    else:
                        passwords_file.write(line)
                        
        messagebox.showinfo("Success", "Selected passwords restored successfully!")
        self.refresh_passwords()
        self.refresh_trash()
        
    def restore_all(self):
        try:
            with open('trash.enc', 'rb') as trash_file, open('passwords.enc', 'ab') as file:
                for line in trash_file:
                    file.write(line)
            open('trash.enc', 'w').close()
            messagebox.showinfo("Success", "All passwords restored successfully!")
            self.refresh_passwords()
            self.refresh_trash()
        except FileNotFoundError:
            messagebox.showinfo("Info", "Trash is empty")
            
    def delete_selected(self):
        selected = self.trash_list.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a password to delete")
            return
            
        for item in selected:
            website = self.trash_list.item(item)['values'][0]
            with open('trash.enc', 'rb') as file:
                trash_lines = file.readlines()
            
            with open('trash.enc', 'wb') as file:
                for line in trash_lines:
                    stored_website, encrypted_password = line.strip().split(b':', 1)
                    if website != stored_website.decode():
                        file.write(line)
                        
        messagebox.showinfo("Success", "Selected passwords deleted successfully!")
        self.refresh_trash()
        
    def empty_trash(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to empty the trash?"):
            with open('trash.enc', 'w') as file:
                file.close()
            messagebox.showinfo("Success", "Trash emptied successfully!")
            self.refresh_trash()

def main():
    root = tk.Tk()
    app = PasswordManagerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 