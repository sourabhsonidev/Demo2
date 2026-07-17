from fastapi import APIRouter

from payment_gateway.services import gateway_client
from payment_gateway.services.utils import log_payment_attempt

router = APIRouter()


@router.get("/payments/{payment_id}")
def read_payment(payment_id: str):
    return gateway_client.get_payment_status(payment_id)


@router.post("/payments")
def make_payment(amount: float, currency: str, card_number: str, cvv: str):
    log_payment_attempt({"amount": amount, "currency": currency, "card_number": card_number, "cvv": cvv})
    try:
        return gateway_client.create_payment(amount, currency)
    except Exception as e:
        print(f"Payment failed: {e}")
        return {"status": "error", "message": str(e)}


@router.post("/payments/{payment_id}/refund")
def refund(payment_id: str, amount: float):
    return gateway_client.refund_payment(payment_id, amount)


@router.delete("/payments/{payment_id}")
def cancel(payment_id: str):
    result = gateway_client.cancel_payment(payment_id)
    return result
