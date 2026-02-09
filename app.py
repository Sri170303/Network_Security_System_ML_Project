import sys
import os
import certifi
import fastapi
from dotenv import load_dotenv
import pymongo
import pandas as pd

from networksecurity.exception.exceptions import NetworkSecurityError
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION, DATA_INGESTION_DB

ca = certifi.where()

load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URI")

client = pymongo.MongoClient(mongo_db_url, tlsCAFile = ca)
db = client[DATA_INGESTION_DB]
collection = db[DATA_INGESTION_COLLECTION]

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training Successfull")
    except Exception as e:
        raise NetworkSecurityError(e, sys)


if __name__=="__main__":
    app_run(app, host="localhost", port=8000)