
from fastapi import FastAPI
from .database import init_db
from .routers import users, posts, auth, vote


app = FastAPI()

"""@app.on_event("startup")
async def on_startup():
    await init_db()"""

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
def root():
    return {"message":  "welcome to my api"}






    
    


    

