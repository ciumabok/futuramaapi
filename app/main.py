import mimetypes

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from app.core import feature_flags, settings
from app.graph_ql.routers import router as graphql_router
from app.routers.callbacks import router as callbacks_router
from app.routers.characters import router as characters_router
from app.routers.episodes import router as episodes_router
from app.routers.notifications import router as notifications_router
from app.routers.root import router as root_router
from app.routers.seasons import router as seasons_router
from app.routers.tokens import router as tokens_router
from app.routers.users import router as users_router
from app.middlewares.secure import HTTPSRedirectMiddleware

mimetypes.add_type("image/webp", ".webp")

app = FastAPI(
    docs_url=None,
    redoc_url=None,
)

if feature_flags.enable_https_redirect:
    app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)

# API
app.include_router(
    characters_router,
    tags=["characters"],
    prefix="/api",
)
app.include_router(
    episodes_router,
    tags=["episodes"],
    prefix="/api",
)
app.include_router(
    notifications_router,
    tags=["notifications"],
    prefix="/api",
)
app.include_router(
    seasons_router,
    tags=["seasons"],
    prefix="/api",
)
app.include_router(
    callbacks_router,
    tags=["callbacks"],
    prefix="/api",
)
app.include_router(
    graphql_router,
    prefix="/api",
    include_in_schema=False,
)
app.include_router(
    users_router,
    tags=["users"],
    prefix="/api",
)
app.include_router(
    tokens_router,
    tags=["tokens"],
    prefix="/api",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

add_pagination(app)
