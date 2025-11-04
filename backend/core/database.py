"""
Configuration de la base de données
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from core.config import settings

# Création du moteur de base de données asynchrone
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base pour les modèles
Base = declarative_base()


async def init_db():
    """Initialise la base de données"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Génère une session de base de données"""
    async with async_session_maker() as session:
        yield session

