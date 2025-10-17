from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.form_routes import router as form_router


app = FastAPI()
app.include_router(user_router)
app.include_router(form_router)
