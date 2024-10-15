import stripe
from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from config import STRIPE_SECRET_KEY, SessionLocal
from models import PaymentLink
from schemas import PaymentLinkCreate, PaymentLinkResponse
from datetime import datetime
from models import *
import json
from starlette.status import HTTP_200_OK

stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter()
YOUR_DOMAIN = "http://localhost:8000"  # Replace with your actual domain in production

# @router.post("/create-payment-link/", response_model=PaymentLinkResponse)
# async def create_payment_link(payment_data: PaymentLinkCreate, user: User = Depends(get_current_user)):
#     try:
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[{
#                 'price_data': {
#                     'currency': payment_data.currency,
#                     'product_data': {
#                         'name': payment_data.description,
#                     },
#                     'unit_amount': int(payment_data.amount * 100),
#                 },
#                 'quantity': 1,
#             }],
#             mode='payment',
#             success_url=f"{YOUR_DOMAIN}/success",
#             cancel_url=f"{YOUR_DOMAIN}/cancel",
#             client_reference_id=payment_link.id  # Pass the payment_link_id here
#         )
        
#         db = SessionLocal()
#         payment_link = PaymentLink(
#             amount=payment_data.amount,
#             currency=payment_data.currency,
#             description=payment_data.description,
#             expiration=payment_data.expiration,
#             payment_url=session.url,
#             user_id=user.id
#         )
#         db.add(payment_link)
#         db.commit()
#         db.refresh(payment_link)
#         return payment_link
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
  
  

@router.post("/create-payment-link/", response_model=PaymentLinkResponse)
async def create_payment_link(payment_data: PaymentLinkCreate, user: User = Depends(get_current_user)):
    db = SessionLocal()  # Open the session
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
        
        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': payment_data.currency,
                    'product_data': {
                        'name': payment_data.description,
                    },
                    'unit_amount': int(payment_data.amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url = "http://localhost:3000/dashboard?status=success",
            cancel_url = "http://localhost:3000/dashboard?status=failed",
            client_reference_id=payment_link.id  # Pass the payment_link_id here
        )

        # Log the session to confirm client_reference_id is present
        print("Stripe session created:", session)

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
    endpoint_secret = "whsec_kyJvoLYkpnyqx4qxGkZRNC7TDKOXNjeX"

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        print("Webhook event received:", event)  # Log the entire event
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid payload: {str(e)}")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid signature: {str(e)}")

    # Log the event object to see where client_reference_id is located
    print("Event datassssss:", event["data"]["object"])
    print("event",event["type"])
    

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]  # This is the session object

        # Directly access the client_reference_id
        client_reference_id = event["data"]["object"]['client_reference_id']
        print("Session data:", session)  #
        
        # Try accessing the client_reference_id
        print("Payment Link ID:", client_reference_id)  # Check if this is printed correctly

        if client_reference_id:
            print("completed")
            db = SessionLocal()
            payment_link = db.query(PaymentLink).filter(PaymentLink.id == client_reference_id).first()
            if payment_link:
                payment_link.status = event["data"]["object"]["status"]  # Update the status
                db.commit()

    return {"status": "success"}, HTTP_200_OK



# @router.post("/webhook")
# async def stripe_webhook(request: Request):
#     payload = await request.body()
#     sig_header = request.headers.get("Stripe-Signature")
#     endpoint_secret = "whsec_bqLhLrgUuvrzt5clhJnn1jo4Fwih0Vwo"  # Get this from your Stripe dashboard

#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#         print("comingggggggg")
#     except ValueError as e:
#         print("NOTCOMING")
#         raise HTTPException(status_code=400, detail=f"Invalid payload: {str(e)}")
#     except stripe.error.SignatureVerificationError as e:
#         raise HTTPException(status_code=400, detail=f"Invalid signature: {str(e)}")

#     # Handle the event

#     if event["data"]["object"]["status"]=="succeeded":
#         print("SDSFDFFDSGFV1111")
        
#         session = event["data"]["object"]

#         payment_link_id = session.get("client_reference_id")  # You can pass this from the client side
#         print("session",session)

#         # Update the payment status in the database
#         db = SessionLocal()
#         payment_link = db.query(PaymentLink).filter(PaymentLink.id == payment_link_id).first()
#         if payment_link:
#             print("payment",payment_link.status)
#             payment_link.status = event["data"]["object"]["status"]  # Update the status
#             db.commit()

#     return {"status": "success"}, HTTP_200_OK


@router.get("/success")
async def payment_success():
    return {"message": "Payment successful!"}


@router.get("/cancel")
async def payment_cancel():
    return {"message": "Payment canceled."}

