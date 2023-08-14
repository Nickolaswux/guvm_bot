from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_button(text, callback_data):
    return InlineKeyboardButton(text, callback_data=callback_data)

def create_keyboard(*buttons):
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(button)
    return keyboard


buttons = {
    "rus": create_button("🇷🇺 Русский 🇷🇺", "rus"),
    "en": create_button("🇬🇧 English 🇬🇧", "en"),

    "ru_rf": create_button("Далее ➡️", "ru_rf"),
    "ru_ig": create_button("Далее ➡️", "ru_ig"),
    "ru_ukr": create_button("Далее ➡️", "ru_ukr"),
    "ru_org": create_button("Далее ➡️", "ru_org"),

    "ru_rf_in": create_button("Далее ➡️", "ru_rf_in"),
    "ru_rf_out": create_button("Далее ➡️", "ru_rf_out"),

    "ru_rf_in_pasp": create_button("Далее ➡️", "ru_rf_in_pasp"),
    "ru_rf_in_zp": create_button("Далее ➡️", "ru_rf_in_zp"),
    "ru_rf_in_regliv": create_button("Далее ➡️", "ru_rf_in_regliv"),
    "ru_rf_in_gospr": create_button("Далее ➡️", "ru_rf_in_gospr"),
    "ru_rf_in_peres": create_button("Далее ➡️", "ru_rf_in_peres"),
    "ru_rf_in_famin": create_button("Далее ➡️", "ru_rf_in_famin"),
    "ru_rf_in_outsitiz": create_button("Далее ➡️", "ru_rf_in_outsitiz"),

    "ru_rf_in_pasp_faq": create_button("Далее ➡️", "ru_rf_in_pasp_faq"),
    "ru_rf_in_pasp_sit": create_button("Далее ➡️", "ru_rf_in_pasp_sit"),

    "ru_rf_in_zp_faq": create_button("Далее ➡️", "ru_rf_in_zp_faq"),
    "ru_rf_in_zp_sit": create_button("Далее ➡️", "ru_rf_in_zp_sit"),

    "ru_rf_in_regliv_faq": create_button("Далее ➡️", "ru_rf_in_regliv_faq"),
    "ru_rf_in_regliv_sit": create_button("Далее ➡️", "ru_rf_in_regliv_sit"),

    "ru_rf_in_regliv_sit_chchel": create_button("Далее ➡️", "ru_rf_in_regliv_sit_chchel"),
    "ru_rf_in_regliv_sit_snone": create_button("Далее ➡️", "ru_rf_in_regliv_sit_snone"),
    "ru_rf_in_regliv_sit_pereezd": create_button("Далее ➡️", "ru_rf_in_regliv_sit_pereezd"),

    "ru_rf_in_regliv_sit_pereezd_yes": create_button("Да ✅", "ru_rf_in_regliv_sit_pereezd_yes"),
    "ru_rf_in_regliv_sit_pereezd_no": create_button("Нет ❌", "ru_rf_in_regliv_sit_pereezd_no"),

    "ru_rf_in_regliv_sit_pereezd_yes_yes": create_button("Да ✅", "ru_rf_in_regliv_sit_pereezd_yes_yes"),
    "ru_rf_in_regliv_sit_pereezd_yes_no": create_button("Нет ❌", "ru_rf_in_regliv_sit_pereezd_yes_no"),

    "ru_rf_in_regliv_sit_pereezd_yes_yes_mfc": create_button("МФЦ", "ru_rf_in_regliv_sit_pereezd_yes_yes_mfc"),
    "ru_rf_in_regliv_sit_pereezd_yes_yes_epgu": create_button("ЕПГУ", "ru_rf_in_regliv_sit_pereezd_yes_yes_epgu"),
}

key_s = {
    "lang_key": create_keyboard(buttons["rus"], buttons["en"]),

    "ru_rf_key": create_keyboard(buttons["ru_rf"]),
    "ru_ig_key": create_keyboard(buttons["ru_ig"]),
    "ru_ukr_key": create_keyboard(buttons["ru_ukr"]),
    "ru_org_key": create_keyboard(buttons["ru_org"]),

    "ru_rf_in_key": create_keyboard(buttons["ru_rf_in"]),
    "ru_rf_out_key": create_keyboard(buttons["ru_rf_out"]),

    "ru_rf_in_pasp_key": create_keyboard(buttons["ru_rf_in_pasp"]),
    "ru_rf_in_zp_key": create_keyboard(buttons["ru_rf_in_zp"]),
    "ru_rf_in_regliv_key": create_keyboard(buttons["ru_rf_in_regliv"]),
    "ru_rf_in_gospr_key": create_keyboard(buttons["ru_rf_in_gospr"]),
    "ru_rf_in_peres_key": create_keyboard(buttons["ru_rf_in_peres"]),
    "ru_rf_in_famin_key": create_keyboard(buttons["ru_rf_in_famin"]),
    "ru_rf_in_outsitiz_key": create_keyboard(buttons["ru_rf_in_outsitiz"]),

    "ru_rf_in_pasp_faq_key": create_keyboard(buttons["ru_rf_in_pasp_faq"]),
    "ru_rf_in_pasp_sit_key": create_keyboard(buttons["ru_rf_in_pasp_sit"]),

    "ru_rf_in_zp_faq_key": create_keyboard(buttons["ru_rf_in_zp_faq"]),
    "ru_rf_in_zp_sit_key": create_keyboard(buttons["ru_rf_in_zp_sit"]),

    "ru_rf_in_regliv_faq_key": create_keyboard(buttons["ru_rf_in_regliv_faq"]),
    "ru_rf_in_regliv_sit_key": create_keyboard(buttons["ru_rf_in_regliv_sit"]),

    "ru_rf_in_regliv_sit_chchel_key": create_keyboard(buttons["ru_rf_in_regliv_sit_chchel"]),
    "ru_rf_in_regliv_sit_snone_key": create_keyboard(buttons["ru_rf_in_regliv_sit_snone"]),
    "ru_rf_in_regliv_sit_pereezd_key": create_keyboard(buttons["ru_rf_in_regliv_sit_pereezd"]),

    "ru_rf_in_regliv_sit_pereezd_yes-no_key": create_keyboard(buttons["ru_rf_in_regliv_sit_pereezd_yes"],
                                                              buttons["ru_rf_in_regliv_sit_pereezd_no"]),

    "ru_rf_in_regliv_sit_pereezd_yes-no_yes-no_key": create_keyboard(buttons["ru_rf_in_regliv_sit_pereezd_yes_yes"],
                                                              buttons["ru_rf_in_regliv_sit_pereezd_yes_no"]),
    "ru_rf_in_regliv_sit_pereezd_yes-no_yes-no_key_1": create_keyboard(buttons["ru_rf_in_regliv_sit_pereezd_yes_yes_mfc"],
                                                              buttons["ru_rf_in_regliv_sit_pereezd_yes_yes_epgu"]),
}
