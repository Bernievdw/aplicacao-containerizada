from fastapi import FastAPI
from app.backend.db.session import create_db_and_tables
from app.backend.api.api_v1.endpoints import auth, clients, assets, allocations, movements, reports

def create_app():
    app = FastAPI(title="Escritório de Investimentos API")
    app.include_router(auth.router)
    app.include_router(clients.router)
    app.include_router(assets.router)
    app.include_router(allocations.router)
    app.include_router(movements.router)
    app.include_router(reports.router)

    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()
    return app

app = create_app()
