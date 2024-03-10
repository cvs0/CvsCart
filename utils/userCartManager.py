from config.config import save_carts, debug
from utils.cart import Cart
import json
from termcolor import colored

class UserCartManager:
    def __init__(self):
        self.user_carts = {}

        if save_carts:
            self.import_carts("data/carts.json")

    def get_cart(self, user_id):
        if not isinstance(user_id, (int, str)):
            raise TypeError("user_id must be an integer or string")

        if user_id not in self.user_carts:
            self.user_carts[user_id] = Cart()
        return self.user_carts[user_id]

    def remove_cart(self, user_id):
        if user_id in self.user_carts:
            del self.user_carts[user_id]

    def list_carts(self):
        for user_id, cart in self.user_carts.items():
            print(f"User ID: {user_id}")
            for item in cart.items:
                print(f"Item: {item.name}, Price: {item.price}, Quantity: {item.quantity}")

    def total_carts(self):
        return len(self.user_carts)

    def clear_all_carts(self):
        self.user_carts.clear()

    def export_carts(self, filename):
        cart_data = {}
        for user_id, cart in self.user_carts.items():
            if user_id not in cart_data:
                cart_data[user_id] = [{'name': item.name, 'price': item.price, 'quantity': item.quantity} for item in
                                      cart.items]

        with open(filename, 'w') as file:
            json.dump(cart_data, file, indent=4)

    def import_carts(self, filename):
        try:
            with open(filename, 'r') as file:
                cart_data = json.load(file)
                print(colored("[+] Cart data loaded successfully.", "green"))
        except json.decoder.JSONDecodeError:
            print(colored("[-] Error: The JSON file is empty or contains invalid JSON data.", "red"))
            return

        for user_id, items in cart_data.items():
            if user_id not in self.user_carts:
                self.user_carts[user_id] = Cart()
                if debug:
                    print(colored(f"[+] Created new cart for user {user_id}", "green"))
            else:
                if debug:
                    print(colored(f"[-] Cart for user {user_id} already exists, updating.", "red"))

            for item_data in items:
                name = item_data['name']
                price = item_data['price']
                quantity = item_data['quantity']
                self.user_carts[user_id].add_item(name, price, quantity)

                if debug:
                    print(colored(f"[+] Added item '{name}' to cart for user {user_id} with price ${price} and quantity {quantity}"), "green")

        if debug:
            print("Current user carts after import:")
            for user_id, cart in self.user_carts.items():
                print(f"User ID: {user_id}")
                for item in cart.items:
                    print(f"Item: {item.name}, Price: {item.price}, Quantity: {item.quantity}")