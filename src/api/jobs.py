from typing import Type

from aiohttp import web

from src.core.database import session
from src.models.job_model import Job
from src.schemas.job_schema import JobCreateSchema, JobResponseSchema, JobUpdateSchema


async def create_job(request: web.Request) -> web.Response:
    data: JobCreateSchema = JobCreateSchema. parse_obj(await request.json())  # получаем данные асинхронно

    job = Job(                         # создаем экземпляр
        title=data.title,
        description=data.description,
        location=data.location,
        company_name=data.company_name
    )

    session.add(job)
    session.commit()

    return web.json_response({'message': 'Created new job vacancy'})


async def get_jobs(request: web.Request) -> web.Response:
    jobs: list[Type[Job]] = session.query(Job).all()

    jobs_info: list[dict] = [
        JobResponseSchema(
            id=job.id,
            title=job.title,
            description=job.description,
            location=job.location,
            company_name=job.company_name
        ).dict() for job in jobs
    ]

    return web.json_response({'info': jobs_info})


async def get_job(request: web.Request) -> web.Response:
    job_id: int = int(request.match_info['id'])

    job: Type[Job] = session.get(Job, job_id)

    return web.json_response(JobResponseSchema(
        id=job.id,
        title=job.title,
        description=job.description,
        location=job.location,
        company_name=job.company_name
    ).dict())


async def update_job(request: web.Request) -> web.Response:
    job_id: int = int(request.match_info['id'])
    data: JobUpdateSchema = JobUpdateSchema. parse_obj(await request.json())

    job: Type[Job] = session.get(Job, job_id)
    job.title = data.title
    job.description = data.description
    job.location = data.location
    job.company_name = data.company_name

    session.add(job)
    session.commit()

    return web.json_response({'message': 'Update job vacancy'})


async def delete_job(request: web.Request) -> web.Response:
    job_id: int = int(request.match_info['id'])

    session.delete(session.get(Job, job_id))
    session.commit()

    return web.json_response({'message': 'Delete job vacancy'})
