import asyncio

import typer
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from app import routes, services
from app.dependencies.database import get_session
from app.exceptions.base import BaseAppException
from app.schemas.base import UsernameField
from app.settings import SETTINGS
from app.db.base import init_models

app_web = FastAPI(
    title="dtech--test-task",
    version="0.5.0",
)
app_web.include_router(routes.auth.router)
app_web.include_router(routes.bills.router)
app_web.include_router(routes.payments.router)
app_web.include_router(routes.products.router)
app_web.include_router(routes.transactions.router)
app_web.include_router(routes.users.router)


@app_web.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
            <html>
                <head>
                    <title>dtech--test-task--old</title>
                </head>
                <body>
                    <h1>API по тестовому заданию</h1>
                    <div>
                        ✍ <a href="./docs">Документация приведена по данному адресу</a> 
                    </div>
                </body>
            </html>
            """
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


# -----------------------------------------------------------------------------
app_cli = typer.Typer(help=f"CLI for application {app_web.title!r}")


@app_cli.command()
def init_database():
    """Database initialization - tables are being created."""
    asyncio.run(init_models())
    print("[*] Database initialized")


@app_cli.command()
def runserver():
    """Launching an application with settings from the environment."""
    uvicorn.run(app_web, host=SETTINGS.APP_HOST, port=SETTINGS.APP_PORT)


@app_cli.command()
def create_superuser(
        username: str = typer.Option(
            ..., "-n", "--username", help="User name"),
        password: str = typer.Option(
            ..., "-p", "--password",
            prompt=True, confirmation_prompt=True,
            hide_input=True, help="User password"),
):
    """Create a superuser"""
    UsernameField.validate(username)
    try:
        asyncio.run(
            services.database.create_superuser(
                username, password, async_generator=get_session()))
    except BaseAppException:
        print("[!] User already exists")
    else:
        print("[*] User created")


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app_cli()
