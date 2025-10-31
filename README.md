# Hotel Agent Center (Powered by Google Live API)

This project is a functional prototype of a hotel customer service agent center that uses the Google Live API to facilitate real-time, multi-turn conversations with a generative AI model (`gemini-live-2.5-flash-preview-native-audio-09-2025`). It supports both text and voice input, and provides responses in streaming audio with synchronized text transcriptions.

The frontend is built with React, TypeScript, and Vite, featuring a modern, minimalist black and white UI. The backend is a Python application using `aiohttp` for WebSocket communication and the `google-genai` SDK to interact with the Live API.

## Core Features

- **Real-time Bimodal Interaction**: Communicate with the AI via text or voice.
- **Streaming Audio I/O**: Both user's speech and AI's audio response are streamed for low-latency interaction.
- **Multi-Turn Conversation**: Maintains conversation context for coherent, multi-step dialogues.
- **Backend-driven VAD**: Leverages the Live API's built-in Voice Activity Detection to automatically determine the end of a user's turn.
- **Conversation Interruption (Barge-in)**: Users can interrupt the AI's response at any time by starting to speak.
- **Modern UI**: A clean, 2025-inspired black and white interface with a tool activity panel.

## Key Challenges & Solutions

This project navigated several complex technical challenges to achieve a seamless conversational experience. Here’s a summary of the major hurdles and their solutions.

### 1. Challenge: Achieving Robust Multi-Turn Conversations

- **Problem**: The application initially struggled to maintain a conversation beyond the first turn. Text messages sent after the first interaction would not receive a response, and the session would stall. Early attempts mixing different API methods (`send_client_content` for text and `send_realtime_input` for audio) led to unpredictable behavior and race conditions.

- **Solution**: The key was to adopt a unified approach using a single, consistent method for all user inputs.
    1. **Unified `send_realtime_input`**: We exclusively used the `send_realtime_input` method for both text and audio streams. This aligns with the "Don't Cross the Streams" best practice for the Live API.
    2. **Explicit Turn Management for Text**: For text messages, each input is wrapped with `activity_start={}` and `activity_end={}` signals. This explicitly defines a "turn" for the API, preventing timeouts and ensuring the model processes the input correctly.
    3. **Persistent Backend Receive Loop**: A critical fix was wrapping the backend's `session.receive()` generator in a `while True:` loop. The generator naturally completes after a `turn_complete` event. The `while` loop ensures that after one turn finishes, the backend immediately starts listening again for the next message from the server, enabling continuous multi-turn dialogue.

### 2. Challenge: Implementing Reliable Voice Input and VAD

- **Problem**: The initial voice input implementation placed Voice Activity Detection (VAD) logic on the frontend. This was problematic as it was unreliable, often cutting off recordings prematurely if the user paused briefly or if there was ambient noise. It also fought with the API's own internal state management.

- **Solution**: We shifted the responsibility of VAD from the frontend to the backend, leveraging the powerful built-in capabilities of the Google Live API, as recommended by the [official documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/multimodal-live).
    1. **Enable Server-Side VAD**: In the backend's `LiveConnectConfig`, we enabled `automatic_activity_detection`. This tells the Live API to use its own advanced algorithms to detect the start and end of speech.
    2. **Simplify the Frontend**: The frontend's role was simplified to purely streaming raw audio data whenever the user holds down the record button. It no longer contains any VAD logic.
    3. **Enable Interruption (Barge-in)**: We configured `activity_handling` to `START_OF_ACTIVITY_INTERRUPTS`. This allows the user to interrupt the AI's response simply by starting to speak, creating a more fluid and natural conversation flow.

### 3. Challenge: Smooth, Streaming Audio Playback

- **Problem**: The first version of the audio playback feature buffered all incoming audio chunks from the AI and only played the complete audio file after the `turn_complete` signal was received. This created a significant delay and a poor user experience, defeating the purpose of a "live" agent.

- **Solution**: The frontend was re-architected to handle true audio streaming using the **Web Audio API**.
    1. **Audio Queue**: An audio queue (`audioQueueRef`) was implemented to hold incoming base64-encoded audio chunks.
    2. **Immediate Decoding & Scheduling**: As each chunk arrives, it is immediately decoded into an `AudioBuffer`.
    3. **Seamless Concatenation**: Using `audioContext.currentTime` and a `nextStartTimeRef`, each new audio buffer is scheduled to play precisely at the moment the previous one ends. This ensures a continuous, seamless stream of audio with minimal latency, just like a real phone call.

## Setup and Running the Application

### Prerequisites

- Python 3.13+
- Node.js and npm
- `uv` (Python package installer)
- A Google Cloud project with the Vertex AI API enabled.
- A service account key file (`telligent-dev-cb65da0697d7.json`) with appropriate permissions.

### 1. Backend Setup

Install Python dependencies:

```bash
uv add aiohttp google-generativeai python-dotenv
```

### 2. Frontend Setup

Install Node.js dependencies:

```bash
npm install
```

### 3. Running the Application

1. **Start the Backend Server**:

    ```bash
    uv run backend_simple.py
    ```

2. **Start the Frontend Development Server**:

    ```bash
    npm run dev
    ```

3. **Open the Application**:
    Open your browser and navigate to `http://localhost:8080`.
