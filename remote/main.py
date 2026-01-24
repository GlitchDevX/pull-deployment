from fastapi import FastAPI
from domains.website.router import router as website_router

app = FastAPI()

app.include_router(website_router)