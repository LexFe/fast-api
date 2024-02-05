from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from watchgod import run_process

# from app.core import security
# from app.core.config import settings
from app.routers.router import routers
from app.core import model
from app.core.database import engine





model.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(AuthenticationMiddleware, backend=security.JWTAuthenticationBackend())

app.include_router(routers)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}
        

def main():
    uvicorn.run(app, host="192.168.100.96", port="8000", reload=True)
    
if __name__ == "__main__":
    run_process("main:main", restart_delay=1)
    


