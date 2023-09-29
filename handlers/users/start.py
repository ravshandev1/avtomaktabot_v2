from loader import dp
import requests
from data.config import BASE_URL
from keyboards.inline.main import change_lang, instructor
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from states.main import InstructorForm, EditInstructor, DeleteIns, Info
from aiogram.dispatcher import FSMContext
from keyboards.default.main import regions, categories, text_ins_reg, text_ins_up, info_btn_for_ins, main_btn, \
    text_info, info_btn, menu_instructor, profile_delete
import re

lang = ''


@dp.message_handler(commands=['start'])
async def stt(mes: Message):
    res = requests.get(url=f"{BASE_URL}/session/user/?id={mes.from_user.id}")
    r = res.json()
    if r['message'] == "Instructor":
        if lang == 'ru':
            await mes.answer("Выберите нужный раздел 👇", reply_markup=menu_instructor(lang))
        else:
            await mes.answer("Керакли булимни танланг 👇", reply_markup=menu_instructor(lang))
    else:
        await mes.answer(
            f"Ассалому алайкум, {mes.from_user.full_name}!\nАвтоинструктор ботга хуш келибсиз\nВыберите язык / Тилни танланг",
            reply_markup=change_lang)


@dp.callback_query_handler(text=['uz', 'ru'])
async def start(call: CallbackQuery):
    res = requests.get(url=f"{BASE_URL}/session/user/?id={call.from_user.id}")
    r = res.json()
    await call.message.delete()
    await call.answer(cache_time=3)
    global lang
    if r['message'] == "Instructor":
        if call.data == 'uz':
            lang = 'uz'
            await call.message.answer("Керакли булимни танланг 👇", reply_markup=menu_instructor(lang))
        elif call.data == 'ru':
            lang = 'ru'
            await call.message.answer("Выберите нужный раздел 👇", reply_markup=menu_instructor(lang))
    else:
        if call.data == 'uz':
            lang = 'uz'
            await call.message.answer(
                f"Ассалому алайкум, {call.from_user.full_name}!\nАвтоинструктор ботга хуш келибсиз. Ботимиздан фойдаланиш учун ўзингизга керакли бўлимни танланг.",
                reply_markup=main_btn(lang))
        elif call.data == 'ru':
            lang = 'ru'
            await call.message.answer(
                f"Здравствуйте, {call.from_user.full_name}!\nДобро пожаловать в Автоинструктор бот. Выберите для себя нужный раздел",
                reply_markup=main_btn(lang))


@dp.message_handler(text=["Изменить язык", "Тилни ўзгартириш"])
async def lang(mes: Message):
    await mes.answer("Выберите язык / Тилни танланг", reply_markup=change_lang)


@dp.message_handler(text=["Маълумот олиш", "Получение информации"])
async def info(mes: Message):
    if mes.text == "Маълумот олиш":
        await mes.answer("Керакли бўлимни танланг 👇", reply_markup=info_btn(lang))
    else:
        await mes.answer("Выберите нужный раздел 👇", reply_markup=info_btn(lang))


@dp.message_handler(text=["Тарифлар", "Тарифы", "Тесты", "Тест бўйича маълумотлар", "⬅️Oртга", "⬅️Назад",
                          "Онлайн дарслар", "Информация об онлайн уроках", "️Профиль", "️Профиль"])
async def ind(mes: Message):
    if mes.text == "Тарифлар":
        await mes.answer(text_info()['text'])
    elif mes.text == "Тарифы":
        await mes.answer(text_info()['text_ru'])
    elif mes.text == "Тесты":
        await mes.answer(f"Тематические тесты в этом боте. <b>{text_info()['bot_link']}</b>")
    elif mes.text == "Тест бўйича маълумотлар":
        await mes.answer(f"Мавзулар бўйича тестлар ушбу ботда. <b>{text_info()['bot_link']}</b>")
    elif mes.text == "Онлайн дарслар":
        await mes.answer(text_info()['online_lesson'])
    elif mes.text == "Информация об онлайн уроках":
        await mes.answer(text_info()['online_lesson_ru'])
    elif mes.text == "⬅️Oртга":
        await mes.answer("Керакли бўлимни танланг 👇", reply_markup=main_btn(lang))
    elif mes.text == "⬅️Назад":
        await mes.answer("Выберите нужный раздел 👇", reply_markup=main_btn(lang))
    elif mes.text == "️Профил":
        await mes.answer("Керакли бўлимни танланг 👇", reply_markup=menu_instructor(lang))
    elif mes.text == "️Профиль":
        await mes.answer("Выберите нужный раздел 👇", reply_markup=menu_instructor(lang))


@dp.message_handler(text=["Главный меню", "Бош меню"])
async def edit_profile(mes: Message):
    if lang == 'uz':
        await mes.answer("Керакли булимни танланг 👇", reply_markup=info_btn_for_ins(lang))
    else:
        await mes.answer("Выберите нужный раздел 👇", reply_markup=info_btn_for_ins(lang))


@dp.message_handler(text=["Инструкторлар ҳақида маълумотлар", "Информация об инструкторах"])
async def ma(mes: Message):
    res = requests.get(url=f"{BASE_URL}/session/")
    cts = res.json()
    if len(cts) == 0:
        if lang == 'uz':
            await mes.answer("Биздан ҳозирча инструcторлар рўйхатдан ўтмаган")
        else:
            await mes.answer("Мы ещё не зарегистрировали инструкторов")
    else:
        markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        for i in cts:
            markup.insert(KeyboardButton(text=f"{i['tuman']}"))
        if lang == 'uz':
            markup.insert(KeyboardButton("⬅️Oртга"))
            await mes.answer('Ўзингизга қулай бўлган туманни танланг', reply_markup=markup)
        else:
            markup.insert(KeyboardButton("⬅️Назад"))
            await mes.answer('Выберите удобный для вас район', reply_markup=markup)
        await Info.tm.set()


@dp.message_handler(state=Info.tm)
async def tm(mes: Message, state: FSMContext):
    if (mes.text == "⬅️Назад") or (mes.text == "⬅️Oртга"):
        res = requests.get(url=f"{BASE_URL}/session/user/?id={mes.from_user.id}")
        r = res.json()
        if r['message'] == "Instructor":
            markup = info_btn_for_ins(lang)
        else:
            markup = info_btn(lang)
        if lang == 'uz':
            await mes.answer("Керакли бўлимни танланг 👇", reply_markup=markup)
        else:
            await mes.answer("Выберите нужный раздел 👇", reply_markup=markup)
        await state.finish()
    else:
        res = requests.get(url=f"{BASE_URL}/session/?tum={mes.text}")
        cts = res.json()
        if cts:
            txt = ""
        else:
            txt = "Error"
        markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        if lang == 'uz':
            for i in cts:
                txt += f"Исм: <b>{i['ism']}</b>\nФамилия: <b>{i['familiya']}</b>\nТелефон: <b>{i['telefon']}</b>\nАвтомобил: <b>{i['moshina']}</b>\nДавлат рақами: <b>{i['nomeri']}</b>\n"
            markup.insert(KeyboardButton("⬅️Oртга"))
            await mes.answer(txt, reply_markup=markup)
        else:
            for i in cts:
                txt += f"Имя: <b>{i['ism']}</b>\nФамилия: <b>{i['familiya']}</b>\nТелефон: <b>{i['telefon']}</b>\nАвтомобиль: <b>{i['moshina']}</b>\nГос.номер: <b>{i['nomeri']}</b>\n"
            markup.insert(KeyboardButton("⬅️Назад"))
            await mes.answer(txt, reply_markup=markup)


@dp.message_handler(text=["👨‍✈️Профилни ўзгартириш", "👨‍✈️Изменение профиля"])
async def edit_profile(mes: Message):
    if lang == 'uz':
        await mes.answer("Нимани ўзгартирмоқчисиз?", reply_markup=instructor(lang))
    else:
        await mes.answer("Что вы хотите изменить?", reply_markup=instructor(lang))


@dp.message_handler(text=["️Профил", "️Профиль"])
async def edit_profile(mes: Message):
    if lang == 'uz':
        await mes.answer("Керакли булимни танланг 👇", reply_markup=menu_instructor(lang))
    else:
        await mes.answer("Выберите нужный раздел 👇", reply_markup=menu_instructor(lang))


@dp.message_handler(text=["👨‍✈️Профилни ўчириш", "👨‍✈️Удалить профиль"])
async def a(mes: Message):
    if lang == 'uz':
        await mes.answer('Профилингизни ўчирмоқчимисиз?', reply_markup=profile_delete(lang))
    else:
        await mes.answer('Хотите удалить свой профиль?', reply_markup=profile_delete(lang))
    await DeleteIns.yes_or_no.set()


@dp.message_handler(text=["👨‍✈️️Профил", "👨‍✈️️Профиль"])
async def get_profile(mes: Message):
    rp = requests.get(url=f"{BASE_URL}/instructor/{mes.from_user.id}/")
    res = rp.json()
    if lang == 'uz':
        text = f"Исмингиз: <b>{res['ism']}</b>\n"
        text += f"Фамилиянгиз: <b>{res['familiya']}</b>\n"
        text += f"Телефон рақамингиз: <b>{res['telefon']}</b>\n"
        text += f"Автомобилингиз: <b>{res['moshina']}</b>\n"
        text += f"Яшаш туманингиз: <b>{res['tuman']}</b>\n"
        text += f"Тоифангиз: <b>{res['toifa_name']}</b>\n"
        text += f"Давлат рақами: <b>{res['nomeri']}</b>\n"
        await mes.answer(text, reply_markup=menu_instructor(lang))
    else:
        text = f"Ваше имя: <b>{res['ism']}</b>\n"
        text += f"Ваша фамилия: <b>{res['familiya']}</b>\n"
        text += f"Ваш номер телефона: <b>{res['telefon']}</b>\n"
        text += f"Ваш автомобиль: <b>{res['moshina']}</b>\n"
        text += f"Ваш адрес: <b>{res['tuman']}</b>\n"
        text += f"Ваша категория: <b>{res['toifa_name']}</b>\n"
        text += f"Государственный номер: <b>{res['nomeri']}</b>\n"
        await mes.answer(text, reply_markup=menu_instructor(lang))


@dp.message_handler(text=['Регистрация в виде инструктора', 'Инструктор сифатида рўйхатдан ўтиш'])
async def register(mes: Message):
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    if mes.text == 'Инструктор сифатида рўйхатдан ўтиш':
        markup.insert(KeyboardButton("⬅️Oртга"))
        await mes.answer(text_ins_reg()['ism'], reply_markup=markup)
    elif mes.text == 'Регистрация в виде инструктора':
        markup.insert(KeyboardButton("⬅️Назад"))
        await mes.answer(text_ins_reg()['ism_ru'], reply_markup=markup)
    await InstructorForm.ism.set()


@dp.message_handler(state=InstructorForm.ism)
async def ism(mes: Message, state: FSMContext):
    if mes.text == "⬅️Назад":
        await state.finish()
        await mes.answer("Выберите нужный раздел 👇", reply_markup=main_btn(lang))
    elif mes.text == "⬅️Oртга":
        await state.finish()
        await mes.answer("Керакли бўлимни танланг 👇", reply_markup=main_btn(lang))
    else:
        await state.update_data(
            {"ism": mes.text}
        )
        if lang == 'uz':
            await mes.answer(text_ins_reg()['familiya'])
        else:
            await mes.answer(text_ins_reg()['familiya_ru'])
        await InstructorForm.next()


@dp.message_handler(state=InstructorForm.familiya)
async def familiya(mes: Message, state: FSMContext):
    await state.update_data(
        {'familiya': mes.text}
    )
    if lang == 'uz':
        await mes.answer(text_ins_reg()['telefon'])
    else:
        await mes.answer(text_ins_reg()['telefon_ru'])
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.telefon, regexp=re.compile(r"^[378]{2}|9[01345789]\d{7}$"))
async def telefon(mes: Message, state: FSMContext):
    await state.update_data(
        {'telefon': f"998{mes.text}"}
    )
    if lang == 'uz':
        await mes.answer(text_ins_reg()['manzil'], reply_markup=regions())
    else:
        await mes.answer(text_ins_reg()['manzil_ru'], reply_markup=regions())
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.telefon, content_types='text')
async def st(mes: Message):
    if lang == 'uz':
        await mes.answer(text_ins_reg()['telefon_qayta'])
    else:
        await mes.answer(text_ins_reg()['telefon_qayta_ru'])
    await InstructorForm.telefon.set()


@dp.message_handler(state=InstructorForm.tuman)
async def region(mes: Message, state: FSMContext):
    await state.update_data(
        {'tuman': mes.text}
    )
    if lang == 'uz':
        await mes.answer(text_ins_reg()['categoriya'], reply_markup=categories())
    else:
        await mes.answer(text_ins_reg()['categoriya_ru'], reply_markup=categories())
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.toifa)
async def category(mes: Message, state: FSMContext):
    await state.update_data(
        {'toifa': mes.text}
    )
    cat = await state.get_data()
    res = requests.get(url=f"{BASE_URL}/instructor/cars/?cat={cat['toifa']}")
    rg = res.json()
    markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    for i in rg:
        markup.insert(KeyboardButton(text=f"{i['nomi']}"))
    if lang == 'uz':
        await mes.answer(text_ins_reg()['moshina'], reply_markup=markup)
    else:
        await mes.answer(text_ins_reg()['moshina_ru'], reply_markup=markup)
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.moshina)
async def car(mes: Message, state: FSMContext):
    await state.update_data(
        {'moshina': mes.text}
    )
    if lang == 'uz':
        await mes.answer(text_ins_reg()['moshina_nomeri'], reply_markup=ReplyKeyboardRemove())
    else:
        await mes.answer(text_ins_reg()['moshina_nomeri_ru'], reply_markup=ReplyKeyboardRemove())
    await InstructorForm.next()


@dp.message_handler(state=InstructorForm.nomeri, regexp=re.compile(
    r"^[0-9][150][ -]([A-Z][ -][0-9]{3}[ -][A-Z]{2})|([0-9]{3}[ -][A-Z]{3})$"))
async def create_instructor(mes: Message, state: FSMContext):
    data = await state.get_data()
    data['nomeri'] = mes.text
    data['telegram_id'] = mes.from_user.id
    res = requests.post(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    r = res.json()
    if lang == 'uz':
        await mes.answer(f"{mes.from_user.first_name} {r['message']}", reply_markup=menu_instructor(lang))
    else:
        await mes.answer(f"{mes.from_user.first_name} {r['message_ru']}", reply_markup=menu_instructor(lang))
    await state.finish()


@dp.message_handler(state=InstructorForm.nomeri, content_types='text')
async def st(mes: Message):
    if lang == 'uz':
        await mes.answer(text_ins_reg()['moshina_nomeri_qayta'])
    else:
        await mes.answer(text_ins_reg()['moshina_nomeri_qayta_ru'])
    await InstructorForm.nomeri.set()


@dp.message_handler(state=DeleteIns.yes_or_no)
async def delete_profile(mes: Message, state: FSMContext):
    if (mes.text == 'Ҳа') or (mes.text == 'Да'):
        rp = requests.delete(url=f"{BASE_URL}/client/delete/{mes.from_user.id}/")
        if rp.status_code == 204:
            if lang == 'uz':
                await mes.answer("Профилингиз ўчирилди", reply_markup=ReplyKeyboardRemove())
            else:
                await mes.answer("Ваш профиль удален", reply_markup=ReplyKeyboardRemove())
        else:
            if lang == 'uz':
                await mes.answer("Нимадир хато кетди қайтадан ўриниб кўринг!")
            else:
                await mes.answer("Попробуйте еще раз, что-то пошло не так!")
    elif (mes.text == 'Йўқ') or (mes.text == 'Нет'):
        if lang == 'uz':
            await mes.answer("Керакли булимни танланг 👇", reply_markup=menu_instructor(lang))
        else:
            await mes.answer("Выберите нужный раздел 👇", reply_markup=menu_instructor(lang))
    await state.finish()


@dp.callback_query_handler(
    text=['instructor:name', 'instructor:surname', 'instructor:phone', 'car', 'number', 'region', 'cat'])
async def set_state(call: CallbackQuery):
    if call.data == "instructor:name":
        if lang == 'uz':
            await call.message.answer(text_ins_up()['ism'])
        else:
            await call.message.answer(text_ins_up()['ism_ru'])
        await EditInstructor.ism.set()
    elif call.data == "instructor:surname":
        if lang == 'uz':
            await call.message.answer(text_ins_up()['familiya'])
        else:
            await call.message.answer(text_ins_up()['familiya_ru'])
        await EditInstructor.familiya.set()
    elif call.data == "instructor:phone":
        if lang == 'uz':
            await call.message.answer(text_ins_up()['telefon'])
        else:
            await call.message.answer(text_ins_up()['telefon_ru'])
        await EditInstructor.telefon.set()
    elif call.data == "car":
        res = requests.get(url=f"{BASE_URL}/instructor/cars/")
        rg = res.json()
        markup = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        for i in rg:
            markup.insert(KeyboardButton(text=f"{i['nomi']}"))
        if lang == 'uz':
            await call.message.answer(text_ins_up()['moshina'], reply_markup=markup)
        else:
            await call.message.answer(text_ins_up()['moshina_ru'], reply_markup=markup)
        await EditInstructor.moshina.set()
    elif call.data == "region":
        if lang == 'uz':
            await call.message.answer(text_ins_up()['manzil'], reply_markup=regions())
        else:
            await call.message.answer(text_ins_up()['manzil_ru'], reply_markup=regions())
        await EditInstructor.tuman.set()
    elif call.data == 'cat':
        if lang == 'uz':
            await call.message.answer(text_ins_up()['categoriya'], reply_markup=categories())
        else:
            await call.message.answer(text_ins_up()['categoriya_ru'], reply_markup=categories())
        await EditInstructor.toifa.set()
    elif call.data == "number":
        if lang == 'uz':
            await call.message.answer(text_ins_up()['moshina_nomeri'])
        else:
            await call.message.answer(text_ins_up()['moshina_nomeri_ru'])
        await EditInstructor.nomeri.set()
    await call.answer(cache_time=3)


@dp.message_handler(content_types=['text'], state=EditInstructor.ism)
async def set_name(mes: Message, state: FSMContext):
    data = {'ism': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    if lang == 'uz':
        await mes.answer(f"Исмингиз <b>{res['ism']}</b> га ўзгартирилди!", reply_markup=menu_instructor(lang))
    else:
        await mes.answer(f"Ваше имя изменён <b>{res['ism']}</b>", reply_markup=menu_instructor(lang))
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.familiya)
async def set_surname(mes: Message, state: FSMContext):
    data = {'familiya': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    if lang == 'uz':
        await mes.answer(f"Фамилиянгиз <b>{res['familiya']}</b> га ўзгартирилди!", reply_markup=menu_instructor(lang))
    else:
        await mes.answer(f"Ваша фамилия изменён <b>{res['familiya']}</b>", reply_markup=menu_instructor(lang))
    await state.finish()


@dp.message_handler(regexp=re.compile(r"^[378]{2}|9[01345789]\d{7}$"), state=EditInstructor.telefon)
async def set_phone(mes: Message, state: FSMContext):
    data = {'telefon': f"998{mes.text}"}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    if lang == 'uz':
        await mes.answer(f"Телефонгиз <b>{res['telefon']}</b> га ўзгартирилди!", reply_markup=menu_instructor(lang))
    else:
        await mes.answer(f"Ваш номер телефона изменён <b>{res['telefon']}</b>", reply_markup=menu_instructor(lang))
    await state.finish()


@dp.message_handler(state=EditInstructor.telefon, content_types=['text'])
async def a(mes: Message):
    if lang == 'uz':
        await mes.answer(text_ins_up()['telefon_qayta'])
    else:
        await mes.answer(text_ins_up()['telefon_qayta_ru'])
    await EditInstructor.telefon.set()


@dp.message_handler(content_types=['text'], state=EditInstructor.tuman)
async def set_region(mes: Message, state: FSMContext):
    data = {'tuman': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    if lang == 'uz':
        await mes.answer(f"Яшаш туманингиз <b>{res['tuman']}</b> га ўзгартирилди!", reply_markup=menu_instructor(lang))
    else:
        await mes.answer(f"Ваш жилой район изменён <b>{res['tuman']}</b>", reply_markup=menu_instructor(lang))
    await state.finish()


@dp.message_handler(content_types=['text'], state=EditInstructor.toifa)
async def set_cat(mes: Message, state: FSMContext):
    data = {'toifa': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    if lang == 'uz':
        await mes.answer(f"Тоифанингиз <b>{res['toifa_name']}</b> га ўзгартирилди!", reply_markup=menu_instructor(lang))
    else:
        await mes.answer(f"Ваша категория изменён <b>{res['toifa_name']}</b>", reply_markup=menu_instructor(lang))
    await state.finish()


@dp.message_handler(state=EditInstructor.nomeri, regexp=re.compile(
    r"^[0-9][150][ -]([A-Z][ -][0-9]{3}[ -][A-Z]{2})|([0-9]{3}[ -][A-Z]{3})$"))
async def set_cat(mes: Message, state: FSMContext):
    data = {'nomeri': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    if lang == 'uz':
        await mes.answer(f"Мошинангиз рақами <b>{res['nomeri']}</b> га ўзгартирилди!",
                         reply_markup=menu_instructor(lang))
    else:
        await mes.answer(f"Номер вашей машины изменён <b>{res['nomeri']}</b>",
                         reply_markup=menu_instructor(lang))
    await state.finish()


@dp.message_handler(state=EditInstructor.nomeri, content_types=['text'])
async def a(mes: Message):
    if lang == 'uz':
        await mes.answer(text_ins_up()['moshina_nomeri_qayta'])
    else:
        await mes.answer(text_ins_up()['moshina_nomeri_qayta_ru'])
    await EditInstructor.nomeri.set()


@dp.message_handler(content_types=['text'], state=EditInstructor.moshina)
async def set_cat(mes: Message, state: FSMContext):
    data = {'moshina': mes.text}
    rp = requests.patch(url=f"{BASE_URL}/instructor/{mes.from_user.id}/", data=data)
    res = rp.json()
    if lang == 'uz':
        await mes.answer(f"Мошинангиз <b>{res['moshina']}</b> га ўзгартирилди!", reply_markup=menu_instructor(lang))
    else:
        await mes.answer(f"Ваша машина изменён <b>{res['moshina']}</b>", reply_markup=menu_instructor(lang))
    await state.finish()
