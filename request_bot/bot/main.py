import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from bot.config import BOT_TOKEN
from bot.handlers.start import router as start_router
from bot.handlers.tickets import router as tickets_router
from bot.handlers.rate import router as rate_router
from bot.handlers.create_ticket import router as create_ticket_router

logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(tickets_router)
dp.include_router(rate_router)
dp.include_router(create_ticket_router)


async def main():
    logger.info("Starting bot...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Fatal error in bot: {e}", exc_info=True)
        raise
    finally:
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
