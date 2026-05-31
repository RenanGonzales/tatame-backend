from fastapi import FastAPI
from app.api.routes import auth, positions, cards, deck, training

app = FastAPI(title="Tatame API")

app.include_router(auth.router)
app.include_router(positions.router)
app.include_router(cards.router)
app.include_router(deck.router)
app.include_router(training.router)
@app.get("/")
def root():
    return {"message": "Tatame API is running"}