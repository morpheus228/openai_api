from sqlalchemy import BigInteger, String, Column, DateTime, ForeignKey, Boolean, Integer, Text, Float, Enum, create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime

from config import MYSQLConfig


def get_engine(config: MYSQLConfig):
	engine_str = f"mysql+pymysql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"
	engine = create_engine(engine_str)
	return engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime(), default=datetime.utcnow)