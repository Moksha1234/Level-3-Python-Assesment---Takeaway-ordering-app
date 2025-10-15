import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import csv
from datetime import datetime



def place_order_gui(app):
    window = tk.Toplevel()
    window.title("Place Order")
    window.geometry("850x500")

    selected_item = {"item": None}
    delivery_option = tk.StringVar(value="Takeaway")
    # make the order summary auto-update when delivery option changes
    delivery_option.trace_add("write", lambda *args: update_order_display())

    # ---------------- FUNCTIONS ----------------
    #  Handles what happens when a menu item is selected:
    #  - Stores the selected item
     # - Displays the name, price, and image
    
    
    def select_item(item):  
        selected_item["item"] = item
        selected_label.config(text=f"{item.name} (${item.price:.2f})")

        try:
            if item.image_path:
                img = Image.open(item.image_path)
            else:
                img = Image.open("images/no_image.png")

            img = img.resize((200, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo, text="", width=200, height=150)
            image_label.image = photo
        except Exception:
            image_label.config(image="", text="No Image", width=200, height=150)

    def add_item_to_order():      #Adds the currently selected item to the order with the specified quantity.
        item = selected_item["item"]
        if not item:
            messagebox.showwarning("No Selection", "Please select an item first.")  # If no item is selected, show a warning and exit the function
            return

        try:
            qty = int(qty_entry.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Quantity", "Please enter a positive quantity.") # If qty is not a positive integer, show error and exit function
            return

        # Global quantity check
        current_qty = app.get_item_quantity(item.item_id)
        total_qty = current_qty + qty
        if total_qty > 10:
            messagebox.showwarning("Quantity Limit", f"You can only order a maximum of 10 {item.name}.") # error message if total qty exceeds 10
            return

        app.add_to_order(item.item_id, qty)
        qty_entry.delete(0, tk.END)
        update_order_display()

    def update_order_display():             #Refreshes the order summary display and updates cost labels.
        for widget in order_list_frame.winfo_children():
            widget.destroy()
        # Display placeholder if no items ordered
        if not app.order:
            tk.Label(order_list_frame, text="No items ordered yet.", fg="black", bg="lightgrey").pack(anchor="w")
        else:
            for name, qty, cost in app.order:
                row = tk.Frame(order_list_frame, bg="lightgrey")
                row.pack(fill="x", pady=2)  # Small vertical padding between items

                tk.Label(row, text=f"{qty} x {name} - ${cost:.2f}", bg="lightgrey").pack(side="left")

                # "+" button (capped at 10)
                tk.Button(
                    row,
                    text="+",
                    highlightbackground="lightgrey",
                    command=lambda n=name, q=qty: (
                        app.update_item_quantity(n, min(q + 1, 10)), update_order_display()  # the "min" function chooses the smaller value therefore capping qty at 10.
                    ) #lambda to capture current name and qty only when clicked. 
                ).pack(side="right", padx=2)

                # "-" button (auto-remove at 0)
                tk.Button(
                    row,
                    text="-",
                    highlightbackground="lightgrey",
                    command=lambda n=name, q=qty: (
                        app.update_item_quantity(n, max(q - 1, 0)), update_order_display() #the "max" module chooses the larger value therefore  qty at 10.
                    )
                ).pack(side="right", padx=2)

        subtotal = app.total_cost 
        delivery_cost = 5.00 if delivery_option.get() == "Delivery" else 0.00
        total = subtotal + delivery_cost

        subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
        delivery_label.config(text=f"Delivery: ${delivery_cost:.2f}")
        total_label.config(text=f"Total: ${total:.2f}")

    def submit_order():            #Finalizes the order, saves to CSV, and shows confirmation.
        if not app.order:
            messagebox.showwarning("No Order", "You haven't added anything to your order.")      # If no items in order, show warning and exit function
            return

        subtotal = app.total_cost
        delivery_cost = 5.00 if delivery_option.get() == "Delivery" else 0.00            # Delivery fee is $5 if delivery selected, otherwise $0
        total = subtotal + delivery_cost                     

        # Format the order summary for the messagebox
        summary = app.get_order_summary()
        summary += f"\nDelivery: ${delivery_cost:.2f}\nTotal: ${total:.2f}"

        # --- CSV Saving Logic ---
        order_items = "; ".join([f"{qty}x {name}" for name, qty, cost in app.order])           
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")                # Current date and time
        csv_data = [order_time, order_items, f"{subtotal:.2f}", f"{delivery_cost:.2f}", f"{total:.2f}"] # Data row to write to CSV

        # Write to CSV (creates if doesn't exist)
        try:
            with open("orders.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # Write header if file is empty
                if file.tell() == 0:
                    writer.writerow(["Date", "Items Ordered", "Subtotal", "Delivery", "Total"])
                writer.writerow(csv_data)
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save order to CSV:\n{e}")
            return

        messagebox.showinfo("Order Confirmation", f"Your order has been placed!\n\n{summary}") # Show confirmation with order summary


    # -------------------- BANNER FRAME --------------------
    banner_frame = tk.Frame(window, bg="#d13f5c", height=60)
    banner_frame.pack(fill="x", side="top")
    banner_frame.pack_propagate(False)      # Prevent frame from resizing to fit contents

    tk.Label(
        banner_frame,
        text="Place Your Order",
        bg="#d13f5c",
        fg="black",
        font=("Arial", 16)
    ).pack(side="left", padx=20)       

    tk.Radiobutton(
        banner_frame, text="Delivery",
        variable=delivery_option, value="Delivery",
        bg="lightgrey",
        fg="black",
    ).pack(side="right", padx=10)

    tk.Radiobutton(
        banner_frame, text="Takeaway",
        variable=delivery_option, value="Takeaway",
        bg="lightgrey",
        fg="black",
    ).pack(side="right", padx=10)

       # -------------------- MAIN CONTAINER --------------------
    # Create the main container frame that holds all sections (menu + order summary)
    main_frame = tk.Frame(window)
    main_frame.pack(fill="both", expand=True)

    # -------- Left: Menu Frame --------
    menu_frame = tk.Frame(main_frame, bg="beige", width=250, relief="solid", borderwidth=1)
    menu_frame.pack(side="left", fill="both", expand=True)
    menu_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

    # Title label for the menu section
    tk.Label(menu_frame, text="Menu", fg="black", font=("Arial", 14, "bold"), bg="beige").pack(pady=5)

    # Dropdown (combobox) to select a food category 
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(
        menu_frame,
        textvariable=category_var,
        values=list(app.menu.keys()),  # Shows all category names from the app's menu dictionary
        state="readonly"               # Makes it read-only (users cant type into the box)
    )
    category_dropdown.current(0)      # Sets the default selected category to the first one
    category_dropdown.pack(pady=5, padx=10, fill="x")

    # seperate frame to hold the list of menu item buttons for the selected category
    menu_items_frame = tk.Frame(menu_frame, bg="beige") 
    menu_items_frame.pack(fill="both", expand=True)

    # Function that displays the items for the currently selected category
    def show_category(event=None):   
        selected_category = category_dropdown.get()  # Get which category was selected
        items = app.menu[selected_category]          # Fetch list of MenuItem objects in that category
        
        # Clear existing item buttons (so it refreshes when user changes category)
        for widget in menu_items_frame.winfo_children():
            widget.destroy()

        # Create a button for each item in the selected category
        for item in items:
            btn = tk.Button(
                menu_items_frame,
                text=f"{item.name} - ${item.price:.2f}",  # Display name and formatted price
                fg="black",
                highlightthickness=5,     # Makes button edges more visible
                highlightbackground="beige",  # beige border color will blend into the frame
                command=lambda i=item: select_item(i)  # When clicked, item is selected 
            )
            btn.pack(pady=5, fill="x")   


    # When the user picks a new category from the dropdown, it runs the show_category() function
    # show_category() is called to refresh displayed items
    category_dropdown.bind("<<ComboboxSelected>>", show_category)        #.bind() binds the event of selecting a the combobox cateogry to the function

    show_category()


    # Middle: Display frame
    display_frame = tk.Frame(main_frame, bg="beige", width=300, relief="solid", borderwidth=1)
    display_frame.pack(side="left", fill="both", expand=True)
    display_frame.pack_propagate(False)

    image_label = tk.Label(display_frame, text="(Image here)", bg="darkgrey", width=25, height=10)
    image_label.pack(pady=20)

    bottom_frame = tk.Frame(display_frame, bg="beige")
    bottom_frame.pack(pady=10)

    tk.Label(bottom_frame, text="Selected:",fg="black", background="beige").grid(row=0, column=0, padx=5, pady=5)
    selected_label = tk.Label(bottom_frame, text="None",fg="black", background="beige")
    selected_label.grid(row=0, column=1)

    tk.Label(bottom_frame, text="Qty:",fg="black", bg="beige").grid(row=1, column=0, padx=5, pady=5)
    qty_entry = tk.Entry(bottom_frame, width=5)
    qty_entry.grid(row=1, column=1)

    tk.Button(display_frame, text="Add to Order", highlightbackground="beige", command=add_item_to_order).pack(pady=10)


    # Right: Order frame
    order_frame = tk.Frame(main_frame, bg="lightgrey", width=250, relief="solid", borderwidth=1)
    order_frame.pack(side="right", fill="y")
    order_frame.pack_propagate(False)

    tk.Label(order_frame, text="Order Summary", fg="black",  font=("Arial", 14), bg="lightgrey").pack(pady=10)

    order_list_frame = tk.Frame(order_frame, bg="lightgrey")
    order_list_frame.pack(fill="both", expand=True)

    subtotal_label = tk.Label(order_frame, text="Subtotal: $0.00",fg="black", bg="lightgrey")
    subtotal_label.pack(anchor="w", padx=10, pady=5)

    delivery_label = tk.Label(order_frame, text="Delivery: $0.00",fg="black",  bg="lightgrey")
    delivery_label.pack(anchor="w", padx=10, pady=5)

    total_label = tk.Label(order_frame, text="Total: $0.00",fg="black", bg="lightgrey")
    total_label.pack(anchor="w", padx=10, pady=5)

    # Create the "Submit Order" button inside the order frame
    submit_btn = tk.Button(
        order_frame,
        text="Submit Order!",
        command=submit_order,
        highlightbackground="lightgrey",
        fg="black",
        
    )
    submit_btn.pack(pady=15, fill="x", padx=10)

    update_order_display()
