import logging
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from ..keyboards import rate_question_kb, rate_confirm_kb
from ..states import RateTicket
from ..utils import send_feedback
from .tickets import render_tickets_page

logger = logging.getLogger(__name__)
router = Router()


QUESTION_TEXTS = {
    1: "Выполнено без задержек?",
    2: "Выполнен полный набор измерений?",
    3: "Качество работы Вас устраивает?",
}

QUESTION_STATES = {
    1: RateTicket.question_1,
    2: RateTicket.question_2,
    3: RateTicket.question_3,
}


async def ask_question(callback: types.CallbackQuery, number: int) -> None:
    await callback.message.edit_text(
        QUESTION_TEXTS[number], reply_markup=rate_question_kb(number)
    )


async def render_confirmation(callback: types.CallbackQuery, data: dict) -> None:
    q1 = "✅" if data.get("question_1", False) else "❌"
    q2 = "✅" if data.get("question_2", False) else "❌"
    q3 = "✅" if data.get("question_3", False) else "❌"

    text = (
        "Проверьте ваши ответы:\n\n"
        f"{q1} Выполнено без задержек\n"
        f"{q2} Выполнен полный набор измерений\n"
        f"{q3} Качество работы Вас устраивает"
    )
    await callback.message.edit_text(text, reply_markup=rate_confirm_kb())


@router.callback_query(F.data.startswith("ticket_rate_"))
async def rate_ticket(callback: types.CallbackQuery, state: FSMContext):
    """Начинает процесс оценки"""
    username = callback.from_user.username
    ticket_id = int(callback.data.split("_")[-1])
    logger.info(f"User {username} rating ticket #{ticket_id}")

    await state.update_data(ticket_id=ticket_id)
    await state.set_state(RateTicket.question_1)
    await ask_question(callback, 1)


@router.callback_query(
    StateFilter(
        RateTicket.question_1,
        RateTicket.question_2,
        RateTicket.question_3,
    ),
    F.data.startswith("rate_q"),
)
async def handle_question_answer(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает ответы на вопросы оценки"""
    _, question_raw, answer_raw = callback.data.split("_")
    question_number = int(question_raw.replace("q", ""))
    answer_value = answer_raw == "yes"

    await state.update_data({f"question_{question_number}": answer_value})

    if question_number < len(QUESTION_TEXTS):
        next_number = question_number + 1
        await state.set_state(QUESTION_STATES[next_number])
        await ask_question(callback, next_number)
        return

    await state.set_state(RateTicket.confirm)
    data = await state.get_data()
    await render_confirmation(callback, data)


@router.callback_query(F.data == "rate_confirm")
async def confirm_rate(callback: types.CallbackQuery, state: FSMContext):
    """Отправляет оценку"""
    username = callback.from_user.username
    data = await state.get_data()
    ticket_id = data.get("ticket_id")
    question_1 = data.get("question_1", False)
    question_2 = data.get("question_2", False)
    question_3 = data.get("question_3", False)

    success = await send_feedback(
        username, ticket_id, question_1, question_2, question_3
    )
    await state.clear()

    if success:
        await callback.answer("Заявка оценена", show_alert=True)
        await render_tickets_page(callback, username, "open", 0)
        logger.info(f"User {username} successfully rated ticket #{ticket_id}")
    else:
        await callback.answer(
            "Ошибка при отправке оценки. Попробуйте позже.", show_alert=True
        )
        logger.error(f"User {username} failed to rate ticket #{ticket_id}")
