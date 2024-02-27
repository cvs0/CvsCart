from utils.cart import Cart


class UserCartManager:
    def __init__(self):
        self.user_carts = {}

    def get_cart(self, user_id):
        if user_id not in self.user_carts:
            self.user_carts[user_id] = Cart()
        return self.user_carts[user_id]

    def remove_cart(self, user_id):
        if user_id in self.user_carts:
            del self.user_carts[user_id]

    def list_carts(self):
        return self.user_carts

    def total_carts(self):
        return len(self.user_carts)

    def clear_all_carts(self):
        self.user_carts.clear()

    def export_carts(self, filename):
        with open(filename, 'w') as file:
            for user_id, cart in self.user_carts.items():
                file.write(f"User ID: {user_id}\n")
                for item in cart.items:
                    file.write(f"Item: {item.name}, Price: {item.price}, Quantity: {item.quantity}\n")

    def import_carts(self, filename):
        with open(filename, 'r') as file:
            user_id = None
            for line in file:
                if line.startswith('User ID:'):
                    user_id = int(line.split(': ')[1])
                    if user_id not in self.user_carts:
                        self.user_carts[user_id] = Cart()
                elif line.startswith('Item:'):
                    parts = line.split(', ')
                    name = parts[0].split(': ')[1]
                    price = float(parts[1].split(': ')[1])
                    quantity = int(parts[2].split(': ')[1])
                    if user_id is not None:
                        self.user_carts[user_id].add_item(name, price, quantity)