from aiogram import Bot, Dispatcher, types

TOKEN = "5467366547:AAE4CmSsbnzlS_GL4YVohj6QMh6tyriRuAM"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

LANGS = ['Русский', 'English']
SERVICES = {
    "Русский": ["Для граждан России", "Для Иностранных граждан", 'Для жителей ДНР, ЛНР, ХО, ЗО', "Для юридических лиц и ИП"],
    "English": ["Citizens of Russia", "Foreign citizens", "Check the document", "Report information"]
}
SUBSERVICES = {
    "Для граждан России": ["В пределах РФ", "За пределами РФ"],
    "Для Иностранных граждан": ["B пределах РФ", "Зa пределами РФ", "В пункте пропуска через границу РФ"],
    "Для жителей ДНР, ЛНР, ХО, ЗО": ["В пределах PФ", "За пределами PФ"],
    "Для юридических лиц и ИП": ["Мы предоставляем услуги гражданам",
                                 "Мы привлекаем трудовых мигрантов",
                                 "У нас дети без гражданства РФ",
                                 "Может ли полиция нас проверять",
                                 "Есть разрешение на привлечение ИГ",
                                 "Вам запретили привлекать ИГ",
                                 "Вы хотите принимать на работу...",
                                 "Прием на работу ИГ, направляем..."],

    "Frequently asked questions": ["Citizens of Russia", "Foreign citizens", "Legal entities and an individual entrepreneur"],
    "Ask your question": ["I am a citizen of Russia", "I am a citizen of a foreign state",
                           "I am a representative of an organization or an individual entrepreneur"],
    "Check the document": ["Passport of a citizen of Russia", "Foreign passport of a Russian citizen",
                           "Compliance of the document and the registration address", "Invitation of foreigners to enter Russia",
                           "Work permit of a foreigner", "A patent for the work of a foreigner",
                           "The presence of a foreigner's ban on entry into Russia"],
    "Report information": ["About trading fictitious documents",
                            "About the signs of an organized illegal migration channel",
                            "About paid services of accelerated registration of a foreign passport",
                            "About the signs of corrupt behavior of employees of migration departments"],

}
SUBSERVICES_2 ={
    'В пределах РФ': ["Внутренний паспорт", "Загранпаспорт", "Регистрация по месту проживания",
                     "Я участник Госпрограммы", "Вынужденные переселенцы", "Мой близкий родственник - иностр", "Я хочу прекратить гр-во РФ"],
    "За пределами РФ": ["Как получить новый паспорт?",
                        "Как оформить новый загранпаспорт?",
                        "Как сняться с регучета в России?",
                        "Я хочу участвовать в Госпрограмме",
                        "Уведомление об ином гражданстве",
                        "Я заключил(а) брак с иностранцем",
                        "Я приёмный родитель ребенка - ИГ",
                        "Нужна помощь в переселении в РФ",
                        "Д(Л)НР,ЗО,ХО, замена паспорта ЕПГУ"]
    "B пределах РФ":["Я хочу гражданство РФ",
                     "Я- участник Госпрограммы",
                     "Я хочу постоянно проживать в РФ",
                     "Я краткосрочно нахожусь в РФ",
                     "Я учусь или готовлюсь поступать",
                     "Я работаю по найму",
                     "Я ищу убежище в РФ",
                     "Нужна помощь с мигр.учетом",
                     "Возникли проблемыс пребыванием"]
}
GREETINGS = {
    "Русский": "Добро пожаловать!",
    "English": "Welcome!"
}



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Выберите язык / Choose a language:", reply_markup=generate_keyboard(LANGS))

@dp.callback_query_handler(lambda c: c.data in LANGS)
async def lang_chosen(callback_query: types.CallbackQuery):
    chosen_lang = callback_query.data
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text=GREETINGS[chosen_lang] + " Теперь выберите пункт меню:",
                                reply_markup=generate_keyboard(SERVICES[chosen_lang]))

@dp.callback_query_handler(lambda c: any(c.data in service_list for service_list in SERVICES.values()))
async def service_chosen(callback_query: types.CallbackQuery):
    chosen_service = callback_query.data
    if chosen_service in SUBSERVICES.keys():
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=f"Где вы сейчас находитесь?",
                                    reply_markup=generate_keyboard(SUBSERVICES[chosen_service]))
    else:
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text=f"Вы выбрали услугу: {chosen_service}.")

@dp.callback_query_handler(lambda c: any(c.data in subservice_list for subservice_list in SUBSERVICES.values()))
async def subservice_chosen(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text=f"{callback_query.data}.")

@dp.callback_query_handler(lambda c: c.data == "Гражданам России")
async def citizens_russia_chosen(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text="Вы выбрали подуслугу 'Гражданам России'.")

@dp.callback_query_handler(lambda c: c.data == "Иностранным гражданам")
async def foreign_citizens_chosen(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text="Вы выбрали подуслугу 'Иностранным гражданам'.")

@dp.callback_query_handler(lambda c: c.data == "Юридическим лицам и ИП")
async def foreign_citizens_chosen(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text="Вы выбрали подуслугу 'Юридическим лицам и ИП'.")
# Добавьте обработку для каждой подуслуги

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
