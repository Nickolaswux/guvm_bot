from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import tokenbot, Text_serv, Dict_serv, asyncio, keyboards_serv


class Form(StatesGroup):
    lang = State()
    service = State()
    subservice = State()
    subservice_2 = State()

TOKEN = tokenbot.TOKONBOT

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

LANGS = ['🇷🇺 Русский 🇷🇺', '🇬🇧 English 🇬🇧']
SERVICES = Dict_serv.SRV1
SUBSERVICES = Dict_serv.SRV2
SUBSERVICES_2 = Dict_serv.SRV3
GREETINGS = {
    "🇷🇺 Русский 🇷🇺": "Добро пожаловать!",
    "🇬🇧 English 🇬🇧": "Welcome!"
}

def generate_keyboard(options, back_button=True, home_button=True):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text=option, callback_data=option) for option in options]
    if back_button:
        buttons.append(types.InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    if home_button:
        buttons.append(types.InlineKeyboardButton(text="🏠 Домой", callback_data="home"))
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await Form.lang.set()
    await bot.send_message(chat_id=message.chat.id, text="Выберите язык / Choose a language:",
                           reply_markup=generate_keyboard(LANGS, back_button=False, home_button=False))

@dp.callback_query_handler(lambda c: c.data in LANGS, state=Form.lang)
async def process_lang_choose(callback_query: types.CallbackQuery, state: FSMContext):
    await Form.service.set()
    chosen_lang = callback_query.data
    await state.update_data(chosen_lang=chosen_lang)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text=GREETINGS[chosen_lang] + " Выберите пункт меню:",
                                reply_markup=generate_keyboard(SERVICES[chosen_lang], back_button=False, home_button=True))

@dp.callback_query_handler(lambda c: any(c.data in service_list for service_list in SERVICES.values()), state=Form.service)
async def process_service_choose(callback_query: types.CallbackQuery, state: FSMContext):
    await Form.subservice.set()
    chosen_service = callback_query.data
    await state.update_data(chosen_service=chosen_service)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text=f"You've chosen: {chosen_service}. Please choose the subservice:",
                                reply_markup=generate_keyboard(SUBSERVICES[chosen_service]))

@dp.callback_query_handler(lambda c: any(c.data in subservice_list for subservice_list in SUBSERVICES.values()), state=Form.subservice)
async def process_subservice_choose(callback_query: types.CallbackQuery, state: FSMContext):
    await Form.subservice_2.set()
    chosen_subservice = callback_query.data
    await state.update_data(chosen_subservice=chosen_subservice)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text=f"You've chosen: {chosen_subservice}. Please choose the next subservice:",
                                reply_markup=generate_keyboard(SUBSERVICES_2[chosen_subservice]))

# @dp.callback_query_handler(lambda c: any(c.data in subservice_2_list for subservice_2_list in SUBSERVICES_2.values()), state=Form.subservice_2)
# async def process_subservice_2_choose(callback_query: types.CallbackQuery, state: FSMContext):
#     chosen_subservice_2 = callback_query.data
#     await bot.edit_message_text(chat_id=callback_query.from_user.id,
#                                 message_id=callback_query.message.message_id,
#                                 text=f"You've chosen: {chosen_subservice_2}.")

# конечные хэндлеры
@dp.callback_query_handler(lambda c: c.data == "Внутренний паспорт", state=Form.subservice_2)
async def inner_passport_handler(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text=Text_serv.iner_pasp_txt1,
                                parse_mode='HTML',
                                )
    await asyncio.sleep(2)
    await bot.send_message(chat_id=callback_query.from_user.id,
                                #message_id=callback_query.message.message_id,
                                text=Text_serv.iner_pasp_txt2,
                                parse_mode='HTML',
                                reply_markup=generate_keyboard([], back_button=True, home_button=True))

@dp.callback_query_handler(lambda c: c.data == "Загранпаспорт", state=Form.subservice_2)
async def inner_inpassport_handler(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text=Text_serv.forein_pasp_txt1,
                                parse_mode='HTML')

    await asyncio.sleep(2)
    await bot.send_message(chat_id=callback_query.from_user.id,
                                #message_id=callback_query.message.message_id,
                                text=Text_serv.forein_pasp_txt2,
                                parse_mode='HTML')

    await asyncio.sleep(2)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           # message_id=callback_query.message.message_id,
                           text=Text_serv.forein_pasp_txt3,
                           parse_mode='HTML')

    await asyncio.sleep(2)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           # message_id=callback_query.message.message_id,
                           text=Text_serv.forein_pasp_txt4,
                           parse_mode='HTML')

    await asyncio.sleep(2)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           # message_id=callback_query.message.message_id,
                           text=Text_serv.forein_pasp_txt5,
                           parse_mode='HTML',
                           reply_markup=generate_keyboard([], back_button=True, home_button=True))
@dp.callback_query_handler(lambda c: c.data == "Регистрация по месту проживания", state=Form.subservice_2)
async def living_place_handler(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text='Я узнал, что в моем жилом помещении прописан неизвестный мне человек. Что в этом случае необходимо сделать?',
                                parse_mode='HTML', reply_markup=keyboards_serv.living_key1
                                )

    await bot.send_message(chat_id=callback_query.from_user.id,
                                #message_id=callback_query.message.message_id,
                                text='Я хочу снять с регистрационного учета одного из жильцов. Как это сделать?',
                                parse_mode='HTML', reply_markup=keyboards_serv.living_key2
                           )
    await bot.send_message(chat_id=callback_query.from_user.id,
                                #message_id=callback_query.message.message_id,
                                text='Переезд в другой регион',
                                parse_mode='HTML', reply_markup=keyboards_serv.living_key3
                           )


@dp.message_handler(commands=['start'], state="*")
async def start_command(message: types.Message, state: FSMContext):
    await state.finish()
    await Form.lang.set()
    await bot.send_message(chat_id=message.chat.id, text="Выберите язык / Choose a language:", reply_markup=generate_keyboard(LANGS, home_button=True))

# Обработчики выбора языка, услуги, подуслуги и т. д.

@dp.callback_query_handler(lambda c: c.data == "back", state="*")
async def back_button_pressed(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()

    if current_state is None:
        return

    if current_state == Form.subservice_2.state:
        await Form.subservice.set()
        # Код для возврата к выбору подуслуги
        chosen_subservice = data.get('chosen_subservice')
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=f"Вы выбрали: {chosen_subservice}. Выберите дальнейшую подуслугу:",
                                    reply_markup=generate_keyboard(SUBSERVICES[chosen_subservice], back_button=True, home_button=True))

    elif current_state == Form.subservice.state:
        await Form.service.set()
        # Код для возврата к выбору услуги
        chosen_lang = data.get('chosen_lang')
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=GREETINGS[chosen_lang] + " Теперь выберите пункт меню:",
                                    reply_markup=generate_keyboard(SERVICES[chosen_lang], back_button=True, home_button=True))

    elif current_state == Form.service.state:
        await Form.lang.set()
        # Код для возврата к выбору языка
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text="Выберите язык / Choose a language:",
                                    reply_markup=generate_keyboard(LANGS, home_button=True))

@dp.callback_query_handler(lambda c: c.data == "home", state="*")
async def home_button_pressed(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await Form.lang.set()
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text="Выберите язык / Choose a language:",
                                reply_markup=generate_keyboard(LANGS, home_button=True))

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
