"""
Hotel function tool definitions for Live API
"""

HOTEL_TOOLS = [
    {
        "function_declarations": [
            {
                "name": "check_room_availability",
                "description": "Check available rooms for specific dates and room types. MUST be called when a guest asks about room availability, vacancies, or if rooms are available for certain dates. Use room_type='all' when guest hasn't specified a preference to show all options.\n\n**Invocation Condition:** Call this tool when:\n1. Guest asks about room availability (e.g., '有房間嗎？', '還有空房嗎？')\n2. BEFORE making a reservation to show available options\n3. When guest wants to modify reservation dates (check new dates availability first)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "check_in_date": {
                            "type": "string",
                            "description": "Check-in date in YYYY-MM-DD format",
                        },
                        "check_out_date": {
                            "type": "string",
                            "description": "Check-out date in YYYY-MM-DD format",
                        },
                        "room_type": {
                            "type": "string",
                            "enum": ["all", "standard", "deluxe", "suite"],
                            "description": "Type of room requested. Use 'all' to check availability for all room types when guest hasn't specified a preference.",
                        },
                    },
                    "required": ["check_in_date", "check_out_date"],
                },
            },
            {
                "name": "make_reservation",
                "description": "Create a new room reservation. Returns a reservation_id that should be remembered for future queries or modifications.\n\n**Invocation Condition:** Call this tool ONLY after:\n1. Guest has provided all required information (name, dates, room type, number of guests)\n2. Optionally checked availability with check_room_availability first\n3. Guest has confirmed they want to proceed with the booking\n\nDO NOT call this if guest is still asking questions or hasn't confirmed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "guest_name": {
                            "type": "string",
                            "description": "Full name of the guest",
                        },
                        "check_in_date": {
                            "type": "string",
                            "description": "Check-in date in YYYY-MM-DD format",
                        },
                        "check_out_date": {
                            "type": "string",
                            "description": "Check-out date in YYYY-MM-DD format",
                        },
                        "room_type": {
                            "type": "string",
                            "enum": ["standard", "deluxe", "suite"],
                            "description": "Type of room to book",
                        },
                        "num_guests": {
                            "type": "integer",
                            "description": "Number of guests",
                        },
                    },
                    "required": [
                        "guest_name",
                        "check_in_date",
                        "check_out_date",
                        "room_type",
                    ],
                },
            },
            {
                "name": "check_reservation",
                "description": "Look up an existing reservation using reservation ID. Can retrieve reservations created in the current session.\n\n**Invocation Condition:** Call this tool when:\n1. Guest asks to check their reservation status\n2. Guest provides a reservation ID/confirmation number\n3. BEFORE canceling a reservation to verify it exists and get details\n4. When guest asks about their booking details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "Reservation ID or confirmation number",
                        },
                        "guest_name": {
                            "type": "string",
                            "description": "Guest name for verification",
                        },
                    },
                    "required": ["reservation_id"],
                },
            },
            {
                "name": "cancel_reservation",
                "description": "Cancel an existing reservation. Refund amount depends on how far in advance the cancellation is made (7+ days: 100%, 3-7 days: 80%, 1-3 days: 50%, same day: 0%).\n\n**Invocation Condition:** Call this tool when:\n1. Guest explicitly requests to cancel a reservation\n2. Guest has provided the reservation_id to cancel\n3. Consider calling check_reservation FIRST to:\n   - Verify the reservation exists\n   - Show guest the booking details before canceling\n   - Confirm it's the correct reservation\n4. When modifying a reservation, call this to cancel the old one before creating a new one",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "Reservation ID to cancel",
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for cancellation",
                        },
                    },
                    "required": ["reservation_id"],
                },
            },
            {
                "name": "get_hotel_amenities",
                "description": "Get information about hotel facilities and amenities. MUST be called whenever a guest asks about hotel facilities, services, amenities, or what the hotel offers. Do not answer from memory.\n\n**Invocation Condition:** Call this tool when:\n1. Guest asks about hotel facilities (e.g., '有什麼設施？', '有健身房嗎？', '有游泳池嗎？')\n2. Guest wants to know about specific amenities (pool, gym, spa, restaurants, parking)\n3. Use amenity_type parameter to filter if guest asks about specific facility\n4. Always use this tool rather than answering from memory to ensure accurate information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "amenity_type": {
                            "type": "string",
                            "enum": [
                                "all",
                                "pool",
                                "gym",
                                "spa",
                                "restaurant",
                                "parking",
                            ],
                            "description": "Type of amenity to inquire about",
                        }
                    },
                },
            },
            {
                "name": "request_room_service",
                "description": "Request room service delivery to a guest's room.\n\n**Invocation Condition:** Call this tool when:\n1. Guest requests room service or food delivery to their room\n2. Guest has provided room number and items to order\n3. Optionally verify guest has an active reservation first (for security)\n4. Make sure to collect room number before calling this tool",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_number": {
                            "type": "string",
                            "description": "Room number for delivery",
                        },
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of items to order",
                        },
                        "special_instructions": {
                            "type": "string",
                            "description": "Any special instructions or dietary requirements",
                        },
                    },
                    "required": ["room_number", "items"],
                },
            },
        ]
    }
]
