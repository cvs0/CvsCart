import discord


def bot_help_command(bot):
    @bot.command(name='bothelp')
    async def help(ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send('**Only administrators can use this command.**')
            return

        embed = discord.Embed(title="Command List", description="Here is a list of available commands:", color=0x3498db)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/713871243620802858/830041129241393685/help_icon.png")
        embed.add_field(name="!add <name> <price> <quantity>", value="Add an item to the cart.", inline=False)
        embed.add_field(name="!remove <name> <quantity>", value="Remove an item from the cart.", inline=False)
        embed.add_field(name="!cart", value="View your cart.", inline=False)
        embed.add_field(name="!purge <amount>", value="Purge a certain amount of messages.", inline=False)
        embed.add_field(name="!clearcart", value="Clear your cart.", inline=False)
        embed.add_field(name="!finalize-purchase <user_id> <customer_paypal_email>", value="Finalize a purchase for a user.", inline=False)
        embed.add_field(name="!setstatus <status_type> <status_text>", value="Status types: watching, playing, listening.")

        await ctx.send(embed=embed)