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


@dp.message_handler(commands="add")
async def add_user(message: types.Message):
    now = datetime.now()
    if message.from_user.id == 936590877:
        userId = message.get_args()
        try:
            db.add_user(ids=userId, created=now.strftime("%d/%m/%Y %H:%M:%S"), name=None, username=None, time=None)
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
    if message.get_args().lower() != '':
        if str(message.get_args()).lower() != "true":
            user_id = message.get_args()
            db.delete_user(user_id)
            await message.answer('User was deleted')
        else:
            db.delete_all_users()
            await message.answer("All user deleted")
    else:
        await message.answer("To delete user add user id after delete command\n\n"
                             "To delete ALL users add TRUE after delete command")


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
