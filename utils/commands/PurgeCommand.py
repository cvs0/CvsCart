import asyncio

import discord

def purge_command(bot):
    @bot.command(name='purge')
    async def purge_messages(ctx, amount: int):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send('**Only administrators can use this command.**')

        if not 1 <= amount <= 100:
            return await ctx.send('**Please provide a number between 1 and 100.**')

        try:
            deleted = await ctx.channel.purge(limit=amount + 1)
        except discord.Forbidden:
            return await ctx.send('**I do not have permission to delete messages.**')
        except discord.HTTPException:
            return await ctx.send('**Failed to delete messages. Please try again later.**')

        deleted_count = len(deleted) - 1
        if deleted_count == 0:
            return await ctx.send('**No messages were found to purge.**')

        embed = discord.Embed(description=f'{deleted_count} messages have been purged.', color=discord.Color.green())
        confirmation_msg = await ctx.send(embed=embed, delete_after=5)

        await asyncio.sleep(5)
        await ctx.message.delete()
