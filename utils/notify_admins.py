import logging

from aiogram import Dispatcher
from loader import db


async def on_startup_notify(dp: Dispatcher):
    admins = db.select_users(adminRights=1)
    for admin in admins:
        try:
            await dp.bot.send_message(admin[0], "Бот Запущен и готов к работе")
        except Exception as err:
            pass

