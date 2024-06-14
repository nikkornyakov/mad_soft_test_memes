from pydantic import BaseModel


class MemeRead(BaseModel):
    """Схема для получения информации о меме."""

    id: int
    image_url: str
    text: str

    class Config:
        from_attributes = True


class MemeCreateUpdate(BaseModel):
    """Схема для создания и обновления мема."""

    image_url: str
    text: str
    user_id: int
