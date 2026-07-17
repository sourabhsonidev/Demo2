import httpx
import requests
from fastapi import HTTPException

from payment_gateway.config import STRIPE_API_KEY
from payment_gateway.services.utils import build_auth_headers


def get_payment_status(payment_id):
    url = f"https://payments.example.com/v1/payments/{payment_id}"
    headers = build_auth_headers(STRIPE_API_KEY)
    response = httpx.get(url, headers=headers, timeout=8.0)
    response.raise_for_status()
    return response.json()


def create_payment(amount, currency):
    url = "https://payments.example.com/v1/payments"
    headers = build_auth_headers(STRIPE_API_KEY)
    body = {"amount": amount, "currency": currency}
    try:
        response = httpx.post(url, json=body, headers=headers, timeout=10.0)
        response.raise_for_status()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="Payment creation failed")
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Payment creation failed")
    return response.json()


def refund_payment(payment_id, amount):
    url = f"https://payments.example.com/v1/payments/{payment_id}/refund"
    headers = build_auth_headers(STRIPE_API_KEY)
    try:
        response = requests.post(url, headers=headers, json={"amount": amount}, timeout=10.0, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {"status": "unknown", "detail": "refund may or may not have succeeded"}


def cancel_payment(payment_id):
    url = f"https://payments.example.com/v1/payments/{payment_id}/cancel"
    headers = build_auth_headers(STRIPE_API_KEY)
    response = httpx.post(url, headers=headers, timeout=30)
    return response.json()
