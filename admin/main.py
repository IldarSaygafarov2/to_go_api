from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

admin_router = APIRouter()


@admin_router.get('/admin/', name='admin')
async def show_admin_home_page(request: Request):
    
    return templates.TemplateResponse('pages/index.html', {'request': request})
