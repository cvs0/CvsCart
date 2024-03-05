import asyncio
import os

import discord


def make_item_command(bot, products):
    @bot.command(name='makeitem')
    async def make_item(ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("**Only administrators can use this command.**")
            return

        def check(p_message):
            return p_message.author == ctx.author and p_message.channel == ctx.channel

        def get_value_message(value_name):
            return f"**Please enter the {value_name} of the item:**"

        await ctx.send("**Do you want to send a message for the item or use a message ID? (send/id)**")
        try:
            item_specification_msg = await bot.wait_for('message', check=check, timeout=30)
            item_specification = item_specification_msg.content.lower()
            if item_specification not in ['send', 'id']:
                raise ValueError("Please respond with 'send' or 'id'.")
        except (ValueError, asyncio.TimeoutError) as e:
            await ctx.send(f"**Invalid response or timeout. Please try again. ({e})**")
            return

        if item_specification == 'send':
            await ctx.send("**Please enter the message content for the item:**")
            try:
                message_content_msg = await bot.wait_for('message', check=check, timeout=30)
                name = message_content_msg.content  # Use the message content as the name
            except asyncio.TimeoutError:
                await ctx.send("**Timeout. Please try again.**")
                return
        else:
            await ctx.send(get_value_message("message ID"))
            try:
                message_id_msg = await bot.wait_for('message', check=check, timeout=30)
                message_id = int(message_id_msg.content)
            except (ValueError, asyncio.TimeoutError):
                await ctx.send("**Invalid message ID or timeout. Please try again.**")
                return

            await ctx.send(get_value_message("name"))
            try:
                name_msg = await bot.wait_for('message', check=check, timeout=30)
                name = name_msg.content
            except asyncio.TimeoutError:
                await ctx.send("**Timeout. Please try again.**")
                return

        await ctx.send(get_value_message("price"))
        try:
            price_msg = await bot.wait_for('message', check=check, timeout=30)
            price = float(price_msg.content)
        except (ValueError, asyncio.TimeoutError) as e:
            await ctx.send(f"**Invalid price or timeout. Please try again. ({e})**")
            return

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

        stock_amount = "Unlimited" if not stock_limit else None
        if stock_limit:
            await ctx.send(get_value_message("stock amount"))
            try:
                stock_amount_msg = await bot.wait_for('message', check=check, timeout=30)
                stock_amount = int(stock_amount_msg.content)
            except (ValueError, asyncio.TimeoutError):
                await ctx.send("**Invalid stock amount or timeout. Please try again.**")
                return

        await ctx.send("**Please enter the channel ID where you want to add the item:**")
        try:
            channel_id_msg = await bot.wait_for('message', check=check, timeout=30)
            channel_id = int(channel_id_msg.content)
        except (ValueError, asyncio.TimeoutError):
            await ctx.send("**Invalid channel ID or timeout. Please try again.**")
            return

        channel = bot.get_channel(channel_id)
        if channel is None:
            await ctx.send("**Channel not found.**")
            return

        color_value = None

        if item_specification == 'send':
            await ctx.send("**Please enter the color for the embed (hex format or name):**")
            try:
                color_msg = await bot.wait_for('message', check=check, timeout=30)
                color_value = color_msg.content
            except asyncio.TimeoutError:
                await ctx.send("**Invalid color or timeout. Using default color.**")
                color_value = None

        if item_specification == 'send':
            color = discord.Color(value=int(color_value.lstrip('#'), 16))
            description = f"Price: ${price}\nStock: {'limited' if stock_limit else 'unlimited'}"
            if stock_limit:
                description += f" stock of {stock_amount}"
            embed = discord.Embed(
                title=name,
                description=description,
                color=color
            )

            message = await channel.send(embed=embed)
        else:
            try:
                message = await channel.fetch_message(message_id)
            except discord.NotFound:
                await ctx.send("**Message not found.**")
                return

        await message.add_reaction("🛒")
        await message.add_reaction("❌")

        server_id = ctx.guild.id
        products[message.id] = {
            "name": name,
            "price": price,
            "channel_id": channel_id,
            "server_id": server_id,
            "stock_limit": stock_limit,
            "stock_amount": stock_amount
        }

        filename = 'products.txt'
        if not os.path.exists(filename):
            with open(filename, 'w'):
                pass

        with open(filename, 'a') as file:
            stock_limit_value = "Unlimited" if not stock_limit else "True"
            stock_amount_value = str(stock_amount) if stock_limit else "0"

            if stock_limit:
                file.write(
                    f"{message.id},{channel_id},{server_id},{name},{price},{stock_limit_value},{stock_amount_value}\n"
                )
            else:
                file.write(f"{message.id},{channel_id},{server_id},{name},{price},{stock_limit_value}\n")

        stock_info = f" with {'limited' if stock_limit else 'unlimited'} stock of {stock_amount}" if stock_limit else ""
        embed = discord.Embed(
            description=f"Item added to the store with message ID {message.id} in channel {channel_id}{stock_info}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
