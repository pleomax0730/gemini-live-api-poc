export interface Message {
    id: string;
    type: 'user' | 'assistant';
    text: string;
    timestamp: Date;
    audioData?: string;
}

export interface ToolCall {
    id: string;
    name: string;
    status: 'idle' | 'running' | 'completed';
    timestamp?: Date;
    args?: Record<string, unknown>;
}

export interface WebSocketMessage {
    type: string;
    data?: unknown;
    text?: string;
}

export const TOOL_DEFINITIONS = [
    {
        id: 'check_room_availability',
        name: 'Check Room Availability',
        description: 'Check available rooms for specific dates',
        icon: 'CA',
        color: '#10a37f',
    },
    {
        id: 'make_reservation',
        name: 'Make Reservation',
        description: 'Create a new room reservation',
        icon: 'MR',
        color: '#0084ff',
    },
    {
        id: 'check_reservation',
        name: 'Check Reservation',
        description: 'Look up existing reservation',
        icon: 'CR',
        color: '#8b5cf6',
    },
    {
        id: 'cancel_reservation',
        name: 'Cancel Reservation',
        description: 'Cancel an existing reservation',
        icon: 'XR',
        color: '#ef4444',
    },
    {
        id: 'get_hotel_amenities',
        name: 'Hotel Amenities',
        description: 'Get information about facilities',
        icon: 'HA',
        color: '#f59e0b',
    },
    {
        id: 'request_room_service',
        name: 'Room Service',
        description: 'Request room service',
        icon: 'RS',
        color: '#ec4899',
    },
] as const;

