import tkinter as tk
from tkinter import messagebox, ttk
import string
import random
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("450x550")
        self.root.configure(bg='#e6f2ff')

        # Initialize variables
        self.password_length = tk.IntVar(value=12)
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_lowercase = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_special = tk.BooleanVar(value=True)
        self.exclude_chars = tk.StringVar()
        self.password_visible = tk.BooleanVar(value=False)
        self.generated_password = ""  # To store the generated password

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Header Label
        header = tk.Label(self.root, text="🔒 Password Generator 🔒", font=("Arial", 16, "bold"), bg='#e6f2ff', fg='#003366')
        header.pack(pady=10)

        # Frame for length input and options
        frame_options = tk.Frame(self.root, bg='#f0f8ff')
        frame_options.pack(pady=10, padx=20)

        # Password Length
        tk.Label(frame_options, text="Password Length:", bg='#f0f8ff', fg='#333333', font=("Arial", 10, "bold")).grid(row=0, column=0, pady=5, sticky=tk.W)
        tk.Spinbox(frame_options, from_=4, to_=64, textvariable=self.password_length, font=("Arial", 10), width=5).grid(row=0, column=1, pady=5)

        # Include Options
        tk.Checkbutton(frame_options, text="Include Uppercase (A-Z)", variable=self.include_uppercase, bg='#f0f8ff', fg='#000000', font=("Arial", 10)).grid(row=1, column=0, columnspan=2, sticky=tk.W)
        tk.Checkbutton(frame_options, text="Include Lowercase (a-z)", variable=self.include_lowercase, bg='#f0f8ff', fg='#000000', font=("Arial", 10)).grid(row=2, column=0, columnspan=2, sticky=tk.W)
        tk.Checkbutton(frame_options, text="Include Digits (0-9)", variable=self.include_digits, bg='#f0f8ff', fg='#000000', font=("Arial", 10)).grid(row=3, column=0, columnspan=2, sticky=tk.W)
        tk.Checkbutton(frame_options, text="Include Special Characters (!@#$%^&*)", variable=self.include_special, bg='#f0f8ff', fg='#000000', font=("Arial", 10)).grid(row=4, column=0, columnspan=2, sticky=tk.W)

        # Exclude Characters Entry
        tk.Label(frame_options, text="Exclude Characters:", bg='#f0f8ff', fg='#333333', font=("Arial", 10, "bold")).grid(row=5, column=0, pady=10, sticky=tk.W)
        tk.Entry(frame_options, textvariable=self.exclude_chars, font=("Arial", 10), width=25).grid(row=5, column=1, pady=5)

        # Button to Generate Password
        self.btn_generate = tk.Button(self.root, text="Generate Password", command=self.generate_password, bg='#4682b4', fg='#ffffff', font=("Arial", 10, "bold"), width=25, pady=5)
        self.btn_generate.pack(pady=10)
        self.btn_generate.bind("<Enter>", self.on_hover)
        self.btn_generate.bind("<Leave>", self.on_leave)

        # Password Display Area
        self.password_frame = tk.Frame(self.root, bg='#e6f2ff')
        self.password_frame.pack(pady=10)
        self.password_label = tk.Label(self.password_frame, text="", font=("Arial", 12, "bold"), bg='#f0f8ff', fg='#003366', relief=tk.SUNKEN, width=30)
        self.password_label.grid(row=0, column=0)
        
        # Toggle visibility
        self.toggle_btn = tk.Button(self.password_frame, text="Show", command=self.toggle_password_visibility, bg='#32cd32', fg='#ffffff', font=("Arial", 10, "bold"))
        self.toggle_btn.grid(row=0, column=1, padx=5)

        # Button to Copy Password to Clipboard
        self.btn_copy = tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard, bg='#ff8c00', fg='#ffffff', font=("Arial", 10, "bold"), width=25, pady=5)
        self.btn_copy.pack(pady=10)
        self.btn_copy.bind("<Enter>", self.on_hover)
        self.btn_copy.bind("<Leave>", self.on_leave)

    def generate_password(self):
        length = self.password_length.get()
        include_uppercase = self.include_uppercase.get()
        include_lowercase = self.include_lowercase.get()
        include_digits = self.include_digits.get()
        include_special = self.include_special.get()
        exclude_chars = self.exclude_chars.get()

        # Define character pools
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        special = "!@#$%^&*()"

        # Build the pool based on user selections
        char_pool = ""
        if include_uppercase:
            char_pool += uppercase
        if include_lowercase:
            char_pool += lowercase
        if include_digits:
            char_pool += digits
        if include_special:
            char_pool += special

        # Remove excluded characters from pool
        if exclude_chars:
            char_pool = ''.join(c for c in char_pool if c not in exclude_chars)

        # Ensure there are enough characters to build a password
        if not char_pool:
            messagebox.showerror("Error", "No characters available to generate password. Please adjust your settings.")
            return

        # Generate password
        self.generated_password = ''.join(random.choice(char_pool) for _ in range(length))
        self.password_label.config(text="*" * len(self.generated_password))  # Start by hiding password
        self.password_visible.set(False)
        self.toggle_btn.config(text="Show")

    def copy_to_clipboard(self):
        if self.generated_password:
            pyperclip.copy(self.generated_password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy. Please generate one first.")

    def toggle_password_visibility(self):
        if self.password_visible.get():  # If the password is currently visible, hide it
            self.password_label.config(text="*" * len(self.generated_password))
            self.toggle_btn.config(text="Show")
        else:  # Show the password
            self.password_label.config(text=self.generated_password)
            self.toggle_btn.config(text="Hide")
        self.password_visible.set(not self.password_visible.get())

    def on_hover(self, event):
        event.widget.config(bg='#3b5998')

    def on_leave(self, event):
        event.widget.config(bg='#4682b4' if event.widget == self.btn_generate else '#ff8c00')

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
