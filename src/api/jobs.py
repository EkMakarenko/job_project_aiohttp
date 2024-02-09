from typing import Type, Any

from aiohttp import web
from sqlalchemy import select, exc

from src.core.database import get_session
from src.models.job_model import Job
from src.schemas.job_schema import JobCreateSchema, JobResponseSchema, JobUpdateSchema


async def create_job(request: web.Request) -> web.Response:
    try:
        data: JobCreateSchema = JobCreateSchema. parse_obj(await request.json())  # получаем данные асинхронно
    except ValueError as e:
        return web.json_response({'status:': e})

    async with get_session() as session:
        job = Job(                         # создаем экземпляр
            title=data.title,
            description=data.description,
            location=data.location,
            company_name=data.company_name
        )
        session.add(job)
        await session.commit()

    return web.json_response({'message': 'Created new job vacancy'})


async def get_jobs(request: web.Request) -> web.Response:
    async with get_session() as session:
        jobs: Any = await session.execute(select(Job))

    jobs_info: list[dict] = [
        JobResponseSchema(
            id=job.id,
            title=job.title,
            description=job.description,
            location=job.location,
            company_name=job.company_name
        ).dict() for job in jobs.scalars()
    ]

    return web.json_response({'info': jobs_info})


async def get_job(request: web.Request) -> web.Response:
    job_id: int = int(request.match_info['id'])
    async with get_session() as session:
        job: Type[Job] = await session.get(Job, job_id)
        if not job:
            return web.json_response({'status': f'Job with {job_id=} not found'}, status=404)

    return web.json_response(JobResponseSchema(
        id=job.id,
        title=job.title,
        description=job.description,
        location=job.location,
        company_name=job.company_name
    ).dict())


async def update_job(request: web.Request) -> web.Response:
    job_id: int = int(request.match_info['id'])

    try:
        data: JobUpdateSchema = JobUpdateSchema. parse_obj(await request.json())  # получаем данные асинхронно
    except ValueError as e:
        return web.json_response({'status:': e})

    async with get_session() as session:
        job: Type[Job] = await session.get(Job, job_id)

        if not job:
            return web.json_response({'status': f'Job with {job_id=} not found'}, status=404)

        job.title = data.title
        job.description = data.description
        job.location = data.location
        job.company_name = data.company_name

        session.add(job)
        await session.commit()

    return web.json_response({'message': 'Update job vacancy'})


async def delete_job(request: web.Request) -> web.Response:
    job_id: int = int(request.match_info['id'])
    async with get_session() as session:
        job = await session.get(Job, job_id)
        if not job:
            return web.json_response({'status': f'Job with {job_id=} not found'}, status=404)

        await session.delete(job)
        await session.commit()

    return web.json_response({'message': 'Delete job vacancy'})
