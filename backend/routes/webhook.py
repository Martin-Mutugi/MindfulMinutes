from flask import Blueprint, request, current_app
import hashlib
import hmac
import json

webhook_bp = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook_bp.route('/paystack', methods=['POST'])
def paystack_webhook():
    payload = request.get_data()
    signature = request.headers.get('x-paystack-signature')

    # Verify webhook signature
    secret = current_app.config['PAYSTACK_SECRET_KEY'].encode()
    expected_signature = hmac.new(secret, payload, hashlib.sha512).hexdigest()

    if signature != expected_signature:
        return "Invalid signature", 400

    data = json.loads(payload)
    event = data.get("event")

    if event == "charge.success":
        reference = data["data"]["reference"]
        email = data["data"]["customer"]["email"]
        # TODO: Lookup user by email and mark as premium
        print(f"✅ Payment confirmed for {email} | Ref: {reference}")

    return "Webhook received", 200
