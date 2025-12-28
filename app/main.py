from fastapi import FastAPI
from app.routers import species

app = FastAPI(title="NatureDex API")

# 2. Register/Include the routers
app.include_router(species.router)
# app.include_router(user_collections.router)
# app.include_router(profiles.router)
# app.include_router(follows.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to NatureDex API!"}

# 👇 Add this block
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
