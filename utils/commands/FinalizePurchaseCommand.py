import datetime

from discord.ext.commands import MissingRequiredArgument

import requests

from config.config import api_url, order_history, order_history_path, ratingsChannel, ratings

from termcolor import colored


async def send_rating_message(p_user_id, p_channel_id, bot):
    user = await bot.fetch_user(p_user_id)
    channel = bot.get_channel(p_channel_id)

    rating_message = await user.send(
        "Please rate the service: "
        "1️⃣ for very bad, "
        "2️⃣ for bad, "
        "3️⃣ for neutral, "
        "4️⃣ for good, "
        "5️⃣ for excellent."
    )

    for emoji in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']:
        await rating_message.add_reaction(emoji)

    def check(p_reaction, reacting_user):
        return reacting_user == user and str(p_reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

    reaction, _ = await bot.wait_for('reaction_add', check=check)

    await rating_message.delete()
    await channel.send(f"Rating: {reaction.emoji} from {user.mention}")


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

        if ratings:
            await send_rating_message(user_id, ratingsChannel, bot)

        cart = user_cart_manager.get_cart(user_id)

        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(order_history_path, 'a+') as file:
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
                with open(order_history_path, 'rb') as file_to_upload:
                    files = {'file': (order_history_path, file_to_upload, 'text/plain')}
                    response = requests.post(api_url, files=files)
                    if response.status_code == 200:
                        print(colored('[+] File uploaded successfully.', "green"))
                    else:
                        print(colored(f'[-] Failed to upload file: {response.text}', "red"))

        except Exception as e:
            await ctx.send(f"**An error occurred while finalizing the purchase: {e}**")
            return

        try:
            cart.clear()
        except Exception as e:
            await ctx.send(f"**An error occurred while clearing the cart: {e}**")
            return

        await ctx.send(f"**The purchase has been finalized.**")

    @finalize_purchase.error
    async def finalize_purchase_error(ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send('**Please provide a valid PayPal email.**')

    return finalize_purchase
