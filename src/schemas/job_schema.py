from pydantic import BaseModel


class JobCreateSchema(BaseModel):
    title: str
    description: str
    location: str
    company_name: str


class JobUpdateSchema(BaseModel):
    title: str
    description: str
    location: str
    company_name: str


class JobResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    location: str
    company_name: str