# Retro SCP Foundation Terminal

A retro-styled SCP Foundation secure terminal emulator built with Python and Tkinter.  
This app simulates a secure terminal with a boot sequence, login screen, and an editor supporting special formatting like redacted sections and colored text.

---

## Features

- Retro green-on-black terminal UI
- Boot sequence with SCP-themed ASCII art and checks
- Secure login screen (mock authentication)
- Text editor with:
  - Protected prompt prefix
  - Support for `[REDACTED]... [REDACTED_END]` blocks that hide sensitive text
  - Color formatting using `[COLOR_RED]... [COLOR_END]` tags
- Save your SCP documents to a file named after your username
- Keyboard shortcuts:
  - Ctrl+S: Save document
  - Ctrl+Q: Quit application

---

## Installation

1. Make sure you have Python 3 installed.
2. Install required dependencies:

```bash
pip install -r requirements.txt
