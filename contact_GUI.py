import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

CONTACTS_FILE = "contacts.json"

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📒 Contact Book")
        self.root.geometry("500x500")

        self.contacts = self.load_contacts()

        # Entry Fields
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # Entry Frame
        entry_frame = tk.Frame(root)
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Name").grid(row=0, column=0, sticky="w")
        tk.Entry(entry_frame, textvariable=self.name_var, width=30).grid(row=0, column=1)

        tk.Label(entry_frame, text="Phone no.").grid(row=1, column=0, sticky="w")
        tk.Entry(entry_frame, textvariable=self.phone_var, width=30).grid(row=1, column=1)

        tk.Label(entry_frame, text="E-mail").grid(row=2, column=0, sticky="w")
        tk.Entry(entry_frame, textvariable=self.email_var, width=30).grid(row=2, column=1)

        tk.Label(entry_frame, text="Address").grid(row=3, column=0, sticky="w")
        tk.Entry(entry_frame, textvariable=self.address_var, width=30).grid(row=3, column=1)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Contact", command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Contact", command=self.update_contact).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Contact", command=self.delete_contact).grid(row=0, column=2, padx=5)

        # Search Field
        tk.Label(root, text="🔍Search by Name or Phone no.").pack()
        tk.Entry(root, textvariable=self.search_var, width=40).pack(pady=5)
        tk.Button(root, text="🔍 Search", command=self.search_contact).pack()

        # Listbox to show contacts
        self.listbox = tk.Listbox(root, width=60, height=15)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.refresh_contact_list()

    def load_contacts(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r") as f:
                return json.load(f)
        return []

    def save_contacts(self):
        with open(CONTACTS_FILE, "w") as f:
            json.dump(self.contacts, f, indent=4)

    def refresh_contact_list(self):
        self.listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")

    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Required", "Name and Phone are required.")
            return

        self.contacts.append({
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        })
        self.save_contacts()
        self.refresh_contact_list()
        self.clear_fields()
        messagebox.showinfo("Success", "Contact added successfully! 😊")

    def on_select(self, event):
        try:
            index = self.listbox.curselection()[0]
            selected = self.contacts[index]
            self.name_var.set(selected["name"])
            self.phone_var.set(selected["phone"])
            self.email_var.set(selected["email"])
            self.address_var.set(selected["address"])
        except IndexError:
            pass

    def update_contact(self):
        try:
            index = self.listbox.curselection()[0]
            self.contacts[index] = {
                "name": self.name_var.get().strip(),
                "phone": self.phone_var.get().strip(),
                "email": self.email_var.get().strip(),
                "address": self.address_var.get().strip()
            }
            self.save_contacts()
            self.refresh_contact_list()
            self.clear_fields()
            messagebox.showinfo("Updated", "Contact updated! 😊")
        except IndexError:
            messagebox.showwarning("No selection", "Select a contact to update.")

    def delete_contact(self):
        try:
            index = self.listbox.curselection()[0]
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?")
            if confirm:
                del self.contacts[index]
                self.save_contacts()
                self.refresh_contact_list()
                self.clear_fields()
        except IndexError:
            messagebox.showwarning("No selection", "Select a contact to delete.")

    def search_contact(self):
        query = self.search_var.get().strip().lower()
        results = [c for c in self.contacts if query in c["name"].lower() or query in c["phone"]]
        self.listbox.delete(0, tk.END)
        for contact in results:
            self.listbox.insert(tk.END, f"{contact['name']} - {contact['phone']} (Phone No.)")


# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
