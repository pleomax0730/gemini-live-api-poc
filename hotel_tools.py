"""
Hotel function tool definitions for Live API
"""

HOTEL_TOOLS = [
    {
        "function_declarations": [
            {
                "name": "check_room_availability",
                "description": "Check available rooms for specific dates and room types. MUST be called when a guest asks about room availability, vacancies, or if rooms are available for certain dates.",
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
                            "enum": ["standard", "deluxe", "suite"],
                            "description": "Type of room requested",
                        },
                    },
                    "required": ["check_in_date", "check_out_date"],
                },
            },
            {
                "name": "make_reservation",
                "description": "Create a new room reservation",
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
                "description": "Look up an existing reservation",
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
                "description": "Cancel an existing reservation",
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
                "description": "Get information about hotel facilities and amenities. MUST be called whenever a guest asks about hotel facilities, services, amenities, or what the hotel offers. Do not answer from memory.",
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
                "description": "Request room service delivery",
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
