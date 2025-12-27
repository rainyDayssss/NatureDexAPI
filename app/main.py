from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to NatureDex API!"}

@app.get("/status")
def get_status():
    return {"status": "Environment is working!"}

@app.get("/health")
def get_health():
    return {"health": "All systems operational!"}


