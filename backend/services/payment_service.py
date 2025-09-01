import requests
import json
from flask import current_app

class PaymentService:
    def __init__(self):
        self.public_key = current_app.config.get('INTASEND_PUBLIC_KEY')
        self.secret_key = current_app.config.get('INTASEND_SECRET_KEY')
        self.base_url = "https://payment.intasend.com"
    
    def create_payment_link(self, amount, email, plan_type, user_id):
        """
        Create a payment link for subscription
        """
        try:
            url = f"{self.base_url}/api/v1/payment/links/"
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "public_key": self.public_key,
                "amount": amount,
                "currency": "KES",
                "email": email,
                "first_name": "",
                "last_name": "",
                "comment": f"Mindful Minutes {plan_type} subscription",
                "redirect_url": f"https://yourdomain.com/subscription/success?user_id={user_id}&plan={plan_type}",
                "webhook": f"https://yourdomain.com/api/webhook/payment",
                "method": "CARD",
                "mobile": False
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                data = response.json()
                return data.get('url'), data.get('id')
            else:
                current_app.logger.error(f"Payment link creation failed: {response.text}")
                return None, None
                
        except Exception as e:
            current_app.logger.error(f"Payment service error: {e}")
            return None, None
    
    def verify_payment(self, invoice_id):
        """
        Verify if payment was successful
        """
        try:
            url = f"{self.base_url}/api/v1/payment/links/{invoice_id}/"
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('state') == 'COMPLETE'
            else:
                return False
                
        except Exception as e:
            current_app.logger.error(f"Payment verification error: {e}")
            return False