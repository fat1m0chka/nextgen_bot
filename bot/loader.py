from aiogram import Bot, Dispatcher
from config.settings import settings


bot = Bot(
    token=settings.BOT_TOKEN
)

dp = Dispatcher()