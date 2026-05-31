from fastapi import FastAPI

app = FastAPI(title="Tatame API")

@app.get("/")
def root():
    return {"message": "Tatame API is running"}