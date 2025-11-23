# Travel Guard for AI

An insurance layer that guarantees any booking made by an AI agent.

## The Problem

AI agents are increasingly being used to make travel bookings, but they make mistakes:
- Wrong dates (confusing "next Friday" across timezones)
- Wrong locations ("Lyon, France" vs "Lyon Township, Michigan")
- Misunderstood preferences (window seat vs aisle)
- Currency and pricing errors
- Incorrect passenger details

When an AI makes a booking error, who pays? The user didn't make the mistake. The AI provider disclaims liability. The travel provider won't refund. Everyone points fingers.

## The Solution

Travel Guard for AI provides:

1. **Booking Guarantee** - If an AI agent makes a booking error, we fix it or cover the cost
2. **Real-time Verification** - API layer that validates bookings before confirmation
3. **Error Detection** - Analysis to catch common AI mistakes before they happen
4. **Instant Resolution** - Automated rebooking and refund processing

## Architecture

```
User: "Book me a train to Barcelona tomorrow morning"
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                   Travel Guard API                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. PARSE INTENT                                         │
│     ├─ origin: (inferred from context)                   │
│     ├─ destination: "Barcelona"                          │
│     ├─ date: "tomorrow"                                  │
│     └─ time_preference: "morning"                        │
│                                                          │
│  2. GET BOOKING OPTIONS                                  │
│     └─ Call renfe_mcp → TrainRide[]                      │
│                                                          │
│  3. VERIFY MATCH                                         │
│     ├─ "Barcelona" → Barcelona-Sants? Passeig de Gràcia? │
│     ├─ "morning" → 06:16? 09:00? 11:30?                  │
│     └─ Price still valid?                                │
│                                                          │
│  4. RETURN VERIFICATION                                  │
│     ├─ confidence: 0.7                                   │
│     ├─ warnings: ["Multiple Barcelona stations"]         │
│     ├─ suggestions: ["Confirm Barcelona-Sants?"]         │
│     └─ matched_booking: TrainRide                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
            Booking Provider (Renfe)
```

## Data Source

Uses [renfe_mcp](../renfe_mcp) as the travel data provider:

```python
class TrainRide:
    train_type: str       # "AVE", "ALVIA"
    origin: str           # "Madrid Pta.Atocha"
    destination: str      # "Barcelona-Sants"
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    price: float          # 94.90
    available: bool
```

## API Endpoints

### POST /verify

Validate a booking intent before execution.

**Request:**
```json
{
  "intent": "Book me a train to Barcelona tomorrow morning",
  "context": {
    "user_location": "Madrid",
    "conversation_history": []
  }
}
```

**Response:**
```json
{
  "confidence": 0.7,
  "warnings": [
    "Multiple Barcelona stations available",
    "Morning is ambiguous (06:00-12:00)"
  ],
  "suggestions": [
    "Confirm destination: Barcelona-Sants?",
    "Confirm departure time: 09:00?"
  ],
  "matched_bookings": [
    {
      "train_type": "AVE",
      "departure": "09:00",
      "arrival": "11:49",
      "price": 94.90
    }
  ],
  "safe_to_book": false
}
```

## Project Structure

```
travel-guard/
├── src/
│   ├── server.py              # FastAPI entry point
│   ├── models.py              # Intent, Booking, Verification models
│   ├── verify/
│   │   ├── intent_parser.py   # Parse user intent from text
│   │   ├── location.py        # Station disambiguation
│   │   ├── datetime.py        # Time/date verification
│   │   └── matcher.py         # Compare intent vs booking
│   └── providers/
│       └── renfe.py           # Integration with renfe_mcp
├── tests/
├── pyproject.toml
└── README.md
```

## Quick Start

```bash
# Install dependencies
uv sync

# Run the server
uv run python -m src.server

# Test verification
curl -X POST http://localhost:8000/verify \
  -H "Content-Type: application/json" \
  -d '{"intent": "Train to Barcelona tomorrow 9am"}'
```

## Business Model

- **Per-booking fee** - Small insurance premium on each transaction
- **Enterprise plans** - For AI agent developers integrating our API
- **Recovery revenue** - Negotiate with providers on error resolution

## Why This Works

This isn't middleware pretending to add value. This solves a real problem:

1. **Clear liability** - We own the risk, not the user or AI provider
2. **Aligned incentives** - We profit by preventing errors, not enabling them
3. **Trust layer** - Users can confidently let AI agents book knowing they're protected
4. **Network effects** - Better error data = better prevention = lower costs

## Status

Early development. Building the core verification engine.

## License

MIT
