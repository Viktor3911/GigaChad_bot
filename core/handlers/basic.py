import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Message


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Привет. Рад видеть!')
