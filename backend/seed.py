from sqlalchemy import select
from sqlalchemy.orm import Session
from db_engine import sync_engine
from models import User, Message


def seed_bot_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            bot_user = session.execute(select(User).filter_by(name="Bot")).scalar_one_or_none()

            if bot_user is None:
                print("Seeding bot user...")
                bot_user = User(name="Bot")
                session.add(bot_user)
                session.commit()
            else:
                print("Bot user already exists. Skipping seeding.")


def seed_user_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            human_user = session.execute(select(User).filter_by(name="ALice")).scalar_one_or_none()

            if human_user is None:
                print("Seeding human user...")
                human_user = User(name="ALice")
                session.add(human_user)
                session.commit()
            else:
                print("Human user already exists. Skipping seeding.")
