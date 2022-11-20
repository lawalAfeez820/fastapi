
from sqlalchemy.ext.asyncio import create_async_engine
from app import config

db_connection_str = f"postgresql+{config.settings.database_driver}://{config.settings.database_user}:{config.settings.database_password}@{config.settings.database_host}:{config.settings.database_port}/{config.settings.database_name}_test"


async_engine = create_async_engine(
   db_connection_str,
   echo=True,
   future=True
)