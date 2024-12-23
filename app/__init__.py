from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
def create_app():
    app = FastAPI(title="fast-api-project", description="Api Description", version="1.0.1")

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust to your frontend's URL
        allow_credentials=True,
        allow_methods=["*"],  # Allows all HTTP methods
        allow_headers=["*"],  # Allows all headers
    )
    from app.authentication.routers import auth_router
    from app.subscription.routers import subscription_router
    app.include_router(auth_router)
    app.include_router(subscription_router)
    return app

