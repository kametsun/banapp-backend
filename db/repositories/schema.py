import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from datetime import datetime

# 環境変数を読み込む
load_dotenv()
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# DBエンジン作成
database = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(500), nullable=False)
    coin = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now)
    cigarettes_price = Column(Integer, nullable=False)


class Pet(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(500), nullable=False)
    hunger = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now)
    death_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True, default=datetime.now)


class History(Base):
    __tablename__ = 'histories'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=False)
    more_money = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now)


class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(String(500), nullable=False)
    reward_coin = Column(Integer, nullable=False)


class GetAchievement(Base):
    __tablename__ = 'get_achievements'

    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    achievement_id = Column('achievement_id', Integer, ForeignKey('achievements.id'), primary_key=True)

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(500), nullable=False)
    price = Column(Integer, nullable=False)
    energy = Column(Integer, nullable=False)

Base.metadata.create_all(database)
