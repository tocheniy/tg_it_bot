"""Импорт класса Base из моделей для дальнейшего создания миграций через Alembic"""

from database.models.dvr import Base  # noqa: F401
from database.models.event import Base  # noqa: F401, F811
from database.models.city import Base  # noqa: F401, F811
from database.models.chat import Base  # noqa: F401, F811
