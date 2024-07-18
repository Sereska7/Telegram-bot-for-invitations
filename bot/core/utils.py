import random

import bot.core.requests as request


async def generate_unique_code():
    """Функция генерирует случайное четырх значное число"""
    code = random.randint(1000, 9999)
    profile = request.get_profile_by_code(code)
    while profile:
        new_code = random.randint(1000, 9999)
        profile = await request.get_profile_by_code(code)
        if not profile:
            return new_code


async def conversion_to_text_for_event(event):
    """Функция на вход получает данные мероприятия из бд и конвертирует
    полученные данные в 'f' строку"""
    event_texts = []
    for text in event:
        event_text = (
            f"Title: {text['title']}\n"
            f"Description: {text["description"]}\n"
            f"Date: {text['date']}\n"
            f"Price: {text['price']}\n"
        )
        event_texts.append(event_text)
    return event_texts


async def conversion_to_text_for_profile(profile_person):
    """Функция на вход получает данные профиля из бд и конвертирует
    полученные данные в 'f' строку"""
    result = []
    for object_profile in profile_person:
        profile_text = (
            f"Имя: {object_profile['first_name']}\n"
            f"Фамилия: {object_profile['last_name']}\n"
            f"Телефон: {object_profile['phone_number']}\n"
            f"Должность: {object_profile["position"]}\n"
            f"Уникальный код: {object_profile["unique_id"]}"
        )
        result.append(profile_text)
        return result


async def conversion_to_text_for_event_id_min(events_id):
    """Функция на вход получает данные мероприятия из бд и конвертирует
    полученные данные в сокращенный вариант 'f' строки"""
    event_texts = []
    for event_id in events_id:
        event = await request.get_event(int(event_id))
        for one in event:
            event_text = (
                f"Title: {one['title']}\n"
                f"Date: {one['date']}\n"
                f"Price: {one['price']}\n"
            )
            event_texts.append(event_text)
    return event_texts


async def conversion_to_text_for_events_min(events):
    event_texts = []
    for event in events:
        event_text = (
            f"Title: {event['title']}\n"
            f"Date: {event['date']}\n"
            f"Price: {event['price']}\n"
        )
        event_texts.append(event_text)
    return event_texts
