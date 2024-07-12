import random

import bot.core.requests as request


async def generate_unique_code():
    code = random.randint(1000, 9999)
    profile = request.get_profile_by_code(code)
    while profile:
        new_code = random.randint(1000, 9999)
        profile = await request.get_profile_by_code(code)
        if not profile:
            return new_code


async def conversion_to_text_for_event(event):
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


async def conversion_to_text_for_profile_by_userid(profile):
    result = []
    for object_profile in profile:
        profile_text = (
            f"Имя: {object_profile['first_name']}\n"
            f"Фамилия: {object_profile['last_name']}\n"
            f"Телефон: {object_profile['phone_number']}\n"
            f"Должность: {object_profile["position"]}\n"
            f"Уникальный код: {object_profile["unique_id"]}"
        )
        result.append(profile_text)
    return result


async def set_user_id(user_tg_id: int):
    user_id = user_tg_id
    return user_id
