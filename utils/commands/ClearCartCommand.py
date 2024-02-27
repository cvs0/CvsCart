def clear_cart_command(bot, user_cart_manager):
    @bot.command(name='clearcart')
    async def clear_cart(ctx):
        cart = user_cart_manager.get_cart(ctx.author.id)
        cart.clear()
        await ctx.author.send("Your cart has been cleared.")