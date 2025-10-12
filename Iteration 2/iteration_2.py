import tkinter as tk
from tkinter import messagebox
from order_gui import place_order_gui   

# -------------------- CLASSES --------------------
class MenuItem:
    #Represents a single menu item with ID, name, price, and optional image.
    def __init__(self, item_id, name, price, image_path=None):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.image_path = image_path

#Main application logic for managing menu, orders, and item quantities.
class TakeawayApp:
    def __init__(self):
        
        self.menu = {
            "Mains": [
                MenuItem(1, "Burger", 8.50, "images/burger.jpeg"),
                MenuItem(2, "Pizza", 12.00, "images/pizza.png"),
                MenuItem(3, "Pasta", 11.00, "images/pasta.png")
            ],
            "Sides": [
                MenuItem(4, "Fries", 4.00, "images/fries.png"),
                MenuItem(5, "Salad", 5.00, "images/salad.png"),
                MenuItem(6, "Garlic naan", 3.50, "images/garlic_naan.png")
            ],
            "Drinks": [
                MenuItem(7, "Cola", 2.50, "images/cola.png"),
                MenuItem(8, "O_Juice", 3.00, "images/o_juice.png"),
                MenuItem(9, "Lemonade", 3.50, "images/lemonade.png")
            ]
        }

        # Stores order as a list of tuples: (item_name, qty, total_cost)
        self.order = []
        self.total_cost = 0.0

        # Tracks how many of each item (by item_id) have been ordered
        self.item_quantities = {}

    def add_to_order(self, item_id, quantity):
        """Add an item to the order, enforcing max qty of 10 per item."""
        for category, items in self.menu.items():
            for item in items:
                if item.item_id == item_id:
                    current_qty = self.item_quantities.get(item_id, 0)
                    total_qty = current_qty + quantity

                    # Restrict max quantity of each item to 10
                    if total_qty > 10:
                        return False

                    self.item_quantities[item_id] = total_qty

                    
                    found = False
                    new_order = []
                    self.total_cost = 0.0
                    for name, qty, cost in self.order:
                        if name == item.name:
                            # Update existing item in order
                            qty += quantity
                            cost = qty * item.price
                            new_order.append((name, qty, cost))
                            found = True
                        else:
                            new_order.append((name, qty, cost))
                        self.total_cost += new_order[-1][2]

                    # If item not already in order, add new entry
                    if not found:
                        new_order.append((item.name, quantity, item.price * quantity))
                        self.total_cost += item.price * quantity

                    self.order = new_order
                    return True
        return False
#Update quantity of an existing item. Remove if new_qty=0.
    def update_item_quantity(self, item_name, new_qty):
        
        new_order = []
        self.total_cost = 0.0
        for name, qty, cost in self.order:
            if name == item_name:
                # Find item_id for updating item_quantities dict
                item_id = next(
                    (item.item_id for cat in self.menu.values() for item in cat if item.name == name),
                    None
                )
                if new_qty > 0:
                    # Update quantity + cost
                    unit_price = cost / qty
                    cost = unit_price * new_qty
                    new_order.append((name, new_qty, cost))
                    self.total_cost += cost
                    if item_id:
                        self.item_quantities[item_id] = new_qty
                else:
                    # If qty = 0, remove item completely
                    if item_id and item_id in self.item_quantities:
                        del self.item_quantities[item_id]
            else:
                new_order.append((name, qty, cost))
                self.total_cost += cost
        self.order = new_order

    def get_item_quantity(self, item_id):
        """Return the quantity of an item currently in the order."""
        return self.item_quantities.get(item_id, 0)

    def get_order_summary(self):
        """Return formatted order summary with all items + total cost."""
        if not self.order:
            return "No items ordered yet."
        summary = ""
        for name, qty, cost in self.order:
            summary += f"{qty} x {name} - ${cost:.2f}\n"
        summary += f"\nTotal cost: ${self.total_cost:.2f}"
        return summary


# -------------------- SIGNUP --------------------
def signup():
    """Signup screen: allows new users to register with username, password, and age check."""
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
        """Validate age + save user details to file."""
        username = username_entry.get()
        password = password_entry.get()
        age = age_entry.get()

        try:
            age = int(age)
            if age < 14:
                messagebox.showerror("Signup Error", "You must be at least 13 years old.")
                return
        except ValueError:
            messagebox.showerror("Signup Error", "Invalid age input.")
            return

        # Save user to text file
        with open("users.txt", "a") as users_file:
            users_file.write(f"{username},{password}\n")
        messagebox.showinfo("Signup", "Signup successful!")
        window.destroy()

    tk.Button(window, text="Submit", command=submit).grid(row=3, column=0, columnspan=2)
    window.mainloop()


# -------------------- LOGIN --------------------
def login(app):
    """Login screen: verifies credentials from users.txt and launches order GUI."""
    window = tk.Tk()
    window.title("Login")

    # Input fields
    tk.Label(window, text='Username:').grid(row=0, column=0)
    username_entry = tk.Entry(window)
    username_entry.grid(row=0, column=1)

    tk.Label(window, text='Password:').grid(row=1, column=0)
    password_entry = tk.Entry(window, show="*")
    password_entry.grid(row=1, column=1)

    def submit():
        """Check credentials against saved users."""
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
            place_order_gui(app)   # Open ordering GUI after successful login
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    tk.Button(window, text="Submit", command=submit).grid(row=2, column=0, columnspan=2)
    window.mainloop()


# -------------------- MAIN HOME SCREEN --------------------
def main():
    """Main app entry point: launches Welcome screen with Signup + Login options."""
    app = TakeawayApp()   

    window = tk.Tk()
    window.title("Welcome")
    window.geometry('600x400')

    # Set background image (optional, fails silently if not found)
    try:
        bg = tk.PhotoImage(file="images/takeawaybg.png")
        window.bg = bg
        background_label = tk.Label(window, image=bg)
        background_label.place(relwidth=1, relheight=1)
    except:
        pass

    # Center frame with buttons
    frame = tk.Frame(window, padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    # Signup + Login buttons
    tk.Button(frame, text="Signup", command=signup).grid(row=0, column=0, padx=10)
    tk.Button(frame, text="Login", command=lambda: login(app)).grid(row=0, column=1, padx=10)

    window.mainloop()


if __name__ == "__main__":
    main()
