import asyncio
import os

import discord

def make_item_command(bot, products):
    @bot.command(name='makeitem')
    async def make_item(ctx):
        # Check if the user has administrator permissions
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("**Only administrators can use this command.**")
            return

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        def get_value_message(value_name):
            return f"**Please enter the {value_name} of the item:**"

        # Ask for message ID
        await ctx.send(get_value_message("message ID"))
        try:
            message_id = await bot.wait_for('message', check=check, timeout=30)
            message_id = int(message_id.content)
        except (ValueError, asyncio.TimeoutError):
            await ctx.send("**Invalid message ID or timeout. Please try again.**")
            return

        # Ask for price
        await ctx.send(get_value_message("price"))
        try:
            price_msg = await bot.wait_for('message', check=check, timeout=30)
            if not price_msg.content:
                raise ValueError("Price cannot be empty")
            price = float(price_msg.content)
        except (ValueError, asyncio.TimeoutError) as e:
            await ctx.send(f"**Invalid price or timeout. Please try again. ({e})**")
            return

        # Ask if there is limited stock
        await ctx.send("**Is there a limited amount of stock for this item? (yes/no)**")
        try:
            stock_limit_msg = await bot.wait_for('message', check=check, timeout=30)
            stock_limit_response = stock_limit_msg.content.lower()
            if stock_limit_response not in ['yes', 'no']:
                raise ValueError("Please respond with 'yes' or 'no'.")
            stock_limit = stock_limit_response == 'yes'
        except (ValueError, asyncio.TimeoutError) as e:
            await ctx.send(f"**Invalid response or timeout. Please try again. ({e})**")
            return

        stock_amount = None
        if stock_limit:
            # Ask for stock amount
            await ctx.send(get_value_message("stock amount"))
            try:
                stock_amount_msg = await bot.wait_for('message', check=check, timeout=30)
                stock_amount = int(stock_amount_msg.content)
            except (ValueError, asyncio.TimeoutError):
                await ctx.send("**Invalid stock amount or timeout. Please try again.**")
                return

        # Ask for channel ID
        await ctx.send(get_value_message("channel ID"))
        try:
            channel_id_msg = await bot.wait_for('message', check=check, timeout=30)
            channel_id = int(channel_id_msg.content)
        except (ValueError, asyncio.TimeoutError):
            await ctx.send("**Invalid channel ID or timeout. Please try again.**")
            return

        # Validate channel ID
        channel = bot.get_channel(channel_id)
        if channel is None:
            await ctx.send("**Channel not found.**")
            return

        # Ask for name
        await ctx.send(get_value_message("name"))
        try:
            name_msg = await bot.wait_for('message', check=check, timeout=30)
            name = name_msg.content
        except asyncio.TimeoutError:
            await ctx.send("**Timeout. Please try again.**")
            return

        # Add reactions to the message
        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("**Message not found.**")
            return

        await message.add_reaction("🛒")
        await message.add_reaction("❌")

        server_id = ctx.guild.id
        products[message_id] = {"name": name, "price": price, "channel_id": channel_id, "server_id": server_id, "stock_limit": stock_limit, "stock_amount": stock_amount}

        # Write the item to the products file
        filename = 'products.txt'
        if not os.path.exists(filename):
            with open(filename, 'w'):
                pass

        with open(filename, 'a') as file:
            file.write(f"{message_id},{channel_id},{server_id},{name},{price},{stock_limit},{stock_amount}\n")

        # Send a confirmation message
        stock_info = f" with {'limited' if stock_limit else 'unlimited'} stock of {stock_amount}" if stock_limit else ""
        embed = discord.Embed(
            description=f"Item added to the store with message ID {message_id} in channel {channel.id}{stock_info}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)