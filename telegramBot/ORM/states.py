from sqlalchemy import Column, Integer, String, select

from ORM.base import Base, Session


class State(Base):
    __tablename__ = "states"

    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    state = Column(String)

    @classmethod
    async def add_user(cls,
                       chat_id: str | int,
                       user_id: str | int):
        async with Session() as session:
            async with session.begin():
                user = cls(
                    chat_id=chat_id,
                    user_id=user_id
                )
                session.add(user)
        return user

    @classmethod
    async def set_user_state(cls,
                             chat_id: str | int,
                             user_id: str | int,
                             state: bytes | str):
        async with Session() as session:
            async with session.begin():
                query = select(
                    cls
                ).filter_by(
                    user_id=user_id
                ).filter_by(
                    chat_id=chat_id
                )
                result = await session.execute(query)
                user: cls = result.scalars().one_or_none()

                if user is None:
                    user = await cls.add_user(
                        chat_id=chat_id,
                        user_id=user_id,
                    )
                user.state = state

    @classmethod
    async def get_all_states(cls):
        async with Session() as session:
            async with session.begin():
                query = select(cls)
                result = await session.execute(query)
                users: list[cls] = result.scalars().all()
                return users
