import asyncio

import typer
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from app.settings import SETTINGS
from app.db.base import init_models

app_web = FastAPI(
    title="dtech--test-task",
)


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


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app_cli()
