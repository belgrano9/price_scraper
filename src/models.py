"""Data models for Travel Guard verification."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserIntent(BaseModel):
    """Parsed user intent from natural language."""

    origin: Optional[str] = Field(None, description="Departure city/station")
    destination: Optional[str] = Field(None, description="Arrival city/station")
    date: Optional[str] = Field(None, description="Travel date (raw text)")
    time_preference: Optional[str] = Field(None, description="Time preference: 'morning', 'afternoon', 'evening', or specific time")
    parsed_date: Optional[datetime] = Field(None, description="Parsed datetime")


class TrainBooking(BaseModel):
    """A train booking option (mirrors renfe_mcp TrainRide)."""

    train_type: str = Field(description="Train type (AVE, ALVIA, etc.)")
    origin: str = Field(description="Origin station name")
    destination: str = Field(description="Destination station name")
    departure_time: datetime = Field(description="Departure datetime")
    arrival_time: datetime = Field(description="Arrival datetime")
    duration_minutes: int = Field(description="Journey duration in minutes")
    price: Optional[float] = Field(None, description="Ticket price in euros")
    available: bool = Field(True, description="Whether tickets are available")


class VerificationWarning(BaseModel):
    """A warning about potential booking issues."""

    type: str = Field(description="Warning type: 'location', 'time', 'price', 'availability'")
    message: str = Field(description="Human-readable warning message")
    severity: str = Field("medium", description="Severity: 'low', 'medium', 'high'")


class VerificationResult(BaseModel):
    """Result of verifying a booking intent."""

    confidence: float = Field(description="Confidence score 0.0 - 1.0")
    safe_to_book: bool = Field(description="Whether it's safe to proceed with booking")

    intent: UserIntent = Field(description="Parsed user intent")
    warnings: list[VerificationWarning] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)

    matched_bookings: list[TrainBooking] = Field(default_factory=list)
    recommended_booking: Optional[TrainBooking] = Field(None)


class VerifyRequest(BaseModel):
    """Request to verify a booking intent."""

    intent: str = Field(description="Natural language booking intent")
    context: Optional[dict] = Field(None, description="Additional context (user_location, history, etc.)")


class VerifyResponse(BaseModel):
    """Response from verification endpoint."""

    success: bool = Field(description="Whether verification completed successfully")
    result: Optional[VerificationResult] = Field(None)
    error: Optional[str] = Field(None)
