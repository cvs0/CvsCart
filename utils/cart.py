from utils.cartItem import CartItem

from termcolor import colored

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            print(colored("Quantity must be a positive integer.", "red"))
            return

        if not isinstance(price, (int, float)) or price <= 0:
            print(colored("Price must be a positive number.", "red"))
            return

        existing_item = next((item for item in self.items if item.name == name), None)
        if existing_item:
            existing_item.quantity += quantity
        else:
            price = round(price, 2)
            self.items.append(CartItem(name, price, quantity))

    def remove_item(self, name, quantity):
        existing_item = next((item for item in self.items if item.name == name), None)
        if existing_item:
            if not isinstance(quantity, int) or quantity <= 0:
                print(colored("Quantity must be a positive integer.", "red"))
                return

            existing_item.quantity -= quantity
            if existing_item.quantity <= 0:
                self.items.remove(existing_item)
        else:
            print(colored("Item not found in cart.", "red"))
            return

    def calculate_total(self):
        try:
            total = sum(item.price * item.quantity for item in self.items)
            return round(total, 2)
        except Exception as e:
            print(colored(f"Error calculating total: {e}", "red"))
            return None

    def clear(self):
        self.items = []