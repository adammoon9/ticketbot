from fastapi import FastAPI

from .routers import subscriptions


def create_app() -> FastAPI:
    app = FastAPI(
        title="Ticketmaster Bot Subscriptions API",
        version="0.1",
        description="API for creating subscriptions to the ticketmaster bot.",
        # lifespan=lifespan,
    )

    app.include_router(
        subscriptions.router, prefix="/subscriptions", tags=["subscriptions"]
    )
    return app


app = create_app()


@app.get("/health")
def health_check():
    return {"status": "healthy"}
