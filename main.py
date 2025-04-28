from dotenv import load_dotenv
from fastapi import FastAPI

from bans.router import router as bans_router
from characters.router import router as characters_router
from characters.router import sub_router as sub_characters_router
from middlewares.logging import LoggingMiddleware
from roles.router import router as roles_router
from security.router import router as security_router
from users.router import router as users_router

load_dotenv()
app = FastAPI()
app.include_router(users_router)
app.include_router(bans_router)
app.include_router(roles_router)
app.include_router(characters_router)
app.include_router(sub_characters_router, prefix=users_router.prefix)
app.include_router(security_router)

app.add_middleware(LoggingMiddleware)
