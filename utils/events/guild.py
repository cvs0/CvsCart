import asyncio

import discord


async def handle_guild_channel_create(bot, user_cart_manager, channel):
    if channel.name.startswith('ticket-'):
        display_name = channel.name.split('ticket-')[1]
        user = discord.utils.get(bot.users, display_name=display_name)

        if user:
            await asyncio.sleep(2)
            embed = discord.Embed(title="Your Cart", color=0x0000ff)
            for item in user_cart_manager.get_cart(user.id).items:
                embed.add_field(name=item.name, value=f"Price: ${item.price} USD | Quantity: {item.quantity}",
                                inline=False)
            total = user_cart_manager.get_cart(user.id).calculate_total()
            embed.add_field(name="Total", value=f"Total: ${total} USD", inline=False)
            message = await channel.send(embed=embed)
            await message.add_reaction("✅")
        else:
            await channel.send("User not found.")