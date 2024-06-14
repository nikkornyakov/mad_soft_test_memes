"""
Импорты класса Base и моделей пользователя и мема
для корректных миграций Alembic.
"""

from core.db import Base  # noqa
from models import Meme, User  # noqa
