from fastapi import FastAPI

app = FastAPI(
    title="Order Inventory System",
    description="Production-grade Order & Inventory Management System",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Order Inventory System"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }