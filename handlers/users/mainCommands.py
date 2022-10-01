from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from states.profileSetup import ProfileUpdate


@dp.message_handler(commands="time")
async def startUpdateUserTime(message: types.Message):
    user_id = message.from_user.id
    if db.select_user(ids=user_id) is not None:
        await message.answer("Send me a time using this format: \n"
                             "1m - 1 minute\n"
                             "1h - 1 hour\n"
                             "1d - 1 day")
        await ProfileUpdate.updateUserTime.set()
    else:
        await message.answer("Your not in my database!")


@dp.message_handler(state=ProfileUpdate.updateUserTime)
async def endUpdateUserTime(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(updateUserTimeAns=answer)
    db.update_Time(answer, message.from_user.id)
    await state.reset_state()
    await message.answer(f'Time was update to {answer}')


@dp.message_handler(commands="tokena")
async def startUpdateUserTokenA(message: types.Message):
    user_id = message.from_user.id
    if db.select_user(ids=user_id) is not None:
        await message.answer("Send me a token A Symbol(Exp. USDT, USDC, BUSD, etc..")
        await ProfileUpdate.updateTokenA.set()
    else:
        await message.answer("Your not in my database!")


@dp.message_handler(state=ProfileUpdate.updateTokenA)
async def endUpdateUserTokenA(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(updateTokenAAns=answer)
    db.update_TokenA(answer, message.from_user.id)
    await state.reset_state()
    await message.answer(f'Token A was update to {answer}')


@dp.message_handler(commands="tokenB")
async def startUpdateUserTokenB(message: types.Message):
    user_id = message.from_user.id
    if db.select_user(ids=user_id) is not None:
        await message.answer("Send me a token B Symbol(Exp. USDT, USDC, BUSD, etc..")
        await ProfileUpdate.updateTokenB.set()
    else:
        await message.answer("Your not in my database!")


@dp.message_handler(state=ProfileUpdate.updateTokenB)
async def endUpdateUserTokenB(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(updateTokenAAns=answer)
    db.update_TokenB(answer, message.from_user.id)
    await state.reset_state()
    await message.answer(f'Token B was update to {answer}')


@dp.message_handler(commands="amount")
async def startUpdateUserDollarAmount(message: types.Message):
    user_id = message.from_user.id
    if db.select_user(ids=user_id) is not None:
        await message.answer("Send me new trading amount")
        await ProfileUpdate.updateDollarAmount.set()
    else:
        await message.answer("Your not in my database!")


@dp.message_handler(state=ProfileUpdate.updateDollarAmount)
async def endUpdateUserDollarAmount(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(updateTokenAAns=answer)
    db.update_DollarAmount(answer, message.from_user.id)
    await state.reset_state()
    await message.answer(f'Dollar amount was update to {answer}')


@dp.message_handler(commands="my")
async def showUserProfile(message: types.Message):
    user_id = message.from_user.id
    try:
        if db.select_user(ids=user_id)[9] != 0 or user_id == 936590877:
            user = db.select_user(ids=user_id)
            await message.answer(f"<b>ID:</b> {user[0]}\n"
                                 f"<b>Created At:</b> {user[1]}\n"
                                 f"<b>Name:</b> {user[2]}\n"
                                 f"<b>Username:</b> {user[3]}\n"
                                 f"<b>Time:</b> {user[4]}\n"
                                 f"<b>Token A:</b> {user[5]}\n"
                                 f"<b>Token B:</b> {user[6]}\n"
                                 f"<b>Dollar Amount:</b> {user[7]}\n"
                                 f"<b>Cross Exchange:</b> {user[8]}\n")
        else:
            await message.answer("You not authorise to use this bot!")
    except:
        await message.answer("Your not in my database!")


@dp.message_handler(commands="myid")
async def showUserProfile(message: types.Message):
    await message.answer(f"Click to copy your id <code>{message.from_user.id}</code>")
