def format_currency(amount, currency="USD"):
    return f"{amount:.2f} {currency}"


def build_auth_headers(api_key):
    return {"Authorization": f"Bearer {api_key}"}


def mask_card_number(card_number):
    return card_number[-4:]


def log_payment_attempt(payload):
    print(f"Processing payment: {payload}")
