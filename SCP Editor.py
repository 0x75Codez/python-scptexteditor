import tkinter as tk
from tkinter import messagebox
import time
import threading
import re

class RetroSCPTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("SCP Foundation Terminal")
        self.root.configure(bg='black')
        self.username = "USER"
        self.boot_screen()

    def boot_screen(self):
        self.boot_frame = tk.Frame(self.root, bg='black')
        self.boot_frame.pack(fill='both', expand=True)

        self.boot_text = tk.Text(self.boot_frame, fg='green', bg='black',
                                 font=("Courier New", 12), bd=0, highlightthickness=0)
        self.boot_text.pack(fill='both', expand=True)
        self.boot_text.configure(state='disabled')

        self.boot_ascii = [
            " ______  ______  ______  ",
            "/\\  ___\\/\\  ___\\/\\  == \\ ",
            "\\ \\___  \\ \\ \\___\\ \\  _-/ ",
            " \\/\\_____\\ \\_____\\ \\_\\   ",
            "  \\/_____/\\/_____/\\/_/   ",
            "                         ",
            "=== SCP FOUNDATION SECURE TERMINAL ===",
            "     Version 1.0 - CLASSIFIED ACCESS",
            "----------------------------------------",
            ""
        ]

        threading.Thread(target=self.run_boot_sequence, daemon=True).start()

    def append_boot_text(self, text):
        self.boot_text.configure(state='normal')
        self.boot_text.insert(tk.END, text + '\n')
        self.boot_text.see(tk.END)
        self.boot_text.configure(state='disabled')

    def run_boot_sequence(self):
        for line in self.boot_ascii:
            self.append_boot_text(line)
            time.sleep(0.3)

        checks = [
            "Checking secure protocols... OK",
            "Loading containment procedures... OK",
            "Authenticating terminal... OK",
            "Initializing user interface... OK",
            "System ready."
        ]
        for check in checks:
            self.append_boot_text(check)
            time.sleep(0.5)

        time.sleep(0.5)
        self.append_boot_text("\nPress Enter to continue...\n")
        self.boot_text.bind("<Return>", self.to_login)

    def to_login(self, event=None):
        self.boot_frame.destroy()
        self.login_screen()

    def login_screen(self):
        self.login_frame = tk.Frame(self.root, bg='black')
        self.login_frame.pack(expand=True)

        self.login_label = tk.Label(self.login_frame, text="=== SCP FOUNDATION SECURE TERMINAL LOGIN ===",
                                    fg="green", bg="black", font=("Courier New", 12, "bold"))
        self.login_label.pack(pady=10)

        self.user_label = tk.Label(self.login_frame, text="Username:", fg="green", bg="black", font=("Courier New", 10))
        self.user_label.pack()
        self.username_entry = tk.Entry(self.login_frame, fg="green", bg="black", insertbackground="green")
        self.username_entry.pack()

        self.pass_label = tk.Label(self.login_frame, text="Password:", fg="green", bg="black", font=("Courier New", 10))
        self.pass_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*", fg="green", bg="black", insertbackground="green")
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="LOGIN", command=self.authenticate,
                                      fg="green", bg="black", activebackground="green", activeforeground="black")
        self.login_button.pack(pady=10)

        self.root.bind("<Return>", lambda e: self.authenticate())

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            self.username = username.upper()
            self.login_frame.destroy()
            self.launch_editor()
        else:
            messagebox.showerror("ACCESS DENIED", "Invalid credentials. Try again.")

    def launch_editor(self):
        self.editor_frame = tk.Frame(self.root, bg='black')
        self.editor_frame.pack(fill='both', expand=True)

        self.header_text = (
            " ______  ______  ______  \n"
            "/\\  ___\\/\\  ___\\/\\  == \\ \n"
            "\\ \\___  \\ \\ \\___\\ \\  _-/ \n"
            " \\/\\_____\\ \\_____\\ \\_\\   \n"
            "  \\/_____/\\/_____/\\/_/   \n"
            "                         \n"
            "=== SCP FOUNDATION SECURE TERMINAL ===\n"
            "     Version 1.0 - CLASSIFIED ACCESS\n"
            "----------------------------------------\n"
        )

        self.header_widget = tk.Text(self.editor_frame, fg='green', bg='black',
                                     font=("Courier New", 12), height=10, bd=0, highlightthickness=0)
        self.header_widget.pack(fill='x')
        self.header_widget.insert('1.0', self.header_text)
        self.header_widget.configure(state='disabled')

        self.text = tk.Text(self.editor_frame, fg='green', bg='black', insertbackground='green',
                            font=("Courier New", 12), undo=True)
        self.text.pack(fill='both', expand=True)

        self.status_bar = tk.Label(self.root, text="Ctrl+S: Save | Ctrl+Q: Quit | [REDACTED], [COLOR_*] supported",
                                   fg='green', bg='black', font=("Courier New", 10))
        self.status_bar.pack(fill='x')

        self.prompt_prefix = f"X:\\{self.username}> "
        self.text.insert('1.0', self.prompt_prefix)

        # Keybindings
        self.text.bind('<KeyPress>', self.protect_prompt_prefix)
        self.text.bind('<Button-1>', self.protect_click)
        self.text.bind('<FocusIn>', self.on_focus_in)
        self.text.bind('<Control-s>', self.save_file)
        self.text.bind('<Control-q>', lambda e: self.root.quit())
        self.text.bind('<KeyRelease>', lambda e: self.apply_formatting())

        # Setup tags for formatting
        self.text.tag_configure("redacted", background="black", foreground="black")
        colors = ['red', 'green', 'yellow', 'blue', 'cyan', 'magenta', 'white']
        for color in colors:
            self.text.tag_configure(f"highlight_{color}", foreground=color)

    def protect_prompt_prefix(self, event):
        cursor_index = self.text.index("insert")
        line, col = map(int, cursor_index.split('.'))
        if line == 1 and col < len(self.prompt_prefix):
            return "break"

    def protect_click(self, event):
        cursor_index = self.text.index(f"@{event.x},{event.y}")
        line, col = map(int, cursor_index.split('.'))
        if line == 1 and col < len(self.prompt_prefix):
            self.text.mark_set("insert", f"1.{len(self.prompt_prefix)}")
            return "break"

    def on_focus_in(self, event):
        cursor_index = self.text.index("insert")
        line, col = map(int, cursor_index.split('.'))
        if line == 1 and col < len(self.prompt_prefix):
            self.text.mark_set("insert", f"1.{len(self.prompt_prefix)}")

    def save_file(self, event=None):
        file_path = f"{self.username}_scp_document.scp"
        try:
            content = self.text.get('1.0', 'end-1c')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Saved", f"File saved as {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
        return "break"

    def apply_formatting(self):
        content = self.text.get('1.0', 'end-1c')

        # Clear all tags
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, '1.0', 'end')

        colors = ['red', 'green', 'yellow', 'blue', 'cyan', 'magenta', 'white']

        # Apply redacted formatting
        redacted_start = 0
        console_output = content

        while True:
            start = content.find("[REDACTED]", redacted_start)
            if start == -1:
                break
            end = content.find("[REDACTED_END]", start)
            if end == -1:
                break
            redact_text_start = start + len("[REDACTED]")
            redact_text_end = end

            start_index = self.text.index(f"1.0 + {redact_text_start} chars")
            end_index = self.text.index(f"1.0 + {redact_text_end} chars")
            self.text.tag_add("redacted", start_index, end_index)

            # Replace redacted content in console with █
            redacted_text = content[redact_text_start:redact_text_end]
            redacted_mask = '█' * len(redacted_text)
            console_output = console_output.replace(redacted_text, redacted_mask)

            redacted_start = end + len("[REDACTED_END]")

        # Apply color formatting
        color_pattern = re.compile(r"\[COLOR_([A-Z]+)\](.*?)\[COLOR_END\]", re.DOTALL)
        ansi_colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'magenta': '\033[95m',
            'white': '\033[97m'
        }

        for match in color_pattern.finditer(content):
            color = match.group(1).lower()
            if color not in colors:
                continue
            start = match.start(2)
            end = match.end(2)
            start_index = self.text.index(f"1.0 + {start} chars")
            end_index = self.text.index(f"1.0 + {end} chars")
            self.text.tag_add(f"highlight_{color}", start_index, end_index)

            # Replace in console with color
            colored_text = match.group(2)
            color_code = ansi_colors[color]
            reset_code = '\033[0m'
            full_tagged = match.group(0)
            colored_version = f"{color_code}{colored_text}{reset_code}"
            console_output = console_output.replace(full_tagged, colored_version)

        # Print formatted output to console (terminal)
        print("\n--- TERMINAL FORMATTED OUTPUT ---")
        print(console_output)
        print("--- END ---\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x700")
    app = RetroSCPTerminal(root)
    root.mainloop()
