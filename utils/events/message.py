import json
from random import random

import discord
from discord import Embed
from discord.utils import get

from config.config import marketplaceChannel, marketplaceRepChannel, reputation_path, debug
from utils.ReputationUtils import get_user_reputation


async def handle_message(bot, message, reviewChannel, randomNumberChannel):
    if message.author == bot.user:
        return

    if message.channel.id == reviewChannel:
        await message.add_reaction('💯')

    if message.channel.id == randomNumberChannel:
        try:
            guessed_number = int(message.content)
        except ValueError:
            await message.channel.send("**Please guess a valid number.**")
            return

        if 'random_number' not in globals():
            random_number = random.randint(1, 100)
            await message.channel.send("**A new game has started! Guess a number between 1 and 100.**")

        if guessed_number == random_number:
            await message.channel.send("**Congratulations! You guessed the right number.**")
            random_number = random.randint(1, 100)

    try:
        with open(reputation_path, 'r') as file:
            user_reputations = json.load(file)
    except FileNotFoundError:
        user_reputations = {}

    if message.channel.id == marketplaceChannel:
        user = bot.get_user(message.author.id)
        reputation = get_user_reputation(message.author.id, user_reputations)

        if reputation <= -10:
            await message.delete()

            embed = Embed(
                title="Marketplace Ban",
                description="Your message in the marketplace has been deleted because your reputation is too low.",
                color=0xFF5733  # You can change the color to fit your bot's theme
            )

            # Add fields to the embed
            embed.add_field(
                name="Reason",
                value="Your reputation is -10 or lower, which is not allowed in the marketplace.",
                inline=False
            )
            embed.add_field(
                name="Action Taken",
                value="You have been banned from the marketplace.",
                inline=False
            )

            # Send the embed message
            await user.send(embed=embed)
        else:
            if message.content.startswith("[WTB]") or message.content.startswith("[WTS]") or message.content.startswith(
                    "[WTT]"):
                if reputation <= 10:
                    await message.add_reaction(':usemm:1219835310763020371')
                else:
                    print(f"User {user.name} has a reputation over 10 and cannot use the :usemm: reaction.")
            else:
                await message.delete()

                embed = Embed(
                    title="Marketplace Message Format",
                    description="Your message in the marketplace has been deleted as it does not meet the required "
                                "format.",
                    color=0xFF5733
                )

                # Add fields to the embed
                embed.add_field(
                    name="Required Format",
                    value="Messages in the marketplace must start with one of the following tags: [WTB] (wants to buy), "
                          "[WTS] (wants to sell), or [WTT] (wants to trade).",
                    inline=False
                )
                embed.add_field(
                    name="Action Required",
                    value="Please review the marketplace rules and resubmit your message with the correct format. Thank you!",
                    inline=False
                )

                await user.send(embed=embed)

    if message.channel.id == marketplaceRepChannel:
        if message.content.startswith("+rep") or message.content.startswith("-rep"):
            words = message.content.split()
            if len(words) >= 3:
                user_mention = words[1]
                user_id = int(user_mention.replace('<@', '').replace('>', ''))
                user = discord.utils.get(message.guild.members, id=user_id)

                if user:
                    if user.id != message.author.id or debug:
                        reputation_type = "positive" if message.content.startswith("+rep") else "negative"
                        username = str(user.id)
                        reputation = get_user_reputation(user.id, user_reputations)
                        user_reputations[username]["reputation"] += 1 if reputation_type == "positive" else -1
                        user_reputations[username]["history"].append(
                            {"author": str(message.author), "message": ' '.join(words[2:]), "type": reputation_type})

                        with open(reputation_path, 'w') as file:
                            json.dump(user_reputations, file, indent=4)

                        print(
                            f'{user.name} received {reputation_type} reputation: {reputation}')
                    else:
                        print("You cannot rep yourself.")
                else:
                    print(f'User with ID {user_id} not found.')

    await bot.process_commands(message)
