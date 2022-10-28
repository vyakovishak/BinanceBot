import re

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import db


async def asMinutes(bot: Bot, scheduler: AsyncIOScheduler, minute, user_id):
    scheduler.add_job(sendPairsToUsers, 'interval', minutes=minute, args=(bot, user_id))


async def asHour(bot: Bot, scheduler: AsyncIOScheduler, hour, user_id):
    scheduler.add_job(sendPairsToUsers, 'interval', hours=hour, args=(bot, user_id))


async def asDay(bot: Bot, scheduler: AsyncIOScheduler, day, user_id):
    scheduler.add_job(sendPairsToUsers, 'interval', days=day, args=(bot, user_id))


async def sendPairsToUsers(bot, user_id):
    await bot.send_message(user_id, "hi")


async def on_startup(scheduler: AsyncIOScheduler):
    scheduler.start()


async def on_shutdown(scheduler):
    scheduler.shutdown


async def updateTradingData(bot: Bot, scheduler: AsyncIOScheduler, restart=False):
    userList = db.select_all_users()
    for user in userList:
        print(user[10])
        if user[10] == "Y" and restart == False:
            try:
                userTime = re.split('(\d+)', user[4])
                number = int(userTime[1])
                timeFormat = userTime[2]
                if timeFormat.lower() == "m":
                    await asMinutes(bot, scheduler, number, user[0])
                elif timeFormat.lower() == "h":
                    await asHour(bot, scheduler, number, user[0])
                elif timeFormat.lower() == "d":
                    await asDay(bot, scheduler, number, user[0])
            except Exception as e:
                print(e)
                await bot.send_message(user[0], "You dont have time setup yet!\nUsing this default time 5m")
                await asMinutes(bot, scheduler, 5, user[0])
