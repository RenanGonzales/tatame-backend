from fastapi import FastAPI
from app.api.routes import auth

app = FastAPI(title="Tatame API")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Tatame API is running"}