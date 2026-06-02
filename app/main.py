from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, games, positions, cards, deck, sequences, training, users

app = FastAPI(title="Tatame API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(games.router)
app.include_router(positions.router)
app.include_router(cards.router)
app.include_router(deck.router)
app.include_router(training.router)
app.include_router(users.router)
app.include_router(sequences.router)

@app.get("/")
def root():
    return {"message": "Tatame API is running"}