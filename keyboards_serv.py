from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def create_button(text, callback_data):
    return InlineKeyboardButton(text, callback_data=callback_data)

def create_keyboard(*buttons, row=4):
    keyboard = InlineKeyboardMarkup(row_width=row, resize_keyboard=True, one_time_keyboard=True)
    for button in buttons:
        keyboard.add(button)
    return keyboard


underline_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
home_btn = KeyboardButton('🏠')
message_btn = KeyboardButton('✉')
#back_btn = KeyboardButton('🔙')
underline_keyboard.add( home_btn, message_btn)

#клавиатура да/нет для отправки сообщения
confirm_keyboard = InlineKeyboardMarkup(row_width=2)
confirm_keyboard.add(InlineKeyboardButton("Да", callback_data="confirm_yes"),
                     InlineKeyboardButton("Нет", callback_data="confirm_no"))

buttons = {


    "rus": create_button("🇷🇺 Русский 🇷🇺", "rus"),
    "en": create_button("❌ 🇬🇧 English 🇬🇧", "en"),

    "ru_rf": create_button("1️⃣", "ru_rf"),
    "ru_ig": create_button("2️⃣", "ru_ig"),
    "ru_ukr": create_button("❌3️⃣", "ru_ukr"),
    "ru_org": create_button("❌4️⃣", "ru_org"),
    #"ru_back": InlineKeyboardButton("🔙", commands = ['start']),

    "ru_rf_in": create_button("1️⃣", "ru_rf_in"),
    "ru_rf_out": create_button("️❌2️⃣", "ru_rf_out"),
    "ru_rf_back": create_button("🔙", "rus"),

    "ru_rf_in_pasp": create_button("1️⃣", "ru_rf_in_pasp"),
    "ru_rf_in_zp": create_button("2️⃣", "ru_rf_in_zp"),
    "ru_rf_in_regliv": create_button("3️⃣", "ru_rf_in_regliv"),
    "ru_rf_in_gospr": create_button("4️⃣", "ru_rf_in_gospr"),
    "ru_rf_in_peres": create_button("❌5️⃣", "ru_rf_in_peres"),
    "ru_rf_in_famin": create_button("❌6️⃣", "ru_rf_in_famin"),
    "ru_rf_in_outsitiz": create_button("❌7️⃣", "ru_rf_in_outsitiz"),
    "ru_rf_in_back": create_button("🔙", "ru_rf"),

    "ru_rf_in_pasp_faq": create_button("1️⃣", "ru_rf_in_pasp_faq"),
    "ru_rf_in_pasp_sit": create_button("2️⃣", "ru_rf_in_pasp_sit"),
    "ru_rf_in_pasp_back": create_button("🔙", "ru_rf_in"),
    "ru_rf_in_pasp_1_back": create_button("🔙", "ru_rf_in_pasp"),

    "ru_rf_in_zp_faq": create_button("1️⃣", "ru_rf_in_zp_faq"),
    "ru_rf_in_zp_sit": create_button("2️⃣", "ru_rf_in_zp_sit"),
    "ru_rf_in_zp_back": create_button("🔙", "ru_rf_in"),
    "ru_rf_in_zp_1_back": create_button("🔙", "ru_rf_in_zp"),


    "ru_rf_in_regliv_faq": create_button("1️⃣", "ru_rf_in_regliv_faq"),
    "ru_rf_in_regliv_sit": create_button("2️⃣", "ru_rf_in_regliv_sit"),
    "ru_rf_in_regliv_back": create_button("🔙", "ru_rf_in"),

    "ru_rf_in_regliv_sit_chchel": create_button("1️⃣", "ru_rf_in_regliv_sit_chchel"),
    "ru_rf_in_regliv_sit_snone": create_button("2️⃣", "ru_rf_in_regliv_sit_snone"),
    "ru_rf_in_regliv_sit_pereezd": create_button("3️⃣", "ru_rf_in_regliv_sit_pereezd"),
    "ru_rf_in_regliv_sit_back": create_button("🔙", "ru_rf_in_regliv"),

    "ru_rf_in_regliv_sit_pereezd_yes": create_button("Да ✅", "ru_rf_in_regliv_sit_pereezd_yes"),
    "ru_rf_in_regliv_sit_pereezd_no": create_button("Нет ❌", "ru_rf_in_regliv_sit_pereezd_no"),
    "ru_rf_in_regliv_sit_pereezd_back": create_button("🔙", "ru_rf_in_regliv_sit"),

    "ru_rf_in_regliv_sit_pereezd1_back": create_button("🔙", "ru_rf_in_regliv_sit"),
    "ru_rf_in_regliv_sit_pereezd_yes_yes": create_button("Да ✅", "ru_rf_in_regliv_sit_pereezd_yes_yes"),
    "ru_rf_in_regliv_sit_pereezd_yes_no": create_button("Нет ❌", "ru_rf_in_regliv_sit_pereezd_yes_no"),

    "ru_rf_in_regliv_sit_pereezd_yes_yes_mfc": create_button("МФЦ", "ru_rf_in_regliv_sit_pereezd_yes_yes_mfc"),
    "ru_rf_in_regliv_sit_pereezd_yes_yes_epgu": create_button("ЕПГУ", "ru_rf_in_regliv_sit_pereezd_yes_yes_epgu"),

    "ru_rf_in_gospr_razmpod": create_button("Далее 1️⃣", "ru_rf_in_gospr_razmpod"),
    "ru_rf_in_gospr_porpolpod": create_button("Далее 2️⃣", "ru_rf_in_gospr_porpolpod"),
    "ru_rf_in_gospr_zamsvid": create_button("Далее 3️⃣", "ru_rf_in_gospr_zamsvid"),
    "ru_rf_in_gospr_zaksroksvid": create_button("Далее 4️⃣", "ru_rf_in_gospr_zaksroksvid"),
    "ru_rf_in_gospr_anulsvid": create_button("Далее 5️⃣", "ru_rf_in_gospr_anulsvid"),
    "ru_rf_in_gospr_otkazsam": create_button("Далее 6️⃣", "ru_rf_in_gospr_otkazsam"),
    "ru_rf_in_gospr_mneotkazali": create_button("Далее 7️⃣", "ru_rf_in_gospr_mneotkazali"),
    "ru_rf_in_gospr_mneotkazalevydat": create_button("Далее 8️⃣", "ru_rf_in_gospr_mneotkazalevydat"),

    "ru_rf_in_gospr_razmpod_yes": create_button("Да ✅", "ru_rf_in_gospr_razmpod_yes"),
    "ru_rf_in_gospr_razmpod_no": create_button("Нет ❌", "ru_rf_in_gospr_razmpod_no"),
    "ru_rf_in_gospr_porpolpod_1": create_button("Порядок получения подъемных", "ru_rf_in_gospr_porpolpod"),
    "ru_rf_in_gospr_mneotkazali1": create_button("Мне отказали в приеме заявления", "ru_rf_in_gospr_mneotkazali"),

    "ru_rf_in_gospr_zamsvid_sostavsevi": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_sostavsevi"),
    "ru_rf_in_gospr_zamsvid_sempoloshen": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_sempoloshen"),
    "ru_rf_in_gospr_zamsvid_poteryali": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_poteryali"),
    "ru_rf_in_gospr_zamsvid_smenaystdannyh": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_smenaystdannyh"),
    "ru_rf_in_gospr_zamsvid_svidoshibky": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_svidoshibky"),
    "ru_rf_in_gospr_zamsvid_svidneprigodno": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_svidneprigodno"),
    "ru_rf_in_gospr_zamsvid_svidsispravl": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_svidsispravl"),
    "ru_rf_in_gospr_zamsvid_utratastatusa": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_utratastatusa"),

    "ru_rf_in_gospr_zamsvid_sostavsevi_rebenok": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_sostavsevi_rebenok"),
    "ru_rf_in_gospr_zamsvid_sostavsevi_umer": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_sostavsevi_umer"),

    "ru_rf_in_gospr_zamsvid_sempoloshen_brak": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_sempoloshen_brak"),
    "ru_rf_in_gospr_zamsvid_sempoloshen_unbrak": create_button("Далее ➡️", "ru_rf_in_gospr_zamsvid_sempoloshen_unbrak"),

    "ru_ig_in": create_button("Далее ➡️", "ru_ig_in"),
    "ru_ig_out": create_button("Далее ➡️", "ru_ig_out"),
    "ru_ig_board": create_button("Далее ➡️", "ru_ig_board"),

    "ru_ig_in_sitizen": create_button("Далее ➡️", "ru_ig_in_sitizen"),

    "ru_ig_in_sitizen_manual": create_button("Далее ➡️", "ru_ig_in_sitizen_manual"),
    "ru_ig_in_sitizen_inf": create_button("Далее ➡️", "ru_ig_in_sitizen_inf"),
    "ru_ig_in_sitizen_pris": create_button("Далее ➡️", "ru_ig_in_sitizen_pris"),

    "ru_ig_in_sitizen_manual_vng_yes": create_button("Да ✅", "ru_ig_in_sitizen_manual_vng_yes"),
    "ru_ig_in_sitizen_manual_vng_no": create_button("Нет ❌", "ru_ig_in_sitizen_manual_vng_no"),

    "ru_ig_in_sitizen_manual_vng+sertrus_yes": create_button("Да ✅", "ru_ig_in_sitizen_manual_vng+sertrus_yes"),
    "ru_ig_in_sitizen_manual_vng+sertrus_no": create_button("Нет ❌", "ru_ig_in_sitizen_manual_vng+sertrus_no"),

    "ru_ig_in_sitizen_manual_vng+gosprog_yes": create_button("Да ✅", "ru_ig_in_sitizen_manual_vng+gosprog_yes"),
    "ru_ig_in_sitizen_manual_vng+gosprog_no": create_button("Нет ❌", "ru_ig_in_sitizen_manual_vng+gosprog_no"),

    "ru_ig_in_sitizen_vng_only_sng": create_button("Далее ➡️", "ru_ig_in_sitizen_vng_only_sng"),
    "ru_ig_in_sitizen_vng_only_blizkorod": create_button("Далее ➡️", "ru_ig_in_sitizen_vng_only_blizkorod"),
    "ru_ig_in_sitizen_vng_only_vladeyrus": create_button("Далее ➡️", "ru_ig_in_sitizen_vng_only_vladeyrus"),
    "ru_ig_in_sitizen_vng_only_lbgussr": create_button("Далее ➡️", "ru_ig_in_sitizen_vng_only_lbgussr"),
    "ru_ig_in_sitizen_vng_only_borninussr": create_button("Далее ➡️", "ru_ig_in_sitizen_vng_only_borninussr"),
    "ru_ig_in_sitizen_vng_only_nothing": create_button("Далее ➡️", "ru_ig_in_sitizen_vng_only_nothing"),

    "ru_ig_in_sitizen_vng_only_sng_yes": create_button("Да ✅", "ru_ig_in_sitizen_vng_only_sng_yes"),
    "ru_ig_in_sitizen_vng_only_sng_no": create_button("Нет ❌", "ru_ig_in_sitizen_vng_only_sng_no"),

    "ru_ig_in_sitizen_vng_only_sng_blizrod_yes": create_button("Да ✅", "ru_ig_in_sitizen_vng_only_sng_blizrod_yes"),
    "ru_ig_in_sitizen_vng_only_sng_blizrod_no": create_button("Нет ❌", "ru_ig_in_sitizen_vng_only_sng_blizrod_no"),
}

key_s = {

    "lang_key": create_keyboard(buttons["rus"], buttons["en"]),

    "ru_rf_key": create_keyboard(buttons["ru_rf"], buttons["ru_ig"], buttons["ru_ukr"], buttons["ru_org"]),


    "ru_rf_in_key": create_keyboard(buttons["ru_rf_in"], buttons["ru_rf_out"], buttons['ru_rf_back']),
    # "ru_rf_out_key": create_keyboard(buttons["ru_rf_out"]),
    # "ru_rf_back_key": create_keyboard(buttons['ru_rf_back']),

    "ru_rf_in_pasp_key": create_keyboard(buttons["ru_rf_in_pasp"], buttons["ru_rf_in_zp"],buttons["ru_rf_in_regliv"], buttons["ru_rf_in_gospr"],
                                         buttons["ru_rf_in_peres"],buttons["ru_rf_in_famin"],buttons["ru_rf_in_outsitiz"], buttons['ru_rf_in_back']),
    # "ru_rf_in_zp_key": create_keyboard(buttons["ru_rf_in_zp"]),
    # "ru_rf_in_regliv_key": create_keyboard(buttons["ru_rf_in_regliv"]),
    # "ru_rf_in_gospr_key": create_keyboard(buttons["ru_rf_in_gospr"]),
    # "ru_rf_in_peres_key": create_keyboard(),
    # "ru_rf_in_famin_key": create_keyboard(),
    # "ru_rf_in_outsitiz_key": create_keyboard(),
    # "ru_rf_in_back_key": create_keyboard(),

    "ru_rf_in_pasp_faq_key": create_keyboard(buttons["ru_rf_in_pasp_faq"], buttons["ru_rf_in_pasp_sit"], buttons['ru_rf_in_pasp_back']),
    # "ru_rf_in_pasp_sit_key": create_keyboard(),
    # "ru_rf_in_pasp_back_key": create_keyboard(),
    "ru_rf_in_pasp_1_back_key": create_keyboard(buttons['ru_rf_in_pasp_1_back']),

    "ru_rf_in_zp_faq_key": create_keyboard(buttons["ru_rf_in_zp_faq"], buttons["ru_rf_in_zp_sit"], buttons["ru_rf_in_zp_back"]),
    # "ru_rf_in_zp_sit_key": create_keyboard(),
    # "ru_rf_in_zp_back_key": create_keyboard(),

    "ru_rf_in_zp_1_back_key": create_keyboard(buttons['ru_rf_in_zp_1_back']),

    "ru_rf_in_regliv_faq_key": create_keyboard(buttons["ru_rf_in_regliv_faq"], buttons["ru_rf_in_regliv_sit"], buttons["ru_rf_in_zp_back"]),
    #"ru_rf_in_regliv_sit_key": create_keyboard(buttons["ru_rf_in_regliv_sit"]),
    "ru_rf_in_regliv_sit_back_key": create_keyboard(buttons["ru_rf_in_regliv_sit_back"]),

    "ru_rf_in_regliv_sit_chchel_key": create_keyboard(buttons["ru_rf_in_regliv_sit_chchel"]),
    "ru_rf_in_regliv_sit_snone_key": create_keyboard(buttons["ru_rf_in_regliv_sit_snone"]),
    "ru_rf_in_regliv_sit_pereezd_key": create_keyboard(buttons["ru_rf_in_regliv_sit_pereezd"]),
    "ru_rf_in_regliv_sit_pereezd_back_key": create_keyboard(buttons["ru_rf_in_regliv_sit_pereezd_back"]),

    "ru_rf_in_regliv_sit_pereezd1_back_key": create_keyboard(buttons["ru_rf_in_regliv_sit_pereezd1_back"]),
    "ru_rf_in_regliv_sit_pereezd_yes-no_key": create_keyboard(buttons["ru_rf_in_regliv_sit_pereezd_yes"],
                                                              buttons["ru_rf_in_regliv_sit_pereezd_no"], buttons["ru_rf_in_regliv_sit_pereezd1_back"]),

    "ru_rf_in_regliv_sit_pereezd_yes-no_yes-no_key": create_keyboard(buttons["ru_rf_in_regliv_sit_pereezd_yes_yes"],
                                                              buttons["ru_rf_in_regliv_sit_pereezd_yes_no"]),

    "ru_rf_in_regliv_sit_pereezd_yes-no_yes-no_key_1": create_keyboard(buttons["ru_rf_in_regliv_sit_pereezd_yes_yes_mfc"],
                                                              buttons["ru_rf_in_regliv_sit_pereezd_yes_yes_epgu"]),

    "ru_rf_in_gospr_razmpod_key": create_keyboard(buttons["ru_rf_in_gospr_razmpod"], buttons["ru_rf_in_gospr_porpolpod"], buttons["ru_rf_in_gospr_zamsvid"],
                                                          buttons["ru_rf_in_gospr_zaksroksvid"], buttons["ru_rf_in_gospr_anulsvid"], buttons["ru_rf_in_gospr_otkazsam"],
                                                          buttons["ru_rf_in_gospr_mneotkazali"], buttons["ru_rf_in_gospr_mneotkazalevydat"], buttons['ru_rf_in_pasp_back']),
    "ru_rf_in_gospr_porpolpod_key": create_keyboard(buttons["ru_rf_in_gospr_porpolpod"]),
    "ru_rf_in_gospr_zamsvid_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid"]),
    "ru_rf_in_gospr_zaksroksvid_key": create_keyboard(buttons["ru_rf_in_gospr_zaksroksvid"]),
    "ru_rf_in_gospr_anulsvid_key": create_keyboard(buttons["ru_rf_in_gospr_anulsvid"]),
    "ru_rf_in_gospr_otkazsam_key": create_keyboard(buttons["ru_rf_in_gospr_otkazsam"]),
    "ru_rf_in_gospr_mneotkazali_key": create_keyboard(buttons["ru_rf_in_gospr_mneotkazali"]),
    "ru_rf_in_gospr_mneotkazalevydat_key": create_keyboard(buttons["ru_rf_in_gospr_mneotkazalevydat"]),

    "ru_rf_in_gospr_razmpod_yes-no_key": create_keyboard(buttons["ru_rf_in_gospr_razmpod_yes"], buttons["ru_rf_in_gospr_razmpod_no"]),
    "ru_rf_in_gospr_porpolpod_1_key": create_keyboard(buttons["ru_rf_in_gospr_porpolpod_1"]),
    "ru_rf_in_gospr_mneotkazali_1_key": create_keyboard(buttons["ru_rf_in_gospr_mneotkazali1"]),

    "ru_rf_in_gospr_zamsvid_sostavsevi_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_sostavsevi"]),
    "ru_rf_in_gospr_zamsvid_sempoloshen_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_sempoloshen"]),
    "ru_rf_in_gospr_zamsvid_poteryali_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_poteryali"]),
    "ru_rf_in_gospr_zamsvid_smenaystdannyh_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_smenaystdannyh"]),
    "ru_rf_in_gospr_zamsvid_svidoshibky_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_svidoshibky"]),
    "ru_rf_in_gospr_zamsvid_svidneprigodno_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_svidneprigodno"]),
    "ru_rf_in_gospr_zamsvid_svidsispravl_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_svidsispravl"]),
    "ru_rf_in_gospr_zamsvid_utratastatusa_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_utratastatusa"]),

    "ru_rf_in_gospr_zamsvid_sostavsevi_rebenok_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_sostavsevi_rebenok"]),
    "ru_rf_in_gospr_zamsvid_sostavsevi_umer_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_sostavsevi_umer"]),

    "ru_rf_in_gospr_zamsvid_sempoloshen_brak_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_sempoloshen_brak"]),
    "ru_rf_in_gospr_zamsvid_sempoloshen_unbrak_key": create_keyboard(buttons["ru_rf_in_gospr_zamsvid_sempoloshen_unbrak"]),

    "ru_ig_in_key": create_keyboard(buttons["ru_ig_in"]),
    "ru_ig_out_key": create_keyboard(buttons["ru_ig_out"]),
    "ru_ig_board_key": create_keyboard(buttons["ru_ig_board"]),

    "ru_ig_in_sitizen_key": create_keyboard(buttons["ru_ig_in_sitizen"]),

    "ru_ig_in_sitizen_manual_key": create_keyboard(buttons["ru_ig_in_sitizen_manual"]),
    "ru_ig_in_sitizen_inf_key": create_keyboard(buttons["ru_ig_in_sitizen_inf"]),
    "ru_ig_in_sitizen_pris_key": create_keyboard(buttons["ru_ig_in_sitizen_pris"]),

    "ru_ig_in_sitizen_manual_vng_key": create_keyboard(buttons["ru_ig_in_sitizen_manual_vng_yes"],
                                                       buttons["ru_ig_in_sitizen_manual_vng_no"]),

    "ru_ig_in_sitizen_manual_vng+sertrus_key": create_keyboard(buttons["ru_ig_in_sitizen_manual_vng+sertrus_yes"],
                                                               buttons["ru_ig_in_sitizen_manual_vng+sertrus_no"]),

    "ru_ig_in_sitizen_manual_vng+gosprog_key": create_keyboard(buttons["ru_ig_in_sitizen_manual_vng+gosprog_yes"],
                                                               buttons["ru_ig_in_sitizen_manual_vng+gosprog_no"]),


    "ru_ig_in_sitizen_vng_only_sng_key": create_keyboard(buttons['ru_ig_in_sitizen_vng_only_sng']),
    "ru_ig_in_sitizen_vng_only_blizkorod_key": create_keyboard(buttons["ru_ig_in_sitizen_vng_only_blizkorod"]),
    "ru_ig_in_sitizen_vng_only_vladeyrus_key": create_keyboard(buttons["ru_ig_in_sitizen_vng_only_vladeyrus"]),
    "ru_ig_in_sitizen_vng_only_lbgussr_key": create_keyboard(buttons[ "ru_ig_in_sitizen_vng_only_lbgussr"]),
    "ru_ig_in_sitizen_vng_only_borninussr_key": create_keyboard(buttons["ru_ig_in_sitizen_vng_only_borninussr"]),
    "ru_ig_in_sitizen_vng_only_nothing_key": create_keyboard(buttons["ru_ig_in_sitizen_vng_only_nothing"]),

    "ru_ig_in_sitizen_vng_only_sng_yn_key": create_keyboard(buttons["ru_ig_in_sitizen_vng_only_sng_yes"],
                                                               buttons["ru_ig_in_sitizen_vng_only_sng_no"]),

"ru_ig_in_sitizen_vng_only_sng_blizrod_yn_key": create_keyboard(buttons["ru_ig_in_sitizen_vng_only_sng_blizrod_yes"],
                                                                buttons["ru_ig_in_sitizen_vng_only_sng_blizrod_no"])
}
