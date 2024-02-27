# CvsCart Discord Cart System

CvsCart is a Discord bot that allows users to manage a shopping cart directly within a Discord server. It also enables your server to have its own shop system with products and product management.

## Commands

- `!add <name> <price> <quantity>`: Add an item to the cart.
- `!remove <name> <quantity>`: Remove an item from the cart.
- `!cart`: View your cart.
- `!purge <amount>`: Purge a certain amount of messages.
- `!clearcart`: Clear your cart.
- `!clearproducts`: Clear all the products.
- `!fixreactions`: Fix the reactions of products.
- `!finalize-purchase <user_id> <customer_paypal_email>`: Finalize a purchase for a user.
- `!setstatus <status_type> <status_text>`: Set the bot's status.

## Installation

1. Clone the repository.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up your environment variables. See `config/.env.example` for an example.
4. Run the bot: `python main.py`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
