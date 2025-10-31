"""
Hotel function implementations (mock data for demo)
"""

import random
from datetime import datetime, timedelta

# In-memory storage for reservations (session-level state)
# Format: {reservation_id: {guest_name, check_in, check_out, room_type, num_guests, room_number, total_amount, status}}
RESERVATIONS_DB = {}


def get_all_active_reservations() -> list:
    """Get all active (not cancelled) reservations."""
    return [res for res in RESERVATIONS_DB.values() if res.get("status") == "confirmed"]


def get_reservation_by_guest_name(guest_name: str) -> list:
    """Find reservations by guest name."""
    return [
        res
        for res in RESERVATIONS_DB.values()
        if guest_name.lower() in res.get("guest_name", "").lower()
    ]


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
    room_type = args.get("room_type", "all")
    check_in = args.get("check_in_date")
    check_out = args.get("check_out_date")

    price_map = {"standard": 4500, "deluxe": 7500, "suite": 12000}  # 新台幣 NT$

    # If room_type is "all" or not specified, return all room types
    if room_type == "all":
        room_availability = []
        total_available = 0

        for rtype, price in price_map.items():
            available = random.randint(3, 15)
            total_available += available
            room_availability.append(
                {
                    "room_type": rtype,
                    "available_count": available,
                    "price_per_night": price,
                }
            )

        return {
            "available": True,
            "room_types": room_availability,
            "total_rooms": total_available,
            "check_in": check_in,
            "check_out": check_out,
            "message": f"We have {total_available} rooms available across all types for your dates.",
        }

    # Single room type query
    else:
        available_rooms = random.randint(5, 20)

        return {
            "available": True,
            "count": available_rooms,
            "room_type": room_type,
            "price_per_night": price_map.get(room_type, 150),
            "check_in": check_in,
            "check_out": check_out,
            "message": f"We have {available_rooms} {room_type} rooms available for your dates.",
        }


async def make_reservation(args: dict) -> dict:
    """Create a new reservation and store in memory."""
    reservation_id = f"RES{random.randint(100000, 999999)}"
    room_number = f"{random.randint(1, 5)}{random.randint(0, 9)}{random.randint(1, 9)}"

    # Calculate total amount
    check_in = datetime.strptime(args.get("check_in_date"), "%Y-%m-%d")
    check_out = datetime.strptime(args.get("check_out_date"), "%Y-%m-%d")
    nights = (check_out - check_in).days

    price_map = {"standard": 4500, "deluxe": 7500, "suite": 12000}
    room_type = args.get("room_type")
    price_per_night = price_map.get(room_type, 4500)
    total_amount = price_per_night * nights

    # Store in memory
    reservation_data = {
        "reservation_id": reservation_id,
        "guest_name": args.get("guest_name"),
        "check_in": args.get("check_in_date"),
        "check_out": args.get("check_out_date"),
        "room_type": room_type,
        "num_guests": args.get("num_guests", 1),
        "room_number": room_number,
        "total_amount": total_amount,
        "price_per_night": price_per_night,
        "nights": nights,
        "status": "confirmed",
        "created_at": datetime.now().isoformat(),
    }

    RESERVATIONS_DB[reservation_id] = reservation_data

    return {
        "success": True,
        "reservation_id": reservation_id,
        "guest_name": args.get("guest_name"),
        "check_in": args.get("check_in_date"),
        "check_out": args.get("check_out_date"),
        "room_type": room_type,
        "num_guests": args.get("num_guests", 1),
        "room_number": room_number,
        "total_amount": total_amount,
        "price_per_night": price_per_night,
        "nights": nights,
        "confirmation": f"Reservation {reservation_id} confirmed",
        "message": f"訂房完成！確認號碼：{reservation_id}，總金額：NT$ {total_amount:,}（{nights} 晚）",
    }


async def check_reservation(args: dict) -> dict:
    """Look up an existing reservation from memory."""
    reservation_id = args.get("reservation_id")

    # Check in-memory database
    if reservation_id in RESERVATIONS_DB:
        reservation = RESERVATIONS_DB[reservation_id]
        return {
            "found": True,
            "reservation_id": reservation_id,
            "guest_name": reservation["guest_name"],
            "check_in": reservation["check_in"],
            "check_out": reservation["check_out"],
            "room_type": reservation["room_type"],
            "room_number": reservation["room_number"],
            "num_guests": reservation["num_guests"],
            "status": reservation["status"],
            "total_amount": reservation["total_amount"],
            "price_per_night": reservation["price_per_night"],
            "nights": reservation["nights"],
            "message": f"找到訂房記錄 {reservation_id}：{reservation['guest_name']}，{reservation['room_type']} {reservation['room_number']} 號房",
        }
    else:
        return {
            "found": False,
            "reservation_id": reservation_id,
            "message": f"查無訂房記錄 {reservation_id}，請確認訂房編號是否正確",
        }


async def cancel_reservation(args: dict) -> dict:
    """Cancel a reservation from memory."""
    reservation_id = args.get("reservation_id")
    reason = args.get("reason", "客人要求取消")

    # Check if reservation exists
    if reservation_id not in RESERVATIONS_DB:
        return {
            "success": False,
            "reservation_id": reservation_id,
            "message": f"查無訂房記錄 {reservation_id}，無法取消",
        }

    reservation = RESERVATIONS_DB[reservation_id]

    # Check if already cancelled
    if reservation["status"] == "cancelled":
        return {
            "success": False,
            "reservation_id": reservation_id,
            "message": f"訂房 {reservation_id} 已經取消過了",
        }

    # Calculate refund based on cancellation timing
    check_in_date = datetime.strptime(reservation["check_in"], "%Y-%m-%d")
    days_until_checkin = (check_in_date - datetime.now()).days
    total_amount = reservation["total_amount"]

    # Refund policy
    if days_until_checkin >= 7:
        refund_rate = 1.0  # 100% refund
        refund_note = "提前 7 天以上取消，全額退款"
    elif days_until_checkin >= 3:
        refund_rate = 0.8  # 80% refund
        refund_note = "提前 3-7 天取消，退款 80%"
    elif days_until_checkin >= 1:
        refund_rate = 0.5  # 50% refund
        refund_note = "提前 1-3 天取消，退款 50%"
    else:
        refund_rate = 0.0  # No refund
        refund_note = "當天取消，無法退款"

    refund_amount = total_amount * refund_rate

    # Update status
    reservation["status"] = "cancelled"
    reservation["cancelled_at"] = datetime.now().isoformat()
    reservation["cancellation_reason"] = reason

    return {
        "success": True,
        "reservation_id": reservation_id,
        "guest_name": reservation["guest_name"],
        "cancellation_reason": reason,
        "original_amount": total_amount,
        "refund_amount": int(refund_amount),
        "refund_rate": f"{int(refund_rate * 100)}%",
        "refund_note": refund_note,
        "refund_method": "原付款方式",
        "processing_time": "3-5 個工作天",
        "message": f"訂房 {reservation_id} 已取消。{refund_note}，退款金額 NT$ {int(refund_amount):,}，預計 3-5 個工作天退回原付款帳戶。",
    }


async def get_hotel_amenities(args: dict) -> dict:
    """Get hotel amenities information (mock implementation)."""
    amenity_type = args.get("amenity_type", "all")

    amenities = {
        "pool": {
            "name": "戶外游泳池",
            "hours": "每日 06:00 - 22:00",
            "features": ["溫水加熱", "池畔酒吧", "躺椅休憩區"],
            "description": "全年開放的溫水戶外泳池，提供池畔服務",
        },
        "gym": {
            "name": "健身中心",
            "hours": "24 小時開放",
            "features": [
                "有氧運動器材",
                "自由重量訓練區",
                "瑜珈墊",
                "毛巾服務",
            ],
            "description": "24 小時開放的健身中心，配備現代化器材",
        },
        "spa": {
            "name": "靜心 SPA",
            "hours": "每日 09:00 - 21:00",
            "services": ["按摩", "臉部護理", "身體療程", "三溫暖"],
            "description": "提供完整放鬆與舒壓療程的全方位 SPA 中心",
        },
        "restaurant": {
            "name": "飯店餐廳",
            "options": [
                "貝拉維塔（義式料理）",
                "櫻花亭（日式料理）",
                "美式烤肉館",
            ],
            "hours": "各餐廳時間不同，整體營業 06:00 - 23:00",
            "description": "三家不同風格的餐廳，提供國際美食料理",
        },
        "parking": {
            "name": "停車服務",
            "type": "免費代客停車",
            "features": ["24小時代客泊車", "室內停車場", "電動車充電站"],
            "description": "為所有住宿旅客提供免費代客停車服務",
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
