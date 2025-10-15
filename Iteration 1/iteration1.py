import tkinter as tk
from tkinter import messagebox
from order_gui import place_order_gui

# -------------------- CLASSES --------------------
class MenuItem:
    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price


class TakeawayApp:
    def __init__(self):
        self.menu = [
            MenuItem(1, "Burger", 8.50),
            MenuItem(2, "Pizza", 12.00),
            MenuItem(3, "Fries", 4.00),
            MenuItem(4, "Soda", 2.50)
        ]
        self.order = []
        self.total_cost = 0.0

    def add_to_order(self, item_id, quantity):
        for item in self.menu:
            if item.item_id == item_id:
                cost = item.price * quantity
                self.order.append((item.name, quantity, cost))
                self.total_cost += cost
                return True
        return False

    def get_order_summary(self):
        if not self.order:
            return "No items ordered yet."
        summary = ""
        for name, qty, cost in self.order:
            summary += f"{qty} x {name} - ${cost:.2f}\n"
        summary += f"\nTotal cost: ${self.total_cost:.2f}"
        return summary


# -------------------- SIGNUP --------------------
import tkinter as tk
from tkinter import messagebox

def signup():
    # Signup screen: allows new users to register with username, password, and age check.
    window = tk.Tk()
    window.title("Signup")

    # Input fields
    tk.Label(window, text="Enter username: ").grid(row=0, column=0)
    username_entry = tk.Entry(window)
    username_entry.grid(row=0, column=1)

    tk.Label(window, text="Enter password: ").grid(row=1, column=0)
    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=1, column=1)

    tk.Label(window, text="Enter age: ").grid(row=2, column=0)
    age_entry = tk.Entry(window)
    age_entry.grid(row=2, column=1)

    def submit():
        """Validate username, password, and age before saving."""
        username = username_entry.get()
        password = password_entry.get()
        age = age_entry.get()

        # --- Username validation ---
        if len(username) < 6:
            messagebox.showerror("Signup Error", "Username must be at least 6 characters long.")
            return

        # --- Password validation ---
        if len(password) < 6:
            messagebox.showerror("Signup Error", "Password must be at least 6 characters long.")
            return

        # --- Age validation ---
        try:
            age = int(age)
            if age < 13:
                messagebox.showerror("Signup Error", "You must be at least 13 years old.")
                return
        except ValueError:
            messagebox.showerror("Signup Error", "Invalid age input.")
            return

        # --- Save user to file ---
        with open("users.txt", "a") as users_file:
            users_file.write(f"{username},{password}\n")

        messagebox.showinfo("Signup", "Signup successful!")
        window.destroy()

    tk.Button(window, text="Submit", command=submit).grid(row=3, column=0, columnspan=2)
    window.mainloop()


# -------------------- LOGIN --------------------
def login(app):
    window = tk.Tk()
    window.title("Login")

    tk.Label(window, text='Username:').grid(row=0, column=0)
    username_entry = tk.Entry(window)
    username_entry.grid(row=0, column=1)

    tk.Label(window, text='Password:').grid(row=1, column=0)
    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=1, column=1)

    def submit():
        username = username_entry.get()
        password = password_entry.get()
        valid_login = False
        
        try:
            with open("users.txt", "r") as users_file:
                for line in users_file:
                    parts = line.strip().split(',')
                    if len(parts) != 2:
                        continue
                    stored_username, stored_password = parts
                    if username == stored_username and password == stored_password:
                        valid_login = True
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "No user file found. Please sign up first.")
            window.destroy()
            return

        if valid_login:
            messagebox.showinfo("Login", "Login successful!")
            window.destroy()
            place_order_gui(app)
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    tk.Button(window, text="Submit", command=submit).grid(row=2, column=0, columnspan=2)
    window.mainloop() #explain


# -------------------- MAIN HOME SCREEN --------------------
def main():
    app = TakeawayApp()

    window = tk.Tk()
    window.title("Welcome")
    window.geometry('600x400')

    try:
        bg = tk.PhotoImage(file="images/takeawaybg.png")
        window.bg = bg
        background_label = tk.Label(window, image=bg)
        background_label.place(relwidth=1, relheight=1)

    except:
        pass

    frame = tk.Frame(window, padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    tk.Button(frame, text="Signup", command=signup).grid(row=0, column=0, padx=10)
    tk.Button(frame, text="Login", command=lambda: login(app)).grid(row=0, column=1, padx=10)

    window.mainloop()


if __name__ == "__main__":
    main()

