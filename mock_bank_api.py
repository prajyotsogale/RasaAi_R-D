from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# mock db inside this program hidden from rasa

ACCOUNTS = {
    "users123" :{
        "savings": {"balance":50000.00, "currency":"USD"},
        "checking":{"balance": 1200.50, "currency": "USD"},
        "credit":{"balance": -450.00, "currency": "USD"}
    }
}

@app.get("/balance/{user_id}/{account_type}")
def get_balance(user_id: str, account_type: str):
    user = ACCOUNTS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    account = user.get(account_type.lower())
    if not account:
        raise HTTPException(status_code=404, detail="Account type not found")

    return account

class TransferRequest(BaseModel):
    user_id: str
    recipient: str
    amount: float

@app.post("/transfer")
def transfer_money(req: TransferRequest):
    user = ACCOUNTS.get(req.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user['checking']['balance']<req.amount:
        return {"status":"failed", "reason":"Insufficient funds"}

    user['checking']['balance'] -= req.amount

    return {
        "status":"success",
        "transferred": req.amount,
        "new_balance": user['checking']['balance'],
        "recipient": req.recipient
    }


# --- MOCK CARD DATA ---
CARDS = {
    "users123": [
        {"id": "1", "name": "Visa Gold", "last4": "4242", "status": "active"},
        {"id": "2", "name": "Mastercard Titanium", "last4": "8888", "status": "active"},
        {"id": "3", "name": "Amex Platinum", "last4": "1234", "status": "active"},
        {"id": "4", "name": "Visa Classic", "last4": "0000", "status": "inactive"},
    ]
}

@app.get("/cards/{user_id}")
def get_cards(user_id: str):
    """Return list of cards for the user"""
    return {"cards": CARDS.get(user_id, [])}

@app.post("/cards/block")
def block_card(payload: dict):
    """Mock endpoint to block a card"""
    # In a real app, we would update the DB here
    card_id = payload.get("card_id")
    return {"status": "success", "message": f"Card {card_id} has been successfully blocked."}


# --- MOCK LOAN DATA ---
LOANS = {
    "users123": [
        {"id": "L-901", "type": "Home Loan", "amount": 5000000, "status": "Pending Approval", "date": "2025-12-01"},
        {"id": "L-102", "type": "Personal Loan", "amount": 200000, "status": "Active", "date": "2024-05-15"},
        {"id": "L-305", "type": "Car Loan", "amount": 800000, "status": "Rejected", "date": "2025-11-20"},
    ]
}

@app.get("/loans/{user_id}")
def get_loans(user_id: str):
    """Return list of loans for the user"""
    return {"loans": LOANS.get(user_id, [])}