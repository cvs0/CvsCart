import discord

from termcolor import colored

from config.config import debug


def cart_command(bot, user_cart_manager):
    @bot.command(name='cart')
    async def view_cart(ctx):
        cart = user_cart_manager.get_cart(ctx.author.id)

        if debug:
            print(colored(f"[D] User ID: {ctx.author.id}, Cart: {cart.items}", "yellow"))

        total = cart.calculate_total()
        embed = discord.Embed(title="Your Cart", color=0x0000ff)

        for item in cart.items:
            embed.add_field(name=item.name, value=f"Price: ${item.price} USD | Quantity: {item.quantity}",
                            inline=False)
        embed.add_field(name="Total", value=f"Total: ${total} USD", inline=False)
        message = await ctx.send(embed=embed)
