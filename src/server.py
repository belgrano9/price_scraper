"""Travel Guard API server."""

from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    VerifyRequest,
    VerifyResponse,
    TrainBooking,
)
from .verify import parse_intent, match_intent_to_bookings


app = FastAPI(
    title="Travel Guard for AI",
    description="Insurance layer that guarantees AI agent travel bookings",
    version="0.1.0",
)

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mock bookings for demo (in production, this would come from renfe_mcp)
def get_mock_bookings(origin: str, destination: str, date: datetime) -> list[TrainBooking]:
    """Generate mock bookings for testing."""
    base_time = datetime.combine(date.date(), datetime.min.time())

    return [
        TrainBooking(
            train_type="AVE",
            origin=f"{origin} Pta.Atocha - Almudena Grandes",
            destination=f"{destination}-Sants",
            departure_time=base_time.replace(hour=6, minute=16),
            arrival_time=base_time.replace(hour=9, minute=5),
            duration_minutes=169,
            price=94.90,
            available=True,
        ),
        TrainBooking(
            train_type="AVE",
            origin=f"{origin} Pta.Atocha - Almudena Grandes",
            destination=f"{destination}-Sants",
            departure_time=base_time.replace(hour=9, minute=0),
            arrival_time=base_time.replace(hour=11, minute=49),
            duration_minutes=169,
            price=118.60,
            available=True,
        ),
        TrainBooking(
            train_type="AVE",
            origin=f"{origin} Pta.Atocha - Almudena Grandes",
            destination=f"{destination}-Sants",
            departure_time=base_time.replace(hour=11, minute=30),
            arrival_time=base_time.replace(hour=14, minute=19),
            duration_minutes=169,
            price=89.90,
            available=True,
        ),
        TrainBooking(
            train_type="ALVIA",
            origin=f"{origin} Pta.Atocha - Almudena Grandes",
            destination=f"{destination}-Sants",
            departure_time=base_time.replace(hour=14, minute=0),
            arrival_time=base_time.replace(hour=17, minute=30),
            duration_minutes=210,
            price=65.00,
            available=True,
        ),
        TrainBooking(
            train_type="AVE",
            origin=f"{origin} Pta.Atocha - Almudena Grandes",
            destination=f"{destination}-Sants",
            departure_time=base_time.replace(hour=18, minute=0),
            arrival_time=base_time.replace(hour=20, minute=49),
            duration_minutes=169,
            price=94.90,
            available=False,  # Sold out
        ),
    ]


@app.get("/")
async def root():
    """API root - health check."""
    return {
        "service": "Travel Guard for AI",
        "version": "0.1.0",
        "status": "operational",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/verify", response_model=VerifyResponse)
async def verify_booking(request: VerifyRequest):
    """
    Verify a booking intent before execution.

    This endpoint:
    1. Parses the natural language intent
    2. Retrieves available bookings
    3. Matches intent to bookings
    4. Returns confidence score, warnings, and recommendations
    """
    try:
        # Parse the intent
        context = request.context or {}
        intent = parse_intent(request.intent, context)

        # Get available bookings
        # In production, this would call renfe_mcp
        origin = intent.origin or context.get("user_location", "Madrid")
        destination = intent.destination or "Barcelona"

        # Parse date or use tomorrow as default
        from .verify.datetime_parser import parse_datetime
        travel_date = parse_datetime(intent.date) or (datetime.now() + timedelta(days=1))

        bookings = get_mock_bookings(origin, destination, travel_date)

        # Match intent to bookings
        result = match_intent_to_bookings(intent, bookings)

        return VerifyResponse(
            success=True,
            result=result,
            error=None,
        )

    except Exception as e:
        return VerifyResponse(
            success=False,
            result=None,
            error=str(e),
        )


@app.post("/verify/quick")
async def quick_verify(intent: str, user_location: str = "Madrid"):
    """
    Quick verification with minimal input.

    Just pass the intent text and optionally the user's location.
    """
    request = VerifyRequest(
        intent=intent,
        context={"user_location": user_location},
    )
    return await verify_booking(request)


# Run with: uvicorn src.server:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
