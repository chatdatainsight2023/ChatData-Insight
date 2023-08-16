import uvicorn
import certifi
import os
import sys

from decouple import config
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1.endpoints import web_insight
from api.v1.endpoints import mobile_insight

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# current_directory = os.path.dirname(os.path.realpath(__file__))
# backend_directory = os.path.abspath(os.path.join(current_directory,".."))
# sys.path.insert(0, backend_directory)

# current_directory = os.getcwd()
# print(current_directory)

# print(os.getcwd())

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")
app.mount("/api/static", StaticFiles(directory="static"), name="static")


DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)


origins = [
    "http://localhost:3005",
    "http://54.151.23.224",
    "https://demo.chatdatainsight.com",
    "https://demo-1.chatdatainsight.com"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
#    app.mongodb_client = AsyncIOMotorClient(DB_URL,tlsCAFile=certifi.where())
#    app.mongodb = app.mongodb_client[DB_NAME]
    pass

@app.on_event("shutdown")
async def shutdown_db_client():
#    app.mongodb_client.close()
    pass

    
# Add the routers
app.include_router(web_insight.router) # web api
app.include_router(mobile_insight.router) # mobile api


if __name__ == "__main__":
    
    uvicorn.run("main:app",  host='0.0.0.0', port=3005) # production
    # uvicorn.run("main:app", reload=True, host='0.0.0.0', port=3006) # development
