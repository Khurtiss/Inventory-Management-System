import tkinter as tk
from tkinter import messagebox, Entry, Button, Toplevel, Text, Label, Canvas
from tkinter import ttk  # Import ttk for Treeview and Scrollbar
from tkinter.ttk import Style
from PIL import Image, ImageTk  # For adding images

class Product:
    def __init__(self, product_id, name, quantity, cost_price, selling_price):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.cost_price = cost_price
        self.selling_price = selling_price

    def __str__(self):
        return f"ID: {self.product_id}, Name: {self.name}, Quantity: {self.quantity}, Cost Price: {self.cost_price}, Selling Price: {self.selling_price}"

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("900x700")
        self.root.configure(bg="#ADD8E6")  # Light blue background
        self.inventory = []

        # Add a header with animation
        self.header_label = Label(root, text="Inventory Management System", font=("Arial", 24, "bold"), bg="#ADD8E6", fg="#333")
        self.header_label.pack(pady=20)
        self.animate_header()

        # Add a canvas for a decorative image
        self.canvas = Canvas(root, width=800, height=150, bg="#ADD8E6", highlightthickness=0)
        self.canvas.pack()

        # Create input fields
        self.create_input_fields()

        # Create buttons
        self.create_buttons()

    def change_background_color(self, color="#ADD8E6"):
        """Change the background color of the application."""
        self.root.configure(bg=color)
        self.header_label.configure(bg=color)
        self.canvas.configure(bg=color)
        for widget in self.root.winfo_children():
            if isinstance(widget, (Label, Entry, Button)):
                widget.configure(bg=color)

    def animate_header(self):
        """Animate the header text color."""
        colors = ["#333", "#555", "#777", "#999", "#bbb", "#ddd", "#333"]
        def change_color(index=0):
            self.header_label.config(fg=colors[index])
            self.root.after(200, change_color, (index + 1) % len(colors))
        change_color()

    def create_input_fields(self):
        """Create input fields for product details."""
        Label(self.root, text="Product ID:", font=("Arial", 12), bg="#ADD8E6").pack(pady=5)
        self.product_id_entry = Entry(self.root, font=("Arial", 12))
        self.product_id_entry.pack()

        Label(self.root, text="Product Name:", font=("Arial", 12), bg="#ADD8E6").pack(pady=5)
        self.name_entry = Entry(self.root, font=("Arial", 12))
        self.name_entry.pack()

        Label(self.root, text="Quantity:", font=("Arial", 12), bg="#ADD8E6").pack(pady=5)
        self.quantity_entry = Entry(self.root, font=("Arial", 12))
        self.quantity_entry.pack()

        Label(self.root, text="Cost Price:", font=("Arial", 12), bg="#ADD8E6").pack(pady=5)
        self.cost_price_entry = Entry(self.root, font=("Arial", 12))
        self.cost_price_entry.pack()

        Label(self.root, text="Selling Price:", font=("Arial", 12), bg="#ADD8E6").pack(pady=5)
        self.selling_price_entry = Entry(self.root, font=("Arial", 12))
        self.selling_price_entry.pack()

    def create_buttons(self):
        """Create buttons for actions."""
        Button(self.root, text="Add Product", command=self.add_product, font=("Arial", 12), bg="#4caf50", fg="white").pack(pady=10)
        Button(self.root, text="Record Sale", command=self.record_sale, font=("Arial", 12), bg="#2196f3", fg="white").pack(pady=10)
        Button(self.root, text="Display Inventory", command=self.display_inventory, font=("Arial", 12), bg="#ff9800", fg="white").pack(pady=10)

    def add_product(self):
        product_id = self.product_id_entry.get().strip()
        name = self.name_entry.get().strip()
        try:
            quantity = int(self.quantity_entry.get())
            cost_price = float(self.cost_price_entry.get())
            selling_price = float(self.selling_price_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for quantity and prices")
            return

        if not product_id or not name or not self.quantity_entry.get() or not self.cost_price_entry.get() or not self.selling_price_entry.get():
            messagebox.showerror("Input Error", "All fields must be filled out")
            return

        existing_product = next((p for p in self.inventory if p.product_id == product_id or p.name == name), None)
        if existing_product:
            existing_product.quantity += quantity
            messagebox.showinfo("Stock Update", f"Stock for '{name}' updated. New quantity: {existing_product.quantity}.")
        else:
            self.inventory.append(Product(product_id, name, quantity, cost_price, selling_price))
            messagebox.showinfo("Success", "Product added successfully!")

    def record_sale(self):
        """Record a sale by reducing the quantity of a product."""
        product_id = self.product_id_entry.get().strip()
        try:
            quantity_sold = int(self.quantity_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for quantity sold")
            return

        if not product_id or not self.quantity_entry.get():
            messagebox.showerror("Input Error", "Product ID and quantity must be filled out")
            return

        product = next((p for p in self.inventory if p.product_id == product_id), None)
        if product:
            if product.quantity >= quantity_sold:
                product.quantity -= quantity_sold
                messagebox.showinfo("Sale Recorded", f"Sale recorded. Remaining quantity of '{product.name}': {product.quantity}.")
            else:
                messagebox.showerror("Stock Error", f"Not enough stock for '{product.name}'. Available quantity: {product.quantity}.")
        else:
            messagebox.showerror("Product Not Found", "No product found with the given Product ID")

    def display_inventory(self):
        """Display the inventory in a tabular form with profit calculation."""
        # Create a new window for the inventory table
        inventory_window = Toplevel(self.root)
        inventory_window.title("Inventory List")
        inventory_window.geometry("900x400")

        # Create a Treeview widget
        columns = ("Product ID", "Name", "Quantity", "Cost Price", "Selling Price", "Profit")
        tree = ttk.Treeview(inventory_window, columns=columns, show="headings")
        tree.pack(fill="both", expand=True)

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        # Insert inventory data into the table
        for product in self.inventory:
            profit = (product.selling_price - product.cost_price) * product.quantity
            tree.insert("", "end", values=(product.product_id, product.name, product.quantity, product.cost_price, product.selling_price, round(profit, 2)))

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(inventory_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()