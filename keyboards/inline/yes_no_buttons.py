from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import yan_callback

yea_and_no_choice = InlineKeyboardMarkup(row_width=2,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="Yes",
                                                     callback_data=yan_callback.new(choice_name='Yes', value="Y")
                                                 ),
                                                 InlineKeyboardButton(
                                                     text="No",
                                                     callback_data=yan_callback.new(choice_name='No', value="N")
                                                 )

                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="Cancel",
                                                     callback_data=yan_callback.new(choice_name='Cancel', value="C")
                                                 )
                                             ]
                                         ])
