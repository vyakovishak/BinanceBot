from aiogram import types
from datetime import datetime
from loader import dp, db


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
