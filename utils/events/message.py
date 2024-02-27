from random import random


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

    await bot.process_commands(message)
