import discord


def purge_command(bot):
    @bot.command(name='purge')
    async def purge_messages(ctx, amount: int):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send('**Only administrators can use this command.**')
            return

        if not isinstance(amount, int):
            await ctx.send('**Please provide a valid number.**')
            return

        if amount < 1 or amount > 100:
            await ctx.send('**Please provide a number between 1 and 100.**')
            return

        deleted = await ctx.channel.purge(limit=amount + 1)

        if len(deleted) == 1:
            await ctx.send('**No messages were found to purge.**')
            return

        embed = discord.Embed(description=f'{len(deleted) - 1} messages have been purged.', color=discord.Color.green())
        await ctx.send(embed=embed, delete_after=5)