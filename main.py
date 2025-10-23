import os

from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from constants import UPLOAD_DIR
from routes.user_routes import router as user_router
from routes.form_routes import router as form_router
from routes.section_routes import router as section_router
from routes.question_routes import router as question_router
from routes.option_routes import router as option_router

app = FastAPI()
app.include_router(user_router)
app.include_router(form_router)
app.include_router(section_router)
app.include_router(question_router)
app.include_router(option_router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    '*'
]
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"),name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def handler(event, context):
    asgi_handler = Mangum(app)
    return asgi_handler(event, context)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

