from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import subscriptions


def create_app() -> FastAPI:
    app = FastAPI(
        title="Ticketmaster Bot Subscriptions API",
        version="0.1",
        description="API for creating subscriptions to the ticketmaster bot.",
        # lifespan=lifespan,
    )

    # Add CORS middleware to allow frontend access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        subscriptions.router, prefix="/subscriptions", tags=["subscriptions"]
    )
    return app


app = create_app()


@app.get("/health")
def health_check():
    return {"status": "healthy"}
