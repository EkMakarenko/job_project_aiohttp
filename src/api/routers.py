from aiohttp import web

from src.api.jobs import create_job, get_jobs, get_job, update_job, delete_job


def setup_routers(app: web.Application) -> None:
    app.router.add_route('GET', '/jobs', get_jobs)
    app.router.add_route('POST', '/jobs', create_job)
    app.router.add_route('GET', '/jobs/{id}', get_job)
    app.router.add_route('PUT', '/jobs/{id}', update_job)
    app.router.add_route('DELETE', '/jobs/{id}', delete_job)
