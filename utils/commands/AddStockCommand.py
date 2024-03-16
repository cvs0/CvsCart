import json
import re

from config.config import products_path


def add_stock_command(bot):
    @bot.command(name='add-stock')
    async def add_stock(ctx, stock_amount: int, action: str, *product_name):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("**Only administrators can use this command.**")
            return

        product_name = ' '.join(product_name)

        with open(products_path, 'r') as file:
            data = json.load(file)

        for product in data['products']:
            if product['name'] == product_name:
                if product['stock_amount'] == "Unlimited":
                    await ctx.send('You cannot change the stock for items that are set to unlimited stock.')
                    return

                if action.lower() == 'add':
                    product['stock_amount'] = int(product['stock_amount']) + stock_amount
                elif action.lower() == 'remove':
                    product['stock_amount'] = int(product['stock_amount']) - stock_amount
                else:
                    await ctx.send('Invalid action. Please specify either "add" or "remove".')
                    return

                with open(products_path, 'w') as file:
                    json.dump(data, file, indent=4)

                await ctx.send(f'Stock for "{product_name}" updated successfully.')
                return

        await ctx.send('Product not found.')
