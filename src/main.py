import os.path
import sys

from aiohttp import web

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.database import init_db, close_db
from src.api.routers import setup_routers

app = web.Application()  # создается web-приложение, внутри app живет все наше приложение

if __name__ == '__main__':  # запуск приложения
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    # Base.metadata.create_all(engine)  # создает таблицу
    setup_routers(app)
    web.run_app(app)
