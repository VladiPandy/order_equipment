import json
import logging
import aiohttp
from datetime import datetime, timedelta
from bot.config import TELEGRAM_SHARED_SECRET, API_URL

logger = logging.getLogger(__name__)

WEEKDAYS_RU_SHORT = {
    0: "ПН",
    1: "ВТ",
    2: "СР",
    3: "ЧТ",
    4: "ПТ",
    5: "СБ",
    6: "ВС",
}


def format_date_with_weekday(date_str: str) -> str:
    """Форматирует дату с днем недели в начале"""
    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        weekday = WEEKDAYS_RU_SHORT[date_obj.weekday()]
        return f"{weekday} - {date_str}"
    except (ValueError, KeyError):
        return date_str


def get_date_range():
    """Возвращает единый диапазон дат для заявок"""
    today = datetime.now()
    current_week_monday = today - timedelta(days=today.weekday())
    start_date = current_week_monday - timedelta(weeks=3)
    end_date = current_week_monday + timedelta(weeks=2, days=6)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")


async def get_project_info(telegram_nick: str):
    """Получает информацию о проекте"""
    url = f"{API_URL}/api/v1/info/project"
    headers = {
        "X-Telegram-Secret": TELEGRAM_SHARED_SECRET,
        "X-Telegram-Nick": telegram_nick,
    }
    logger.debug(f"GET {url}")
    logger.debug(f"HEADERS: {headers}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                logger.debug(f"RESPONSE STATUS: {resp.status}")
                ctype = resp.headers.get("Content-Type", "")
                logger.debug(f"RESPONSE CONTENT-TYPE: {ctype}")
                if "application/json" in ctype:
                    data = await resp.json()
                    logger.debug(f"RESPONSE JSON: {data}")
                    if isinstance(data, dict) and data.get("detail") == "Ник телеграмма не авторизован":
                        logger.warning(
                            f"Telegram nick '{telegram_nick}' is not authorized. Returning None."
                        )
                        return None
                    logger.info(
                        f"Successfully retrieved project info for user: {telegram_nick}"
                    )
                    return data
                text = await resp.text()
                logger.warning(
                    f"NON-JSON RESPONSE for {telegram_nick}, BODY (first 500):\n{text[:500]}"
                )
                return None
    except aiohttp.ClientError as e:
        logger.error(f"API request error for {telegram_nick}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error for {telegram_nick}: {e}")
        return None


async def get_bookings(telegram_nick: str, start_date: str, end_date: str):
    """Получает список заявок за период"""
    url = f"{API_URL}/api/v1/info/bookings"
    headers = {
        "X-Telegram-Secret": TELEGRAM_SHARED_SECRET,
        "X-Telegram-Nick": telegram_nick,
        "Content-Type": "application/json",
    }
    params = {"user": telegram_nick}
    body = {"start": start_date, "end": end_date}
    logger.debug(f"POST {url} with params {params} and body {body}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=headers, params=params, json=body
            ) as resp:
                logger.debug(f"RESPONSE STATUS: {resp.status}")
                ctype = resp.headers.get("Content-Type", "")
                logger.debug(f"RESPONSE CONTENT-TYPE: {ctype}")
                if resp.status == 200 and "application/json" in ctype:
                    data = await resp.json()
                    logger.debug(f"RESPONSE JSON: {len(data)} bookings")
                    logger.debug(f"RESPONSE DATA: {data}")
                    logger.info(
                        f"Successfully retrieved {len(data)} bookings for {telegram_nick}"
                    )
                    return data
                text = await resp.text()
                logger.warning(
                    f"Non-200 or non-JSON response for {telegram_nick}, status {resp.status}, BODY (first 500):\n{text[:500]}"
                )
                return []
    except aiohttp.ClientError as e:
        logger.error(f"API request error for {telegram_nick}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error for {telegram_nick}: {e}")
        return []


async def send_feedback(
    telegram_nick: str,
    ticket_id: int,
    question_1: bool,
    question_2: bool,
    question_3: bool,
):
    """Отправляет оценку заявки"""
    url = f"{API_URL}/api/v1/booking/feedback"
    headers = {
        "X-Telegram-Secret": TELEGRAM_SHARED_SECRET,
        "X-Telegram-Nick": telegram_nick,
        "Content-Type": "application/json",
    }
    params = {"user": telegram_nick}
    body = {
        "id": ticket_id,
        "question_1": question_1,
        "question_2": question_2,
        "question_3": question_3,
    }
    logger.debug(f"POST {url} with params {params} and body {body}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=headers, params=params, json=body
            ) as resp:
                logger.debug(f"RESPONSE STATUS: {resp.status}")
                ctype = resp.headers.get("Content-Type", "")
                logger.debug(f"RESPONSE CONTENT-TYPE: {ctype}")
                if resp.status == 200:
                    logger.info(
                        f"Successfully sent feedback for ticket #{ticket_id} by {telegram_nick}"
                    )
                    return True
                text = await resp.text()
                logger.warning(
                    f"Non-200 response for feedback, status {resp.status}, BODY (first 500):\n{text[:500]}"
                )
                return False
    except aiohttp.ClientError as e:
        logger.error(f"API request error for feedback: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error for feedback: {e}")
        return False


async def cancel_booking(telegram_nick: str, ticket_id: int):
    """Отменяет заявку"""
    url = f"{API_URL}/api/v1/booking/cancel"
    headers = {
        "X-Telegram-Secret": TELEGRAM_SHARED_SECRET,
        "X-Telegram-Nick": telegram_nick,
        "Content-Type": "application/json",
    }
    params = {"user": telegram_nick}
    body = {"id": ticket_id}
    logger.debug(f"DELETE {url} with params {params} and body {body}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                url, headers=headers, params=params, json=body
            ) as resp:
                logger.debug(f"RESPONSE STATUS: {resp.status}")
                ctype = resp.headers.get("Content-Type", "")
                logger.debug(f"RESPONSE CONTENT-TYPE: {ctype}")
                if resp.status == 200:
                    logger.info(
                        f"Successfully cancelled booking #{ticket_id} by {telegram_nick}"
                    )
                    return True
                text = await resp.text()
                logger.warning(
                    f"Non-200 response for cancel, status {resp.status}, BODY (first 500):\n{text[:500]}"
                )
                return False
    except aiohttp.ClientError as e:
        logger.error(f"API request error for cancel: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error for cancel: {e}")
        return False


async def get_possible_create_options(
    telegram_nick: str,
    analysis_name: str = None,
    date: str = None,
    device_name: str = None,
    executor_name: str = None,
    create_key: str = None,
):
    """Получает возможные варианты для создания заявки"""
    url = f"{API_URL}/api/v1/booking/possible_create"
    headers = {
        "X-Telegram-Secret": TELEGRAM_SHARED_SECRET,
        "X-Telegram-Nick": telegram_nick,
        "Content-Type": "application/json",
    }
    if create_key:
        headers["x-createkey"] = create_key

    params = {"user": telegram_nick}

    body = {}
    if analysis_name:
        body["analyse"] = analysis_name
    if date:
        body["date"] = date
    if device_name:
        body["equipment"] = device_name
    if executor_name:
        body["executor"] = executor_name

    logger.debug(f"POST {url} with params {params} and body {body}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=headers, params=params, json=body
            ) as resp:
                logger.debug(f"RESPONSE STATUS: {resp.status}")
                ctype = resp.headers.get("Content-Type", "")
                logger.debug(f"RESPONSE CONTENT-TYPE: {ctype}")
                if resp.status == 200 and "application/json" in ctype:
                    data = await resp.json()
                    create_key_from_response = resp.headers.get("x-createkey")
                    if create_key_from_response:
                        data["create_key"] = create_key_from_response
                        logger.debug(
                            f"Received x-createkey: {create_key_from_response}"
                        )
                    logger.info(
                        f"Successfully retrieved possible create options for {telegram_nick}"
                    )
                    logger.info(
                        f"POSSIBLE CREATE OPTIONS JSON:\n{json.dumps(data, ensure_ascii=False, indent=2)}"
                    )
                    return data
                elif resp.status in [400, 403, 404] and "application/json" in ctype:
                    error_data = await resp.json()
                    error_message = error_data.get(
                        "detail", "Нет доступных вариантов для создания заявки"
                    )
                    logger.warning(
                        f"{resp.status} response for {telegram_nick}: {error_message}"
                    )
                    return {"error": error_message, "status": resp.status}
                text = await resp.text()
                logger.warning(
                    f"Non-200 or non-JSON response for {telegram_nick}, status {resp.status}, BODY (first 500):\n{text[:500]}"
                )
                return None
    except aiohttp.ClientError as e:
        logger.error(f"API request error for possible_create: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error for possible_create: {e}")
        return None


async def create_booking(
    telegram_nick: str,
    date: str,
    analyse: str,
    equipment: str,
    executor: str,
    samples: int,
    create_key: str = None,
):
    """Создает заявку"""
    url = f"{API_URL}/api/v1/booking/create"
    headers = {
        "X-Telegram-Secret": TELEGRAM_SHARED_SECRET,
        "X-Telegram-Nick": telegram_nick,
        "Content-Type": "application/json",
    }
    if create_key:
        headers["x-createkey"] = create_key

    params = {"user": telegram_nick}

    body = {
        "date": date,
        "analyse": analyse,
        "equipment": equipment,
        "executor": executor,
        "samples": samples,
    }

    logger.debug(f"POST {url} with params {params} and body {body}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, headers=headers, params=params, json=body
            ) as resp:
                logger.debug(f"RESPONSE STATUS: {resp.status}")
                ctype = resp.headers.get("Content-Type", "")
                logger.debug(f"RESPONSE CONTENT-TYPE: {ctype}")
                if resp.status == 200 and "application/json" in ctype:
                    data = await resp.json()
                    logger.info(f"Successfully created booking for {telegram_nick}")
                    logger.debug(
                        f"CREATED BOOKING JSON:\n{json.dumps(data, ensure_ascii=False, indent=2)}"
                    )
                    return data
                elif resp.status in [400, 403, 404] and "application/json" in ctype:
                    error_data = await resp.json()
                    error_message = error_data.get(
                        "detail", "Ошибка при создании заявки"
                    )
                    logger.warning(
                        f"{resp.status} response for {telegram_nick}: {error_message}"
                    )
                    return {"error": error_message, "status": resp.status}
                text = await resp.text()
                logger.warning(
                    f"Non-200 or non-JSON response for {telegram_nick}, status {resp.status}, BODY (first 500):\n{text[:500]}"
                )
                return None
    except aiohttp.ClientError as e:
        logger.error(f"API request error for create: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error for create: {e}")
        return None
