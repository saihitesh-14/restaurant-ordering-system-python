import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

# Load menu data from CSV
menu_items = {}
with open('menu.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header
    for row in reader:
        name, price = row
        menu_items[name.strip()] = float(price.strip())

# Global order dictionary
current_order = {}

# Add item to current order
def add_to_order(item):
    if item in current_order:
        current_order[item] += 1
    else:
        current_order[item] = 1
    update_order_display()
# Update the order display and total
def update_order_display():
    order_text.delete(1.0, tk.END)
    total = 0
    for item, quantity in current_order.items():
        price = menu_items[item]
        line_total = price * quantity
        order_text.insert(tk.END, f"{item} x{quantity} - ₹{line_total:.2f}\n")
        total += line_total
    order_text.insert(tk.END, f"\nTotal: ₹{total:.2f}")

# Save order to a single file with timestamp
def save_order_to_file():
    table_no = table_entry.get().strip()
    if not table_no.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid table number.")
        return
    if not current_order:
        messagebox.showerror("Empty Order", "No items in the order.")
        return

    filename = "orders.txt"
    timestamp = datetime.now().strftime("%Y-%d-%m- %H:%M:%S")

    try:
        with open(filename, "a") as file:
            file.write(f"--- Order at {timestamp} ---\n")
            file.write(f"Table Number: {table_no}\n")
            total = 0
            for item, quantity in current_order.items():
                price = menu_items[item]
                subtotal = price * quantity
                file.write(f"{item} x{quantity} - ₹{subtotal:.2f}\n")
                total += subtotal
            file.write(f"Total: ₹{total:.2f}\n")
            file.write("-" * 30 + "\n\n")
        messagebox.showinfo("Saved", f"Order saved to {filename}")
        clear_order()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Clear current order
def clear_order():
    global current_order
    current_order = {}
    update_order_display()
    table_entry.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Restaurant Ordering System")

tk.Label(root, text="Table Number:").grid(row=0, column=0)
table_entry = tk.Entry(root)
table_entry.grid(row=0, column=1)

menu_frame = tk.Frame(root)
menu_frame.grid(row=1, column=0, columnspan=2, pady=10)

row = 0
col = 0
for item, price in menu_items.items():
    btn = tk.Button(menu_frame, text=f"{item} - ₹{price:.2f}", width=16, height=2, command=lambda i=item: add_to_order(i))
    btn.grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 3:
        col = 0
        row += 1

order_text = tk.Text(root, width=40, height=10)
order_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


# Centered button frame with larger buttons
button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, columnspan=2, pady=10)

save_btn = tk.Button(button_frame, text="Place Order", command=save_order_to_file, bg="green", fg="black", width=15, height=2)
save_btn.pack(side=tk.LEFT, padx=10)

clear_btn = tk.Button(button_frame, text="Clear", command=clear_order, bg="red", fg="black", width=15, height=2)
clear_btn.pack(side=tk.LEFT, padx=10)

root.mainloop()