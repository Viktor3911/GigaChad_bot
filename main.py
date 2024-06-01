import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from time import sleep
from aiogram.types import Message, ContentType
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram import F

from core.settings import settings
from core.utils.commands import set_commands

# GIGAchat

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models.gigachat import GigaChat


async def start_bot(bot: Bot):
    await set_commands(bot)

user_conversations = {}


async def start():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bot.bot_token)
    dp = Dispatcher()

# КОМАНДА СТАРТ
    @dp.message(F.text, Command("start"))
    async def get_start(message: types.Message):
        kb = [
            [
                types.KeyboardButton(text="Новый диалог")
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder=""
        )

        await message.answer(f'Привет. Я ГигаЧад, задавай вопросы', reply_markup=keyboard)

# ФИЛЬТР НА ТЕКСТ
    @dp.message(F.audio)
    async def not_text(message: types.Message):
        await message.answer(f'Я отвечаю только на запросы с текстом')

    @dp.message(F.video)
    async def not_text(message: types.Message):
        await message.answer(f'Я отвечаю только на запросы с текстом')

    @dp.message(F.photo)
    async def not_text(message: types.Message):
        await message.answer(f'Я отвечаю только на запросы с текстом')

    @dp.message(F.photo)
    async def not_text(message: types.Message):
        await message.answer(f'Я отвечаю только на запросы с текстом')

    @dp.message(F.document)
    async def not_text(message: types.Message):
        await message.answer(f'Я отвечаю только на запросы с текстом')

    @dp.message(F.sticker)
    async def not_text(message: types.Message):
        await message.answer(f'Я отвечаю только на запросы с текстом')

    @dp.message(F.voice)
    async def not_text(message: types.Message):
        await message.answer(f'Я отвечаю только на запросы с текстом')

    @dp.message(F.text)
    async def handle_text_message(message: types.Message):
        user_id = message.from_user.id

        llm = GigaChat(credentials=settings.bot.sber, verify_ssl_certs=False)
        conversation = ConversationChain(llm=llm,
                                         verbose=True,
                                         memory=ConversationBufferMemory())

    # ПРОМПТ
    #         template = '''
    # Отвечай, как ГигаЧад, пользующийся огромной популярностью в своей социальной сети, всегда уверен в себе и\
    # готов поделиться искрой своего настроения.\
    # Он всегда находится в поиске интересных идей, которыми может поделиться,\
    # и готов помочь советом, основанным на своем богатом жизненном опыте. При этом ГигаЧад никогда не забывает про границы и уважает мнения других, поддерживая положительную и созидательную атмосферу в общении.   \
    #         \n\nТекущий разговор:\n{history}\nHuman: {input}\nAI:
    #         '''
    #         conversation = ConversationChain(llm=llm,
    #                                          verbose=True,
    #                                          memory=ConversationBufferMemory())
    #         conversation.prompt.template = template
    #         conversation.prompt

        if user_id not in user_conversations:
            user_conversations[user_id] = ConversationBufferMemory()

        conversation.memory = user_conversations[user_id]

        if message.text == "Новый диалог":
            user_conversations[user_id].clear()
            await message.answer('Новый диалог создан')
        else:
            conversation.predict(input=message.text)
            await message.answer(conversation.memory.chat_memory.messages[-1].content, parse_mode='MARKDOWN')
            sleep(0)

    dp.startup.register(start_bot)

    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
