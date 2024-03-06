import asyncio
import json
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

        await ctx.send(get_value_message("stock amount"))
        try:
            stock_amount_msg = await bot.wait_for('message', check=check, timeout=30)
            stock_amount_input = stock_amount_msg.content
            if stock_amount_input.lower() == 'unlimited':
                stock_amount = 'Unlimited'
            else:
                stock_amount = int(stock_amount_input)
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
            description = f"Price: ${price}\nStock: {stock_amount if stock_amount == 'Unlimited' else 'limited'}"
            embed = discord.Embed(
                title=name,
                description=description,
                color=color
            )

            # Send the message and capture the returned message object
            message = await channel.send(embed=embed)
            message_id = message.id  # Get the message ID from the message object
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

        await message.add_reaction("🛒")
        await message.add_reaction("❌")

        server_id = ctx.guild.id
        products[message_id] = {
            "name": name,
            "price": price,
            "channel_id": channel_id,
            "server_id": server_id,
            "stock_amount": stock_amount
        }

        filename = 'products.json'

        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                json.dump({"products": []}, file, indent=4)

        with open(filename, 'r') as file:
            data = json.load(file)

        if not isinstance(data.get("products"), list):
            data["products"] = []

        data["products"].append(products[message_id])

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)