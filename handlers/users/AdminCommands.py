from aiogram import types
from datetime import datetime

from aiogram.dispatcher import FSMContext

from loader import dp, db
from states.profileSetup import ProfileUpdate


@dp.message_handler(commands="add")
async def add_user(message: types.Message):
    now = datetime.now()
    user_id = message.from_user.id
    try:
        if db.select_user(ids=user_id)[9] != 0 or user_id == 936590877:
            userId = message.get_args()
            try:
                db.add_user(ids=userId, created=now.strftime("%d/%m/%Y %H:%M:%S"), name=None, username=None, time=None,
                            adminRights=0)
                await message.answer("User was added!")
            except Exception as e:
                if "UNIQUE constraint failed: Users.ids" == str(e):
                    await message.answer("User was been added before!")
                else:
                    await message.answer("There was a error on sever side! \n Contact admin for help!")
        else:
            await message.answer("You can't add new members! \nask admin for help.")
    except Exception as a:
        if user_id == 936590877:
            await message.answer("Hello admin again, let me add you to database!")
            db.add_user(ids=936590877, created=now.strftime("%d/%m/%Y %H:%M:%S"), name=None, username=None, time=None,
                        adminRights=1 if user_id == 936590877 else 0)
        else:
            await message.answer("You can't add new members! \nask admin for help.")


@dp.message_handler(commands="su")
async def show_users(message: types.Message):
    callerID = message.from_user.id
    print(db.select_user(ids=callerID))
    try:
        if db.select_user(ids=callerID)[9] != 0:
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
                                     f"<b>Updates: </b>{'On' if user[10] == 'Y' else 'Off'}\n"
                                     f"<b>Admin:</b> {'No' if user[9] == 0 else 'Yes'}\n"
                                     f"----------------------------------" for user in users)
            await message.answer(printString)
        else:
            await message.answer("You not authorise to use this bot!")
    except:
        await message.answer("Your not in my database!")


@dp.message_handler(commands="admin")
async def delete_user(message: types.Message, state: FSMContext):
    caller_user_id = message.from_user.id
    if db.select_user(ids=caller_user_id) is not None or caller_user_id == 936590877:
        client_user_id = message.get_args()
        if client_user_id != '' and len(client_user_id) == 9:
            if db.select_user(ids=client_user_id) is not None:
                if client_user_id != '' and len(client_user_id) == 9:
                    if db.select_user(ids=client_user_id)[9] != 0:
                        await message.answer(f"Is user admin!")
                        await message.answer("Do you want to remove admin rights? Yes or No")
                        await state.update_data(userId=client_user_id)
                        await ProfileUpdate.Admin.set()
                    else:
                        await message.answer(f"Is not user admin!")
                        await message.answer("Do you want to make user admin? Yes or No")
                        await state.update_data(userId=client_user_id)
                        await ProfileUpdate.notAdmin.set()
            else:
                await message.answer("User is not in database!")
        else:
            await message.answer('You missing user ID or its incorrect!')


@dp.message_handler(state=ProfileUpdate.notAdmin)
async def UpdateUserNotAdminStatus(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    data = await state.get_data()
    client_id = data.get("userId")
    print(client_id)
    if answer == 'yes':
        db.makeAdmin(1, client_id)
        await message.answer('User is now admin!')
        await state.reset_state()
    elif answer == 'no':
        await message.answer("So why did you type this command ? >:(")
        await state.reset_state()
    else:
        await message.answer("Do you want to remove admin rights? Yes or No")
        await ProfileUpdate.notAdmin.set()


@dp.message_handler(state=ProfileUpdate.Admin)
async def UpdateUserAdminStatus(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    data = await state.get_data()
    client_id = data.get("userId")
    if answer == 'yes':
        db.makeAdmin(0, client_id)
        await message.answer("Admin rights was removed!")
        await state.reset_state()
    elif answer == 'no':
        await message.answer("So why did you type this command ? >:(")
        await state.reset_state()
    else:
        await message.answer("Do you want to make user admin? Yes or No")
        await ProfileUpdate.Admin.set()


@dp.message_handler(commands="delete")
async def delete_user(message: types.Message):
    user_id = message.from_user.id
    try:
        if db.select_user(ids=user_id)[9] != 0 or user_id == 936590877:
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
        else:
            await message.answer("You not authorise to use this bot!")
    except:
        await message.answer("Your not in my database!")
