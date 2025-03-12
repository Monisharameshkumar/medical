CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-------------------------
CREATE TABLE medicines (
    medicine_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
--------------------------------
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
--------------------------------------

CREATE TABLE order_details (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    medicine_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
);
-----------------------------------------------

import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Sample medicines menu
medicines = [
    {"name": "Paracetamol", "price": 5.00},
    {"name": "Aspirin", "price": 4.50},
    {"name": "Amoxicillin", "price": 10.00},
    {"name": "Ibuprofen", "price": 6.50},
    {"name": "Vitamin C", "price": 8.00},
]

# Global variables
user_name = None
user_email = None
order = []
total_price = 0.0

# Function to connect to the database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="medical"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

# Function to save user details to the database
def save_user_details(name, email):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (name, email)
        VALUES (%s, %s)
        ''', (name, email))
        conn.commit()
        conn.close()

# Home Page: To input user details
def home_page():
    global main_window
    main_window = tk.Tk()
    main_window.title("Medical Shop Billing System")
    main_window.configure(bg="#FFDDC1")

    tk.Label(main_window, text="Welcome to the Medical Shop", font=("Arial", 20), bg="#FFDDC1").pack(pady=10)

    tk.Label(main_window, text="Enter Your Name:", bg="#FFDDC1", font=("Arial", 12)).pack(pady=5)
    name_entry = tk.Entry(main_window, width=30, font=("Arial", 12))
    name_entry.pack(pady=5)

    tk.Label(main_window, text="Enter Your Email:", bg="#FFDDC1", font=("Arial", 12)).pack(pady=5)
    email_entry = tk.Entry(main_window, width=30, font=("Arial", 12))
    email_entry.pack(pady=5)

    def next_page():
        global user_name, user_email
        user_name = name_entry.get()
        user_email = email_entry.get()

        if not user_name or not user_email:
            messagebox.showerror("Input Error", "Both name and email must be provided.")
            return
       
        save_user_details(user_name, user_email)
       
        main_window.withdraw()
        menu_page()
   
    tk.Button(main_window, text="Next", command=next_page, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=10)

    main_window.mainloop()

# Menu Page: To display available medicines
def menu_page():
    global second_window
    second_window = tk.Toplevel()
    second_window.title("Select Medicines")
    second_window.configure(bg="#FFDDC1")

    tk.Label(second_window, text="Medicines Menu", font=("Arial", 16), bg="#FFDDC1").pack(pady=10)

    medicine_listbox = tk.Listbox(second_window, selectmode=tk.MULTIPLE, height=6, width=50, font=("Arial", 12))
    medicine_listbox.pack(pady=10)

    for med in medicines:
        medicine_listbox.insert(tk.END, f"{med['name']} - ${med['price']}")

    def add_to_order():
        global order, total_price
        selected_items = medicine_listbox.curselection()

        if not selected_items:
            messagebox.showerror("Selection Error", "Please select at least one medicine.")
            return

        order = []
        total_price = 0.0

        for item in selected_items:
            medicine = medicines[item]
            order.append(medicine)
            total_price += medicine['price']

        second_window.withdraw()
        confirmation_page()

    tk.Button(second_window, text="Add to Order", command=add_to_order, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=20)

    second_window.mainloop()

# Confirmation Page: To confirm order details
def confirmation_page():
    global third_window
    third_window = tk.Toplevel()
    third_window.title("Confirm Your Order")
    third_window.configure(bg="#FFDDC1")

    tk.Label(third_window, text="Order Confirmation", font=("Arial", 16), bg="#FFDDC1").pack(pady=10)

    if order:
        tk.Label(third_window, text="Your Order:", bg="#FFDDC1", font=("Arial", 12)).pack(pady=5)
        for medicine in order:
            tk.Label(third_window, text=f"{medicine['name']} - ${medicine['price']}", bg="#FFDDC1", font=("Arial", 12)).pack(pady=5)

        tk.Label(third_window, text=f"Total Price: ${total_price}", bg="#FFDDC1", font=("Arial", 14)).pack(pady=10)

    tk.Label(third_window, text=f"Name: {user_name}", bg="#FFDDC1", font=("Arial", 12)).pack(pady=5)
    tk.Label(third_window, text=f"Email: {user_email}", bg="#FFDDC1", font=("Arial", 12)).pack(pady=5)

    def confirm_order():
        messagebox.showinfo("Order Confirmed", f"Your order has been confirmed!\nTotal: ${total_price}")
        third_window.destroy()
        bill_page()

    tk.Button(third_window, text="Confirm Order", command=confirm_order, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=20)

    def back_to_menu():
        third_window.withdraw()
        menu_page()

    tk.Button(third_window, text="Modify Order", command=back_to_menu, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=5)

    third_window.mainloop()

# Bill Page: Display the final bill
def bill_page():
    global fourth_window
    fourth_window = tk.Toplevel()
    fourth_window.title("Bill")
    fourth_window.configure(bg="#FFDDC1")

    tk.Label(fourth_window, text="Final Bill", font=("Arial", 16), bg="#FFDDC1").pack(pady=10)

    if order:
        tk.Label(fourth_window, text="Your Medicines:", bg="#FFDDC1", font=("Arial", 12)).pack(pady=5)
        for medicine in order:
            tk.Label(fourth_window, text=f"{medicine['name']} - ${medicine['price']}", bg="#FFDDC1", font=("Arial", 12)).pack(pady=5)

        tk.Label(fourth_window, text=f"Total Price: ${total_price}", bg="#FFDDC1", font=("Arial", 14)).pack(pady=10)

    tk.Button(fourth_window, text="Exit", command=fourth_window.destroy, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=20)

    fourth_window.mainloop()

# Start the app by calling the home page
home_page()