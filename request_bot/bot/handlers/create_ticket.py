import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from ..states import CreateTicket
from ..keyboards import (
    create_ticket_analysis_kb,
    create_ticket_day_kb,
    create_ticket_device_kb,
    create_ticket_executor_kb,
    create_ticket_confirm_kb,
    main_menu_kb,
)
from ..utils import get_possible_create_options, get_project_info, create_booking

logger = logging.getLogger(__name__)
router = Router()


def format_ticket_summary(data: dict) -> str:
    """Формирует текст с выбранными параметрами заявки"""
    lines = []
    if data.get("analysis_name"):
        lines.append(f"Анализ: {data.get('analysis_name')}")
    if data.get("day"):
        lines.append(f"Дата: {data.get('day')}")
    if data.get("device_name"):
        lines.append(f"Прибор: {data.get('device_name')}")
    if data.get("executor_name"):
        lines.append(f"Исполнитель: {data.get('executor_name')}")
    if data.get("quantity"):
        lines.append(f"Количество: {data.get('quantity')}")
    return "\n".join(lines) if lines else ""


async def handle_api_error(callback_or_message, state: FSMContext, options: dict):
    """Обрабатывает ошибки и показывает alert при 403"""
    error_status = options.get("status")
    error_message = options.get("error", "")

    if error_status == 403:
        await state.clear()
        if isinstance(callback_or_message, types.CallbackQuery):
            alert_message = "Попробуйте позже."
            if len(alert_message) > 200:
                alert_message = alert_message[:197] + "..."
            await callback_or_message.answer(alert_message, show_alert=True)
            username = callback_or_message.from_user.username
            info = await get_project_info(username)
            if info:
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
                await callback_or_message.message.edit_text(msg, reply_markup=kb)
        return True

    if isinstance(callback_or_message, types.CallbackQuery):
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback_or_message.answer(error_message, show_alert=True)
    return False


@router.callback_query(F.data == "create_ticket")
async def create_ticket(callback: types.CallbackQuery, state: FSMContext):
    """Начинает процесс создания заявки"""
    username = callback.from_user.username
    logger.info(f"User {username} started creating ticket")

    data = await state.get_data()
    create_key = data.get("create_key")
    options = await get_possible_create_options(username, create_key=create_key)
    if options is None:
        await callback.answer(
            "Ошибка при получении вариантов для создания заявки. Попробуйте позже.",
            show_alert=True,
        )
        return

    if isinstance(options, dict) and "error" in options:
        if await handle_api_error(callback, state, options):
            return
        error_message = options.get("error", "")
        if error_message == "Нет доступных вариантов":
            error_message = "Нет доступных вариантов для создания заявки"
        elif not error_message:
            error_message = "Нет доступных вариантов для создания заявки"
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    create_key = options.pop("create_key", None)
    if create_key:
        await state.update_data(create_key=create_key)
        logger.debug(f"Saved create_key for user {username}")

    await state.update_data(possible_options=options)
    await state.set_state(CreateTicket.analysis)
    await callback.message.edit_text(
        "Выберите анализ:", reply_markup=create_ticket_analysis_kb(options)
    )


@router.callback_query(F.data.startswith("analysis_"), CreateTicket.analysis)
async def choose_analysis(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает выбор анализа"""
    username = callback.from_user.username
    analysis_uuid = callback.data.replace("analysis_", "")
    data = await state.get_data()
    possible_options = data.get("possible_options", {})
    analyse_dict = possible_options.get("analyse", {})
    analysis_name = analyse_dict.get(analysis_uuid, "")

    await state.update_data(analysis_uuid=analysis_uuid, analysis_name=analysis_name)

    data = await state.get_data()
    create_key = data.get("create_key")
    options = await get_possible_create_options(username, analysis_name=analysis_name, create_key=create_key)
    if options is None:
        await callback.answer(
            "Ошибка при получении вариантов. Попробуйте позже.", show_alert=True
        )
        return

    if isinstance(options, dict) and "error" in options:
        if await handle_api_error(callback, state, options):
            return
        error_message = options.get("error", "Нет доступных вариантов")
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    create_key = options.pop("create_key", None)
    if create_key:
        await state.update_data(create_key=create_key)
        logger.debug(f"Updated create_key for user {username}")

    await state.update_data(possible_options=options)
    await state.set_state(CreateTicket.day)
    logger.debug(
        f"User {username} selected analysis: {analysis_name} ({analysis_uuid})"
    )
    data = await state.get_data()
    summary = format_ticket_summary(data)
    text = f"{summary}\n\nВыберите день:" if summary else "Выберите день:"
    await callback.message.edit_text(
        text, reply_markup=create_ticket_day_kb(options)
    )


@router.callback_query(F.data == "analysis_back")
async def back_to_analysis_from_day(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает к выбору анализа"""
    username = callback.from_user.username
    data = await state.get_data()
    create_key = data.get("create_key")
    options = await get_possible_create_options(username, create_key=create_key)
    if options is None:
        await callback.answer(
            "Ошибка при получении вариантов. Попробуйте позже.", show_alert=True
        )
        return

    if isinstance(options, dict) and "error" in options:
        if await handle_api_error(callback, state, options):
            return
        error_message = options.get("error", "Нет доступных вариантов")
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    create_key = options.pop("create_key", None)
    if create_key:
        await state.update_data(create_key=create_key)
        logger.debug(f"Updated create_key for user {username}")

    await state.update_data(possible_options=options)
    await state.update_data(analysis_uuid=None, analysis_name=None, day=None)
    await state.set_state(CreateTicket.analysis)
    await callback.message.edit_text(
        "Выберите анализ:", reply_markup=create_ticket_analysis_kb(options)
    )


@router.callback_query(F.data.startswith("day_"), CreateTicket.day)
async def choose_day(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает выбор дня"""
    username = callback.from_user.username
    selected_date = callback.data.replace("day_", "")
    data = await state.get_data()
    analysis_name = data.get("analysis_name")

    await state.update_data(day=selected_date)

    data = await state.get_data()
    create_key = data.get("create_key")
    options = await get_possible_create_options(
        username, analysis_name=analysis_name, date=selected_date, create_key=create_key
    )
    if options is None:
        await callback.answer(
            "Ошибка при получении вариантов. Попробуйте позже.", show_alert=True
        )
        return

    if isinstance(options, dict) and "error" in options:
        if await handle_api_error(callback, state, options):
            return
        error_message = options.get("error", "Нет доступных вариантов")
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    create_key = options.pop("create_key", None)
    if create_key:
        await state.update_data(create_key=create_key)
        logger.debug(f"Updated create_key for user {username}")

    await state.update_data(possible_options=options)
    await state.set_state(CreateTicket.device)
    logger.debug(f"User {username} selected day: {selected_date}")
    data = await state.get_data()
    summary = format_ticket_summary(data)
    text = f"{summary}\n\nВыберите прибор:" if summary else "Выберите прибор:"
    await callback.message.edit_text(
        text, reply_markup=create_ticket_device_kb(options)
    )


@router.callback_query(F.data == "day_back")
async def back_to_day(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает к выбору дня"""
    username = callback.from_user.username
    data = await state.get_data()
    analysis_name = data.get("analysis_name")
    create_key = data.get("create_key")
    options = await get_possible_create_options(
        username, analysis_name=analysis_name, create_key=create_key
    )
    if options is None:
        await callback.answer(
            "Ошибка при получении вариантов. Попробуйте позже.", show_alert=True
        )
        return

    if isinstance(options, dict) and "error" in options:
        if await handle_api_error(callback, state, options):
            return
        error_message = options.get("error", "Нет доступных вариантов")
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    create_key = options.pop("create_key", None)
    if create_key:
        await state.update_data(create_key=create_key)
        logger.debug(f"Updated create_key for user {username}")

    await state.update_data(possible_options=options)
    await state.update_data(day=None, device_uuid=None, device_name=None)
    await state.set_state(CreateTicket.day)
    data = await state.get_data()
    summary = format_ticket_summary(data)
    text = f"{summary}\n\nВыберите день:" if summary else "Выберите день:"
    await callback.message.edit_text(
        text, reply_markup=create_ticket_day_kb(options)
    )


@router.callback_query(F.data.startswith("device_"), CreateTicket.device)
async def choose_device(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает выбор прибора"""
    username = callback.from_user.username
    device_uuid = callback.data.replace("device_", "")
    data = await state.get_data()
    possible_options = data.get("possible_options", {})
    equipment_dict = possible_options.get("equipment", {})
    device_name = equipment_dict.get(device_uuid, "")

    analysis_name = data.get("analysis_name")
    selected_date = data.get("day")

    await state.update_data(device_uuid=device_uuid, device_name=device_name)

    data = await state.get_data()
    create_key = data.get("create_key")
    options = await get_possible_create_options(
        username,
        analysis_name=analysis_name,
        date=selected_date,
        device_name=device_name,
        create_key=create_key
    )
    if options is None:
        await callback.answer(
            "Ошибка при получении вариантов. Попробуйте позже.", show_alert=True
        )
        return

    if isinstance(options, dict) and "error" in options:
        if await handle_api_error(callback, state, options):
            return
        error_message = options.get("error", "Нет доступных вариантов")
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    create_key = options.pop("create_key", None)
    if create_key:
        await state.update_data(create_key=create_key)
        logger.debug(f"Updated create_key for user {username}")

    await state.update_data(possible_options=options)
    await state.set_state(CreateTicket.executor)
    logger.debug(f"User {username} selected device: {device_name} ({device_uuid})")
    data = await state.get_data()
    summary = format_ticket_summary(data)
    text = f"{summary}\n\nВыберите исполнителя:" if summary else "Выберите исполнителя:"
    await callback.message.edit_text(
        text, reply_markup=create_ticket_executor_kb(options)
    )


@router.callback_query(F.data == "device_back")
async def back_to_device(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает к выбору прибора"""
    username = callback.from_user.username
    data = await state.get_data()
    analysis_name = data.get("analysis_name")
    selected_date = data.get("day")
    create_key = data.get("create_key")
    options = await get_possible_create_options(
        username, analysis_name=analysis_name, date=selected_date, create_key=create_key
    )
    if options is None:
        await callback.answer(
            "Ошибка при получении вариантов. Попробуйте позже.", show_alert=True
        )
        return

    if isinstance(options, dict) and "error" in options:
        if await handle_api_error(callback, state, options):
            return
        error_message = options.get("error", "Нет доступных вариантов")
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    create_key = options.pop("create_key", None)
    if create_key:
        await state.update_data(create_key=create_key)
        logger.debug(f"Updated create_key for user {username}")

    await state.update_data(possible_options=options)
    await state.update_data(device_uuid=None, device_name=None, executor_uuid=None, executor_name=None)
    await state.set_state(CreateTicket.device)
    data = await state.get_data()
    summary = format_ticket_summary(data)
    text = f"{summary}\n\nВыберите прибор:" if summary else "Выберите прибор:"
    await callback.message.edit_text(
        text, reply_markup=create_ticket_device_kb(options)
    )


@router.callback_query(F.data.startswith("exec_"), CreateTicket.executor)
async def choose_executor(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает выбор исполнителя"""
    username = callback.from_user.username
    executor_uuid = callback.data.replace("exec_", "")
    data = await state.get_data()
    possible_options = data.get("possible_options", {})
    executor_dict = possible_options.get("executor", {})
    executor_name = executor_dict.get(executor_uuid, "")

    analysis_name = data.get("analysis_name")
    selected_date = data.get("day")
    device_name = data.get("device_name")

    await state.update_data(executor_uuid=executor_uuid, executor_name=executor_name)

    data = await state.get_data()
    create_key = data.get("create_key")
    options = await get_possible_create_options(
        username,
        analysis_name=analysis_name,
        date=selected_date,
        device_name=device_name,
        executor_name=executor_name,
        create_key=create_key
    )
    if options is None:
        await callback.answer(
            "Ошибка при получении вариантов. Попробуйте позже.", show_alert=True
        )
        return

    if isinstance(options, dict) and "error" in options:
        if await handle_api_error(callback, state, options):
            return
        error_message = options.get("error", "Нет доступных вариантов")
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    create_key = options.pop("create_key", None)
    if create_key:
        await state.update_data(create_key=create_key)
        logger.debug(f"Updated create_key for user {username}")

    await state.update_data(possible_options=options)
    await state.set_state(CreateTicket.quantity)

    samples_limit = options.get("samples_limit", 0)

    logger.debug(
        f"User {username} selected executor: {executor_name} ({executor_uuid})"
    )
    from ..keyboards import create_ticket_quantity_kb
    data = await state.get_data()
    summary = format_ticket_summary(data)
    text = f"{summary}\n\nВведите количество (доступно: {samples_limit}):\n\nОтправьте число сообщением."
    await callback.message.edit_text(
        text, reply_markup=create_ticket_quantity_kb()
    )


@router.callback_query(F.data == "executor_back")
async def back_to_executor(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает к выбору исполнителя"""
    username = callback.from_user.username
    data = await state.get_data()
    analysis_name = data.get("analysis_name")
    selected_date = data.get("day")
    device_name = data.get("device_name")
    create_key = data.get("create_key")

    options = await get_possible_create_options(
        username,
        analysis_name=analysis_name,
        date=selected_date,
        device_name=device_name,
        create_key=create_key
    )
    if options is None:
        await callback.answer(
            "Ошибка при получении вариантов. Попробуйте позже.", show_alert=True
        )
        return

    if isinstance(options, dict) and "error" in options:
        if await handle_api_error(callback, state, options):
            return
        error_message = options.get("error", "Нет доступных вариантов")
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    create_key = options.pop("create_key", None)
    if create_key:
        await state.update_data(create_key=create_key)
        logger.debug(f"Updated create_key for user {username}")

    await state.update_data(possible_options=options)
    await state.update_data(executor_uuid=None, executor_name=None, quantity=None)
    await state.set_state(CreateTicket.executor)
    data = await state.get_data()
    summary = format_ticket_summary(data)
    text = f"{summary}\n\nВыберите исполнителя:" if summary else "Выберите исполнителя:"
    await callback.message.edit_text(
        text, reply_markup=create_ticket_executor_kb(options)
    )


@router.callback_query(F.data == "quantity_back", CreateTicket.quantity)
async def back_to_quantity(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает к выбору исполнителя"""
    username = callback.from_user.username
    data = await state.get_data()
    analysis_name = data.get("analysis_name")
    selected_date = data.get("day")
    device_name = data.get("device_name")
    create_key = data.get("create_key")

    options = await get_possible_create_options(
        username,
        analysis_name=analysis_name,
        date=selected_date,
        device_name=device_name,
        create_key=create_key
    )
    if options is None:
        await callback.answer(
            "Ошибка при получении вариантов. Попробуйте позже.", show_alert=True
        )
        return

    if isinstance(options, dict) and "error" in options:
        if await handle_api_error(callback, state, options):
            return
        error_message = options.get("error", "Нет доступных вариантов")
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    create_key = options.pop("create_key", None)
    if create_key:
        await state.update_data(create_key=create_key)
        logger.debug(f"Updated create_key for user {username}")

    await state.update_data(possible_options=options)
    await state.update_data(quantity=None)
    await state.set_state(CreateTicket.executor)
    data = await state.get_data()
    summary = format_ticket_summary(data)
    text = f"{summary}\n\nВыберите исполнителя:" if summary else "Выберите исполнителя:"
    await callback.message.edit_text(
        text, reply_markup=create_ticket_executor_kb(options)
    )


@router.message(CreateTicket.quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    """Обрабатывает ввод количества"""
    if not message.text.isdigit():
        logger.warning(
            f"User {message.from_user.username} entered invalid quantity: {message.text}"
        )
        await message.answer("Введите корректное число.")
        return

    qty = int(message.text)
    if qty <= 0:
        logger.warning(
            f"User {message.from_user.username} entered quantity <= 0: {qty}"
        )
        await message.answer("Количество должно быть больше нуля.")
        return

    data = await state.get_data()
    possible_options = data.get("possible_options", {})
    samples_limit = possible_options.get("samples_limit", 0)

    if qty > samples_limit:
        logger.warning(
            f"User {message.from_user.username} entered quantity > limit: {qty} > {samples_limit}"
        )
        await message.answer(
            f"Максимально допустимое количество — {samples_limit}. Попробуйте снова."
        )
        return

    await state.update_data(quantity=qty)
    await state.set_state(CreateTicket.confirm)
    logger.debug(f"User {message.from_user.username} entered valid quantity: {qty}")

    data = await state.get_data()
    text = (
        "Проверьте данные перед подтверждением:\n\n"
        f"Анализ: {data.get('analysis_name', '')}\n"
        f"Дата: {data.get('day', '')}\n"
        f"Прибор: {data.get('device_name', '')}\n"
        f"Исполнитель: {data.get('executor_name', '')}\n"
        f"Количество: {data.get('quantity', '')}"
    )
    await message.answer(text, reply_markup=create_ticket_confirm_kb())


@router.callback_query(F.data == "quantity_back", CreateTicket.confirm)
async def back_from_confirm_to_quantity(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает к вводу количества"""
    await state.set_state(CreateTicket.quantity)
    data = await state.get_data()
    possible_options = data.get("possible_options", {})
    samples_limit = possible_options.get("samples_limit", 0)
    from ..keyboards import create_ticket_quantity_kb
    summary = format_ticket_summary(data)
    text = f"{summary}\n\nВведите количество (доступно: {samples_limit}):\n\nОтправьте число сообщением."
    await callback.message.edit_text(
        text, reply_markup=create_ticket_quantity_kb()
    )


@router.callback_query(F.data == "confirm_ticket", CreateTicket.confirm)
async def confirm_ticket(callback: types.CallbackQuery, state: FSMContext):
    """Подтверждает создание заявки"""
    username = callback.from_user.username
    data = await state.get_data()

    date = data.get("day", "")
    analyse = data.get("analysis_name", "")
    equipment = data.get("device_name", "")
    executor = data.get("executor_name", "")
    samples = data.get("quantity", 0)
    create_key = data.get("create_key")

    logger.info(
        f"User {username} confirmed ticket creation: date={date}, analyse={analyse}, "
        f"equipment={equipment}, executor={executor}, samples={samples}"
    )

    result = await create_booking(
        username,
        date=date,
        analyse=analyse,
        equipment=equipment,
        executor=executor,
        samples=samples,
        create_key=create_key
    )

    await state.clear()

    if result is None:
        await callback.answer(
            "Ошибка при создании заявки. Попробуйте позже.",
            show_alert=True
        )
        return

    if isinstance(result, dict) and "error" in result:
        error_message = result.get("error", "Ошибка при создании заявки")
        if len(error_message) > 200:
            error_message = error_message[:197] + "..."
        await callback.answer(error_message, show_alert=True)
        return

    ticket_id = result.get("id", "N/A")
    logger.info(f"Successfully created ticket #{ticket_id} for user {username}")

    alert_message = f"Заявка #{ticket_id} успешно создана!"
    if len(alert_message) > 200:
        alert_message = alert_message[:197] + "..."
    await callback.answer(alert_message, show_alert=True)

    info = await get_project_info(username)
    if info:
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
        await callback.message.edit_text(msg, reply_markup=kb)
