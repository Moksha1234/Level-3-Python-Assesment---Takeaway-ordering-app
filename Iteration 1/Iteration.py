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

    def display_menu(self):
        print("\n--- MENU ---")
        for item in self.menu:
            print(f"{item.item_id}. {item.name} - ${item.price:.2f}")

    def add_to_order(self, item_id, quantity):
        for item in self.menu:
            if item.item_id == item_id:
                cost = item.price * quantity
                self.order.append((item.name, quantity, cost))
                self.total_cost += cost
                print(f"Added {quantity} x {item.name} to your order.")
                return True
        print("Invalid item number.")
        return False

    def view_order(self):
        print("\n--- YOUR ORDER ---")
        if not self.order:
            print("No items ordered yet.")
        else:
            for name, qty, cost in self.order:
                print(f"{qty} x {name} - ${cost:.2f}")
            print(f"Total cost: ${self.total_cost:.2f}")
menu = TakeawayApp()

while True:
    menu.display_menu()
    choice = input("\nChoose an option: (a)dd item, (v)iew order, (q)uit: ").lower()
    
    if choice == "a":
        try:
            item_number = int(input("Enter item number: "))
            quantity = int(input("Enter quantity: "))
            menu.add_to_order(item_number, quantity)
        except ValueError:
            print("Please enter valid numbers.")
    elif choice == "v":
        menu.view_order()
    elif choice == "q":
        print("Thanks for ordering! Final order:")
        menu.view_order()
        break
    else:
        print("Invalid choice. Please try again.")
