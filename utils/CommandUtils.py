def add_command_if_not_exists(bot, command_name, command_func):
    if not bot.get_command(command_name):
        bot.add_command(command_func)