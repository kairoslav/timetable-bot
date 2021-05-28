from datetime import datetime
import json

import pytz
from aiogram.types import Message, CallbackQuery

from keyboards.inline.chose_day_keyboard import chose_day_keyboard
from loader import dp

short_day_name = {
    "Пн": "Monday",
    "Вт": "Tuesday",
    "Ср": "Wednesday",
    "Чт": "Thursday",
    "Пт": "Friday",
    "Сб": "Saturday",
    "Вс": "Sunday"
}

day_name = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}


@dp.message_handler(text="Расписание на определенный день")
async def chose_day(message: Message):
    await message.answer(text="Выберите день недели",
                         reply_markup=chose_day_keyboard)


@dp.callback_query_handler(text="cancel")
async def cancel_day_chose(call: CallbackQuery):
    await call.answer("Отмена", show_alert=True)
    await call.message.edit_reply_markup()


@dp.callback_query_handler(state="*")
async def chose_day(call: CallbackQuery):
    await call.answer(cache_time=60)
    chosen_day = call.data
    print(chosen_day)
    with open("data/timetable.json", "r", encoding='utf-8') as f:
        timetable = json.load(f)
        print(timetable)
        for day_of_week in timetable:
            if day_of_week.get("day") == short_day_name.get(chosen_day):
                today_classes = day_of_week.get("classes")
                all_today_classes = ""
                for class_ in today_classes:
                    all_today_classes += f"{class_.get('name')} c {class_.get('start_time')} до {class_.get('end_time')}, аудитория {class_.get('place')}\n"
        await call.message.answer(text=all_today_classes)
        await call.message.edit_reply_markup()



@dp.message_handler(text="Расписание на сегодня")
async def today_timetable(message: Message):
    with open("data/timetable.json", "r", encoding='utf-8') as f:
        timetable = json.load(f)
        today_date = datetime.now(pytz.timezone('Europe/Moscow'))
        day, hour, minute = day_name.get(today_date.weekday()), today_date.hour, today_date.minute
        hour_minute = str(hour) + ":" + str(minute)

        print(timetable)
        for day_of_week in timetable:
            if day_of_week.get("day") == day:
                today_classes = day_of_week.get("classes")
                all_today_classes = ""
                for class_ in today_classes:
                    all_today_classes += f"{class_.get('name')} c {class_.get('start_time')} " \
                                         f"до {class_.get('end_time')}, аудитория {class_.get('place')}\n "
        if len(all_today_classes) == 0:
            await message.answer("Пар сегодня нет, иди отдыхай, боец.")
            return
        await message.answer(text=all_today_classes)


@dp.message_handler(text="Какая сейчас пара?")
async def class_now(message: Message):
    print(message.chat.full_name)
    with open("data/timetable.json", "r", encoding='utf-8') as f:
        timetable = json.load(f)
    today_date = datetime.now(pytz.timezone('Europe/Moscow'))
    day, hour, minute = day_name.get(today_date.weekday()), today_date.hour, today_date.minute
    if minute // 10 == 0:
        minute = "0" + str(minute)
    if hour // 10 == 0:
        hour = "0" + str(hour)
    hour_minute = str(hour) + ":" + str(minute)
    print(hour_minute)
    print(timetable)
    for day_of_week in timetable:
        if day_of_week.get("day") == day:
            today_classes = day_of_week.get("classes")
            if len(today_classes) == 0:
                await message.answer("На сегодня пар нет.")
            for class_index, class_ in enumerate(today_classes):
                # пары закончились
                if today_classes[len(today_classes) - 1].get("end_time") <= hour_minute:
                    await message.answer(text="Пар на сегодня больше нет! Пора пить пиво 🍺!")
                    return
                # Пара идёт сейчас
                elif class_.get("start_time") <= hour_minute <= class_.get("end_time"):
                    await message.answer(text=f"Сейчас {class_.get('name')} в {class_.get('place')}, окончание в {class_.get('end_time')}")
                # Перерыв между парами
                elif class_.get("end_time") <= hour_minute <= today_classes[class_index + 1].get("start_time"):
                    await message.answer(text=f"Сейчас перерыв, следующая пара {today_classes[class_index + 1].get('name')}, "
                                              f"начало в {today_classes[class_index + 1].get('start_time')}, аудитория {class_.get('place')}")
                # пары еще не начинались
                elif hour_minute < today_classes[0].get("start_time"):
                    await message.answer(text=f"Пары еще не начались, следующая пара {today_classes[0].get('name')} в {today_classes[0].get('start_time')}, аудитория {today_classes[0].get('place')}")
                    return
            print(today_classes)
    # await message.answer()
