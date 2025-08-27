# Pomidor Manager

A simple password manager with a GUI, built for a school project.  
**Not secure for real use — educational purposes only.**

---

## Features
- GUI built with Tkinter  
- Master password login  
- Strong password generator (using `secrets`)  
- Encrypted SQLite storage  
- Copy to clipboard support  

---

## Requirements
- Python 3.x  
- Libraries: `sqlite3`, `cryptography`, `hashlib`, `pyperclip`, `tkinter`, `secrets`  

---

## Installation
```bash
git clone https://github.com/authand/pomidor-manager
cd pomidor-manager
pip install -r requirements.txt
python password_manager_gui.py
```

---

## Usage
- First run: set a master password  
- Tabs: **Add**, **Retrieve**, **Generate**, **List**  
