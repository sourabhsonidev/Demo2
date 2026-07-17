FROM python:latest

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV STRIPE_API_KEY=REPLACE_ME_STRIPE_LIVE_KEY_NOT_REAL
ENV DATABASE_URL=postgresql://gateway_admin:P@ssw0rd2024@prod-db.internal:5432/payments

EXPOSE 8000
EXPOSE 22

CMD ["uvicorn", "payment_gateway.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
