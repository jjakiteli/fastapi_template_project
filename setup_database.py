import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncSession

from bans.models import BanDB  # noqa
from characters.models import CharacterDB  # noqa
from database.database_session import engine
from database.models import Base
from roles.models import RoleDB  # noqa
from security.authorization import get_password_hash
from users.models import UserDB  # noqa


async def setup_db():
    load_dotenv()

    print("📁 DB path set to:", os.getenv("DB_PATH"))
    if not os.path.exists(os.getenv("DB_PATH")):
        os.makedirs(os.getenv("DB_PATH"))

    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA foreign_keys=ON"))
        await conn.run_sync(Base.metadata.create_all)

        def show_tables(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()

        tables = await conn.run_sync(show_tables)
        print("✅ Tables created or verified:", tables)

    async with AsyncSession(engine) as session:
        root_role = RoleDB(
            name="root", description="default root permission", permissions=["ADMIN"]
        )
        session.add(root_role)

        rootname = os.getenv("ROOT_NAME")
        rootpw = os.getenv("ROOT_PASSWORD")
        root_user = UserDB(
            username=rootname, password=get_password_hash(rootpw), role=root_role.name
        )
        session.add(root_user)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(setup_db())
