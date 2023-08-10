from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

living_key1 = InlineKeyboardMarkup()
living_key2 = InlineKeyboardMarkup()
living_key3 = InlineKeyboardMarkup()

button1 = InlineKeyboardButton("Далее", callback_data="data_1")
button2 = InlineKeyboardButton("Далее ▶️", callback_data="data_2")
button3 = InlineKeyboardButton("Далее ➡️", callback_data="data_3")

living_key1.add(button1)
living_key2.add(button2)
living_key3.add(button3)