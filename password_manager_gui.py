import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
import pyperclip
import importlib.util
import sys
import os
import sqlite3

# Importēt module
spec = importlib.util.spec_from_file_location("password_manager", "backend.py")
password_manager = importlib.util.module_from_spec(spec)
sys.modules["password_manager"] = password_manager
spec.loader.exec_module(password_manager)
PasswordManager = password_manager.PasswordManager

class PasswordManagerGUI:
    # Inicializēt mainīgos un funkcijas
    def __init__(self, root):
        self.root = root
        self.root.title("Paroļu Pārvaldnieks")
        self.root.geometry("500x400")
        self.pm = PasswordManager()
        self.create_widgets()
        self.check_master_password()

    def create_widgets(self):
        # Galvenā notebook priekš lietiņām
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Pievienot tabus
        self.add_password_frame = ttk.Frame(self.notebook)
        self.get_password_frame = ttk.Frame(self.notebook)
        self.generate_password_frame = ttk.Frame(self.notebook)
        self.list_services_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.add_password_frame, text='Pievienot Paroli')
        self.notebook.add(self.get_password_frame, text='Iegūt Paroli')
        self.notebook.add(self.generate_password_frame, text='Ģenerēt Paroli')
        self.notebook.add(self.list_services_frame, text='Pakalpojumu Saraksts')

        # Pievienot paroles tabu
        ttk.Label(self.add_password_frame, text="Pakalpojums:").grid(row=0, column=0, padx=5, pady=5)
        self.add_service_entry = ttk.Entry(self.add_password_frame)
        self.add_service_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_password_frame, text="Lietotājvārds:").grid(row=1, column=0, padx=5, pady=5)
        self.add_username_entry = ttk.Entry(self.add_password_frame)
        self.add_username_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_password_frame, text="Parole:").grid(row=2, column=0, padx=5, pady=5)
        self.add_password_entry = ttk.Entry(self.add_password_frame, show="*")
        self.add_password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.use_generated_var = tk.BooleanVar()
        ttk.Checkbutton(self.add_password_frame, text="Izmantot Ģenerētu Paroli", 
                       variable=self.use_generated_var, 
                       command=self.toggle_password_entry).grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Button(self.add_password_frame, text="Pievienot Paroli", 
                  command=self.add_password).grid(row=4, column=0, columnspan=2, pady=10)

        # Iegūt paroles tabu
        ttk.Label(self.get_password_frame, text="Pakalpojums:").grid(row=0, column=0, padx=5, pady=5)
        self.get_service_entry = ttk.Entry(self.get_password_frame)
        self.get_service_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.get_password_frame, text="Lietotājvārds:").grid(row=1, column=0, padx=5, pady=5)
        self.get_username_entry = ttk.Entry(self.get_password_frame)
        self.get_username_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.get_password_frame, text="Iegūt Paroli", 
                  command=self.get_password).grid(row=2, column=0, columnspan=2, pady=10)

        # Ģenerēt paroles tabu
        ttk.Label(self.generate_password_frame, text="Paroles Garums:").grid(row=0, column=0, padx=5, pady=5)
        self.length_entry = ttk.Entry(self.generate_password_frame)
        self.length_entry.insert(0, "16")
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.generate_password_frame, text="Ģenerēt Paroli", 
                  command=self.generate_password).grid(row=1, column=0, columnspan=2, pady=10)

        self.generated_password_var = tk.StringVar()
        ttk.Label(self.generate_password_frame, textvariable=self.generated_password_var).grid(
            row=2, column=0, columnspan=2, pady=5)

        # Rādīt pakalpojumu tabu
        self.services_tree = ttk.Treeview(self.list_services_frame, columns=('Pakalpojums', 'Lietotājvārds'), 
                                        show='headings')
        self.services_tree.heading('Pakalpojums', text='Pakalpojums')
        self.services_tree.heading('Lietotājvārds', text='Lietotājvārds')
        self.services_tree.pack(expand=True, fill='both', padx=5, pady=5)

        ttk.Button(self.list_services_frame, text="Atjaunot Sarakstu", 
                  command=self.update_services_list).pack(pady=5)

    def check_master_password(self):
        conn = sqlite3.connect(self.pm.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM master_password")
        is_initialized = cursor.fetchone()[0] > 0
        conn.close()

        if not is_initialized:
            self.initialize_master_password_dialog()
        else:
            self.master_password_dialog()

    def initialize_master_password_dialog(self):
        # izveido dialogu master paroles ievadisanai
        dialog = tk.Toplevel(self.root)
        dialog.title("Inicializēt Galveno Paroli")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # paroles ievades lauki
        ttk.Label(dialog, text="Izveidot Galveno Paroli:").pack(pady=10)
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.pack(pady=5)

        ttk.Label(dialog, text="Apstiprināt Galveno Paroli:").pack(pady=10)
        confirm_entry = ttk.Entry(dialog, show="*")
        confirm_entry.pack(pady=5)

        def submit():
            # parbauda vai paroles sakrit un nav tuksas
            password = password_entry.get()
            confirm = confirm_entry.get()
            
            if not password:
                messagebox.showerror("Kļūda", "Parole nevar būt tukša!")
                return
                
            if password != confirm:
                messagebox.showerror("Kļūda", "Paroles nesakrīt!")
                return

            try:
                self.pm.initialize_master_password(password)
                messagebox.showinfo("Veiksmīgi", "Galvenā parole veiksmīgi inicializēta!")
                dialog.destroy()
                self.update_services_list()
            except Exception as e:
                messagebox.showerror("Kļūda", str(e))

        ttk.Button(dialog, text="Apstiprināt", command=submit).pack(pady=10)
        dialog.protocol("WM_DELETE_WINDOW", lambda: None)

    def master_password_dialog(self):
        # izveido dialogu master paroles ievadei
        dialog = tk.Toplevel(self.root)
        dialog.title("Galvenā Parole")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Ievadiet Galveno Paroli:").pack(pady=10)
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.pack(pady=5)

        def submit():
            # parbauda vai ievadita parole ir pareiza vai nav
            if self.pm.unlock(password_entry.get()):
                dialog.destroy()
                self.update_services_list()
            else:
                messagebox.showerror("Kļūda", "Nepareiza galvenā parole!")

        ttk.Button(dialog, text="Apstiprināt", command=submit).pack(pady=10)
        dialog.protocol("WM_DELETE_WINDOW", lambda: None)

    def toggle_password_entry(self):
        # parsledz paroles ievades lauka stavokli vai var ievadit vai nevar
        if self.use_generated_var.get():
            self.add_password_entry.configure(state='disabled')
        else:
            self.add_password_entry.configure(state='normal')

    def add_password(self):
        # pievieno jaunu paroli sistemai, var manuali ievadit vai automatiski generetu izmantot
        service = self.add_service_entry.get()
        username = self.add_username_entry.get()
        
        if self.use_generated_var.get():
            password = self.pm.generate_password(16)
            messagebox.showinfo("Veiksmīgi", f"Ģenerētā parole: {password}\nParole nokopēta starpliktuvē!")
        else:
            password = self.add_password_entry.get()

        try:
            self.pm.add_password(service, username, password)
            messagebox.showinfo("Veiksmīgi", "Parole veiksmīgi pievienota!")
            self.update_services_list()
            self.clear_add_entries()
        except Exception as e:
            messagebox.showerror("Kļūda", str(e))

    def get_password(self):
        # genere jaunu paroli un nokope vinu
        try:
            password = self.pm.get_password(
                self.get_service_entry.get(),
                self.get_username_entry.get()
            )
            pyperclip.copy(password)
            messagebox.showinfo("Veiksmīgi", f"Parole: {password}\nNokopēta starpliktuvē!")
        except Exception as e:
            messagebox.showerror("Kļūda", str(e))

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            password = self.pm.generate_password(length)
            self.generated_password_var.set(f"Ģenerētā Parole: {password}")
            pyperclip.copy(password)
            messagebox.showinfo("Veiksmīgi", "Parole nokopēta starpliktuvē!")
        except ValueError:
            messagebox.showerror("Kļūda", "Lūdzu ievadiet derīgu skaitli paroles garumam")
        except Exception as e:
            messagebox.showerror("Kļūda", str(e))

    def update_services_list(self):
        # notira sarakstu kas pagaidam ir
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)
        
        # ievieto jaunos datus
        services = self.pm.list_services()
        for service, username in services:
            self.services_tree.insert('', 'end', values=(service, username))

    def clear_add_entries(self):
        # notīra visus ievades laukus pēc paroles pievienošanas
        self.add_service_entry.delete(0, 'end')
        self.add_username_entry.delete(0, 'end')
        self.add_password_entry.delete(0, 'end')

def main():
    # izveido galveno logu un palaiž lietotāju ievadu pieņemšanu
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()