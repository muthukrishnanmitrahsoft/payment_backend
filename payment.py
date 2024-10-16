import stripe
from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from config import *
from models import PaymentLink
from schemas import PaymentLinkCreate, PaymentLinkResponse
from datetime import datetime
from models import *
import json
from starlette.status import HTTP_200_OK

stripe.api_key = STRIPE_SECRET_KEY
success_url_data = SUCCESS_URL
cancel_url_data = CANCEL_URL
end_point = END_POINT

router = APIRouter()



@router.post("/create-payment-link/", response_model=PaymentLinkResponse)
async def create_payment_link(payment_data: PaymentLinkCreate, user: User = Depends(get_current_user)):
    db = SessionLocal()  # Open the session
    tax_rate = stripe.TaxRate.create(
    display_name="Service Tax",
    percentage=8.5,
    inclusive=False,  # Change to True if tax is included in item prices
)
    tax_rate_id = tax_rate.id  # Get the ID of the created tax rate
    try:    
        # Create the PaymentLink in the database
        payment_link = PaymentLink(
            amount=payment_data.amount,
            currency=payment_data.currency,
            description=payment_data.description,
            expiration=payment_data.expiration,
            user_id=user.id,
            status="pending"  # Default status
        )
        db.add(payment_link)
        db.commit()
        db.refresh(payment_link)  # Refresh to get the updated instance from the database
        line_items = [
            {
       
                'price_data': {
                    'currency': payment_data.currency,

                    'product_data': {
                        'name': item.name,  # Access 'name' using dot notation
                    },
                    'unit_amount': int(item.price * 100),  # Stripe expects amounts in cents
                },
                'quantity': item.quantity,  # Access 'quantity' using dot notation
                        'tax_rates': [tax_rate_id],  # Add the tax rate here
            } for item in payment_data.items  # Loop over each item in payment_data.items
        ]
        if payment_data.currency == 'EUR':
            payment_method_types = ['card', 'ideal']
        else:
            payment_method_types = ['card']
        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=payment_method_types,
            line_items=line_items,
            mode='payment',
            success_url = success_url_data,
            cancel_url = cancel_url_data,
            client_reference_id=payment_link.id  # Pass the payment_link_id here
        )

        # Log the session to confirm client_reference_id is present

        # Update the payment_url and commit the update to the session
        payment_link.payment_url = session.url
        db.commit()  # Commit the update
        
        # Serialize the payment_link object
        payment_link_data = {
            "id": payment_link.id,
            "amount": payment_link.amount,
            "currency": payment_link.currency,
            "description": payment_link.description,
            "expiration": payment_link.expiration,
            "payment_url": payment_link.payment_url,
            "status": payment_link.status,
            "created_at": payment_link.created_at,
            "user_id": payment_link.user_id
        }

        return payment_link_data  # Return the serialized data

    except Exception as e:
        db.rollback()  # Rollback on exception
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()  # Ensure the session is closed

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = end_point

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid payload: {str(e)}")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid signature: {str(e)}")

    # Log the event object to see where client_reference_id is located
    

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]  # This is the session object

        # Directly access the client_reference_id
        client_reference_id = event["data"]["object"]['client_reference_id']
        
        # Try accessing the client_reference_id

        if client_reference_id:
            db = SessionLocal()
            payment_link = db.query(PaymentLink).filter(PaymentLink.id == client_reference_id).first()
            if payment_link:
                payment_link.status = event["data"]["object"]["status"]  # Update the status
                db.commit()

    return {"status": "success"}, HTTP_200_OK

