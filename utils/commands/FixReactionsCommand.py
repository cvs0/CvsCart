import discord


def fix_reactions_command(bot, products):
    @bot.command(name='fixreactions')
    async def fix_reactions(ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("**Only administrators can use this command.**")
            return

        for message_id in products:
            channel_id = products[message_id]["channel_id"]
            channel = bot.get_channel(channel_id)
            try:
                message = await channel.fetch_message(message_id)
                if message:
                    await message.add_reaction("🛒")
                    await message.add_reaction("❌")
            except discord.NotFound:
                pass

        await ctx.send("**Reactions on all products have been fixed.**")
