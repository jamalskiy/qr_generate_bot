from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.config import API_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


class QRStates(StatesGroup):
    waiting_for_qr_text = State()
    waiting_for_qr_photo = State()

main_menu = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(text="Создать QR", callback_data="create_qr"),
    InlineKeyboardButton(text="Распознать QR", callback_data="recognize_qr")
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="start")
async def start_handler(message: types.Message):
    with open("gif.mp4", "rb") as animation:
        await message.answer_animation(
            animation=animation,
            caption="Привет! Я бот, который создаёт и распознаёт QR-коды.\nВыберите подходящий пункт:",
            reply_markup=main_menu,
        )


@dp.callback_query_handler(lambda c: c.data in ["create_qr", "recognize_qr"])
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "create_qr":
        await QRStates.waiting_for_qr_text.set()
        await bot.edit_message_caption(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            caption="Введите текст для создания QR-кода:",
            reply_markup=None,
        )
    elif callback_query.data == "recognize_qr":
        await QRStates.waiting_for_qr_photo.set()
        await bot.edit_message_caption(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            caption="Отправьте изображение с QR-кодом, который вы хотите распознать:",
            reply_markup=None,
        )


@dp.message_handler(state=QRStates.waiting_for_qr_text, content_types=types.ContentTypes.TEXT)
async def create_qr_handler(message: types.Message, state: FSMContext):
    user_text = message.text
    chat_id = message.chat.id

    await message.delete()

    qr_image = qrcode.make(user_text)
    qr_image_path = f"qr_{chat_id}.png"
    qr_image.save(qr_image_path)

    try:
        with open(qr_image_path, "rb") as qr_file:
            await bot.edit_message_media(
                media=InputMediaPhoto(
                    media=qr_file,
                    caption="Вот ваш QR-код!",
                ),
                chat_id=chat_id,
                message_id=message.message_id - 1,
            )

        await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message.message_id - 1,
            caption="Вот ваш QR-код!",
            reply_markup=main_menu,
        )

    except Exception as e:
        with open(qr_image_path, "rb") as qr_file:
            await bot.send_photo(chat_id=chat_id, photo=qr_file, caption="Вот ваш QR-код!", reply_markup=main_menu)

    await state.finish()


@dp.message_handler(state=QRStates.waiting_for_qr_photo, content_types=types.ContentTypes.PHOTO)
async def recognize_qr_handler(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    photo = await bot.download_file(file_path)

    image = Image.open(photo)

    decoded_objects = decode(image)
    if decoded_objects:
        qr_data = decoded_objects[0].data.decode("utf-8")
        caption = f"Распознанный текст: {qr_data}"
    else:
        caption = "QR-код не распознан."

    try:
        await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message.message_id - 1,
            caption=caption,
            reply_markup=main_menu,
        )
        await message.delete()

    except Exception as e:
        await message.delete()
        with open("gif.mp4", "rb") as animation:
            await message.answer_animation(
                animation=animation,
                caption=f"Распознанный текст: {qr_data}",
                reply_markup=main_menu,
            )

    await state.finish()
