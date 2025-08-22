import tkinter as tk
from tkinter import messagebox

def place_order_gui(app):
    window = tk.Tk()
    window.title("Place Order")
    window.geometry("850x500")

    selected_item = {"item": None}
    delivery_option = tk.StringVar(value="Takeaway")

    # ---------------- FUNCTIONS ----------------
    def select_item(item):
        selected_item["item"] = item
        selected_label.config(text=f"{item.name} (${item.price:.2f})")

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
            messagebox.showerror("Invalid Quantity", "Please enter a positive integer for quantity.")
            return

        app.add_to_order(item.item_id, qty)   # use class method
        qty_entry.delete(0, tk.END)
        update_order_display()

    def update_order_display():
        # Clear old labels
        for widget in order_list_frame.winfo_children():
            widget.destroy()

        # Use class method for summary
        summary_text = app.get_order_summary()
        tk.Label(order_list_frame, text=summary_text, bg="lightgrey", justify="left").pack(anchor="w")

        # Totals
        subtotal = app.total_cost
        delivery_cost = 5.00 if delivery_option.get() == "Delivery" else 0.00
        total = subtotal + delivery_cost

        subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
        delivery_label.config(text=f"Delivery: ${delivery_cost:.2f}")
        total_label.config(text=f"Total: ${total:.2f}")

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

    tk.Label(banner_frame, text="Place Your Order", bg="lightgrey", font=("Arial", 16)).pack(side="left", padx=20)
    tk.Radiobutton(banner_frame, text="Delivery", variable=delivery_option, value="Delivery", bg="lightgrey").pack(side="right", padx=10)
    tk.Radiobutton(banner_frame, text="Takeaway", variable=delivery_option, value="Takeaway", bg="lightgrey").pack(side="right", padx=10)


    # -------------------- MAIN CONTAINER --------------------
    main_frame = tk.Frame(window)
    main_frame.pack(fill="both", expand=True)

    # Left: Menu frame
    menu_frame = tk.Frame(main_frame, bg="white", width=250, relief="solid", borderwidth=1)
    menu_frame.pack(side="left", fill="y")
    menu_frame.pack_propagate(False)

    tk.Label(menu_frame, text="Menu", font=("Arial", 14), bg="white").pack(pady=10)

    for item in app.menu:
        row = tk.Frame(menu_frame, bg="white")
        row.pack(fill="x", padx=10, pady=2)

        tk.Button(row, text=item.name, width=15, 
                  command=lambda i=item: select_item(i)).pack(side="left")
        tk.Label(row, text=f"${item.price:.2f}", bg="white").pack(side="right")

    # Middle: Display frame
    display_frame = tk.Frame(main_frame, bg="lightgrey", width=300, relief="solid", borderwidth=1)
    display_frame.pack(side="left", fill="both", expand=True)
    display_frame.pack_propagate(False)

    image_label = tk.Label(display_frame, text="(Image here)", bg="darkgrey", width=25, height=10)
    image_label.pack(pady=20)

    # Selected + qty
    bottom_frame = tk.Frame(display_frame, bg="lightgrey")
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

    # Totals
    subtotal_label = tk.Label(order_frame, text="Subtotal: $0.00", bg="lightgrey")
    subtotal_label.pack(anchor="w", padx=10, pady=5)

    delivery_label = tk.Label(order_frame, text="Delivery: $0.00", bg="lightgrey")
    delivery_label.pack(anchor="w", padx=10, pady=5)

    total_label = tk.Label(order_frame, text="Total: $0.00", bg="lightgrey")
    total_label.pack(anchor="w", padx=10, pady=5)

    # --- Submit button ---
    submit_btn = tk.Button(
        order_frame,
        text="Submit Order!",
        command=submit_order,
        bg="#2e7d32",         # dark green
        fg="black",           # black text
        activebackground="#1b5e20",  # darker when clicked
        activeforeground="white",
        font=("Arial", 12, "bold")
    )
    submit_btn.pack(pady=15, fill="x", padx=10)

    update_order_display()  # initial display
    window.mainloop()
