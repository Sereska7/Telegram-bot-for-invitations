from .db_helper import db_helper as db
from sqlalchemy import select

from .models import User, Profile, Event, RecordEvent


async def add_user(tg_id: int, name: str):
    async with db.session_factory() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, tg_name=name))
            await session.commit()


async def get_user_id(tg_id: int):
    async with db.session_factory() as session:
        query = select(User).where(User.tg_id == tg_id)
        result = await session.execute(query)
        user = result.scalar()
        return user.id


async def get_event(event_id: int):
    async with db.session_factory() as session:
        query = select(Event.__table__.columns).where(Event.id == event_id)
        events = await session.execute(query)
        return events.mappings().all()


async def get_events(offset: int = 0, limit: int = 2):
    async with db.session_factory() as session:
        query = select(Event.__table__.columns).offset(offset).limit(limit)
        events = await session.execute(query)
        return events.mappings().all()


async def create_profile(
    user_id,
    first_name,
    last_name,
    phone_number,
    position,
    unique_id,
):
    async with db.session_factory() as session:
        new_profile = Profile(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            position=position,
            unique_id=unique_id,
        )
        session.add(new_profile)
        await session.commit()
        return f"Позьзователь зарегистрирован\nУникальный код: {unique_id}"


async def get_profile(user_id: int):
    async with db.session_factory() as session:
        query = select(Profile.__table__.columns).where(user_id == user_id)
        result = await session.execute(query)
        profile = result.mappings().all()
        return profile


async def get_profile_by_code(un_code: int):
    async with db.session_factory() as session:
        query = select(Profile.__table__.columns).where(Profile.unique_id == un_code)
        result = await session.execute(query)
        profile = result.mappings().all()
        return profile


async def record_event(profile_id: int, event_id: int):
    async with db.session_factory() as session:
        new_record = RecordEvent(profile_id=profile_id, event_id=event_id)
        session.add(new_record)
        await session.commit()


async def get_profile_id(user_id: int):
    async with db.session_factory() as session:
        profile = select(Profile).where(Profile.user_id == user_id)
        result = await session.execute(profile)
        return result.scalar()


async def get_records(profile_id: int, offset: int = 0):
    async with db.session_factory() as session:
        records = (
            select(RecordEvent.__table__.columns)
            .where(RecordEvent.profile_id == profile_id)
            .offset(offset)
            .limit(2)
        )
        result = await session.execute(records)
        return result.mappings().all()
