import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from ..keyboards import (
    tickets_list_kb,
    ticket_actions_kb,
    back_to_menu_kb,
    delete_confirm_kb,
)
from ..utils import (
    get_bookings,
    get_date_range,
    cancel_booking,
)

logger = logging.getLogger(__name__)
router = Router()


ITEMS_PER_PAGE = 7


def get_status_emoji(status: str) -> str:
    """Возвращает эмодзи кружок для статуса"""
    status_lower = status.lower()
    if status_lower == "на рассмотрении":
        return "🟠"
    elif status_lower == "отклонено":
        return "🔴"
    elif status_lower in ["принято", "выполнено"]:
        return "🟢"
    elif status_lower == "оценить":
        return "🔵"
    else:
        return ""


async def get_tickets_page(tickets, page: int):
    """Получает срез заявок для страницы"""
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    return tickets[start_idx:end_idx]


async def render_tickets_page(callback, username, ticket_type: str, page: int = 0):
    """Рендерит страницу с заявками"""
    start_date, end_date, today_date = get_date_range()
    title = "Открытые заявки:" if ticket_type == "open" else "Закрытые заявки:"

    tickets = await get_bookings(username, start_date, end_date)
    logger.debug(
        f"Retrieved {len(tickets)} tickets for filtering (date range: {start_date} to {end_date}, today: {today_date})"
    )

    if tickets:
        logger.debug(f"Sample ticket structure: {tickets[0]}")
        all_statuses = [t.get("status", "") for t in tickets]
        unique_statuses = list(set(all_statuses))
        logger.debug(f"All unique statuses in response: {unique_statuses}")

    tickets_before = len(tickets)
    if ticket_type == "open":
        open_statuses = ["принято", "на рассмотрении", "оценить"]
        tickets = [
            t
            for t in tickets
            if t.get("status", "").lower() in [s.lower() for s in open_statuses]
        ]
    else:
        closed_statuses = ["отклонено", "выполнено"]
        tickets = [
            t
            for t in tickets
            if t.get("status", "").lower() in [s.lower() for s in closed_statuses]
        ]
        if tickets_before > 0 and len(tickets) == 0:
            logger.warning(
                f"Found {tickets_before} tickets but none matched closed statuses: {closed_statuses}"
            )
            logger.warning(f"Actual statuses were: {unique_statuses}")
    logger.debug(
        f"After filtering by status '{ticket_type}': {len(tickets)} tickets (was {tickets_before})"
    )

    total_pages = (
        (len(tickets) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE if tickets else 1
    )
    page = min(page, total_pages - 1) if total_pages > 0 else 0

    page_tickets = await get_tickets_page(tickets, page)

    text = f"{title}"

    if not page_tickets:
        text += "\n\nЗаявки не найдены"
    else:
        text += "\n\n\n"
        for ticket in page_tickets:
            ticket_id = ticket.get("id", "")
            date = ticket.get("date", "N/A")
            analyse = ticket.get("analyse", "N/A")
            samples = ticket.get("samples", 0)
            status = ticket.get("status", "")
            status_emoji = get_status_emoji(status)
            text += f"{status_emoji} {ticket_id} - {date} - {analyse} - {samples}\n\n"

    if total_pages > 1:
        text += f"\nСтраница {page + 1} из {total_pages}"

    kb = tickets_list_kb(page_tickets, page, total_pages, ticket_type)
    await callback.message.edit_text(text, reply_markup=kb)


@router.callback_query(F.data == "open_tickets")
async def show_open_tickets(callback: types.CallbackQuery, state: FSMContext):
    """Показывает список открытых заявок"""
    username = callback.from_user.username
    logger.info(f"User {username} viewing open tickets")
    await state.clear()
    await render_tickets_page(callback, username, "open", 0)


@router.callback_query(F.data.startswith("open_tickets_pg_"))
async def show_open_tickets_page(callback: types.CallbackQuery):
    username = callback.from_user.username
    page = int(callback.data.split("_")[-1])
    logger.debug(f"User {username} viewing open tickets page {page}")
    await render_tickets_page(callback, username, "open", page)


async def get_ticket_by_id(username: str, ticket_id: int, ticket_type: str):
    """Получает заявку по id"""
    start_date, end_date, _ = get_date_range()

    tickets = await get_bookings(username, start_date, end_date)
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return ticket
    return None


def format_ticket_details(ticket):
    """Форматирует детали заявки"""
    status = ticket.get('status', 'N/A')
    status_emoji = get_status_emoji(status)
    text = (
        f"<b>Заявка #{ticket.get('id', 'N/A')}</b>\n\n"
        f"Проект: {ticket.get('project', 'N/A')}\n"
        f"Дата: {ticket.get('date', 'N/A')}\n"
        f"Анализ: {ticket.get('analyse', 'N/A')}\n"
        f"Прибор: {ticket.get('equipment', 'N/A')}\n"
        f"Исполнитель: {ticket.get('executor', 'N/A')}\n"
        f"Количество образцов: {ticket.get('samples', 0)}\n"
        f"Статус: {status} {status_emoji}\n"
    )
    comment = ticket.get("comment", "")
    if comment:
        text += f"Комментарий: {comment}\n"
    return text


@router.callback_query(F.data.startswith("open_ticket_details_"))
async def open_ticket_details(callback: types.CallbackQuery):
    username = callback.from_user.username
    ticket_id = int(callback.data.split("_")[-1])
    logger.debug(f"User {username} viewing ticket details #{ticket_id}")

    ticket = await get_ticket_by_id(username, ticket_id, "open")
    if not ticket:
        await callback.message.edit_text(
            "Заявка не найдена", reply_markup=back_to_menu_kb()
        )
        return

    text = format_ticket_details(ticket)
    kb = ticket_actions_kb(ticket, "open")
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("closed_ticket_details_"))
async def closed_ticket_details(callback: types.CallbackQuery):
    username = callback.from_user.username
    ticket_id = int(callback.data.split("_")[-1])
    logger.debug(f"User {username} viewing ticket details #{ticket_id}")

    ticket = await get_ticket_by_id(username, ticket_id, "closed")
    if not ticket:
        await callback.message.edit_text(
            "Заявка не найдена", reply_markup=back_to_menu_kb()
        )
        return

    text = format_ticket_details(ticket)
    kb = ticket_actions_kb(ticket, "closed")
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")


@router.callback_query(F.data.startswith("ticket_delete_"))
async def delete_ticket(callback: types.CallbackQuery, state: FSMContext):
    """Показывает подтверждение удаления"""
    ticket_id = int(callback.data.split("_")[-1])
    await state.update_data(delete_ticket_id=ticket_id)
    text = f"Вы уверены, что хотите удалить заявку #{ticket_id}?"
    await callback.message.edit_text(text, reply_markup=delete_confirm_kb(ticket_id))


@router.callback_query(F.data.startswith("delete_confirm_"))
async def confirm_delete_ticket(callback: types.CallbackQuery, state: FSMContext):
    """Подтверждает и удаляет заявку"""
    username = callback.from_user.username
    ticket_id = int(callback.data.split("_")[-1])
    logger.info(f"User {username} confirming deletion of ticket #{ticket_id}")

    success = await cancel_booking(username, ticket_id)

    if success:
        await callback.answer(f"Заявка #{ticket_id} успешно удалена", show_alert=True)
        await state.clear()
        await render_tickets_page(callback, username, "open", 0)
        logger.info(f"User {username} successfully deleted ticket #{ticket_id}")
    else:
        await callback.answer(
            "Ошибка при удалении заявки. Попробуйте позже.", show_alert=True
        )
        logger.error(f"User {username} failed to delete ticket #{ticket_id}")


@router.callback_query(F.data == "delete_cancel")
async def cancel_delete(callback: types.CallbackQuery, state: FSMContext):
    """Отменяет удаление"""
    await callback.answer("Удаление отменено")
    username = callback.from_user.username
    data = await state.get_data()
    ticket_id = data.get("delete_ticket_id")
    if ticket_id:
        ticket = await get_ticket_by_id(username, ticket_id, "open")
        if ticket:
            text = format_ticket_details(ticket)
            kb = ticket_actions_kb(ticket, "open")
            await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    await state.clear()


@router.callback_query(F.data == "closed_tickets")
async def show_closed_tickets(callback: types.CallbackQuery):
    username = callback.from_user.username
    logger.info(f"User {username} viewing closed tickets")
    await render_tickets_page(callback, username, "closed", 0)


@router.callback_query(F.data.startswith("closed_tickets_pg_"))
async def show_closed_tickets_page(callback: types.CallbackQuery):
    username = callback.from_user.username
    page = int(callback.data.split("_")[-1])
    logger.debug(f"User {username} viewing closed tickets page {page}")
    await render_tickets_page(callback, username, "closed", page)
