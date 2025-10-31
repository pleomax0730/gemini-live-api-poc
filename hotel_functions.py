"""
Hotel function implementations (mock data for demo)
"""

import random
from datetime import datetime, timedelta


async def execute_hotel_function(function_name: str, args: dict) -> dict:
    """
    Execute hotel functions with mock data.

    In a real implementation, these would call actual hotel systems:
    - Database queries for availability
    - Booking system APIs
    - Payment processing
    - Inventory management
    """

    if function_name == "check_room_availability":
        return await check_room_availability(args)

    elif function_name == "make_reservation":
        return await make_reservation(args)

    elif function_name == "check_reservation":
        return await check_reservation(args)

    elif function_name == "cancel_reservation":
        return await cancel_reservation(args)

    elif function_name == "get_hotel_amenities":
        return await get_hotel_amenities(args)

    elif function_name == "request_room_service":
        return await request_room_service(args)

    else:
        return {
            "error": f"Unknown function: {function_name}",
            "message": "Function not implemented",
        }


async def check_room_availability(args: dict) -> dict:
    """Check room availability (mock implementation)."""
    available_rooms = random.randint(5, 20)
    room_type = args.get("room_type", "standard")

    price_map = {"standard": 150, "deluxe": 250, "suite": 400}

    return {
        "available": True,
        "count": available_rooms,
        "room_type": room_type,
        "price_per_night": price_map.get(room_type, 150),
        "check_in": args.get("check_in_date"),
        "check_out": args.get("check_out_date"),
        "message": f"We have {available_rooms} {room_type} rooms available for your dates.",
    }


async def make_reservation(args: dict) -> dict:
    """Create a new reservation (mock implementation)."""
    reservation_id = f"RES{random.randint(100000, 999999)}"

    return {
        "success": True,
        "reservation_id": reservation_id,
        "guest_name": args.get("guest_name"),
        "check_in": args.get("check_in_date"),
        "check_out": args.get("check_out_date"),
        "room_type": args.get("room_type"),
        "num_guests": args.get("num_guests", 1),
        "room_number": f"{random.randint(1, 5)}{random.randint(0, 9)}{random.randint(1, 9)}",
        "confirmation": f"Reservation {reservation_id} confirmed",
        "message": f"Your reservation has been confirmed! Confirmation number: {reservation_id}",
    }


async def check_reservation(args: dict) -> dict:
    """Look up an existing reservation (mock implementation)."""
    reservation_id = args.get("reservation_id")
    guest_name = args.get("guest_name", "John Doe")

    return {
        "found": True,
        "reservation_id": reservation_id,
        "guest_name": guest_name,
        "check_in": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "check_out": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
        "room_type": "deluxe",
        "room_number": "305",
        "num_guests": 2,
        "status": "confirmed",
        "total_amount": 750.00,
        "message": f"Found reservation {reservation_id} for {guest_name} - deluxe room #305",
    }


async def cancel_reservation(args: dict) -> dict:
    """Cancel a reservation (mock implementation)."""
    reservation_id = args.get("reservation_id")
    reason = args.get("reason", "Guest requested")

    refund_amount = random.uniform(300, 600)

    return {
        "success": True,
        "reservation_id": reservation_id,
        "cancellation_reason": reason,
        "refund_amount": round(refund_amount, 2),
        "refund_method": "Original payment method",
        "processing_time": "3-5 business days",
        "message": f"Reservation {reservation_id} has been cancelled. Refund of ${refund_amount:.2f} will be processed in 3-5 business days.",
    }


async def get_hotel_amenities(args: dict) -> dict:
    """Get hotel amenities information (mock implementation)."""
    amenity_type = args.get("amenity_type", "all")

    amenities = {
        "pool": {
            "name": "Outdoor Pool",
            "hours": "6:00 AM - 10:00 PM daily",
            "features": ["Heated", "Poolside bar", "Lounge chairs"],
            "description": "Outdoor heated pool open year-round with poolside service",
        },
        "gym": {
            "name": "Fitness Center",
            "hours": "24 hours",
            "features": [
                "Cardio equipment",
                "Free weights",
                "Yoga mats",
                "Towel service",
            ],
            "description": "24-hour fitness center with modern equipment",
        },
        "spa": {
            "name": "Serenity Spa",
            "hours": "9:00 AM - 9:00 PM",
            "services": ["Massages", "Facials", "Body treatments", "Sauna"],
            "description": "Full-service spa offering relaxation and rejuvenation treatments",
        },
        "restaurant": {
            "name": "Hotel Restaurants",
            "options": [
                "La Bella Vita (Italian cuisine)",
                "Sakura (Japanese restaurant)",
                "The American Grill",
            ],
            "hours": "Various - 6:00 AM - 11:00 PM",
            "description": "Three on-site restaurants serving international cuisine",
        },
        "parking": {
            "name": "Parking Services",
            "type": "Complimentary valet parking",
            "features": ["24-hour valet", "Covered parking", "EV charging stations"],
            "description": "Complimentary valet parking for all hotel guests",
        },
    }

    if amenity_type == "all":
        return {
            "amenities": amenities,
            "count": len(amenities),
            "message": "Here are all our hotel amenities and facilities",
        }
    else:
        amenity_info = amenities.get(amenity_type)
        if amenity_info:
            return {
                "amenity_type": amenity_type,
                "details": amenity_info,
                "message": f"Information about our {amenity_type} facilities",
            }
        else:
            return {
                "error": "Amenity not found",
                "message": f"No information available for {amenity_type}",
            }


async def request_room_service(args: dict) -> dict:
    """Request room service (mock implementation)."""
    order_id = f"RS{random.randint(1000, 9999)}"
    items = args.get("items", [])

    # Calculate estimated delivery based on number of items
    base_time = 20
    additional_time = len(items) * 5
    total_time = min(base_time + additional_time, 45)

    # Calculate estimated delivery time as ISO format string
    estimated_datetime = datetime.now() + timedelta(minutes=total_time)

    return {
        "success": True,
        "order_id": order_id,
        "room_number": args.get("room_number"),
        "items": items,
        "item_count": len(items),
        "special_instructions": args.get("special_instructions", "None"),
        "estimated_delivery": f"{total_time} minutes",
        "estimated_time": estimated_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "message": f"Room service order {order_id} placed successfully. Estimated delivery in {total_time} minutes.",
    }
