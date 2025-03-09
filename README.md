# Password Manager Program

## Project Description
The **Password Manager Program** is a secure and user-friendly tool with a graphical interface for generating, storing, and managing passwords. It uses modern encryption algorithms to ensure data protection. Suitable for both everyday users and professional needs.

**(Not 100% secure, do not use for sensitive data, for educational purposes only).**

---

## Features

- **Graphical User Interface**: Simple and intuitive usage
- **Master Password Protection**: Secure access using a master password
- **Secure Password Generation**: Create unique, strong passwords with a chosen length
- **Password Storage**: Save passwords in an encrypted database
- **Password Retrieval**: Retrieve and copy passwords to the clipboard
- **Stored Data Overview**: View all services and usernames
- **Easy Navigation**: Switch between different functions using tabs

---

## System Requirements

- **Python Version**: Python 3.x
- **Operating System**: Windows, macOS, or Linux
- **Additional Libraries**:
  - sqlite3
  - cryptography
  - hashlib
  - pyperclip
  - tkinter
  - secrets

---

## Installation Instructions

1. **Download the project files** from the repository
2. **Open the terminal in the correct directory** by right-clicking and selecting "Open In Terminal"
3. **Install the required libraries** by running the following command in the terminal:
```bash
pip install -r requirements.txt
```
4. **Ensure** that Python 3 is installed on your system
5. **Run the program** using the command:
```bash
python password_manager_gui.py
```

---

## User Guide

### First Launch
1. **Initialize the Master Password**
   - Enter and confirm the master password during the first launch
   - This password will be required each time the program is opened

### Main Interface
The program offers four main tabs:

1. **Add Password**
   - Enter the service name
   - Enter the username
   - Choose between manual password entry or automatic generation

2. **Retrieve Password**
   - Enter the service name and username
   - The password will be displayed and automatically copied to the clipboard

3. **Generate Password**
   - Specify the desired password length
   - The generated password will be displayed and copied to the clipboard

4. **Service List**
   - A comprehensive list of all stored services
   - Displays service names and usernames
   - Option to update the list

---

## Security Features

- **Encrypted Database**: All passwords are stored in an encrypted format
- **Secure Master Password**: Uses PBKDF2 and SHA-256 hashing functions
- **Secure Password Generator**: Uses Python's secrets module
- **Automatic Copying**: Passwords are automatically copied to the clipboard

---

## License Information

This project is distributed under the **MIT License**. For more details, see the LICENSE file.

---

## Author

**Developer**: evanora  
**Contact**: [sokarihinji@gmail.com](mailto:sokarihinji@gmail.com)
