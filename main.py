from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove

import aiogram.utils.markdown as mar
import Text_serv, asyncio, logging
from tokenbot import TOKONBOT, MESSAGE_GROUP
from keyboards_serv import key_s, underline_keyboard, confirm_keyboard



token = TOKONBOT
group_id = MESSAGE_GROUP

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

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


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Выберите язык / Choose a language:",
                           reply_markup=key_s["lang_key"])

    await bot.send_message(chat_id=message.chat.id, text="*",
                           reply_markup=ReplyKeyboardRemove())

@dp.message_handler(lambda message: not any(symbol in message.text for symbol in ['✉', '🏠']))
async def store_user_message(message: types.Message):
    last_user_messages[message.from_user.id] = mar.quote_html(message.text)

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


@dp.message_handler(lambda message: '🏠' in message.text)
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Выберите язык / Choose a language:",
                           reply_markup=key_s["lang_key"], )
    await bot.send_message(chat_id=message.chat.id, text="*",
                           reply_markup=ReplyKeyboardRemove())

@dp.callback_query_handler(text="rus")
async def choose_section_rus(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_languages[callback_query.from_user.id] = 'rus'
    message_texts = [
        '<b>Выберите раздел</b>                                                      ᅠ ᅠ ',
        'Для граждан России                                                     ᅠ ᅠ ',
        'Для иностранных граждан                                          ᅠ ᅠ ',
        '❌ Для граждан Украины, ЛНР, ДНР, Херсонской области, Запорожской области',
        '❌ Для Юридических лиц и индивидуальных предпринимателей'
    ]
    keyboards = [None, key_s['ru_rf_key'], key_s['ru_ig_key'], key_s['ru_ukr_key'], key_s['ru_org_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="<b>❗️❗️❗️ Чтоб отправить свое сообщение в ГУВМ МВД России, отправьте его в чат боту, после чего нажмите ✉ на нижней клавиатуре</b>",
                           reply_markup=underline_keyboard)


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

@dp.callback_query_handler(lambda query: query.data == "confirm_no")
async def cancel_send(query: types.CallbackQuery):
    await bot.edit_message_text("Отправка отменена.", chat_id=query.from_user.id, message_id=query.message.message_id, reply_markup=None)
    await bot.answer_callback_query(query.id, "Отправка отменена.")
    await bot.send_message(chat_id=query.from_user.id, text="Чтоб отправить свое сообщение в ГУВМ МВД России, отправьте его в чат боту, после чего нажмите ✉ на нижней клавиатуре", reply_markup=underline_keyboard)


@dp.callback_query_handler(text="ru_rf")
async def query_ru_rf(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        '<b>Где Вы сейчас находитесь?</b>                                                      ᅠ ᅠ ',
        'В Российской Федерации                                         ᅠ ᅠ ',
        '❌ За пределами Российской Федерации                                          ᅠ ᅠ '
    ]
    keyboards = [None, key_s['ru_rf_in_key'], key_s['ru_rf_out_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in")
async def query_ru_rf_in(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        '<b>Выберите нужный раздел</b>                                                      ᅠ ᅠ ',
        'Внутренний паспорт                                         ᅠ ᅠ ',
        'Загранпаспорт                                         ᅠ ᅠ ',
        'Регистрация по месту проживания                                         ᅠ ᅠ ',
        'Я стал участником Государственной программы по оказанию содействия добровольному переселению в Российскую федерацию соотечественников, проживающих за рубежом, на территории иностранного государства',
        '❌ Я и(или) члены моей семьи - вынужденные переселенцы',
        '❌ Член моей семьи или близкий родственник - иностранный гражданин',
        '❌ Я хочу оформить выход из гражданства Российской Федерации'
    ]
    keyboards = [None, key_s['ru_rf_in_pasp_key'], key_s['ru_rf_in_zp_key'], key_s['ru_rf_in_regliv_key'],
                 key_s['ru_rf_in_gospr_key'], key_s['ru_rf_in_peres_key'], key_s['ru_rf_in_famin_key'],
                 key_s['ru_rf_in_outsitiz_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_pasp")
async def query_ru_rf_in_pasp(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        '''<b>В разделе часто задаваемые вопросы даны короткие ответы и разъяснения.</b>

<b>В разделе жизненные ситуации Вы найдете инструкции</b>''',
        'Часто задаваемые вопросы                                       ᅠ ᅠ ',
        'Жизненные ситуации                                         ᅠ ᅠ ',
    ]
    keyboards = [None, key_s['ru_rf_in_pasp_faq_key'], key_s['ru_rf_in_pasp_sit_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_pasp_faq")
async def query_ru_rf_in_pasp_faq(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.iner_pasp_txt1, Text_serv.iner_pasp_txt2]
    keyboards = [None] * len(message_texts)
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_pasp_sit")
async def query_ru_rf_in_pasp_sit(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе заполнения']
    keyboards = [None] * len(message_texts)
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_zp")
async def query_ru_rf_in_zp(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        '''<b>В разделе часто задаваемые вопросы даны короткие ответы и разъяснения.</b>

<b>В разделе жизненные ситуации Вы найдете инструкции</b>''',
        'Часто задаваемые вопросы                                       ᅠ ᅠ ',
        'Жизненные ситуации                                         ᅠ ᅠ ',
    ]
    keyboards = [None, key_s['ru_rf_in_zp_faq_key'], key_s['ru_rf_in_zp_sit_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_zp_faq")
async def query_ru_rf_in_zp_faq(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [None] * len(message_texts)
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_zp_sit")
async def query_ru_rf_in_zp_sit(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [None] * len(message_texts)
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv")
async def query_ru_rf_in_regliv(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        '''<b>В разделе часто задаваемые вопросы даны короткие ответы и разъяснения.</b>

<b>В разделе жизненные ситуации Вы найдете инструкции</b>''',
        'Часто задаваемые вопросы                                       ᅠ ᅠ ',
        'Жизненные ситуации                                         ᅠ ᅠ ',
    ]
    keyboards = [None, key_s['ru_rf_in_regliv_faq_key'], key_s['ru_rf_in_regliv_sit_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_faq")
async def query_ru_rf_in_regliv_faq(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.reg_liv_txt1, Text_serv.reg_liv_txt2, Text_serv.reg_liv_txt3, Text_serv.reg_liv_txt3,]
    keyboards = [None] * len(message_texts)
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit")
async def query_ru_rf_in_regliv_sit(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        'Я узнал, что в моем жилом помещении прописан неизвестный мне человек. Что в этом случае необходимо делать?',
        'Я хочу снять с регистрационного учета одного из жильцов. Как это сделать?',
        'Переезд в другой регион']
    keyboards = [key_s['ru_rf_in_regliv_sit_chchel_key'], key_s['ru_rf_in_regliv_sit_snone_key'],
                 key_s['ru_rf_in_regliv_sit_pereezd_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_chchel")
async def query_ru_rf_in_regliv_sit_chchel(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [None] * len(message_texts)
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_snone")
async def query_ru_rf_in_regliv_sit_snone(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [None] * len(message_texts)
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


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
    message_texts = ['Зарегистрировано ли право собственности на избранное жилоепомещение в ЕГРН?']
    keyboards = [key_s['ru_rf_in_regliv_sit_pereezd_yes-no_yes-no_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_pereezd_no")
async def query_ru_rf_in_regliv_sit_pereezd_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [None] * len(message_texts)
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
    keyboards = [None] * len(message_texts)
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_pereezd_yes_yes_mfc")
async def ru_rf_in_regliv_sit_pereezd_yes_yes_mfc(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [None] * len(message_texts)
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_regliv_sit_pereezd_yes_yes_epgu")
async def ru_rf_in_regliv_sit_pereezd_yes_yes_epgu(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Раздел в процессе наполнения']
    keyboards = [None] * len(message_texts)
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr")
async def query_ru_rf_in_gospr(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Какой размер подъемныхмне полагается?',
                     'Какой порядок получения подъемных',
                     'Вам необходимо заменить свидетельство об участии в государственной программе?',
                     'Что делать, если заканчивается срок действия свидетельства участника Государственной программы?',
                     'В каких случаях анулируется свидетельство участника государственной программы?',
                     'Как самому отказаться от участия в Государственной программе?',
                     'Мне отказали в приеме заявления об участии в Государственной программе',
                     'Мне отказали в выдаче свидельства об участии в Государственной программе'
                     ]
    keyboards = [key_s['ru_rf_in_gospr_razmpod_key'], key_s['ru_rf_in_gospr_porpolpod_key'],
                 key_s['ru_rf_in_gospr_zamsvid_key'], key_s['ru_rf_in_gospr_zaksroksvid_key'],
                 key_s['ru_rf_in_gospr_anulsvid_key'], key_s['ru_rf_in_gospr_otkazsam_key'],
                 key_s['ru_rf_in_gospr_mneotkazali_key'], key_s['ru_rf_in_gospr_mneotkazali_key']
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
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid")
async def query_ru_rf_in_gospr(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['У вас изменился состав семьи?',
                     'У Вас изменилось семейное положение?',
                     'Вы потеряли свидетельство участника Государственной программы?',
                     'У Вас либо членов Вашей семьи произошло изменение фамилии, имени, отчества?',
                     'Что делать, если в выданном свидетельстве участника Государственной программы обнаружены неточности, ошибки или отсутствие необходимых записей, печатей, штампов?',
                     'Что делать, если выданное свидетельство участника Государственной программы непригодно по причине повреждений, нарушающих целостность свидетельства или его частей?',
                     'Что делать, если в выданном свидетельстве участника Государственной программы обнаружены исправления, подчистки, отсутствует или переклеена фотография?',
                     'Что делать в случае утраты членом семьи участника ГОсударственной программы, указанным в свидетельстве, статуса члена семьи участника ГОсударственной программы?'
                     ]
    keyboards = [key_s['ru_rf_in_gospr_zamsvid_sostavsevi_key'], key_s['ru_rf_in_gospr_zamsvid_sempoloshen_key'],
                 key_s['ru_rf_in_gospr_zamsvid_poteryali_key'], key_s['ru_rf_in_gospr_zamsvid_smenaystdannyh_key'],
                 key_s['ru_rf_in_gospr_zamsvid_svidoshibky_key'], key_s['ru_rf_in_gospr_zamsvid_svidneprigodno_key'],
                 key_s['ru_rf_in_gospr_zamsvid_svidsispravl_key'], key_s['ru_rf_in_gospr_zamsvid_utratastatusa_key']
                 ]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sostavsevi")
async def query_ru_rf_in_gospr_zamsvid_sostavsevi(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['У вас родился ребёнок или Вы усыновили, приняли под опеку или попечительство ребенка?',
                     'У Вас умер один из членов Вашей семьи?']
    keyboards = [key_s['ru_rf_in_gospr_zamsvid_sostavsevi_rebenok_key'],
                 key_s['ru_rf_in_gospr_zamsvid_sostavsevi_umer_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sempoloshen")
async def query_ru_rf_in_gospr_zamsvid_sempoloshen(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = ['Вы вступили в брак?', 'Вы расторгли брак?']
    keyboards = [key_s['ru_rf_in_gospr_zamsvid_sempoloshen_brak_key'],
                 key_s['ru_rf_in_gospr_zamsvid_sempoloshen_unbrak_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_poteryali")
async def query_ru_rf_in_gospr_zamsvid_poteryali(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_poteryli_txt]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_smenaystdannyh")
async def query_ru_rf_in_gospr_zamsvid_smenaystdannyh(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_smenadanyh_txt]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_svidoshibky")
async def query_ru_rf_in_gospr_zamsvid_svidoshibky(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_smenadanyh_txt]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_svidneprigodno")
async def query_ru_rf_in_gospr_zamsvid_svidneprigodno(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_smenadanyh_txt]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_svidsispravl")
async def query_ru_rf_in_gospr_zamsvid_svidsispravl(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_smenadanyh_txt]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_utratastatusa")
async def query_ru_rf_in_gospr_zamsvid_utratastatusa(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_smenadanyh_txt]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sostavsevi_rebenok")
async def query_ru_rf_in_gospr_zamsvid_sostavsevi_rebenok(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_rebenok_txt]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sostavsevi_umer")
async def query_ru_rf_in_gospr_zamsvid_sostavsevi_umer(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_umer_txt]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sempoloshen_brak")
async def query_ru_rf_in_gospr_zamsvid_sempoloshen_brak(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_brak_txt]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_rf_in_gospr_zamsvid_sempoloshen_unbrak")
async def query_ru_rf_in_gospr_zamsvid_sempoloshen_unbrak(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [Text_serv.gosprog_unbrak_txt]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig")
async def query_ru_ig(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        '<b>Где Вы сейчас находитесь?</b>                                                      ᅠ ᅠ ',
        'В Российской Федерации                                         ᅠ ᅠ ',
        '❌ За пределами Российской Федерации                                          ᅠ ᅠ ',
        '❌ В пункте пропуска через Государственную границу Российской Федерации'
    ]
    keyboards = [None, key_s['ru_ig_in_key'], key_s['ru_ig_out_key'], key_s['ru_ig_board_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in")
async def query_ru_ig_in(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        '<b>Выберите характер вашей ситуации</b>',
        'Я хочу стать гражданином России                  ᅠ ᅠ ',
        '❌ Я - Участник Государственной программы по оказанию содействия добровольному преселению в Российскую Федерацию соотечественников, проживающих за рубежом',
        '❌ Я намерен постоянно проживать в России',
        '❌ Я нахожусь с краткосрочным визитом в России',
        '❌ Я учусь в образовательной организации или готовлюсь к поступлению',
        '❌ Я работаю по найму или буду трудоустраиваться',
        '❌ Я ищу убежище в Российской Федерации',
        '❌ Мне нужна помощь с постановкой на миграционный учет, а также с регистрацией по месту пребывания или изменения места пребывания',
        '❌ У меня возникли проблемы с пребыванием в России'
    ]
    keyboards = [None, key_s['ru_ig_in_sitizen_key'], None, None, None,None,None,None,None,None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen")
async def query_ru_ig_in_sitizen(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>{Text_serv.sitizen_txt1}</b>                                                      ᅠ ᅠ ',
        'Получить персональную инструкцию                                         ᅠ ᅠ ',
        'Полезная информация',
        'Как принести Присягу гражданина Российской Федерации'
]
    keyboards = [None, key_s['ru_ig_in_sitizen_manual_key'], key_s['ru_ig_in_sitizen_inf_key'], key_s['ru_ig_in_sitizen_pris_key'],]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual")
async def query_ru_ig_in_sitizen_manual(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>У вас есть?</b>                                                      ᅠ ᅠ ',
        'Вид на жительство в Российской Федерации'
]
    keyboards = [None, key_s['ru_ig_in_sitizen_manual_vng_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual_vng_yes")
async def query_ru_ig_in_sitizen_manual_vng_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>У вас есть?</b>                                                      ᅠ ᅠ ',
        'Сертификат носителя русского языка'
]
    keyboards = [None, key_s['ru_ig_in_sitizen_manual_vng+sertrus_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual_vng+sertrus_yes")
async def query_ru_ig_in_sitizen_manual_vngsertrus_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>{Text_serv.sitizen_man1}</b>                                                      ᅠ ᅠ ',
        ]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual_vng+sertrus_no")
async def query_ru_ig_in_sitizen_manual_vngsertrus_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>У вас есть?</b>                                                      ᅠ ᅠ ',
        'Свидетельство участника Госпрограммы'
]
    keyboards = [None, key_s['ru_ig_in_sitizen_manual_vng+gosprog_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual_vng+gosprog_yes")
async def query_ru_ig_in_sitizen_manual_vnggosprog_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>{Text_serv.sitizen_man2}</b>                                                      ᅠ ᅠ ',
        ]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_manual_vng+gosprog_no")
async def query_ru_ig_in_sitizen_manual_vnggosprog_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        '<b>Перед Вами перечень самых распространенных оснований, позволяющих получить гражданство в упрощенном порядке</b>',
        'Я являюсь гражданином Украины, республики Беларусь, Республики Молдова, республики Казахстан или Кыргызской Республики',
        '''Мой близкий родственник - гражданин России.
(близкими родственниками являются: родители, дети, родные братья и сестры, бабушки, дедушки,внуки''',
        'Я владею русским языком как родным и готов пройти процедуру признания носителем русского языка',
        'Являюсь лицом без гражданства и ранее состял в гражданстве СССР',
        "Родился на территории РСФСР и ранее состоял в гражданстве бывшего СССР",
        "Мне ничего из вышеперечисленного не подходит"
        ]
    keyboards = [None, key_s["ru_ig_in_sitizen_vng_only_sng_key"], key_s["ru_ig_in_sitizen_vng_only_blizkorod_key"],
                 key_s["ru_ig_in_sitizen_vng_only_vladeyrus_key"], key_s["ru_ig_in_sitizen_vng_only_lbgussr_key"],
                 key_s["ru_ig_in_sitizen_vng_only_borninussr_key"], key_s["ru_ig_in_sitizen_vng_only_nothing_key"]]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_sng")
async def query_ru_ig_in_sitizen_vng_only_sng(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>Вы в прошлом состяли в гражданстве Белорусской ССР, Казахской ССР, или Киргизской ССР и одновременно в гражданстве бывшего СССР, либо родились или проживали на территории одной из указанных республик приобретаемого гражданства РСФСР до 21 декабря 1991 года</b>',

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
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_sng_no")
async def ru_ig_in_sitizen_vng_only_sng_no(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>{Text_serv.sitizen_txt2}</b>'
    ]
    keyboards = [key_s['ru_ig_in_sitizen_vng_only_sng_blizrod_yn_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_sng_yes")
async def ru_ig_in_sitizen_vng_only_sng_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>{Text_serv.sitizen_txt2}</b>'
    ]
    keyboards = [None, key_s['ru_ig_in_sitizen_vng_only_sng_blizrod_yn_key']]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

@dp.callback_query_handler(text="ru_ig_in_sitizen_vng_only_sng_blizrod_yes")
async def ru_ig_in_sitizen_vng_only_sng_blizrod_yes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        Text_serv.sitizen_man4
    ]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_ig_in_sitizen_inf")
async def query_ru_ig_in_sitizen_inf(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>{Text_serv.sitizen_txt1}</b>                                                    ᅠ ᅠ ',
]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)


@dp.callback_query_handler(text="ru_ig_in_sitizen_pris")
async def query_ru_ig_in_sitizen_pris(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_texts = [
        f'<b>{Text_serv.sitizen_txt1}</b>                                                      ᅠ ᅠ ',
]
    keyboards = [None]
    await delete_previous_messages(user_id, message_storage)
    await send_and_save_messages(user_id, message_texts, keyboards, message_storage)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    message_storage = {}
    last_user_messages = {}
    user_languages = {}
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)