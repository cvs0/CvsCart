import os

import discord

def make_item_command(bot, products):
    @bot.command(name='makeitem')
    async def make_item(ctx, message_id: int, price: float, channel_id: int, *name):
        # Check if the user has administrator permissions
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("**Only administrators can use this command.**")
            return

        # Validate price
        if price <= 0:
            await ctx.send("**Price must be a positive number.**")
            return

        # Validate channel ID
        if channel_id is None:
            channel = ctx.channel
        else:
            channel = bot.get_channel(channel_id)
            if channel is None:
                await ctx.send("**Channel not found.**")
                return

        # Validate message ID
        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("**Message not found.**")
            return

        # Validate name
        name = " ".join(name)
        if not name:
            await ctx.send("**Please provide a name for the item.**")
            return

        # Add reactions to the message
        await message.add_reaction("🛒")
        await message.add_reaction("❌")

        server_id = ctx.guild.id
        products[message_id] = {"name": name, "price": price, "channel_id": channel_id, "server_id": server_id}

        # Write the item to the products file
        filename = 'products.txt'
        if not os.path.exists(filename):
            with open(filename, 'w'):
                pass

        with open(filename, 'a') as file:
            file.write(f"{message_id},{channel_id}, {server_id},{name},{price}\n")

        # Send a confirmation message
        embed = discord.Embed(description=f"Item added to the store with message ID {message_id} in channel {channel.id}.",
                              color=discord.Color.green())
        await ctx.send(embed=embed)