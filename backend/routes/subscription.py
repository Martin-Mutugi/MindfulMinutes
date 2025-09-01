from flask import Blueprint, render_template, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user
import requests
import uuid

from backend.extensions import db  # ✅ Needed for committing user updates

subscription_bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@subscription_bp.route('/')
def redirect_to_plans():
    return redirect(url_for('subscription.plans'))

@subscription_bp.route('/plans')
def plans():
    return render_template('subscription/plans.html')

@subscription_bp.route('/checkout')
@login_required
def checkout():
    try:
        tx_ref = f"MM-{uuid.uuid4().hex[:10]}"

        payload = {
            "email": current_user.email,
            "amount": 100000,  # Amount in kobo (1000 KES = 100000 kobo)
            "currency": "KES",
            "reference": tx_ref,
            "callback_url": url_for('subscription.confirm', _external=True)
        }

        headers = {
            "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
            "Content-Type": "application/json"
        }

        response = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)
        data = response.json()

        if data.get("status") and data["data"].get("authorization_url"):
            return redirect(data["data"]["authorization_url"])
        else:
            flash("Payment initiation failed. Please try again.", "error")
            return render_template("subscription/error.html", error=data.get("message", "Unknown error"))

    except Exception as e:
        flash("An unexpected error occurred during payment.", "error")
        print("Paystack error:", e)
        return render_template("subscription/error.html", error=str(e))

@subscription_bp.route('/confirm')
@login_required
def confirm():
    reference = request.args.get("reference")
    if not reference:
        flash("Missing transaction reference.", "error")
        return redirect(url_for("subscription.plans"))

    headers = {
        "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}"
    }
    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(verify_url, headers=headers)
    data = response.json()

    if data.get("status") and data["data"].get("status") == "success":
        # ✅ Upgrade user to premium
        current_user.is_premium = True
        db.session.commit()

        flash("🎉 Payment successful! Premium unlocked.", "success")
        return render_template("subscription/confirm.html", reference=reference)

    else:
        flash("Payment verification failed. Please contact support.", "error")
        return render_template("subscription/error.html", error=data.get("message", "Unknown error"))
