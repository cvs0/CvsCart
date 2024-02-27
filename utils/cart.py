from utils.cartItem import CartItem


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            print("Quantity must be a positive integer.")
            return

        if not isinstance(price, (int, float)) or price <= 0:
            print("Price must be a positive number.")
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
                print("Quantity must be a positive integer.")
                return

            existing_item.quantity -= quantity
            if existing_item.quantity <= 0:
                self.items.remove(existing_item)
        else:
            print("Item not found in cart.")
            return

    def calculate_total(self):
        try:
            total = sum(item.price * item.quantity for item in self.items)
            return round(total, 2)
        except Exception as e:
            print(f"Error calculating total: {e}")
            return None

    def clear(self):
        self.items = []