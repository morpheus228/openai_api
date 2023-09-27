from ..interfaces import Users

from sqlalchemy.orm import Session
from .mysql import User

from aiogram import types


class UsersMYSQL(Users):
    def __init__(self, engine):
        self.engine = engine

    def get_by_id(self, user_id: int) -> User|None:
        with Session(self.engine) as session:
            return session.query(User).get(user_id)
    
    def create(self, user: types.User) -> User:
        with Session(self.engine) as session:

            user = User(id = user.id,
                        chat_id = user.id,
                        username = user.username,
                        first_name = user.first_name,
                        last_name = user.last_name, 
                        is_replay = False,
                        status = False)
        
            session.add(user)
            session.commit()
            
            return user
		