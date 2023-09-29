from aiogram.dispatcher.filters.state import State, StatesGroup


class InstructorForm(StatesGroup):
    ism = State()
    familiya = State()
    telefon = State()
    tuman = State()
    toifa = State()
    moshina = State()
    nomeri = State()


class EditInstructor(StatesGroup):
    ism = State()
    familiya = State()
    telefon = State()
    tuman = State()
    toifa = State()
    moshina = State()
    nomeri = State()


class DeleteIns(StatesGroup):
    yes_or_no = State()


class Info(StatesGroup):
    tm = State()
