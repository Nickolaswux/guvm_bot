from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove

import aiogram.utils.markdown as mar
import Text_serv, asyncio, logging
from tokenbot import TOKONBOT, MESSAGE_GROUP, TOKONBOT_POST
from keyboards_serv import key_s, underline_keyboard, confirm_keyboard

token = TOKONBOT
group_id = MESSAGE_GROUP
token_post = TOKONBOT_POST
group_id_guvm ='-1002022336658'

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

bot_post = Bot(token=token_post, parse_mode='HTML')
dp_post = Dispatcher(bot_post)

async def send_and_save_messages(user_id, message_texts, keyboards, storage):
    message_ids = []
    for text, keyboard in zip(message_texts, keyboards):
        message = await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
        message_ids.append(message.message_id)
    storage[user_id] = message_ids


async def delete_previous_messages(user_id, storage):
    message_ids = storage.get(user_id, [])
    for message_id in message_ids:
        await bot.delete_message(chat_id=user_id, message_id=message_id)
    storage.pop(user_id, None)


async def send_section_messages(user_id, callback_query, message_texts, keyboards):
    await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
    for text, keyboard in zip(message_texts, keyboards):
        await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
@dp_post.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Выберите язык / Choose a language:",
                           reply_markup=key_s["lang_key"])

    await bot.send_message(chat_id=message.chat.id, text="*",
                           reply_markup=ReplyKeyboardRemove())

#обработка команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Выберите язык / Choose a language:",
                           reply_markup=key_s["lang_key"])

    await bot.send_message(chat_id=message.chat.id, text="*",
                           reply_markup=ReplyKeyboardRemove())


@dp.message_handler(lambda message: not any(symbol in message.text for symbol in ['✉', '🏠']))
async def store_user_message(message: types.Message):
    last_user_messages[message.from_user.id] = mar.quote_html(message.text)

#обработчик для отправки сообщения по конверту
@dp.message_handler(lambda message: '✉' in message.text)
async def send_user_message(message: types.Message):
    user_message = last_user_messages.get(message.from_user.id)
    error_txt = ''
    qwest_txt = ''
    lang = user_languages.get(message.from_user.id, 'rus')
    if not user_message or user_message.strip() == '':

        if lang == 'rus':
            error_txt = "Вы не написали сообщение или ваше сообщение пустое. Пожалуйста, отправьте сообщение боту и нажмите ✉ снова."
        elif lang == 'eng':
            pass
        await message.answer(error_txt)
        return
    else:
        if lang == 'rus':
            qwest_txt = f'''<b>Отправить Ваше сообщение?</b>
            "{user_message[:4000]}"...
            в ГУВМ МВД России?'''
        elif lang == 'eng':
            pass
        await bot.send_message(chat_id=message.chat.id, text=qwest_txt, reply_markup=confirm_keyboard)

#Обработка кнопки домой
@dp.message_handler(lambda message: '🏠' in message.text)
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Выберите язык / Choose a language:",
                           reply_markup=key_s["lang_key"], )
    await bot.send_message(chat_id=message.chat.id, text="*",
                           reply_markup=ReplyKeyboardRemove())
#выбран русский язык
@dp.callback_query_handler(text="rus")
async def choose_section_rus(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_languages[callback_query.from_user.id] = 'rus'
    message_texts = [f'''<b>Выберите раздел:</b>
    
1️⃣ Для граждан России.
2️⃣ Для иностранных граждан.
❌3️⃣ Для граждан Украины, ЛНР, ДНР, Херсонской области, Запорожской области.
❌4️⃣ Для Юридических лиц и индивидуальных предпринимателей.
{Text_serv.ru_ancor_bottom}''',

    ]
    keyboards = [key_s['ru_rf_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="<b>❗️❗️❗️ Чтоб отправить свое сообщение в ГУВМ МВД России, отправьте его в чат боту, после чего нажмите ✉ на нижней клавиатуре</b>",
                           reply_markup=underline_keyboard)

#нажата кнопка да, для подтверждения отпраки сообщения в ГУВМ
@dp.callback_query_handler(lambda query: query.data == "confirm_yes")
async def confirm_send(query: types.CallbackQuery):
    user_message = last_user_messages.get(query.from_user.id)
    user_mention = f'<a href="tg://user?id={query.from_user.id}">{query.from_user.first_name}</a>'
    await bot.edit_message_text("*", chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=None)
    await bot.send_message(chat_id=query.from_user.id, text="Отправка сообщения...", reply_markup=ReplyKeyboardRemove())
    await bot.send_message(group_id, f"Сообщение от {user_mention}: {user_message}")

    await asyncio.sleep(5)
    await bot.answer_callback_query(query.id, "Сообщение отправлено.")
    await bot.send_message(chat_id=query.from_user.id, text="Сообщение отправлено.", reply_markup=underline_keyboard)

#Нажата кнопка нет, для отмены отправки сообщения в ГУВМ
@dp.callback_query_handler(lambda query: query.data == "confirm_no")
async def cancel_send(query: types.CallbackQuery):
    await bot.edit_message_text("Отправка отменена.", chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=None)
    await bot.answer_callback_query(query.id, "Отправка отменена.")
    await bot.send_message(chat_id=query.from_user.id, text="Чтоб отправить свое сообщение в ГУВМ МВД России, отправьте его в чат боту, после чего нажмите ✉ на нижней клавиатуре", reply_markup=underline_keyboard)

#Русский язык - для граждан РФ
@dp.callback_query_handler(text="ru_rf")
async def query_ru_rf(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''<b>Где Вы сейчас находитесь?</b>
1️⃣ В Российской Федерации
❌2️⃣ За пределами Российской Федерации
{Text_serv.ru_ancor_bottom}                                       ᅠ ᅠ '''
    ]
    keyboards = [key_s['ru_rf_in_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации
@dp.callback_query_handler(text="ru_rf_in")
async def query_ru_rf_in(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''<b>Выберите нужный раздел</b>
1️⃣ Внутренний паспорт 
2️⃣ Загранпаспорт
3️⃣ Регистрация по месту проживания
4️⃣ Я стал участником Государственной программы по оказанию содействия добровольному переселению в Российскую федерацию соотечественников, проживающих за рубежом, на территории иностранного государства
❌5️⃣ Я и(или) члены моей семьи - вынужденные переселенцы
❌6️⃣ Член моей семьи или близкий родственник - иностранный гражданин
❌7️⃣ Я хочу оформить выход из гражданства Российской Федерации
{Text_serv.ru_ancor_bottom}'''
]
    keyboards = [key_s['ru_rf_in_pasp_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт
@dp.callback_query_handler(text="ru_rf_in_pasp")
async def query_ru_rf_in_pasp(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''<b>В разделе часто задаваемые вопросы даны короткие ответы и разъяснения.</b>

<b>В разделе жизненные ситуации Вы найдете инструкции</b>,
1️⃣ Часто задаваемые вопросы                                       ᅠ ᅠ ',
2️⃣ Жизненные ситуации                                         ᅠ ᅠ ',
{Text_serv.ru_ancor_bottom}                                                              '''
    ]
    keyboards = [key_s['ru_rf_in_pasp_faq_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - ЧаВо
@dp.callback_query_handler(text="ru_rf_in_pasp_faq")
async def query_ru_rf_in_pasp_faq(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.iner_pasp_txt1, Text_serv.iner_pasp_txt2]
    keyboards = [None, key_s['ru_rf_in_pasp_1_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации
@dp.callback_query_handler(text="ru_rf_in_pasp_sit")
async def query_ru_rf_in_pasp_sit(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
1️⃣ Я хочу оформить паспорт
2️⃣ Украли паспорт, что делать?
3️⃣ Я потерял паспорт, что делать?
4️⃣ Я просрочил замену паспорта
5️⃣ Отказали в выдаче
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_1_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen")
async def query_ru_rf_in_pasp_sit_oformlen(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
1️⃣ У меня изменилась фамилия, имя или отчество.
2️⃣ Паспорт испорчен
3️⃣ У меня изменилась внешность
4️⃣ Замена паспорта гражданина СССР
5️⃣ Исполнилось 20 или 45 лет
6️⃣ Получение паспорта в 14 лет впервые
7️⃣ Я обнаружил ошибку в паспорте
8️⃣ У меня изменилось место или дата рождения

<b>Что делать, если причин несколько?</b>
Если вы одновременно сменили ФИО и вам исполнилось 20 или 45 лет, выберите 1️⃣ «Изменились фамилия, имя или отчество»
Если паспорт испорчен и вам исполнилось 20 или 45 лет, у вас изменилась внешность или закончилось место для штампов, выберите 2️⃣ «Паспорт испорчен»
В остальных случаях подать заявление можно только лично.
Запишитесь на приём в МФЦ или в МВД для оформления паспорта
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_tf_pasp_sit_oformlen_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-изменились ФИО
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_fio")
async def query_ru_rf_in_pasp_sit_oformlen_fio(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
1️⃣ Замена ФИО в связи с заключением брака
2️⃣ Замена ФИО в связи с зрасторжением брака
3️⃣ Другие причины
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_sit_oformlen_fio_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-изменились ФИО-брак
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_fio_brak")
async def query_ru_rf_in_pasp_sit_oformlen_fio_brak(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit1}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_sit_oformlen_fio_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)
#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-изменились ФИО-развод
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_fio_unbrak")
async def query_ru_rf_in_pasp_sit_oformlen_fio_unbrak(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit2}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_sit_oformlen_fio_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-изменились ФИО-другие причины
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_fio_another")
async def query_ru_rf_in_pasp_sit_oformlen_fio_another(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit3}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_sit_oformlen_fio_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-паспорт испорчен
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_neprigoden")
async def query_ru_rf_in_pasp_sit_neprigoden(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit4}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_sit_oformlen_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-смена внешности
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_vneshnost")
async def query_ru_rf_in_pasp_sit_oformlen_vneshnost(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit5}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_sit_oformlen_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-паспорт cccp
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_ussr")
async def query_ru_rf_in_pasp_sit_oformlen_ussr(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit6}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_sit_oformlen_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-20-45
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_2045")
async def query_ru_rf_in_pasp_sit_oformlen_2045(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit7}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_sit_oformlen_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-14 впервые
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_14")
async def query_ru_rf_in_pasp_sit_oformlen_14(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit8}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_sit_oformlen_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-ошибка в паспорте
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_mistake")
async def query_ru_rf_in_pasp_sit_oformlen_mistake(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit9}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_sit_oformlen_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-оформить паспорт-изменилось место или дата рождениЯ
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_oformlen_izmdata")
async def query_ru_rf_in_pasp_sit_oformlen_izmdata(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit10}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_in_pasp_sit_oformlen_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-украли паспорт
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_ukraly")
async def query_ru_rf_in_pasp_sit_ukraly(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit11}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_pasp_sit_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации-потерял паспорт
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_poteral")
async def query_ru_rf_in_pasp_sit_poteral(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit12}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_pasp_sit_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации- просрочил подачу
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_prosrochil")
async def query_ru_rf_in_pasp_sit_prosrochil(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit13}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_pasp_sit_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Внутренний паспорт - Жизненные ситуации- отказали
@dp.callback_query_handler(text="ru_rf_in_pasp_sit_otkaz")
async def query_ru_rf_in_pasp_sit_otkaz(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''
{Text_serv.iner_pasp_sit14}
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s['ru_rf_pasp_sit_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Заграничный паспорт
@dp.callback_query_handler(text="ru_rf_in_zp")
async def query_ru_rf_in_zp(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'''<b>В разделе часто задаваемые вопросы даны короткие ответы и разъяснения.</b>

<b>В разделе жизненные ситуации Вы найдете инструкции</b>
1️⃣ Часто задаваемые вопросы                                       ᅠ ᅠ ',
2️⃣ Жизненные ситуации                                         ᅠ ᅠ ',
{Text_serv.ru_ancor_bottom}                                                                  ᅠ ᅠ '''
    ]
    keyboards = [key_s['ru_rf_in_zp_faq_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Заграничный паспорт - ЧаВо
@dp.callback_query_handler(text="ru_rf_in_zp_faq")
async def query_ru_rf_in_zp_faq(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [key_s['ru_rf_in_zp_1_back_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Заграничный паспорт - Жизненные ситуации
@dp.callback_query_handler(text="ru_rf_in_zp_sit")
async def query_ru_rf_in_zp_sit(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''<b>В разделе жизненные ситуации Вы найдете инструкции</b>
    
1️⃣ Я хочу оформить загранпаспорт себе или своему ребенку
2️⃣ Мне надо сдать загарнпаспорт на хранение
3️⃣ У меня есть проблема с загранпаспортом
4️⃣ Мне нужен второй загранпаспорт
    {Text_serv.ru_ancor_bottom}''']
    keyboards = [key_s["ru_rf_in_zp_sit_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


# Русский язык - для граждан РФ - В Российской Федерации - Заграничный паспорт - Жизненные ситуации-оформление
@dp.callback_query_handler(text="ru_rf_in_zp_sit_oformlen")
async def query_ru_rf_in_zp_sit_oformlen(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''{Text_serv.forein_pasp_sit1}
1️⃣ Загранпаспорт нового поколения
2️⃣ Загранпаспорт старого поколения
{Text_serv.ru_ancor_bottom}''']
    keyboards = [key_s["ru_rf_in_zp_sit_oformlen_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

# Русский язык - для граждан РФ - В Российской Федерации - Заграничный паспорт - Жизненные ситуации-оформление
@dp.callback_query_handler(text="ru_rf_in_zp_sit_oformlen_new")
async def query_ru_rf_in_zp_sit_oformlen_new(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''<b>Кому требуется оформить загранпаспорт?</b>
1️⃣ Мне
2️⃣ Детям
3️⃣ Недееспособному лицу
4️⃣ Другому человеку
{Text_serv.ru_ancor_bottom}''']
    keyboards = [key_s["ru_rf_in_zp_sit_oformlen_new_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Регистрация по месту пребывания
@dp.callback_query_handler(text="ru_rf_in_regliv")
async def query_ru_rf_in_regliv(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
f'''<b>В разделе часто задаваемые вопросы даны короткие ответы и разъяснения.</b>

<b>В разделе жизненные ситуации Вы найдете инструкции</b>
1️⃣ Часто задаваемые вопросы                                       ᅠ ᅠ 
2️⃣ Жизненные ситуации                                         ᅠ ᅠ 
{Text_serv.ru_ancor_bottom}                                                            '''
    ]
    keyboards = [key_s['ru_rf_in_regliv_faq_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Регистрация по месту пребывания - ЧаВо
@dp.callback_query_handler(text="ru_rf_in_regliv_faq")
async def query_ru_rf_in_regliv_faq(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.reg_liv_txt1, Text_serv.reg_liv_txt2,
                     Text_serv.reg_liv_txt3, Text_serv.reg_liv_txt4]
    keyboards = [None, None, None, key_s["ru_rf_in_regliv_faq_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Регистрация по месту пребывания - Жизненные ситуации
@dp.callback_query_handler(text="ru_rf_in_regliv_sit")
async def query_ru_rf_in_regliv_sit(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
f'''1️⃣ Я узнал, что в моем жилом помещении прописан неизвестный мне человек. Что в этом случае необходимо делать?
2️⃣ Я хочу снять с регистрационного учета одного из жильцов. Как это сделать?
3️⃣ Переезд в другой регион
{Text_serv.ru_ancor_bottom} '''
    ]
    keyboards = [key_s['ru_rf_in_regliv_sit_chchel_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Регистрация по месту пребывания - Жизненные ситуации - прописан неизвестный мне человек
@dp.callback_query_handler(text="ru_rf_in_regliv_sit_chchel")
async def query_ru_rf_in_regliv_sit_chchel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [key_s["ru_rf_in_regliv_sit_pereezd_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Регистрация по месту пребывания - Жизненные ситуации - Я хочу снять с регистрационного учета одного из жильцов
@dp.callback_query_handler(text="ru_rf_in_regliv_sit_snone")
async def query_ru_rf_in_regliv_sit_snone(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [key_s["ru_rf_in_regliv_sit_pereezd_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

#Русский язык - для граждан РФ - В Российской Федерации - Регистрация по месту пребывания - Жизненные ситуации - переезд в другой регион
@dp.callback_query_handler(text="ru_rf_in_regliv_sit_pereezd")
async def query_ru_rf_in_regliv_sit_pereezd(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Вы регистрируетесь в собственном жилом помежении?']
    keyboards = [key_s['ru_rf_in_regliv_sit_pereezd_yes-no_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_pereezd_yes")
async def query_ru_rf_in_regliv_sit_pereezd_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Зарегистрировано ли право собственности на избранное жилое помещение в ЕГРН?']
    keyboards = [key_s['ru_rf_in_regliv_sit_pereezd_yes-no_yes-no_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_pereezd_no")
async def query_ru_rf_in_regliv_sit_pereezd_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [key_s['ru_rf_in_regliv_sit_pereezd_yes_yes-no_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_pereezd_yes_yes")
async def query_ru_rf_in_regliv_pereezd_yes_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Для регистрации по месту жительства Вам...']
    keyboards = [key_s['ru_rf_in_regliv_sit_pereezd_yes-no_yes-no_key_1']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_pereezd_yes_no")
async def query_ru_rf_in_regliv_sit_pereezd_yes_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [key_s["ru_rf_in_regliv_sit_pereezd_yes_-no_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_pereezd_yes_yes_mfc")
async def ru_rf_in_regliv_sit_pereezd_yes_yes_mfc(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [key_s["ru_rf_in_regliv_sit_pereezd_yes_yes_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_pereezd_yes_yes_epgu")
async def ru_rf_in_regliv_sit_pereezd_yes_yes_epgu(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [key_s["ru_rf_in_regliv_sit_pereezd_yes_yes_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr")
async def query_ru_rf_in_gospr(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''1️⃣ Какой размер подъемных мне полагается
2️⃣ Какой порядок получения подъемных
3️⃣ Вам необходимо заменить свидетельство об участии в государственной программе?
4️⃣ Что делать, если заканчивается срок действия свидетельства участника Государственной программы?
5️⃣ В каких случаях анулируется свидетельство участника государственной программы?
6️⃣ Как самому отказаться от участия в Государственной программе?
7️⃣ Мне отказали в приеме заявления об участии в Государственной программе
8️⃣ Мне отказали в выдаче свидельства об участии в Государственной программе
{Text_serv.ru_ancor_bottom} '''
                     ]
    keyboards = [key_s['ru_rf_in_gospr_razmpod_key']
                 ]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_razmpod")
async def query_ru_rf_in_gospr_razmpod(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_txt]
    keyboards = [key_s['ru_rf_in_gospr_razmpod_yes-no_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_razmpod_yes")
async def query_ru_rf_in_gospr_razmpod_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_txt1]
    keyboards = [key_s['ru_rf_in_gospr_porpolpod_1_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_razmpod_no")
async def query_ru_rf_in_gospr_razmpod_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_txt2]
    keyboards = [key_s['ru_rf_in_gospr_porpolpod_1_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_porpolpod")
async def query_ru_rf_in_gospr_porpolpod(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_txt3]
    keyboards = [key_s['ru_rf_in_gospr_mneotkazali_1_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_mneotkazali")
async def query_ru_rf_in_gospr_mneotkazali(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_txt4]
    keyboards = [key_s["ru_rf_in_gospr_home_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid")
async def query_ru_rf_in_gospr(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''1️⃣ У вас изменился состав семьи?
2️⃣ У Вас изменилось семейное положение?
3️⃣ Вы потеряли свидетельство участника Государственной программы?
4️⃣ У Вас либо членов Вашей семьи произошло изменение фамилии, имени, отчества?',
5️⃣ Что делать, если в выданном свидетельстве участника Государственной программы обнаружены неточности, ошибки или отсутствие необходимых записей, печатей, штампов?',
6️⃣ Что делать, если выданное свидетельство участника Государственной программы непригодно по причине повреждений, нарушающих целостность свидетельства или его частей?',
7️⃣ Что делать, если в выданном свидетельстве участника Государственной программы обнаружены исправления, подчистки, отсутствует или переклеена фотография?',
8️⃣ Что делать в случае утраты членом семьи участника ГОсударственной программы, указанным в свидетельстве, статуса члена семьи участника ГОсударственной программы?'
{Text_serv.ru_ancor_bottom} ''']
    keyboards = [key_s['ru_rf_in_gospr_zamsvid_sostavsevi_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sostavsevi")
async def query_ru_rf_in_gospr_zamsvid_sostavsevi(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['''1️⃣ У вас родился ребёнок или Вы усыновили, приняли под опеку или попечительство ребенка?
2️⃣ У Вас умер один из членов Вашей семьи?''']
    keyboards = [key_s['ru_rf_in_gospr_zamsvid_sostavsevi_rebenok_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sempoloshen")
async def query_ru_rf_in_gospr_zamsvid_sempoloshen(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['''1️⃣ Вы вступили в брак?
2️⃣ Вы расторгли брак?''']
    keyboards = [key_s['ru_rf_in_gospr_zamsvid_sempoloshen_brak_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_poteryali")
async def query_ru_rf_in_gospr_zamsvid_poteryali(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_poteryli_txt]
    keyboards = [key_s["ru_rf_in_gospr_zamsvid_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_smenaystdannyh")
async def query_ru_rf_in_gospr_zamsvid_smenaystdannyh(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_smenadanyh_txt]
    keyboards = [key_s["ru_rf_in_gospr_zamsvid_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_svidoshibky")
async def query_ru_rf_in_gospr_zamsvid_svidoshibky(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_smenadanyh_txt]
    keyboards = [key_s["ru_rf_in_gospr_zamsvid_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_svidneprigodno")
async def query_ru_rf_in_gospr_zamsvid_svidneprigodno(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_smenadanyh_txt]
    keyboards = [key_s["ru_rf_in_gospr_zamsvid_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_svidsispravl")
async def query_ru_rf_in_gospr_zamsvid_svidsispravl(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_smenadanyh_txt]
    keyboards = [key_s["ru_rf_in_gospr_zamsvid_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_utratastatusa")
async def query_ru_rf_in_gospr_zamsvid_utratastatusa(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_smenadanyh_txt]
    keyboards = [key_s["ru_rf_in_gospr_zamsvid_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sostavsevi_rebenok")
async def query_ru_rf_in_gospr_zamsvid_sostavsevi_rebenok(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_rebenok_txt]
    keyboards = [key_s["ru_rf_in_gospr_zamsvid_sostavsevi_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sostavsevi_umer")
async def query_ru_rf_in_gospr_zamsvid_sostavsevi_umer(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_umer_txt]
    keyboards = [key_s["ru_rf_in_gospr_zamsvid_sostavsevi_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sempoloshen_brak")
async def query_ru_rf_in_gospr_zamsvid_sempoloshen_brak(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_brak_txt]
    keyboards = [key_s["ru_rf_in_gospr_zamsvid_sempoloshen_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sempoloshen_unbrak")
async def query_ru_rf_in_gospr_zamsvid_sempoloshen_unbrak(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_unbrak_txt]
    keyboards = [key_s["ru_rf_in_gospr_zamsvid_sempoloshen_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_rf_in_gospr_zaksroksvid")
async def query_ru_rf_in_gospr_zaksroksvid(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_txt5]
    keyboards = [key_s["ru_rf_in_gospr_home_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_rf_in_gospr_anulsvid")
async def query_ru_rf_in_gospr_anulsvid(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_txt6p1,Text_serv.gosprog_txt6p1]
    keyboards = [key_s[None, "ru_rf_in_gospr_home_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_rf_in_gospr_mneotkazalevydat")
async def query_ru_rf_in_gospr_mneotkazalevydat(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_txt7]
    keyboards = [key_s["ru_rf_in_gospr_home_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig")
async def query_ru_ig(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
f'''<b>Где Вы сейчас находитесь?</b>
В Российской Федерации
❌ За пределами Российской Федерации
❌ В пункте пропуска через Государственную границу Российской Федерации
{Text_serv.ru_ancor_bottom}        '''
    ]
    keyboards = [key_s['ru_ig_in_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in")
async def query_ru_ig_in(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
f'''<b>Выберите характер вашей ситуации</b>'
Я хочу стать гражданином России                  ᅠ ᅠ 
{Text_serv.ru_ancor_bottom} '''
        # '❌ Я - Участник Государственной программы по оказанию содействия добровольному преселению в Российскую Федерацию соотечественников, проживающих за рубежом',
        # '❌ Я намерен постоянно проживать в России',
        # '❌ Я нахожусь с краткосрочным визитом в России',
        # '❌ Я учусь в образовательной организации или готовлюсь к поступлению',
        # '❌ Я работаю по найму или буду трудоустраиваться',
        # '❌ Я ищу убежище в Российской Федерации',
        # '❌ Мне нужна помощь с постановкой на миграционный учет, а также с регистрацией по месту пребывания или изменения места пребывания',
        # '❌ У меня возникли проблемы с пребыванием в России'
    ]
    keyboards = [key_s['ru_ig_in_sitizen_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen")
async def query_ru_ig_in_sitizen(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
f'''<b>{Text_serv.sitizen_txt1}</b>
1️⃣ Получить персональную инструкцию
2️⃣ Полезная информация
3️⃣ Как принести Присягу гражданина Российской Федерации
{Text_serv.ru_ancor_bottom} '''
]
    keyboards = [key_s['ru_ig_in_sitizen_manual_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual")
async def query_ru_ig_in_sitizen_manual(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
f'''<b>У вас есть?</b>                                                      ᅠ ᅠ 
Вид на жительство в Российской Федерации
{Text_serv.ru_ancor_bottom} 
'''
]
    keyboards = [key_s['ru_ig_in_sitizen_manual_vng_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual_vng_yes")
async def query_ru_ig_in_sitizen_manual_vng_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
f'''<b>У вас есть?</b>                                                      ᅠ ᅠ 
Сертификат носителя русского языка
{Text_serv.ru_ancor_bottom} 
'''
]
    keyboards = [key_s['ru_ig_in_sitizen_manual_vng+sertrus_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual_vng+sertrus_yes")
async def query_ru_ig_in_sitizen_manual_vngsertrus_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man1p1,
        Text_serv.sitizen_man1p2
        ]
    keyboards = [None, key_s["ru_ig_in_sitizen_manual_vng+sertrus_yes_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual_vng+sertrus_no")
async def query_ru_ig_in_sitizen_manual_vngsertrus_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
f'''<b>У вас есть?</b>                                                      ᅠ ᅠ 
Свидетельство участника Госпрограммы
{Text_serv.ru_ancor_bottom} 
'''
]
    keyboards = [key_s['ru_ig_in_sitizen_manual_vng+gosprog_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual_vng+gosprog_yes")
async def query_ru_ig_in_sitizen_manual_vnggosprog_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man2
        ]
    keyboards = [key_s["ru_ig_in_sitizen_manual_vng+gosprog_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual_vng+gosprog_no")
async def query_ru_ig_in_sitizen_manual_vnggosprog_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
f'''<b>Перед Вами перечень самых распространенных оснований, позволяющих получить гражданство в упрощенном порядке</b>
1️⃣ Я являюсь гражданином Украины, республики Беларусь, Республики Молдова, республики Казахстан или Кыргызской Республики.
2️⃣ Мой близкий родственник - гражданин России.
(близкими родственниками являются: родители, дети, родные братья и сестры, бабушки, дедушки,внуки
3️⃣ Я владею русским языком как родным и готов пройти процедуру признания носителем русского языка.
4️⃣ Являюсь лицом без гражданства и ранее состял в гражданстве СССР.
5️⃣ Родился на территории РСФСР и ранее состоял в гражданстве бывшего СССР.
6️⃣ Мне ничего из вышеперечисленного не подходит.
{Text_serv.ru_ancor_bottom}'''
        ]
    keyboards = [key_s["ru_ig_in_sitizen_vng_only_sng_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_sng")
async def query_ru_ig_in_sitizen_vng_only_sng(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'''<b>Вы в прошлом состяли в гражданстве Белорусской ССР, Казахской ССР, или Киргизской ССР и одновременно в гражданстве бывшего СССР, либо родились или проживали на территории одной из указанных республик приобретаемого гражданства РСФСР до 21 декабря 1991 года</b>
{Text_serv.ru_ancor_bottom} '''

]
    keyboards = [key_s['ru_ig_in_sitizen_vng_only_sng_yn_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_sng_yes")
async def ru_ig_in_sitizen_vng_only_sng_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man3
    ]
    keyboards = [key_s["ru_ig_in_sitizen_vng_only_sng_back1_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_sng_no")
async def ru_ig_in_sitizen_vng_only_sng_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_txt2
    ]
    keyboards = [key_s['ru_ig_in_sitizen_vng_only_sng_blizrod_yn_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_sng_yes")
async def ru_ig_in_sitizen_vng_only_sng_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_txt2
    ]
    keyboards = [None, key_s['ru_ig_in_sitizen_vng_only_sng_blizrod_yn_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_sng_blizrod_yes")
async def ru_ig_in_sitizen_vng_only_sng_blizrod_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man4p1,
        Text_serv.sitizen_man4p2
    ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_sng_no_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_sng_blizrod_no")
async def ru_ig_in_sitizen_vng_only_sng_blizrod_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man5p1,
        Text_serv.sitizen_man5p2
    ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_sng_no_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_inf")
async def query_ru_ig_in_sitizen_inf(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_txt3
]
    keyboards = [key_s["ru_ig_in_sitizen1_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_ig_in_sitizen_pris")
async def query_ru_ig_in_sitizen_pris(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_txt4

]
    keyboards = [key_s["ru_ig_in_sitizen1_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_blizkorod")
async def query_ru_ig_in_sitizen_vng_only_blizkorod(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [f'''1️⃣ Состою не менее трех лет в браке с гражданином Российской Федерации, проживающим на трерритории Российской Федерации.
2️⃣ Состою в браке с гражданином Российской Федерации, проживающим на трерритории Российской Федерации и имею в этом браке общих детей (до 18 лет).
3️⃣ Один из родителейгражданин Российской Федерации и проживает на территории Российской Федерации.
4️⃣ Дееспособный сын или дочь достигли возраста 18 лет иявляются гражданами Российской Федерации.
5️⃣ Мой ребенок гражданин Российской Федерации, а другой родитель ребенка, являющийся гражданином Российской Федерации, умер либо решением суда вступившим в законную силу, признан безвестно отсутствующим, недееспособным или ограничен в родительских правах.
6️⃣ Сын или дочь, достигшие 18 лет, признаны недееспособными. 
<i>(Дети являются гражданами РФ, решение суда вступило в законную силу, а другой родитель ребенка, являющийся гражданином Российской Федерации, умер либо решением суда вступившим в законную силу, признан безвестно отсутствующим, недееспособным или ограничен в родительских правах.</i>
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s["ru_ig_sitizen_vng_only_blizrod"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_blizrod_3brak")
async def query_ru_ig_in_sitizen_vng_only_blizrod_3brak(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man6p1,
        Text_serv.sitizen_man6p2
]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_blizrod_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_blizrod_brakdeti")
async def query_ru_ig_in_sitizen_vng_only_blizrod_brakdeti(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man7p1,
        Text_serv.sitizen_man7p2
]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_blizrod_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_blizrod_roditeli")
async def query_ru_ig_in_sitizen_vng_only_blizrod_poditeli(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man8p1,
        Text_serv.sitizen_man8p2
]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_blizrod_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_blizrod_deerebenok")
async def query_ru_ig_in_sitizen_vng_only_blizrod_deesrebenok(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man9p1,
        Text_serv.sitizen_man9p2
]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_blizrod_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_blizrod_rebenok+1roditel")
async def query_ru_ig_in_sitizen_vng_only_blizrod_rebenokroditel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man9p1,
        Text_serv.sitizen_man9p2
]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_blizrod_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_blizrod_nedeesrebenok")
async def query_ru_ig_in_sitizen_vng_only_blizrod_nedeesrebenok(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man9p1,
        Text_serv.sitizen_man9p2]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_blizrod_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_vladeyrus")
async def query_ru_ig_in_sitizen_vng_only_vladeyrus(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man12]
    keyboards = [key_s["ru_ig_in_sitizen_vng_only_sng_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_lbgussr")
async def query_ru_ig_in_sitizen_vng_only_lbgussr(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man13p1, Text_serv.sitizen_man13p1
    ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_sng_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_borninussr")
async def query_ru_ig_in_sitizen_vng_only_borninussr(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man9p1, Text_serv.sitizen_man9p1
    ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_sng_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_nothing")
async def query_ru_ig_in_sitizen_vng_only_nothing(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'''<b>Посмотрите, может что-то из этого Вам подходит</b>
1️⃣ Ветеран Великой Отечественной войны и ранее состоял в гражданстве бывшего СССР.
2️⃣ Ранее состоял в гражданстве РФ (оформил выход из Российского гражданства).
3️⃣ Получил после 1 июля 202 года профессиональное образование в России.
4️⃣ Являюсь индивидуальным предпринимателем и осуществляю предпринимательскую деятельность на территории РФ не менее трех лет.
5️⃣ Являюсь инвестором.
6️⃣ Квалифицированный специалист.
7️⃣ Нетрудоспособный гражанин, прибыл в РФ из государства, входившее в состав СССР, и зарегистрирован по месту жительства в Российской Федерации по состоянию на 1июля 2002 года.
8️⃣ Мне, увы, ничего из этого не подходит
{Text_serv.ru_ancor_bottom}
''']
    keyboards = [key_s["ru_ig_sitizen_vng_only_nothing_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_vov")
async def query_ru_ig_in_sitizen_vng_only_vov(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man15p1, Text_serv.sitizen_man15p2
    ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_nothing_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_raneerf")
async def query_ru_ig_in_sitizen_vng_only_raneerf(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man16
    ]
    keyboards = [key_s["ru_ig_in_sitizen_vng_only_nothing_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_profobraz")
async def query_ru_ig_in_sitizen_vng_only_profobraz(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man17p1, Text_serv.sitizen_man17p2
    ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_nothing_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_ip")
async def query_ru_ig_in_sitizen_vng_only_ip(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man18p1, Text_serv.sitizen_man18p2
    ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_nothing_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_investor")
async def query_ru_ig_in_sitizen_vng_only_investor(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man19p1, Text_serv.sitizen_man19p2
    ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_nothing_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_kvspec")
async def query_ru_ig_in_sitizen_vng_only_kvspec(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man20p1, Text_serv.sitizen_man20p2
    ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_nothing_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_netrud")
async def query_ru_ig_in_sitizen_vng_only_netrud(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man21p1, Text_serv.sitizen_man21p2
    ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_nothing_back_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)
async def send_startup_temp():
    await bot.send_message(chat_id=group_id_guvm, text='Я онлайн')

async def on_startup(dp):
    await send_startup_temp()

async def send_shutdown_temp():
    await bot.send_message(chat_id=group_id_guvm, text='Я офлайн')

async def on_shutdown(dp):
    await send_shutdown_temp()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    message_storage = {}
    last_user_messages = {}
    user_languages = {}
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)