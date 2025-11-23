"""Demo script showing how to use Travel Guard API."""

import httpx

API_URL = "http://localhost:8000"


def verify_booking(intent: str, user_location: str = "Madrid") -> dict:
    """
    Verify a booking intent before execution.

    Args:
        intent: Natural language booking request
        user_location: User's current city (for origin inference)

    Returns:
        Verification result with confidence, warnings, and recommendations
    """
    response = httpx.post(
        f"{API_URL}/verify",
        json={
            "intent": intent,
            "context": {"user_location": user_location}
        }
    )
    return response.json()


def print_result(result: dict):
    """Pretty print verification result."""
    if not result["success"]:
        print(f"[ERROR] {result['error']}")
        return

    r = result["result"]

    print(f"\n{'='*50}")
    print(f"Confidence: {r['confidence']:.0%}")
    print(f"Safe to book: {'YES' if r['safe_to_book'] else 'NO - needs clarification'}")

    print(f"\n[Parsed Intent]")
    intent = r["intent"]
    print(f"   From: {intent.get('origin') or '(not specified)'}")
    print(f"   To: {intent.get('destination') or '(not specified)'}")
    print(f"   Date: {intent.get('date') or '(not specified)'}")
    print(f"   Time: {intent.get('time_preference') or '(any)'}")

    if r["warnings"]:
        print(f"\n[Warnings]")
        for w in r["warnings"]:
            severity = {"low": "LOW", "medium": "MED", "high": "HIGH"}[w["severity"]]
            print(f"   [{severity}] {w['message']}")

    if r["suggestions"]:
        print(f"\n[Suggestions]")
        for s in r["suggestions"]:
            print(f"   - {s}")

    if r["matched_bookings"]:
        print(f"\n[Matched Trains] ({len(r['matched_bookings'])} found)")
        for i, b in enumerate(r["matched_bookings"][:3], 1):
            dep = b["departure_time"].split("T")[1][:5]
            arr = b["arrival_time"].split("T")[1][:5]
            avail = "available" if b["available"] else "SOLD OUT"
            print(f"   {i}. {b['train_type']} {dep} -> {arr}  EUR {b['price']:.2f} ({avail})")

    if r["recommended_booking"]:
        rec = r["recommended_booking"]
        dep = rec["departure_time"].split("T")[1][:5]
        print(f"\n[RECOMMENDED] {rec['train_type']} at {dep} for EUR {rec['price']:.2f}")

    print(f"{'='*50}\n")


def main():
    print("\n" + "="*50)
    print("  TRAVEL GUARD FOR AI - Demo")
    print("="*50 + "\n")

    # Test cases showing different scenarios
    test_cases = [
        # 1. Clear intent - should have high confidence
        ("Train from Madrid to Sevilla tomorrow at 9am", "Madrid"),

        # 2. Ambiguous destination (Barcelona has multiple stations)
        ("Train to Barcelona tomorrow morning", "Madrid"),

        # 3. Missing origin (will use context)
        ("Book a train to Valencia this afternoon", "Barcelona"),

        # 4. Vague time preference
        ("Train to Malaga tomorrow", "Madrid"),

        # 5. Missing critical info
        ("Book me a train", "Madrid"),
    ]

    for i, (intent, location) in enumerate(test_cases, 1):
        print(f"--- Test {i} ---")
        print(f"Request: \"{intent}\"")
        print(f"Context: User in {location}")

        try:
            result = verify_booking(intent, location)
            print_result(result)
        except httpx.ConnectError:
            print("[ERROR] Server not running!")
            print("Start with: uv run uvicorn src.server:app --reload")
            break


if __name__ == "__main__":
    main()
