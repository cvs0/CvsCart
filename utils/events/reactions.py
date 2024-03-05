import discord

from config.config import 
from utils.cartItem import CartItem

from termcolor import colored

async def handle_reactions(payload, user_cart_manager, products, bot):
    if payload.user_id == bot.user.id:
        return

    if str(payload.emoji) == "✅":
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.remove_reaction("✅", payload.member)
        user_id = payload.user_id
        cart = user_cart_manager.get_cart(user_id)
        total = cart.calculate_total()
        embed = discord.Embed(title="Payment",
                              description=f"Please send ${total} USD to the following email address:\n\n{}\n\nMake sure to use the 'Send money to friends and family' option.\n\nDon't forget to include your email associated with your payment account below.",
                              color=0x00ff00)
        await channel.send(embed=embed)

    if str(payload.emoji) == "🛒" or str(payload.emoji) == "❌":
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if payload.message_id in products:
            product = products[payload.message_id]

            user_id = payload.user_id
            cart = user_cart_manager.get_cart(user_id)

            if str(payload.emoji) == "🛒":
                stock_limit = product.get("stock_limit")
                stock_amount = product.get("stock_amount")
                if stock_limit is not None and stock_amount is not None and (not stock_limit or (stock_limit and int(stock_amount) <= 0)):
                    await message.remove_reaction("🛒", payload.member)
                    user = bot.get_user(user_id)
                    if user:
                        embed = discord.Embed(title="Item Out of Stock",
                                              description="This item is currently out of stock.",
                                              color=0xff0000)
                        await user.send(embed=embed)
                    return

                cart.add_item(product["name"], product["price"], 1)
                if stock_limit is not None and stock_amount is not None and stock_limit != "Unlimited":
                    products[payload.message_id]["stock_amount"] -= 1

                await message.remove_reaction("🛒", payload.member)
                user = bot.get_user(user_id)
                if user:
                    cart_item = CartItem(product["name"], product["price"], 1)
                    stock_amount_display = "Unlimited" if stock_amount is None else stock_amount
                    embed = discord.Embed(title="Item Added to Cart",
                                          description=f"**{cart_item.name}**\nPrice: ${cart_item.price:.2f} USD\nQuantity: {cart_item.quantity}\nStock: {stock_amount_display}",
                                          color=0x00ff00)
                    await user.send(embed=embed)
                else:
                    print(colored("User not found.", "red"))
            elif str(payload.emoji) == "❌":
                if any(item.name == product["name"] for item in cart.items):
                    cart.remove_item(product["name"], 1)
                    if product.get("stock_limit") is not None:
                        products[payload.message_id]["stock_amount"] += 1

                    await message.remove_reaction("❌", payload.member)
                    user = bot.get_user(user_id)
                    if user:
                        cart_item = CartItem(product["name"], product["price"], 1)
                        stock_amount = product.get("stock_amount", "Unlimited")
                        embed = discord.Embed(title="Item Removed From Cart",
                                              description=f"**{cart_item.name}**\nPrice: ${cart_item.price:.2f} USD\nQuantity: {cart_item.quantity}\nStock: {stock_amount}",
                                              color=0x00ff00)
                        await user.send(embed=embed)
                else:
                    await message.remove_reaction("❌", payload.member)
