import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram import F
from ..keyboards import main_menu_kb
from ..utils import get_project_info

logger = logging.getLogger(__name__)
router = Router()


async def show_main_menu(username):
    """Формирует сообщение и клавиатуру главного меню"""
    info = await get_project_info(username)
    if not info:
        msg = (
            "Похоже, вы ещё не зарегистрированы в системе."
        )
        return msg, None
    fio = info.get("responsible_fio", "")
    proj = info.get("project_name", "Ваш проект")
    is_open = info.get("is_open", 0)
    msg = (
        f"Добрый день!\n"
        f"Ваш проект: {proj}\n"
        f"Ответственный за проект: {fio}\n"
        f"Перед началом работы обновите форму командой: /start."
    )
    if not is_open:
        msg += "\n\nВ данный момент регистрация новых заявок закрыта."
        kb = main_menu_kb(open_allowed=False)
    else:
        kb = main_menu_kb(open_allowed=True)
    return msg, kb


async def handle_main_menu(username, send_func):
    """Обрабатывает показ главного меню"""
    msg, kb = await show_main_menu(username)
    if msg and kb:
        await send_func(msg, reply_markup=kb)
        logger.info(f"Main menu shown for user: {username}")
    if msg:
        await send_func(msg)
        logger.info(f"Main not menu shown for user: {username}")
    else:
        await send_func("Ошибка доступа.")
        logger.error(f"Failed to show main menu for user: {username}")


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    username = message.from_user.username
    if not username:
        logger.warning(
            f"Start command from user without username (ID: {message.from_user.id})"
        )
        await message.answer(
            "Не найдено имя пользователя Telegram (username). Это требуется для доступа к сервису."
        )
        return
    logger.info(f"Start command from user: {username} (ID: {message.from_user.id})")
    await handle_main_menu(username, message.answer)


@router.callback_query(F.data == "back_main")
async def back_to_menu(callback: types.CallbackQuery):
    username = callback.from_user.username
    logger.debug(f"Back to main menu from user: {username}")
    await handle_main_menu(username, callback.message.edit_text)
