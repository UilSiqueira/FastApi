from fastapi import FastAPI
from app.routes.category_routes import router as category_routers
from app.routes.product_routes import router as product_routers
from app.routes.user_routes import router as user_routers


app = FastAPI()


@app.get("/health-check")
def health_check():
    return True


app.include_router(category_routers)
app.include_router(product_routers)
app.include_router(user_routers)
