import discord

from config.config import paypal_email
from utils.cartItem import CartItem

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
        embed = discord.Embed(title="Pay with PayPal",
                              description=f"Please send ${total} USD to the following PayPal email address:\n\n{paypal_email}\n\nMake sure to use the 'Send money to friends and family' option.\n\nDon't forget to include your email associated with your PayPal account below.",
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
                cart.add_item(product["name"], product["price"], 1)
                await message.remove_reaction("🛒", payload.member)
                user = bot.get_user(user_id)
                if user:
                    cart_item = CartItem(product["name"], product["price"], 1)
                    embed = discord.Embed(title="Item Added to Cart",
                                          description=f"**{cart_item.name}**\nPrice: ${cart_item.price:.2f} USD\nQuantity: {cart_item.quantity}",
                                          color=0x00ff00)
                    await user.send(embed=embed)
                else:
                    print("User not found.")
            elif str(payload.emoji) == "❌":
                    if any(item.name == product["name"] for item in cart.items):
                        cart.remove_item(product["name"], 1)
                        await message.remove_reaction("❌", payload.member)
                        user = bot.get_user(user_id)
                        if user:
                            cart_item = CartItem(product["name"], product["price"], 1)
                            embed = discord.Embed(title="Item Removed From Cart",
                                                  description=f"**{cart_item.name}**\nPrice: ${cart_item.price:.2f} USD\nQuantity: {cart_item.quantity}",
                                                  color=0x00ff00)
                            await user.send(embed=embed)
                    else:
                        await message.remove_reaction("❌", payload.member)
