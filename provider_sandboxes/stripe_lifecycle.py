import base64
import json
import os
import urllib.parse
import urllib.request
import uuid

API_ROOT = "https://api.stripe.com/v1"


def _auth_header(key):
    token = base64.b64encode((key + ":").encode()).decode()
    return "Basic " + token


def _post(key, url, payload=None, idempotency_key=None):
    body = urllib.parse.urlencode(payload or {}).encode()
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Authorization", _auth_header(key))
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    if idempotency_key:
        request.add_header("Idempotency-Key", idempotency_key)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def build_authorize_payload(amount=1299, currency="eur"):
    return {
        "amount": str(amount),
        "currency": currency,
        "payment_method": "pm_card_visa",
        "payment_method_types[]": "card",
        "capture_method": "manual",
        "confirm": "true",
        "metadata[portfolio_flow]": "authorize_capture_refund",
    }


def summarize_payment_intent(data, stage):
    return {
        "stage": stage,
        "payment_intent": data.get("id"),
        "status": data.get("status"),
        "amount": data.get("amount"),
        "amount_capturable": data.get("amount_capturable"),
        "amount_received": data.get("amount_received"),
        "currency": data.get("currency"),
        "livemode": data.get("livemode"),
        "latest_charge": data.get("latest_charge"),
    }


def summarize_refund(data):
    return {
        "stage": "refund",
        "refund": data.get("id"),
        "status": data.get("status"),
        "amount": data.get("amount"),
        "currency": data.get("currency"),
        "payment_intent": data.get("payment_intent"),
    }


def run(amount=1299, currency="eur"):
    key = os.getenv("STRIPE_TEST_SECRET_KEY")
    if not key:
        raise SystemExit("Set STRIPE_TEST_SECRET_KEY to a Stripe test secret key.")

    run_id = uuid.uuid4().hex[:12]

    authorized = _post(
        key,
        f"{API_ROOT}/payment_intents",
        build_authorize_payload(amount, currency),
        f"layan-lifecycle-{run_id}-authorize",
    )
    if authorized.get("status") != "requires_capture":
        raise RuntimeError(
            f"Expected requires_capture after authorization, got {authorized.get('status')!r}"
        )

    payment_intent_id = authorized["id"]
    captured = _post(
        key,
        f"{API_ROOT}/payment_intents/{payment_intent_id}/capture",
        {},
        f"layan-lifecycle-{run_id}-capture",
    )
    if captured.get("status") != "succeeded":
        raise RuntimeError(
            f"Expected succeeded after capture, got {captured.get('status')!r}"
        )

    refunded = _post(
        key,
        f"{API_ROOT}/refunds",
        {"payment_intent": payment_intent_id},
        f"layan-lifecycle-{run_id}-refund",
    )

    evidence = {
        "provider": "stripe",
        "environment": "test",
        "flow": "authorize_capture_refund",
        "authorization": summarize_payment_intent(authorized, "authorization"),
        "capture": summarize_payment_intent(captured, "capture"),
        "refund": summarize_refund(refunded),
    }
    print(json.dumps(evidence, indent=2))
    return evidence


if __name__ == "__main__":
    run()
