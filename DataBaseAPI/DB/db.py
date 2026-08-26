from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from DataBaseAPI.DB.Model.BaseModel import BaseModel
from DataBaseAPI.DB.Model.UserModel import UserModel
from DataBaseAPI.DB.Model.EventModel import EventModel


#engine = create_async_engine("sqlite+aiosqlite:///mainbase.db")
engine = None

#sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
sessionmaker = None

async def start_database(name:str = "mainbase"):
    global engine, sessionmaker
    engine = create_async_engine(f"sqlite+aiosqlite:///{name}.db")
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

async def drop_all_tables():
    async with engine.begin() as conn:
        print("DROP TABLES")
        print(BaseModel.metadata.tables.keys())
        await conn.run_sync(BaseModel.metadata.drop_all)

async def get_async_session():
    async with sessionmaker() as session:
        yield session

async def create_all_tables():
    async with engine.begin() as conn:
        print("CREATE TABLES")
        print(BaseModel.metadata.tables.keys())
        await conn.run_sync(BaseModel.metadata.create_all)
        print("CREATED")