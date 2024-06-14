from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class Meme(Base):
    image_url: Mapped[str] = mapped_column(String(), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id', name='fk_meme_user_id_user')
    )

    def __repr__(self):
        return (
            f'{type(self).__name__}('
            f'id={self.id}, image={self.image}, '
            f'text={self.text})'
        )
