from fastapi import FastAPI
import os
API_KEY = os.getenv("API_KEY")
if( not API_KEY):
    raise NotImplementedError("API_KEY is not set in the environment variables")
app=FastAPI()
@app.get("/")
def read_root():
    return {"Hello! You  Ghafar": f"World {API_KEY}"}