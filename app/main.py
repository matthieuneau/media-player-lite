from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import songs, users, playlists

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


# Include the router AFTER defining the routes
app.include_router(songs.router, tags=["Songs"])
app.include_router(users.router, tags=["Users"])
app.include_router(playlists.router, tags=["Playlists"])
