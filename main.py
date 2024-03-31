import asyncio

import discord
from discord.ext import commands
from termcolor import colored

from config.config import bot_token, reviewChannel, randomNumberChannel, products_path, marketplaceChannel
from utils.CommandUtils import add_command_if_not_exists
from utils.commands.AddStockCommand import add_stock_command
from utils.commands.BotHelpCommand import bot_help_command
from utils.commands.CartCommand import cart_command
from utils.commands.ClearCartCommand import clear_cart_command
from utils.commands.ClearProductsCommand import clear_products_command
from utils.commands.FinalizePurchaseCommand import finalize_purchase_command
from utils.commands.FixReactionsCommand import fix_reactions_command
from utils.commands.MakeItemCommand import make_item_command
from utils.commands.PurgeCommand import purge_command
from utils.commands.SetStatusCommand import set_status_command
from utils.events.guild import handle_guild_channel_create
from utils.events.message import handle_message
from utils.events.reactions import handle_reactions
from utils.userCartManager import UserCartManager
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
user_cart_manager = UserCartManager()

# Assuming 'products_data' is loaded correctly from the JSON file
with open(products_path, 'r') as file:
    products_data = json.load(file)['products']

products = {}

for product in products_data:
    message_id = product['message_id']
    channel_id = product['channel_id']
    server_id = product['server_id']
    name = product['name']
    price = product['price']
    stock_amount = product.get('stock_amount', None)

    # Add the product to your products dictionary if needed
    products[message_id] = {
        "name": name,
        "price": price,
        "channel_id": channel_id,
        "server_id": server_id,
        "stock_amount": stock_amount
    }

add_command_if_not_exists(bot, 'clearcart', clear_cart_command(bot, user_cart_manager))
add_command_if_not_exists(bot, 'cart', cart_command(bot, user_cart_manager))
add_command_if_not_exists(bot, 'fixreactions', fix_reactions_command(bot, products))
add_command_if_not_exists(bot, 'makeitem', make_item_command(bot, products))
add_command_if_not_exists(bot, 'clearproducts', clear_products_command(bot, products))
add_command_if_not_exists(bot, 'purge', purge_command(bot))
add_command_if_not_exists(bot, 'finalize-purchase', finalize_purchase_command(bot, user_cart_manager))
add_command_if_not_exists(bot, 'bothelp', bot_help_command(bot))
add_command_if_not_exists(bot, 'setstatus', set_status_command(bot))
add_command_if_not_exists(bot, 'add-stock', add_stock_command(bot))


@bot.event
async def on_guild_channel_create(channel):
    await handle_guild_channel_create(bot, user_cart_manager, channel)


@bot.event
async def on_message(message):
    await handle_message(bot, message, reviewChannel, randomNumberChannel)


@bot.event
async def on_raw_reaction_add(payload):
    await handle_reactions(payload, user_cart_manager, products, bot)


async def send_marketplace_safety_msg():
    while True:
        channel = bot.get_channel(marketplaceChannel)
        embed = discord.Embed(
            title="Marketplace Guidelines",
            description=(
                "Messages in the marketplace must start with one of the following tags: "
                "[WTB] (wants to buy), [WTS] (wants to sell), or [WTT] (wants to trade).\n\n"
                "Scamming is not tolerated."
            ),
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)
        await asyncio.sleep(900)  # 15 minutes in seconds


@bot.event
async def on_ready():
    print(colored("Bot ready", "green"))
    await send_marketplace_safety_msg()


bot.run(bot_token)
