from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", ""),
        types.BotCommand("setup", "Setup trading profile"),
        types.BotCommand("time", "Update refresh time"),
        types.BotCommand("tokenA", "Update token A (First token)"),
        types.BotCommand("tokenB", "Update token B (Secound token)"),
        types.BotCommand("amount", "Update trading amount"),
        types.BotCommand("add", "Add user to bot (Admins Only)"),
        types.BotCommand("delete", "Delete user from bot (Admins Only)"),
        types.BotCommand("su", "Show users profiles (Admins Only)"),

    ])
