
# FastAPI Stripe Payment Integration

This is a FastAPI backend project that enables payment processing using Stripe. The application allows users to create payment links, process payments securely, and track payment analytics. It also includes webhook support for handling Stripe events such as payment success.
Table of Contents

    Features
    Technologies Used
    Installation
    Usage
    API Endpoints
        Create Payment Link
        Stripe Webhook
        Get Payment Analytics
    Payment Analytics
    Stripe Webhook
    License

Features

    Create payment links for one-time payments.
    Integrate with Stripe for secure payment processing.
    Automatic handling of payment status updates via webhooks.
    Analytics for tracking payment success, failures, and pending payments.

Technologies Used

    FastAPI - A modern web framework for building APIs with Python 3.7+ based on standard Python type hints.
    SQLAlchemy - SQL toolkit and Object-Relational Mapping (ORM) system for Python.
    Stripe - Payment processing API.
    Pydantic - Data validation and settings management using Python type annotations.
    SQLite/PostgreSQL/MySQL - Database to store payment links and user data.

Installation
Prerequisites

    Python 3.7 or higher: Ensure you have Python installed. You can download it from python.org.
    pip: Python package installer, which usually comes with Python.
    Stripe Account: Set up a Stripe account to obtain your API keys.

Setup Instructions

    Clone the repository:

    bash

git clone https://github.com/yourusername/fastapi-stripe-integration.git
cd fastapi-stripe-integration

Create a virtual environment and activate it:

bash

python3 -m venv env
source env/bin/activate  # On Windows: `env\Scripts\activate`

Install the required dependencies:

bash

pip install -r requirements.txt



Start the FastAPI server:

bash

    uvicorn main:app --reload

    Access the API documentation via:
        Swagger UI: http://127.0.0.1:8000/docs
        ReDoc: http://127.0.0.1:8000/redoc

Usage

This project allows you to create payment links using the Stripe API, track payment analytics, and process webhook notifications for payment statuses. Below are the available API endpoints.
API Endpoints
1. Create Payment Link

This endpoint allows users to create a payment link by generating a Stripe checkout session.

    Method: POST

    Endpoint: /create-payment-link/

    Request Body:

    json

{
    "amount": 100.00,
    "currency": "USD",
    "description": "Payment for services",
    "expiration": "2024-10-16T07:38:55Z",
    "items": [
        {
            "name": "Service 1",
            "price": 50.00,
            "quantity": 1
        },
        {
            "name": "Service 2",
            "price": 50.00,
            "quantity": 1
        }
    ]
}

Response:

json

    {
        "id": 1,
        "amount": 100.00,
        "currency": "USD",
        "description": "Payment for services",
        "expiration": "2024-10-16T07:38:55Z",
        "payment_url": "https://checkout.stripe.com/pay/cs_test_...",
        "status": "pending",
        "created_at": "2024-10-16T07:38:55Z",
        "user_id": 1
    }

2. Stripe Webhook

Stripe sends a notification (webhook) when a payment is completed. This endpoint listens for Stripe webhook events and updates the payment status accordingly.

    Method: POST

    Endpoint: /webhook

    Request: Stripe sends the event payload directly to this endpoint. The event payload includes details about the session and payment status.

    Response:

    json

    {
        "status": "success"
    }

3. Get Payment Analytics

Retrieve analytics for payments (total payments, successful, failed, pending) for the authenticated user.

    Method: GET

    Endpoint: /analytics

    Response:

    json

    {
        "total_payments": 10,
        "total_success": 7,
        "total_failure": 2,
        "total_pending": 1
    }

Payment Analytics

The /analytics endpoint returns a summary of the user's payment activities, providing insights into total payments, successful transactions, failed payments, and pending payments.
Stripe Webhook

The /webhook endpoint listens for Stripe events like checkout.session.completed and updates the status of the payment link based on the Stripe session details.
License

This project is licensed under the MIT License.
