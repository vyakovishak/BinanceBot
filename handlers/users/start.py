from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from datetime import datetime
from loader import dp, db
from states import ProfileSetup


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    if None != db.select_user(ids=user_id):
        await message.answer(f'Hello, {message.from_user.full_name}!')
    else:
        await message.answer("You not authorise to use this bot!")


@dp.message_handler(commands="add")
async def add_user(message: types.Message):
    now = datetime.now()
    if message.from_user.id == 936590877:
        userId = message.get_args()
        try:
            db.add_user(ids=userId, created=now.strftime("%d/%m/%Y %H:%M:%S"), name=1, username=2, time=3)
            await message.answer("User was added!")
        except Exception as e:
            print(e)
            if "UNIQUE constraint failed: Users.ids" == str(e):
                await message.answer("User was been added before!")
            else:
                await message.answer("There was a error on sever side! \n Contact admin for help!")
    else:
        await message.answer("You can't add new members! \nask admin for help.")


@dp.message_handler(commands="su")
async def show_users(message: types.Message):
    users = db.select_all_users()
    printString = ''
    printString += "\n".join(f"<b>ID:</b> {user[0]}\n"
                             f"<b>Created At:</b> {user[1]}\n"
                             f"<b>Name:</b> {user[2]}\n"
                             f"<b>Username:</b> {user[3]}\n"
                             f"<b>Time:</b> {user[4]}\n"
                             f"<b>Token A:</b> {user[5]}\n"
                             f"<b>Token B:</b> {user[6]}\n"
                             f"<b>Dollar Amount:</b> {user[7]}\n"
                             f"<b>Cross Exchange:</b> {user[8]}\n"
                             f"----------------------------------" for user in users)

    await message.answer(printString)


@dp.message_handler(commands="delete")
async def delete_user(message: types.Message):
    if message.get_args() != "True" or message.get_args() != "true":
        user_id = message.get_args()
        db.delete_user(user_id)
        await message.answer('User was deleted')
    else:
        db.delete_all_users()


@dp.message_handler(Command("setup"))
async def setup_user_profile_time_question(message: types.Message):
    await message.answer("Before you can use this bot let's set it up first!\n"
                         "How offend you want to get updates?\n"
                         "Please follow this format number and type\n"
                         "Example:"
                         "1m - 1 minute\n"
                         "1h - 1 hour\n"
                         "1d - 1 day")

    await ProfileSetup.userTime.set()
    # await ProfileSetup.first()


@dp.message_handler(states=ProfileSetup.userTime)
async def setup_user_profile_tokenA_question(message: types.Message):
    await message.answer("Send me a name of token that you want to enter with? Exp. USDT, BTC, BNB etc.")
    await ProfileSetup.tokenA.set()


@dp.message_handler(states=ProfileSetup.tokenA)
async def setup_user_profile_tokenA_question(message: types.Message):
    await message.answer("Do you want to use a pair? Yes or No")
    if str(message.text).lower() == 'yes':
        await message.answer("Send me a pair like this USDT/BTC")
        await ProfileSetup.tokenB.set()
    else:
        await ProfileSetup.next()

@dp.message_handler(states=ProfileSetup.tokenA)
async def setup_user_profile_tokenA_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q1 = data.get()
    q2
    q3
