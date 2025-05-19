from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram import F
import cv2
import main
import true_false


bot_token = "7862424051:AAG0o6XtaM9H9lElz6Za-rhfpNLH5IvfZlo"

states = {'status': None}

bot = Bot(token=bot_token)
dp = Dispatcher()
n = 0
def otpravka_photo(nomer_kameri):
    coordinates, image = main.get_image_and_coordinates(nomer_kameri)  # Получение координат парковок и обрезанного изображения
    _, image = main.detected_image(image)  # Распознавание авто
    main.draw_parking(coordinates, image)  # Отрисовка парковок
    coordinates, image = main.get_image_and_coordinates(nomer_kameri) # Получение координат парковок и обрезанного изображения
    transport_box, image = main.detected_image(image) # Распознавание авто
    main.draw_parking(coordinates, image) # Отрисовка парковок
    t_f = true_false.true_false(coordinates, transport_box) # Массив True/False
    true_false.draw_parking_markings(coordinates, image, t_f) # Отрисовка занятых/свободных мест

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
        await message.answer_photo(photo=FSInputFile('src/img/result.jpg'))

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

