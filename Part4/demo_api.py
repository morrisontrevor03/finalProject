from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List

# -------------------------------
# App setup
# -------------------------------
app = FastAPI(
    title="Demo API",
    description="A demo FastAPI app with hardcoded customer data and API key protection.",
    version="1.0.0",
)

# -------------------------------
# API Key Authentication
# -------------------------------
VALID_API_KEYS = {"demo-key-123", "test-key-456"}

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

async def require_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    return api_key


# -------------------------------
# Fake Customer Data
# -------------------------------
class Customer(BaseModel):
    id: int
    name: str
    email: str
    city: str
    balance: float

fake_customers = [
    Customer(id=1, name="Alice Johnson", email="alice@example.com", city="Los Angeles", balance=2530.75),
    Customer(id=2, name="Bob Smith", email="bob@example.com", city="New York", balance=10450.10),
    Customer(id=3, name="Carlos Hernandez", email="carlos@example.com", city="Austin", balance=760.00),
]

# -------------------------------
# Routes
# -------------------------------
@app.get("/customers", response_model=List[Customer])
async def get_customers(api_key: str = Depends(require_api_key)):
    """Return all customers (API key required)."""
    return fake_customers


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, api_key: str = Depends(require_api_key)):
    """Return a specific customer by ID (API key required)."""
    for c in fake_customers:
        if c.id == customer_id:
            return c
    raise HTTPException(status_code=404, detail="Customer not found")


class CustomerCreate(BaseModel):
    name: str
    email: str
    city: str
    balance: float

@app.post("/customers", response_model=Customer, status_code=201)
async def create_customer(customer: CustomerCreate, api_key: str = Depends(require_api_key)):
    """Create a new customer (API key required)."""
    new_id = max(c.id for c in fake_customers) + 1
    new_customer = Customer(id=new_id, **customer.dict())
    fake_customers.append(new_customer)
    return new_customer


@app.get("/health")
async def health_check():
    """Public endpoint (no key required)."""
    return {"status": "ok", "message": "Demo API is running!"}