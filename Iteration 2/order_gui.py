import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


def place_order_gui(app):
    window = tk.Toplevel()
    window.title("Place Order")
    window.geometry("850x500")

    selected_item = {"item": None}
    delivery_option = tk.StringVar(value="Takeaway")

    # ---------------- FUNCTIONS ----------------
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

    def add_item_to_order():
        item = selected_item["item"]
        if not item:
            messagebox.showwarning("No Selection", "Please select an item first.")
            return

        try:
            qty = int(qty_entry.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Quantity", "Please enter a quantity greater than 0.")
            return

        # Check current quantity in order to enforce max 10
        current_qty = app.get_item_quantity(item.item_id)
        if current_qty + qty > 10:
            messagebox.showerror("Quantity Limit", "You can only order up to 10 of this item in total.")
            return

        app.add_to_order(item.item_id, qty)
        qty_entry.delete(0, tk.END)
        update_order_display()

    def update_order_display():
        for widget in order_list_frame.winfo_children():
            widget.destroy()

        if not app.order:
            tk.Label(order_list_frame, text="No items ordered yet.", bg="lightgrey").pack(anchor="w")
        else:
            for name, qty, cost in app.order:
                row = tk.Frame(order_list_frame, bg="lightgrey")
                row.pack(fill="x", pady=2)

                tk.Label(row, text=f"{qty} x {name} - ${cost:.2f}", bg="lightgrey").pack(side="left")

                # "+" button
                tk.Button(
                    row,
                    text="+",
                    command=lambda n=name, q=qty: (increase_qty(n, q))
                ).pack(side="right", padx=2)

                # "-" button
                tk.Button(
                    row,
                    text="-",
                    command=lambda n=name, q=qty: (decrease_qty(n, q))
                ).pack(side="right", padx=2)

        subtotal = app.total_cost
        delivery_cost = 5.00 if delivery_option.get() == "Delivery" else 0.00
        total = subtotal + delivery_cost

        subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
        delivery_label.config(text=f"Delivery: ${delivery_cost:.2f}")
        total_label.config(text=f"Total: ${total:.2f}")

    def increase_qty(name, qty):
        item_id = app.get_item_id_by_name(name)
        if qty + 1 > 10:
            messagebox.showerror("Quantity Limit", "You can only order up to 10 of this item.")
            return
        app.update_item_quantity(name, qty + 1)
        update_order_display()

    def decrease_qty(name, qty):
        if qty - 1 <= 0:
            app.update_item_quantity(name, 0)  # automatically remove
        else:
            app.update_item_quantity(name, qty - 1)
        update_order_display()

    def submit_order():
        if not app.order:
            messagebox.showwarning("No Order", "You haven't added anything to your order.")
            return

        subtotal = app.total_cost
        delivery_cost = 5.00 if delivery_option.get() == "Delivery" else 0.00
        total = subtotal + delivery_cost

        summary = app.get_order_summary()
        summary += f"\nDelivery: ${delivery_cost:.2f}\nTotal: ${total:.2f}"

        messagebox.showinfo("Order Confirmation", f"Your order has been placed!\n\n{summary}")

    delivery_option.trace_add("write", lambda *args: update_order_display())

    # -------------------- BANNER FRAME --------------------
    banner_frame = tk.Frame(window, bg="lightgrey", height=60)
    banner_frame.pack(fill="x", side="top")
    banner_frame.pack_propagate(False)

    tk.Label(
        banner_frame,
        text="Place Your Order",
        bg="lightgrey",
        font=("Arial", 16)
    ).pack(side="left", padx=20)

    tk.Radiobutton(
        banner_frame, text="Delivery",
        variable=delivery_option, value="Delivery",
        bg="lightgrey"
    ).pack(side="right", padx=10)

    tk.Radiobutton(
        banner_frame, text="Takeaway",
        variable=delivery_option, value="Takeaway",
        bg="lightgrey"
    ).pack(side="right", padx=10)

    # -------------------- MAIN CONTAINER --------------------
    main_frame = tk.Frame(window)
    main_frame.pack(fill="both", expand=True)

    # Left: Menu frame
    menu_frame = tk.Frame(main_frame, bg="white", width=250, relief="solid", borderwidth=1)
    menu_frame.pack(side="left", fill="y")
    menu_frame.pack_propagate(False)

    tk.Label(menu_frame, text="Menu", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(
        menu_frame, textvariable=category_var,
        values=list(app.menu.keys()), state="readonly"
    )
    category_dropdown.current(0)
    category_dropdown.pack(pady=5, padx=10, fill="x")

    menu_items_frame = tk.Frame(menu_frame, bg="white")
    menu_items_frame.pack(fill="both", expand=True)

    def show_category(event=None):
        selected_category = category_dropdown.get()
        items = app.menu[selected_category]
        for widget in menu_items_frame.winfo_children():
            widget.destroy()
        for item in items:
            btn = tk.Button(
                menu_items_frame,
                text=f"{item.name} - ${item.price:.2f}",
                command=lambda i=item: select_item(i)
            )
            btn.pack(pady=2, fill="x")

    category_dropdown.bind("<<ComboboxSelected>>", show_category)
    show_category()

    # Middle: Display frame
    display_frame = tk.Frame(main_frame, bg="white", width=300, relief="solid", borderwidth=1)
    display_frame.pack(side="left", fill="both", expand=True)
    display_frame.pack_propagate(False)

    image_label = tk.Label(display_frame, text="(Image here)", bg="darkgrey", width=25, height=10)
    image_label.pack(pady=20)

    bottom_frame = tk.Frame(display_frame, bg="white")
    bottom_frame.pack(pady=10)

    tk.Label(bottom_frame, text="Selected:").grid(row=0, column=0, padx=5, pady=5)
    selected_label = tk.Label(bottom_frame, text="None")
    selected_label.grid(row=0, column=1)

    tk.Label(bottom_frame, text="Qty:").grid(row=1, column=0, padx=5, pady=5)
    qty_entry = tk.Entry(bottom_frame, width=5)
    qty_entry.grid(row=1, column=1)

    tk.Button(display_frame, text="Add to Order", command=add_item_to_order).pack(pady=15)

    # Right: Order frame
    order_frame = tk.Frame(main_frame, bg="lightgrey", width=250, relief="solid", borderwidth=1)
    order_frame.pack(side="right", fill="y")
    order_frame.pack_propagate(False)

    tk.Label(order_frame, text="Order Summary", font=("Arial", 14), bg="lightgrey").pack(pady=10)

    order_list_frame = tk.Frame(order_frame, bg="lightgrey")
    order_list_frame.pack(fill="both", expand=True)

    subtotal_label = tk.Label(order_frame, text="Subtotal: $0.00", bg="lightgrey")
    subtotal_label.pack(anchor="w", padx=10, pady=5)

    delivery_label = tk.Label(order_frame, text="Delivery: $0.00", bg="lightgrey")
    delivery_label.pack(anchor="w", padx=10, pady=5)

    total_label = tk.Label(order_frame, text="Total: $0.00", bg="lightgrey")
    total_label.pack(anchor="w", padx=10, pady=5)

    submit_btn = tk.Button(
        order_frame,
        text="Submit Order!",
        command=submit_order,
        fg="black",
        font=("Arial", 12, "bold")
    )
    submit_btn.pack(pady=15, fill="x", padx=10)

    update_order_display()
