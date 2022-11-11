from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="dtech--test-task",
)


@app.get("/", response_class=HTMLResponse)
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
