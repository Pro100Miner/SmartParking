from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram import F
import class_parking, true_false

import os
from dotenv import load_dotenv
load_dotenv()  # Загружает переменные из .env
TOKEN = os.getenv("BOT_TOKEN")  # Получает токен
bot = Bot(token=TOKEN)

states = {'status': None}

dp = Dispatcher()

def otpravka_photo(num):
    park1 = class_parking.Parking(num)
    park1.set_cropped_image()  # Получить обрезанное изображение
    park1.detect_cars()  # Распознать автомобили
    park1.is_vehicle_in_parking()  # Получить массив true_false

    park1.get_parking_layout()  # Получить макет
    true_false.draw_parking_markings(park1.parking_spots, park1.image, park1.is_in_parking)

@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.answer("    Здравствуйте!:)\nДля начала работы введите команду /rec")

@dp.message(Command(commands=['help']))
async def send_help(message: Message):
    await message.answer('        Нужна помощь? \n /start - приветствие и начало работы\n /help - помощь('
                         'да, да.. Вы сейчас именно здесь!)\n /rec - команда для выбора нужной Вам камеры\n /add -'
                         ' команда для добавление новой камеры')


@dp.message(Command(commands=['rec']))   #recognition
async def send_rec(message: Message):
    states['status'] = "rec"
    await message.answer("Введите номер парковки")

# =============================================================================

@dp.message(Command(commands=['add']))
async def start_add(message: Message):
    await message.answer("Начало добавление парковки. Введите ссылку на камеру")
    states['status'] = "add"


@dp.message(F.text)
async def add_kam(message: Message):
    text = message.text.strip()
    if states['status'] == "add":
        await message.answer("Ща добавим")
        with open('src/Камеры.txt', 'a') as f:
            f.write('\n')
            f.write(text)
        await message.answer("Теперь добавьте координаты парковок")
        states['status'] = "add_coord"
        return
    if states['status'] == "add_coord":
        await message.answer("Ща добавим")
        with open('src/Координаты.txt', 'a') as f:
            f.write("!" + '\n')
            f.write(text)
        await message.answer("Теперь добавьте координаты для обрезки камеры")
        states['status'] = "add_coord_otr"
        return
    if states['status'] == "add_coord_otr":
        await message.answer("Ща добавим")
        with open('src/НеобхФрагмент.txt', 'a') as f:
            f.write('\n')
            f.write(text)
    if states['status'] == "rec":
        await message.answer("Подождите немного!.. Сейчас всё сделаю!")
        n = int(text)
        otpravka_photo(n)
        await message.answer_photo(photo=FSInputFile('src/img/out_parking.jpg'))

@dp.message(Command(commands=['parkovka']))
async def send_welcome(message: Message):
    kb = [
        [
            types.KeyboardButton(text="/start"),
            types.KeyboardButton(text="/help"),
            types.KeyboardButton(text="/rec"),
            types.KeyboardButton(text="/add")

        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard = kb,
        resize_keyboard = True,
    )
    await message.answer("Выберите камеру", reply_markup=keyboard)


if __name__ == '__main__':
    dp.run_polling(bot)

