from app import create_app
from app.database import init_db
app = create_app()

@app.on_event("startup")
async def start_db():
    await init_db()


