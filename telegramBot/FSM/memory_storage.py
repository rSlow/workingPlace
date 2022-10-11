from aiogram.contrib.fsm_storage.memory import MemoryStorage

from ORM.states import State


class ModifiedMemoryStorage(MemoryStorage):
    async def set_state(self, *,
                        chat: str | int | None = None,
                        user: str | int | None = None,
                        state: bytes | str = None):
        await super(ModifiedMemoryStorage, self).set_state(
            chat=chat,
            user=user,
            state=state
        )
        await State.set_user_state(
            chat_id=chat,
            user_id=user,
            state=state
        )

    async def set_all_states(self):
        users = await State.get_all_states()
        for user in users:
            await self.set_state(
                chat=user.chat_id,
                user=user.user_id,
                state=user.state,
            )
