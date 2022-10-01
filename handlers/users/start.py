from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from datetime import datetime
from loader import dp, db
from states import ProfileSetup


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    if db.select_user(ids=user_id) is not None:
        await message.answer(f'Hello, {message.from_user.full_name}!')
    else:
        await message.answer("You not authorise to use this bot!")


@dp.message_handler(Command("setup"))
async def setup_user_profile_question(message: types.Message):
    await message.answer("Before you can use this bot let's set it up first!\n"
                         "How offend you want to get updates?\n"
                         "Please follow this format number and type\n"
                         "Example:"
                         "1m - 1 minute\n"
                         "1h - 1 hour\n"
                         "1d - 1 day")

    await ProfileSetup.userTime.set()
    # await ProfileSetup.first()


@dp.message_handler(state=ProfileSetup.userTime)
async def setup_user_profile_userTime_question(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(userTimeAns=answer)

    await message.answer("Send me a name of Token A that you want to enter with? Exp. USDT, BTC, BNB etc.")
    await ProfileSetup.tokenA.set()


@dp.message_handler(state=ProfileSetup.tokenA)
async def setup_user_profile_tokenA_question(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(tokenAAns=answer)
    await message.answer("Do you want to pair your starting token? Yes or No")
    await ProfileSetup.yan.set()


@dp.message_handler(state=ProfileSetup.yan)
async def setup_user_profile_yesAndNo_question(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(yanAns=answer)
    if answer.lower() == "yes":
        await message.answer("Please send me a second token name:")
        await ProfileSetup.tokenB.set()
    elif answer.lower() == "no":
        await message.answer("What amount of dollars you tying to trade?")
        await ProfileSetup.dollarAmount.set()
    else:
        await message.answer("Do you want to pair your starting token? Yes or No")
        await ProfileSetup.yan.set()


@dp.message_handler(state=ProfileSetup.tokenB)
async def setup_user_profile_tokenB_question(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(tokenBAns=answer)
    await message.answer("What amount of dollars you tying to trade?")
    await ProfileSetup.dollarAmount.set()


@dp.message_handler(state=ProfileSetup.dollarAmount)
async def setup_user_profile_dollarAmount_question(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(dollarAmountAns=answer)

    data = await state.get_data()
    q1 = data.get("userTimeAns")
    q2 = data.get("tokenAAns")
    q3 = data.get("tokenBAns")
    q4 = data.get("dollarAmountAns")
    q5 = data.get("yanAns")

    await message.answer(f"First Token:  {q2}\n"
                         f"Second Token: {q3}\n"
                         f"Make a pair?: {q5}\n"
                         f"Trade Amount: {q4}\n"
                         f"Refresh Time: {q1}\n\n"
                         f"Did i got everything right? Yes and No")

    await ProfileSetup.final.set()


@dp.message_handler(state=ProfileSetup.final)
async def setup_user_profile_Final_question(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(final=answer)

    data = await state.get_data()
    q1 = data.get("userTimeAns")
    q2 = data.get("tokenAAns")
    q3 = data.get("tokenBAns")
    q4 = data.get("dollarAmountAns")
    q5 = data.get("yanAns")
    if answer.lower() == "no":
        await message.answer("Okay let's start from the begging /setup")
        await state.finish()
        await state.reset_state(with_data=True)
    elif answer.lower() == "yes":
        db.update_user(message.from_user.id, q1, q2, q3, q4)
        await message.answer("Saved !")
        await state.finish()
        await state.reset_state(with_data=True)
    else:
        await message.answer("I didn't get that...")

        await message.answer(f"First Token:  {q2}\n"
                             f"Second Token: {q3}\n"
                             f"Make a pair?: {q5}\n"
                             f"Trade Amount: {q4}\n"
                             f"Refresh Time: {q1}\n\n"
                             f"Did i got everything right? Yes and No")
        await ProfileSetup.final.set()
