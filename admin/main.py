from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

admin_router = APIRouter(
    prefix='/admin'
)


@admin_router.get('/', name='admin')
async def show_admin_home_page(request: Request):

    return templates.TemplateResponse('pages/index.html', {'request': request})


@admin_router.get('/login/', name='login')
async def admin_login(request: Request):
    return templates.TemplateResponse('pages/login.html', {'request': request})