from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from payment_gateway.config import DEBUG
from payment_gateway.routes import payments

app = FastAPI(debug=DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payments.router)


@app.get("/health")
def health():
    return {"status": "ok"}
