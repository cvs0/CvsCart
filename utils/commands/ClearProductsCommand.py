import discord


def clear_products_command(bot, products):
    @bot.command(name='clearproducts')
    async def clear_products(ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send('**Only administrators can use this command.**')
            return

        products.clear()

        for message_id in products:
            channel_id = products[message_id]["channel_id"]
            channel = bot.get_channel(channel_id)
            try:
                message = await channel.fetch_message(message_id)
                await message.clear_reaction("🛒")
            except discord.NotFound:
                pass

        await ctx.send("**All products and reactions have been cleared.**")
