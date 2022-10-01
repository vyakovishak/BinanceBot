from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileSetup(StatesGroup):
    userTime = State()
    tokenA = State()
    yan = State()
    tokenB = State()
    dollarAmount = State()
    crossExchange = State()
    final = State()