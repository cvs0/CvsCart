import discord


def set_status_command(bot):
    @bot.command(name='setstatus')
    async def set_status(ctx, status_type, *, status_text=None):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send('**Only administrators can use this command.**')
            return

        if not status_type:
            await ctx.send("**Please provide a status type.**")
            return

        if not status_text:
            await ctx.send("**Please provide a status text.**")
            return

        if status_type.lower() == 'playing':
            await bot.change_presence(activity=discord.Game(name=status_text))
        elif status_type.lower() == 'listening':
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status_text))
        elif status_type.lower() == 'watching':
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_text))
        else:
            await ctx.send("**Invalid status type. Please use 'playing', 'listening', or 'watching'.**")