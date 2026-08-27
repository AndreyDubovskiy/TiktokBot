from sqlalchemy import select
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from DB.Model.UserModel import UserModel

class  UserController:

    async def get_all_users(self, session: AsyncSession, offset: int = 0, limit: int = 100) -> List[UserModel]:
        query = select(UserModel).offset(offset).limit(limit)
        res: List[UserModel] = (await session.scalars(query)).all()
        return res

    async def create_user(self, session: AsyncSession, user_name: str, user_tg_id: str):
        user = UserModel(user_tg_id, user_name)
        session.add(user)
        await session.commit()

    async def get_user(self, session: AsyncSession, user_name: str = None, user_tg_id: str = None, user_id: int = None) -> UserModel | None:
        query = select(UserModel)
        if user_name:
            query = query.where(UserModel.tg_name==user_name)
        if user_tg_id:
            query = query.where(UserModel.tg_id==user_tg_id)
        if user_id:
            query = query.where(UserModel.id==user_id)
        res: UserModel = await session.scalar(query)
        return res

    async def delete_user(self, session: AsyncSession, user_id: int):
        query = select(UserModel).where(UserModel.id==user_id)
        res: UserModel = await session.scalar(query)
        if res:
            await session.delete(res)
            await session.commit()

    async def update_user(self, session: AsyncSession, user_id: int, user_name: str, user_tg_id: str):
        query = select(UserModel).where(UserModel.id==user_id)
        res: UserModel = await session.scalar(query)
        if res:
            res.tg_name = user_name
            res.tg_id = user_tg_id
            await session.commit()










