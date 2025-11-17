import logging
import os
import re

from aiogram import Bot, Dispatcher  
from aiogram.types import Message
from aiogram.filters.command import Command

TOKEN = os.getenv('TOKEN')
tgbot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Словарь транслитерации
TRANSLIT_MAP = {    
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': 'ie', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'iu', 'я': 'ia',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
    'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M',
    'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
    'Ъ': 'Ie', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Iu', 'Я': 'Ia'
}

def transliterate_fio(text: str) -> str:
    result = []
    for char in text:
        if char in TRANSLIT_MAP:
            result.append(TRANSLIT_MAP[char])
        else:
            result.append(char)
    return ''.join(result)

def is_cyrillic_fio(text: str) -> bool:
    return bool(re.match(r'^[а-яёА-ЯЁ\s\-]+$', text.strip()))

@dp.message(Command(commands=['start']))
async def process_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}!'
    logging.info(f'{user_name} {user_id} запустил бота!')
    await tgbot.send_message(chat_id=user_id, text=text)

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    help_text = 'Отправьте ФИО на кириллице для транслитерации'
    await message.answer(text=help_text)
    
@dp.message()
async def send_echo(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text
    logging.info(f'{user_name} {user_id}: {text}')
    
    if is_cyrillic_fio(text):
        transliterated = transliterate_fio(text)
        await message.answer(text=transliterated)
    else:
        await message.answer(text=text)
 
if __name__ == '__main__':
    dp.run_polling(tgbot)