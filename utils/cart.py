from config.config import debug
from utils.cartItem import CartItem
from termcolor import colored


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            if debug:
                print(colored("[-] Quantity must be a positive integer.", "red"))
            return

        if not isinstance(price, (int, float)) or price <= 0:
            if debug:
                print(colored("[-] Price must be a positive number.", "red"))

            return

        existing_item = next((item for item in self.items if item.name == name), None)
        if existing_item:
            existing_item.quantity += quantity
        else:
            price = round(price, 2)
            new_item = CartItem(name, price, quantity)
            self.items.append(new_item)

            if debug:
                print(colored(f"[+] Added item '{name}' to cart. Price: ${price}, Quantity: {quantity}", "green"))

    def remove_item(self, name, quantity):
        existing_item = next((item for item in self.items if item.name == name), None)
        if existing_item:
            if not isinstance(quantity, int) or quantity <= 0:
                if debug:
                    print(colored("[-] Quantity must be a positive integer.", "red"))

                return

            existing_item.quantity -= quantity
            if existing_item.quantity <= 0:
                self.items.remove(existing_item)

            if debug:
                print(colored(f"[+] Removed {quantity} of item '{name}' from cart.", "green"))
        else:
            if debug:
                print(colored("[-] Item not found in cart.", "red"))

            return

    def calculate_total(self):
        try:
            total = sum(item.price * item.quantity for item in self.items)

            if debug:
                print(colored(f"[+] Calculated total: ${total}", "green"))

            return round(total, 2)
        except Exception as e:
            if debug:
                print(colored(f"[-] Error calculating total: {e}", "red"))

            return None

    def clear(self):
        self.items = []

        if debug:
            print(colored("[+] Cleared cart.", "green"))
