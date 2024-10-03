import os

from fastapi import FastAPI, Depends, Query
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, Response, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated

from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler


def dependency_1(param_1 ):
    print("Global dependency 1")

def dependency_2():
    print("Global dependency 2")


app = FastAPI(dependencies=[Depends(dependency_1), Depends(dependency_2)])
app.title = "First application"
app.version = "1.0.0"
# app.add_middleware(HTTPErrorHandler)

@app.middleware('http')
async def http_error_handler(request: Request, call_next)-> Response | JSONResponse:
    print('Middelware is running!')
    return await call_next(request)


static_path = os.path.join(os.path.dirname(__file__), 'static/')
templates_path = os.path.join(os.path.dirname(__file__), 'templates/')

app.mount('/static', StaticFiles(directory=static_path), 'static')
templates = Jinja2Templates(directory=templates_path)


@app.get('/', tags=['Home'])
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'message': 'Welcome'})

# def common_params(start_date: str, end_date:str):
#     return {"start_date": start_date, "end_date": end_date}

# commonDep = Annotated[dict, Depends(common_params)]

class CommonDep:
    def __init__(self, start_date: str, end_date:str):
        self.start_date = start_date
        self.end_date = end_date

@app.get('/users')
def get_users(commons: CommonDep = Depends() ):
    return f"Users created between {commons.start_date} and {commons.end_date}"

@app.get('/customers')
def get_customers(commons: CommonDep = Depends()):
    return f"Customers created between {commons.start_date} and {commons.end_date}"

app.include_router(prefix='/movies', router=movie_router)


# @app.get('/get_file')
# def get_file():
#     return FileResponse('archivo_de_prueba.pdf')