import sqlite3
import hashlib
import secrets
import base64
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass
import sys
import pyperclip

class PasswordManager:
    def __init__(self, database_name="passwords.db"):
        # inicialize mainigos
        self.database_name = database_name
        self.key = None
        self.cipher_suite = None
        self.setup_database()

    def setup_database(self):
        # uzsāk SQLite datubāzi ar vajadzīgajām tabulām
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        
        # veido master paroles tabulu (priekš hash un salta)
        # Lowkey nezinu sql es šito kodu daļu pats netaisīju
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_password (
            id INTEGER PRIMARY KEY,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )''')
        
        # veido paroles tabulu (glabā šifrētus datus)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password TEXT NOT NULL
        )''')
        
        conn.commit()
        conn.close()

    def generate_password(self, length=16, copy_to_clipboard=True):
        # izveidot drošu paroli un pēc izvēles kopējiet to.
        if length < 8:
            raise ValueError("Paroles garumam ir jābūt vismaz 8 rakstzīmēm")
        elif length > 64:
            raise ValueError("Paroles garums nevar pārsniegt 64 rakstzīmēs")
            
        # iekļauj visas rakstzīmes
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # nodrošina vismaz vienu rakstzīmi no visiem
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(special)
        ]
        
        # iepilda pārējo ar random rakstzīmēm
        all_chars = lowercase + uppercase + digits + special
        remaining_length = length - len(password)
        password.extend(secrets.choice(all_chars) for _ in range(remaining_length))
        
        # sajauc paroli
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)
        
        final_password = ''.join(password_list)
        
        # nokopē paroli ja tas ir nepieciešams
        if copy_to_clipboard:
            pyperclip.copy(final_password)
        
        return final_password

    def generate_key(self, password: str, salt: bytes = None) -> bytes:
        # izveido šifrēšanas atslēgu no paroles izmantojot PBKDF2 (Password-Based Key Derivation Function 2)
        if salt is None:
            salt = secrets.token_bytes(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def hash_password(self, password: str, salt: bytes = None) -> tuple:
        # hasho paroli ar saltu izmantojot SHA-256
        if salt is None:
            salt = secrets.token_bytes(16)
        
        hasher = hashlib.sha256()
        hasher.update(salt + password.encode())
        password_hash = hasher.hexdigest()
        
        return password_hash, salt

    def initialize_master_password(self, master_password: str):
        # iestata master paroli pirmo reizi
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        
        # pārbauda vai master parole jau eksistē
        cursor.execute("SELECT COUNT(*) FROM master_password")
        if cursor.fetchone()[0] > 0:
            raise Exception("Master parole jau inicializēta")
        
        # hasho master paroli ar jaunu saltu
        password_hash, salt = self.hash_password(master_password)
        
        # glabā hashu un saltu
        cursor.execute(
            "INSERT INTO master_password (password_hash, salt) VALUES (?, ?)",
            (password_hash, base64.b64encode(salt).decode())
        )
        
        conn.commit()
        conn.close()
        
        # uzāk šifrēšanas atslēgu
        self.key, _ = self.generate_key(master_password, salt)
        self.cipher_suite = Fernet(self.key)

    def unlock(self, master_password: str) -> bool:
        # pārbaude master paroli un uzsāk šifrēšanas atslēgu
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT password_hash, salt FROM master_password")
        stored_hash, stored_salt = cursor.fetchone()
        stored_salt = base64.b64decode(stored_salt)
        
        # pārbauda paroli
        password_hash, _ = self.hash_password(master_password, stored_salt)
        if password_hash != stored_hash:
            conn.close()
            return False
        
        # uzsāk šifrēsanas atslēgu
        self.key, _ = self.generate_key(master_password, stored_salt)
        self.cipher_suite = Fernet(self.key)
        
        conn.close()
        return True

    def add_password(self, service: str, username: str, password: str):
        # pievieno jaunu paroli
        if not self.cipher_suite:
            raise Exception("Paroļu pārvaldnieks ir slēgts")
        
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO passwords (service, username, encrypted_password) VALUES (?, ?, ?)",
            (service, username, encrypted_password.decode())
        )
        
        conn.commit()
        conn.close()

    def get_password(self, service: str, username: str) -> str:
        # nem paroli priekš specifiskā pakalpojuma un lietotājvārda
        if not self.cipher_suite:
            raise Exception("Paroļu pārvaldnieks ir slēgts")
        
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT encrypted_password FROM passwords WHERE service = ? AND username = ?",
            (service, username)
        )
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            raise Exception("Parole nav atrasta")
        
        encrypted_password = result[0]
        decrypted_password = self.cipher_suite.decrypt(encrypted_password.encode()).decode()
        
        conn.close()
        return decrypted_password

    def list_services(self) -> list:
        # norāda visus glabātos pakalpojumus un lietotājvārdus
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT service, username FROM passwords")
        services = cursor.fetchall()
        
        conn.close()
        return services

def main():
    # mēģina importēt pyperclip, ja datorā tas nav instalēts tad to izprintē
    try:
        import pyperclip
    except ImportError:
        print("Pyperclip bibliotēka ir nepieciešama priekš kopēšanas funkcionalitātes")
        print("Lūdzu instalējat to izmantojot: pip install pyperclip")
        return

    pm = PasswordManager()
    
    # pārbauda vai master parolei vajag būt uzsāktai
    conn = sqlite3.connect(pm.database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM master_password")
    is_initialized = cursor.fetchone()[0] > 0
    conn.close()
    
    if not is_initialized:
        print("Inicializējiet savu paroļu pārvaldnieku:")
        master_password = getpass.getpass("Izveidojiet master paroli: ")
        confirm_password = getpass.getpass("Apstipriniet galveno paroli: ")
        
        if master_password != confirm_password:
            print("Paroles nesakrīt")
            return
        
        pm.initialize_master_password(master_password)
        print("Master parole veiksmīgi inicializēta!")
    
    # galvenais loops, ieņem user ievadus
    while True:
        if not pm.cipher_suite:
            master_password = getpass.getpass("Ievadiet master paroli: ")
            if not pm.unlock(master_password):
                print("Nederīga master parole!")
                continue
        
        print("\n1. Pievienot paroli")
        print("2. Dabūt paroli")
        print("3. Izveidot drošu paroli")
        print("4. Norādīt glabātos datus")
        print("5. Iziet")
        
        choice = input("\nIzvēlies opciju: ")
        
        try:
            if choice == "1":
                service = input("\nPakalpojums: ")
                username = input("Lietotājvārds: ")
                use_generated = input("Izmantot drošu paroli? (y/n): ").lower() == 'y'
                
                if use_generated:
                    length = int(input("Password length (minimum 8): "))
                    password = pm.generate_password(length)
                    print(f"Izveidotā parole: {password}")
                    print("Parole tika nokopēta!")
                else:
                    password = getpass.getpass("Parole: ")
                
                pm.add_password(service, username, password)
                print("Parole tika pievienota!")
            
            elif choice == "2":
                service = input("\nPakalpojums: ")
                username = input("Lietotajvards: ")
                password = pm.get_password(service, username)
                pyperclip.copy(password)
                print(f"Parole: {password}")
                print("Parole tika nokopēta!")
            
            elif choice == "3":
                length = int(input("Paroles garums (minimums 8): "))
                password = pm.generate_password(length)
                print(f"Izveidotā parole: {password}")
                print("Parole tika nokopēta!")
            
            elif choice == "4":
                services = pm.list_services()
                print("\nGlabātie dati:")
                for service, username in services:
                    print(f"Pakalpojums: {service}, Lietotājvārds: {username}")
            
            elif choice == "5":
                print("Uz redzēšanos!")
                break
            
            else:
                print("Nederīga opcija!")

        # ja kaut kas gāja greizi tad izprintēt kas notikās
        except Exception as e:
            print(f"Kļūda: {e}")

# lai šo var izmantot citās programmās
if __name__ == "__main__":
    main()