from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import AppError
from app.routers import categoria_router, material_router

app = FastAPI(
    title="API Estoque Almoxarifado",
    version="1.0.0",
)


@app.exception_handler(AppError)
def tratar_app_error(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.mensagem},
    )


@app.get("/", tags=["Sistema"])
def health_check():
    return {"status": "ok", "mensagem": "API Estoque Almoxarifado rodando"}


app.include_router(categoria_router.router)
app.include_router(material_router.router)