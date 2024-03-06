import discord
from config.config import paypal_email, debug
from utils.cartItem import CartItem
from termcolor import colored


async def handle_reactions(payload, user_cart_manager, products, bot):
    if payload.user_id == bot.user.id:
        return

    if debug:
        print(colored(f"[D] Handling reaction: {payload.emoji}", "yellow"))

    if str(payload.emoji) == "✅":
        if debug:
            print(colored("[D] Processing payment...", "yellow"))

        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction("✅", payload.member)
        user_id = payload.user_id
        cart = user_cart_manager.get_cart(user_id)
        total = cart.calculate_total()
        embed = discord.Embed(
            title="Pay with PayPal",
            description=f"Please send ${total} USD to the following PayPal email address:\n\n{paypal_email}\n\nMake sure to use the 'Send money to friends and family' option.\n\nDon't forget to include your email associated with your PayPal account below.",
            color=0x00ff00
        )
        await channel.send(embed=embed)

        if debug:
            print(colored(f"[D] Payment processed. Total: ${total}", "yellow"))

    if str(payload.emoji) in ["🛒", "❌"]:
        if debug:
            print(colored("[D] Processing cart action...", "yellow"))
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if debug:
            print(colored("[D] Checking if message ID is in products...", "yellow"))
            print(colored(f"[D] Payload message ID: {payload.message_id}", "yellow"))
            print(colored(f"[D] Products keys: {products.keys()}", "yellow"))

        if payload.message_id in products:
            product = products[payload.message_id]

            if debug:
                print(colored(f"[D] Product found: {product['name']}", "yellow"))

            user_id = payload.user_id
            cart = user_cart_manager.get_cart(user_id)

            if str(payload.emoji) == "🛒":
                if debug:
                    print(colored("[D] Adding item to cart...", "yellow"))

                stock_amount = product.get("stock_amount")
                if stock_amount != 'Unlimited' and (stock_amount is None or int(stock_amount) <= 0):
                    await message.remove_reaction("🛒", payload.member)
                    user = bot.get_user(user_id)
                    if user:
                        embed = discord.Embed(
                            title="Item Out of Stock",
                            description="This item is currently out of stock.",
                            color=0xff0000
                        )
                        await user.send(embed=embed)

                    if debug:
                        print(colored("[D] Item out of stock", "yellow"))
                    return

                cart.add_item(product["name"], product["price"], 1)
                if stock_amount != 'Unlimited':
                    products[payload.message_id]["stock_amount"] -= 1

                await message.remove_reaction("🛒", payload.member)
                user = bot.get_user(user_id)
                if user:
                    cart_item = CartItem(product["name"], product["price"], 1)
                    stock_amount_display = "Unlimited" if stock_amount is None else stock_amount
                    embed = discord.Embed(
                        title="Item Added to Cart",
                        description=f"**{cart_item.name}**\nPrice: ${cart_item.price:.2f} USD\nQuantity: {cart_item.quantity}\nStock: {stock_amount_display}",
                        color=0x00ff00
                    )
                    await user.send(embed=embed)

                    if debug:
                        print(colored("[D] Item added to cart", "yellow"))
                else:
                    print(colored("[-] User not found.", "red"))
            elif str(payload.emoji) == "❌":
                if debug:
                    print(colored("[-] Removing item from cart...", "yellow"))

                if any(item.name == product["name"] for item in cart.items):
                    cart.remove_item(product["name"], 1)
                    stock_amount = product.get("stock_amount")
                    if stock_amount != 'Unlimited':
                        products[payload.message_id]["stock_amount"] += 1

                    await message.remove_reaction("❌", payload.member)
                    user = bot.get_user(user_id)
                    if user:
                        cart_item = CartItem(product["name"], product["price"], 1)
                        stock_amount_display = "Unlimited" if stock_amount is None else stock_amount
                        embed = discord.Embed(
                            title="Item Removed From Cart",
                            description=f"**{cart_item.name}**\nPrice: ${cart_item.price:.2f} USD\nQuantity: {cart_item.quantity}\nStock: {stock_amount_display}",
                            color=0x00ff00
                        )
                        await user.send(embed=embed)

                        if debug:
                            print(colored("[D] Item removed from cart", "yellow"))
                else:
                    await message.remove_reaction("❌", payload.member)

                    if debug:
                        print(colored("[D] Item not found in cart", "yellow"))
