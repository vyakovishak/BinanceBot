from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from utils import scheduleHandler


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
