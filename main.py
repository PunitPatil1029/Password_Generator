
import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


# Character sets
CHARACTER_TYPES = {
    "Uppercase": string.ascii_uppercase,
    "Lowercase": string.ascii_lowercase,
    "Numbers": string.digits,
    "Symbols": "!@#$%^&*()-_=+[]{};:,.<>?/"
}

AMBIGUOUS = "0Ol1"


class PasswordGenerator:

    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("580x780")
        self.root.configure(bg="#1e293b")
        self.root.resizable(False, False)

        self.history = []

        self.length = tk.IntVar(value=12)
        self.uppercase = tk.BooleanVar(value=True)
        self.lowercase = tk.BooleanVar(value=True)
        self.numbers = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):

        tk.Label(
            self.root,
            text="🔐 Password Generator",
            font=("Arial", 22, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(pady=12)

        # Password length
        tk.Label(
            self.root,
            text="Password Length (8-64)",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack()

        tk.Spinbox(
            self.root,
            from_=8,
            to=64,
            textvariable=self.length,
            font=("Arial", 12),
            width=10
        ).pack(pady=5)

        # Character selection
        tk.Label(
            self.root,
            text="Select Character Types (minimum 2)",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(pady=8)

        options = [
            ("Uppercase Letters (A-Z)", self.uppercase),
            ("Lowercase Letters (a-z)", self.lowercase),
            ("Numbers (0-9)", self.numbers),
            ("Symbols (!@#$)", self.symbols)
        ]

        for text, variable in options:
            tk.Checkbutton(
                self.root,
                text=text,
                variable=variable,
                bg="#1e293b",
                fg="white",
                selectcolor="#334155",
                activebackground="#1e293b",
                activeforeground="white",
                font=("Arial", 11)
            ).pack(anchor="w", padx=150)

        tk.Checkbutton(
            self.root,
            text="Exclude ambiguous characters (0, O, l, 1)",
            variable=self.exclude_ambiguous,
            bg="#1e293b",
            fg="white",
            selectcolor="#334155",
            activebackground="#1e293b",
            activeforeground="white"
        ).pack(pady=7)

        # Generate button
        tk.Button(
            self.root,
            text="Generate Password",
            command=self.generate_password,
            bg="#2563eb",
            fg="white",
            font=("Arial", 12, "bold"),
            width=22
        ).pack(pady=10)

        # Password display
        self.password_entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            justify="center",
            width=35
        )
        self.password_entry.pack(pady=7)

        # Copy button
        tk.Button(
            self.root,
            text="Copy to Clipboard",
            command=self.copy_password,
            bg="#16a34a",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        # Password strength
        self.strength_label = tk.Label(
            self.root,
            text="Password Strength: Not generated",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="white"
        )
        self.strength_label.pack(pady=10)

        # History heading
        tk.Label(
            self.root,
            text="Recent Passwords (Last 5)",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(pady=5)

        # History frame
        history_frame = tk.Frame(self.root, bg="#1e293b")
        history_frame.pack(pady=5)

        # History listbox
        self.history_box = tk.Listbox(
            history_frame,
            width=45,
            height=5,
            font=("Arial", 10),
            bg="#334155",
            fg="white",
            selectbackground="#2563eb"
        )
        self.history_box.pack(side=tk.LEFT)

        # Scrollbar
        scrollbar = tk.Scrollbar(
            history_frame,
            orient=tk.VERTICAL,
            command=self.history_box.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_box.config(
            yscrollcommand=scrollbar.set
        )

        # Clear history button
        tk.Button(
            self.root,
            text="Clear History",
            command=self.clear_history,
            bg="#dc2626",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=8)

        tk.Label(
            self.root,
            text="History is stored only during this session.",
            font=("Arial", 9),
            bg="#1e293b",
            fg="#cbd5e1"
        ).pack(pady=3)

    def generate_password(self):

        try:
            length = int(self.length.get())

            if length < 8 or length > 64:
                messagebox.showerror(
                    "Invalid Length",
                    "Password length must be between 8 and 64."
                )
                return

        except (tk.TclError, ValueError):
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid password length."
            )
            return

        selected = []

        if self.uppercase.get():
            selected.append(CHARACTER_TYPES["Uppercase"])

        if self.lowercase.get():
            selected.append(CHARACTER_TYPES["Lowercase"])

        if self.numbers.get():
            selected.append(CHARACTER_TYPES["Numbers"])

        if self.symbols.get():
            selected.append(CHARACTER_TYPES["Symbols"])

        if len(selected) < 2:
            messagebox.showerror(
                "Selection Error",
                "Please select at least two character types."
            )
            return

        # Exclude ambiguous characters
        if self.exclude_ambiguous.get():
            selected = [
                "".join(
                    char for char in group
                    if char not in AMBIGUOUS
                )
                for group in selected
            ]

        # Guarantee at least one character
        # from each selected character type
        password_chars = [
            secrets.choice(group)
            for group in selected
        ]

        all_characters = "".join(selected)

        # Generate remaining characters
        for _ in range(length - len(password_chars)):
            password_chars.append(
                secrets.choice(all_characters)
            )

        # Securely shuffle the password
        for i in range(len(password_chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)

            password_chars[i], password_chars[j] = (
                password_chars[j],
                password_chars[i]
            )

        password = "".join(password_chars)

        # Display generated password
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        # Update strength
        self.update_strength(length, len(selected))

        # Update history
        self.history.insert(0, password)

        # Keep only the latest 5 passwords
        self.history = self.history[:5]

        # Refresh history display
        self.history_box.delete(0, tk.END)

        for item in self.history:
            self.history_box.insert(tk.END, item)

        self.history_box.update_idletasks()

        # Automatically copy password
        try:
            pyperclip.copy(password)

        except pyperclip.PyperclipException:
            messagebox.showwarning(
                "Clipboard Warning",
                "Password generated, but automatic copying failed."
            )

    def update_strength(self, length, diversity):

        if length >= 16 and diversity >= 4:
            strength = "Strong"
            color = "#22c55e"

        elif length >= 12 and diversity >= 3:
            strength = "Medium"
            color = "#facc15"

        else:
            strength = "Weak"
            color = "#ef4444"

        self.strength_label.config(
            text=f"Password Strength: {strength}",
            fg=color
        )

    def copy_password(self):

        password = self.password_entry.get()

        if not password:
            messagebox.showwarning(
                "No Password",
                "Generate a password first."
            )
            return

        try:
            pyperclip.copy(password)

            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard!"
            )

        except pyperclip.PyperclipException:
            messagebox.showerror(
                "Clipboard Error",
                "Could not access the clipboard."
            )

    def clear_history(self):

        self.history.clear()
        self.history_box.delete(0, tk.END)

        messagebox.showinfo(
            "History Cleared",
            "Password history has been cleared."
        )


if __name__ == "__main__":

    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
