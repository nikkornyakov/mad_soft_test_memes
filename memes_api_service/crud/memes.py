from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Meme


class CRUDBase:
    """Базовый класс для операций CRUD."""

    def __init__(self, model):
        """
        Метод инициализации класса.
        Принимает модель в качестве параметра.
        """
        self.model = model

    async def create(self, data, session: AsyncSession):
        """Метод для создания объекта."""
        object = self.model(**data.dict())
        session.add(object)
        await session.commit()
        await session.refresh(object)
        return object

    async def update(self, object, new_data, session: AsyncSession):
        """Метод для изменения объекта."""
        update_data = new_data.model_dump()
        for field in jsonable_encoder(object):
            if field in update_data:
                setattr(object, field, update_data[field])
        session.add(object)
        await session.commit()
        await session.refresh(object)
        return object

    async def remove(self, object, session: AsyncSession):
        """Метод для удаления объекта."""
        await session.delete(object)
        await session.commit()
        return object

    async def get(self, object_id: int, session: AsyncSession):
        """Метод для получения объекта по id."""
        return (
            (
                await session.execute(
                    select(self.model).where(self.model.id == object_id)
                )
            )
            .scalars()
            .first()
        )

    async def get_all(self, session: AsyncSession):
        """Метод для получения всех объектов."""
        return (
            (await session.execute(select(self.model).order_by(self.model.id)))
            .scalars()
            .all()
        )


memes_crud = CRUDBase(Meme)
