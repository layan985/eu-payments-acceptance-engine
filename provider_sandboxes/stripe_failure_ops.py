import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
import uuid

API = "https://api.stripe.com/v1/payment_intents"

SCENARIOS = {
    "generic_decline": "pm_card_visa_chargeDeclined",
    "insufficient_funds": "pm_card_visa_chargeDeclinedInsufficientFunds",
    "lost_card": "pm_card_visa_chargeDeclinedLostCard",
    "stolen_card": "pm_card_visa_chargeDeclinedStolenCard",
    "expired_card": "pm_card_chargeDeclinedExpiredCard",
    "incorrect_cvc": "pm_card_chargeDeclinedIncorrectCvc",
    "processing_error": "pm_card_chargeDeclinedProcessingError",
    "velocity_limit": "pm_card_visa_chargeDeclinedVelocityLimitExceeded",
}


def build_payload(scenario, amount=1299, currency="eur"):
    if scenario not in SCENARIOS:
        raise ValueError(f"unknown scenario: {scenario}")
    return {
        "amount": str(amount),
        "currency": currency,
        "payment_method": SCENARIOS[scenario],
        "payment_method_types[]": "card",
        "confirm": "true",
        "metadata[portfolio_failure_scenario]": scenario,
    }


def decide_failure(error_code=None, decline_code=None, advice_code=None):
    if advice_code == "do_not_try_again":
        return {
            "retry_policy": "do_not_retry",
            "customer_action": "use_another_payment_method_or_contact_issuer",
            "safe_customer_message": "Payment was declined. Try another payment method or contact your card issuer.",
        }
    if advice_code == "try_again_later":
        return {
            "retry_policy": "retry_later",
            "customer_action": "retry_later",
            "safe_customer_message": "Payment could not be completed. Please try again later.",
        }
    if advice_code == "confirm_card_data":
        return {
            "retry_policy": "retry_after_data_correction",
            "customer_action": "confirm_card_details",
            "safe_customer_message": "Check your card details and try again.",
        }

    if decline_code in {"lost_card", "stolen_card", "fraudulent"}:
        return {
            "retry_policy": "do_not_retry",
            "customer_action": "use_another_payment_method",
            "safe_customer_message": "Payment was declined. Try another payment method.",
        }
    if decline_code == "insufficient_funds":
        return {
            "retry_policy": "retry_after_customer_action",
            "customer_action": "use_another_payment_method_or_retry_after_funds_available",
            "safe_customer_message": "Payment was declined. Try another payment method or try again later.",
        }
    if decline_code in {"generic_decline", "do_not_honor"}:
        return {
            "retry_policy": "no_automatic_retry",
            "customer_action": "use_another_payment_method_or_contact_issuer",
            "safe_customer_message": "Payment was declined. Try another payment method or contact your card issuer.",
        }
    if decline_code == "card_velocity_exceeded":
        return {
            "retry_policy": "no_immediate_retry",
            "customer_action": "wait_or_use_another_payment_method",
            "safe_customer_message": "Payment was declined. Please wait before retrying or use another payment method.",
        }
    if error_code in {"expired_card", "incorrect_cvc", "incorrect_number"}:
        return {
            "retry_policy": "retry_after_data_correction",
            "customer_action": "correct_card_details_or_use_another_payment_method",
            "safe_customer_message": "Check your card details or use another payment method.",
        }
    if error_code == "processing_error":
        return {
            "retry_policy": "retry_later",
            "customer_action": "retry_later",
            "safe_customer_message": "Payment could not be processed. Please try again.",
        }
    return {
        "retry_policy": "manual_review",
        "customer_action": "use_another_payment_method_or_contact_support",
        "safe_customer_message": "Payment could not be completed. Try another payment method.",
    }


def summarize_error(data, scenario, http_status):
    error = data.get("error") or {}
    payment_intent = error.get("payment_intent") or {}
    decline_code = error.get("decline_code")
    error_code = error.get("code")
    advice_code = error.get("advice_code")
    return {
        "provider": "stripe",
        "environment": "test",
        "scenario": scenario,
        "http_status": http_status,
        "error_type": error.get("type"),
        "error_code": error_code,
        "decline_code": decline_code,
        "advice_code": advice_code,
        "payment_intent": payment_intent.get("id"),
        "decision": decide_failure(error_code, decline_code, advice_code),
    }


def run(scenario):
    key = os.getenv("STRIPE_TEST_SECRET_KEY")
    if not key:
        raise SystemExit("Set STRIPE_TEST_SECRET_KEY to a Stripe test secret key.")

    body = urllib.parse.urlencode(build_payload(scenario)).encode()
    request = urllib.request.Request(API, data=body, method="POST")
    token = base64.b64encode((key + ":").encode()).decode()
    request.add_header("Authorization", "Basic " + token)
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    request.add_header("Idempotency-Key", f"layan-failure-{scenario}-{uuid.uuid4().hex[:10]}")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
            result = {
                "provider": "stripe",
                "environment": "test",
                "scenario": scenario,
                "unexpected_status": data.get("status"),
                "payment_intent": data.get("id"),
            }
            print(json.dumps(result, indent=2))
            return result
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {"error": {"type": "non_json_error"}}
        result = summarize_error(data, scenario, exc.code)
        print(json.dumps(result, indent=2))
        return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", choices=sorted(SCENARIOS))
    run(parser.parse_args().scenario)
