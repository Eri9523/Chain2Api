import logging

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from injector import Injector

from settings.settings import Settings
from api.tokens import router as tokens_router


logger = logging.getLogger(__name__)

def create_app(root_injector: Injector) -> FastAPI:

    async def bind_injector_to_request(request: Request) -> None:
        request.state.injector = root_injector

    app = FastAPI(dependencies=[Depends(bind_injector_to_request)])

    app.include_router(tokens_router)

    settings = root_injector.get(Settings)
    # Assuming settings has server.cors.enabled, if not we'll just skip or default
    # For now, let's just enable CORS for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

