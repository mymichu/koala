from fastapi import FastAPI
from koala.interface import user


app = FastAPI()
app.include_router(user.router)
