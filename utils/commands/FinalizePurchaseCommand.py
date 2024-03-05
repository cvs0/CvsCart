import datetime

import requests

from config.config import api_url, order_history

from termcolor import colored


def finalize_purchase_command(bot, user_cart_manager):
    @bot.command(name='finalize-purchase')
    async def finalize_purchase(ctx, user_id: int, customer_paypal_email: str):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send('**Only administrators can use this command.**')
            return

        if user_id <= 0:
            await ctx.send('**Please provide a valid user ID.**')
            return

        user = bot.get_user(user_id)
        if not user:
            await ctx.send('**User not found.**')
            return

        cart = user_cart_manager.get_cart(user_id)

        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open('order_history.txt', 'a+') as file:
                file.write(f"Date: {formatted_datetime}\n")
                file.write(f"User ID: {user_id}, Username: {user.name}\n")
                file.write(f"Users PayPal: {customer_paypal_email}\n")
                file.write("Items:\n")
                for item in cart.items:
                    file.write(f"  - Item: {item.name}, Price: ${item.price:.2f} USD, Quantity: {item.quantity}\n")
                file.write("Total: ${:.2f} USD\n".format(cart.calculate_total()))
                file.write("\n")

            if order_history:
                # Upload the file to the API
                with open('order_history.txt', 'rb') as file_to_upload:
                    files = {'file': ('order_history.txt', file_to_upload, 'text/plain')}
                    response = requests.post(api_url, files=files)
                    if response.status_code == 200:
                        print(colored('File uploaded successfully.', "green"))
                    else:
                        print(colored(f'Failed to upload file: {response.text}', "red"))

        except Exception as e:
            await ctx.send(f"**An error occurred while finalizing the purchase: {e}**")
            return

        try:
            cart.clear()
        except Exception as e:
            await ctx.send(f"**An error occurred while clearing the cart: {e}**")
            return

        await ctx.send(f"**The purchase has been finalized.**")

    return finalize_purchase
