from aiogram import types


def main_menu_kb(open_allowed: bool = True):
    """Создает клавиатуру главного меню"""
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Открытые заявки", callback_data="open_tickets"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Закрытые заявки", callback_data="closed_tickets"
            )
        ],
    ]
    if open_allowed:
        buttons.append(
            [
                types.InlineKeyboardButton(
                    text="Создать заявку", callback_data="create_ticket"
                )
            ]
        )
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu_kb():
    """Создает клавиатуру с кнопкой возврата в главное меню"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="В главное меню", callback_data="back_main"
                )
            ]
        ]
    )


def tickets_list_kb(tickets, page: int, total_pages: int, ticket_type: str):
    """Создает клавиатуру со списком заявок и навигацией"""
    buttons = []
    row = []
    for i, ticket in enumerate(tickets):
        ticket_id = ticket.get("id", "")
        text = f"#{ticket_id}"
        callback_data = f"{ticket_type}_ticket_details_{ticket_id}"
        row.append(types.InlineKeyboardButton(text=text, callback_data=callback_data))
        if len(row) == 2 or i == len(tickets) - 1:
            buttons.append(row)
            row = []

    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(
                types.InlineKeyboardButton(
                    text="◀️ Пред. страница", callback_data=f"{ticket_type}_tickets_pg_{page - 1}"
                )
            )
        if page < total_pages - 1:
            nav_buttons.append(
                types.InlineKeyboardButton(
                    text="След. страница ▶️",
                    callback_data=f"{ticket_type}_tickets_pg_{page + 1}",
                )
            )
        if nav_buttons:
            buttons.append(nav_buttons)

    buttons.append(
        [types.InlineKeyboardButton(text="Назад", callback_data="back_main")]
    )

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def open_tickets_kb():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Заявка #123", callback_data="open_ticket_details_123"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Заявка #124", callback_data="open_ticket_details_124"
                )
            ],
            [types.InlineKeyboardButton(text="Назад", callback_data="back_main")],
        ]
    )


def closed_tickets_kb():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Заявка #200", callback_data="closed_ticket_200"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Заявка #201", callback_data="closed_ticket_201"
                )
            ],
            [types.InlineKeyboardButton(text="Назад", callback_data="back_main")],
        ]
    )


def ticket_actions_kb(ticket, ticket_type: str):
    """Создает клавиатуру действий для заявки в зависимости от статуса"""
    buttons = []
    status = ticket.get("status", "").lower()
    ticket_id = ticket.get("id", "")

    if ticket_type == "open":
        if status == "на рассмотрении":
            buttons.append(
                [
                    types.InlineKeyboardButton(
                        text="Удалить", callback_data=f"ticket_delete_{ticket_id}"
                    )
                ]
            )
        elif status == "оценить":
            buttons.append(
                [
                    types.InlineKeyboardButton(
                        text="Оценить", callback_data=f"ticket_rate_{ticket_id}"
                    )
                ]
            )
        buttons.append(
            [types.InlineKeyboardButton(text="Назад", callback_data="open_tickets")]
        )
    else:
        buttons.append(
            [types.InlineKeyboardButton(text="Назад", callback_data="closed_tickets")]
        )

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def create_ticket_analysis_kb(possible_options: dict):
    """Создает клавиатуру выбора анализа"""
    buttons = []
    analyse_dict = possible_options.get("analyse", {})

    for uuid, name in analyse_dict.items():
        buttons.append([
            types.InlineKeyboardButton(
                text=name, callback_data=f"analysis_{uuid}"
            )
        ])

    buttons.append(
        [types.InlineKeyboardButton(text="Назад", callback_data="back_main")]
    )

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def create_ticket_day_kb(possible_options: dict):
    """Создает клавиатуру выбора даты"""
    from .utils import format_date_with_weekday

    buttons = []
    date_dict = possible_options.get("date", {})

    for date_str, available in date_dict.items():
        if available == 1:
            date_display = format_date_with_weekday(date_str)
            buttons.append([
                types.InlineKeyboardButton(
                    text=date_display, callback_data=f"day_{date_str}"
                )
            ])

    buttons.append(
        [types.InlineKeyboardButton(text="Назад", callback_data="analysis_back")]
    )

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def create_ticket_device_kb(possible_options: dict):
    """Создает клавиатуру выбора прибора"""
    buttons = []
    equipment_dict = possible_options.get("equipment", {})

    for uuid, name in equipment_dict.items():
        buttons.append([
            types.InlineKeyboardButton(
                text=name, callback_data=f"device_{uuid}"
            )
        ])

    buttons.append(
        [types.InlineKeyboardButton(text="Назад", callback_data="day_back")]
    )

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def create_ticket_executor_kb(possible_options: dict):
    """Создает клавиатуру выбора исполнителя"""
    buttons = []
    executor_dict = possible_options.get("executor", {})

    for uuid, name in executor_dict.items():
        buttons.append([
            types.InlineKeyboardButton(
                text=name, callback_data=f"exec_{uuid}"
            )
        ])

    buttons.append(
        [types.InlineKeyboardButton(text="Назад", callback_data="device_back")]
    )

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def create_ticket_quantity_kb():
    """Создает клавиатуру для ввода количества"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Назад", callback_data="quantity_back")]
        ]
    )


def create_ticket_confirm_kb():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Подтвердить", callback_data="confirm_ticket"
                ),
                types.InlineKeyboardButton(text="Отмена", callback_data="back_main"),
            ],
            [types.InlineKeyboardButton(text="Назад", callback_data="quantity_back")],
        ]
    )


def rate_question_kb(question_num: int):
    """Создает клавиатуру для вопроса опросника"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Да", callback_data=f"rate_q{question_num}_yes"
                ),
                types.InlineKeyboardButton(
                    text="Нет", callback_data=f"rate_q{question_num}_no"
                ),
            ],
            [types.InlineKeyboardButton(text="Назад", callback_data="open_tickets")],
        ]
    )


def rate_confirm_kb():
    """Создает клавиатуру подтверждения"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Отправить", callback_data="rate_confirm"
                )
            ],
            [types.InlineKeyboardButton(text="Отмена", callback_data="open_tickets")],
        ]
    )


def delete_confirm_kb(ticket_id: int):
    """Создает клавиатуру подтверждения удаления"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Да, удалить", callback_data=f"delete_confirm_{ticket_id}"
                ),
                types.InlineKeyboardButton(
                    text="Отмена", callback_data="delete_cancel"
                ),
            ]
        ]
    )
