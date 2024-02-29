import discord
from discord.ext import commands

from config.config import bot_token, reviewChannel, randomNumberChannel
from utils.CommandUtils import add_command_if_not_exists
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

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
user_cart_manager = UserCartManager()
products = {}

with open('products.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(',')
        message_id, channel_id, server_id, name, price = parts[:5]
        stock_limit = False
        stock_amount = None
        if len(parts) >= 6:
            stock_limit = parts[5].lower() == 'true'
        if len(parts) >= 7 and parts[6].strip():  # Check if parts[6] is not empty
            try:
                stock_amount = int(parts[6])
            except ValueError:
                print(f"Invalid stock_amount value: {parts[6]}")
        products[int(message_id)] = {
            "name": name,
            "price": float(price),
            "channel_id": int(channel_id),
            "server_id": int(server_id),
            "stock_limit": stock_limit,
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


@bot.event
async def on_guild_channel_create(channel):
    await handle_guild_channel_create(bot, user_cart_manager, channel)

@bot.event
async def on_message(message):
    await handle_message(bot, message, reviewChannel, randomNumberChannel)

@bot.event
async def on_raw_reaction_add(payload):
    await handle_reactions(payload, user_cart_manager, products, bot)

bot.run(bot_token)