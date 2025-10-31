#!/usr/bin/env python3
"""
Text-only backend for testing multi-turn conversations
"""

import asyncio
import json
import logging
import os

import aiohttp
from aiohttp import web
from google import genai
from google.genai import types
from google.genai.live import AsyncSession
from google.genai.types import AudioTranscriptionConfig, Blob, Content, Part

# Import hotel tools, functions, and system instruction
from hotel_tools import HOTEL_TOOLS
from hotel_functions import execute_hotel_function
from hotel_system_instruction import get_system_instruction

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend_text_only.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Configuration
PROJECT_ID = "telligent-dev"
LOCATION = "us-central1"
MODEL_ID = "gemini-live-2.5-flash-preview-native-audio-09-2025"
CREDENTIALS_PATH = "../telligent-dev-cb65da0697d7.json"

# Initialize client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)


class LiveAPISession:
    """Manages a session with Google Live API - realtime input (audio + text)."""

    def __init__(self, client_ws: web.WebSocketResponse):
        self.client_ws = client_ws
        self.session: AsyncSession | None = None
        self.running = False
        self.conversation_history = []
        self.current_model_text = []
        self.activity_open = False  # Track if a realtime activity is open

    async def start(self):
        """Start the Live API session - uses async with to manage lifecycle."""
        try:
            model_path = f"publishers/google/models/{MODEL_ID}"

            # Get current time in UTC+8 (Taiwan time)
            from datetime import datetime, timezone, timedelta

            utc_plus_8 = timezone(timedelta(hours=8))
            now = datetime.now(utc_plus_8)

            # Format: "2024-10-31 14:30:00 (星期四)"
            weekdays = [
                "星期一",
                "星期二",
                "星期三",
                "星期四",
                "星期五",
                "星期六",
                "星期日",
            ]
            current_time_str = (
                f"{now.strftime('%Y-%m-%d %H:%M:%S')} ({weekdays[now.weekday()]})"
            )

            logger.info(f"   Current Time (UTC+8): {current_time_str}")

            # Get system instruction with current time
            system_instruction = get_system_instruction(current_time=current_time_str)

            config = types.LiveConnectConfig(
                response_modalities=["AUDIO"],
                input_audio_transcription=AudioTranscriptionConfig(),
                output_audio_transcription=AudioTranscriptionConfig(),
                system_instruction=system_instruction,
                tools=HOTEL_TOOLS,  # Import from hotel_tools module
                # Enable automatic VAD by Live API
                realtime_input_config=types.RealtimeInputConfig(
                    automatic_activity_detection=types.AutomaticActivityDetection(
                        disabled=False,  # Enable automatic VAD
                        # Adjust sensitivity for better detection
                        start_of_speech_sensitivity=types.StartSensitivity.START_SENSITIVITY_LOW,
                        end_of_speech_sensitivity=types.EndSensitivity.END_SENSITIVITY_LOW,
                        silence_duration_ms=800,  # Wait 800ms of silence before ending turn
                    ),
                    # Enable barge-in: user can interrupt AI's response
                    activity_handling=types.ActivityHandling.START_OF_ACTIVITY_INTERRUPTS,
                ),
            )

            logger.info("=" * 80)
            logger.info(f"[INIT] CONNECTING TO LIVE API")
            logger.info("=" * 80)
            logger.info(f"   Model: {MODEL_ID}")
            logger.info(f"   Project: {PROJECT_ID}")
            logger.info(f"   Location: {LOCATION}")
            logger.info(f"   Response Modality: AUDIO")
            logger.info(
                f"   Tools Enabled: {len(HOTEL_TOOLS[0]['function_declarations'])} functions"
            )

            # Use async with to properly manage the session lifecycle
            async with client.aio.live.connect(
                model=model_path, config=config
            ) as session:
                self.session = session
                self.running = True
                logger.info("   [SUCCESS] Live API session started successfully")
                logger.info("=" * 80)

                # Send session ready to client
                await self.client_ws.send_json(
                    {"type": "session_ready", "data": {"status": "connected"}}
                )

                # Start forwarding tasks and wait for them
                forward_client = asyncio.create_task(self.forward_from_client())
                forward_gemini = asyncio.create_task(self.forward_from_gemini())

                # Wait for either task to complete (which means error or disconnect)
                await asyncio.gather(
                    forward_client, forward_gemini, return_exceptions=True
                )

        except Exception as e:
            logger.error(f"Failed to start Live API session: {e}", exc_info=True)
            raise

    async def forward_from_client(self):
        """Forward messages from client to Gemini using realtime input for both text and audio."""
        try:
            async for msg in self.client_ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)

                    if data.get("type") == "text":
                        text = data["text"]
                        logger.info("=" * 80)
                        logger.info("[USER TEXT] INPUT")
                        logger.info("=" * 80)
                        logger.info(f"   Message: {text}")
                        logger.info(
                            f"   History Length: {len(self.conversation_history)} turns"
                        )
                        logger.info("   [SEND] Sending to Live API...")

                        # Reset accumulator for new turn
                        self.current_model_text = []
                        # Open activity, send text, close activity
                        await self.session.send_realtime_input(activity_start={})
                        await self.session.send_realtime_input(text=text)
                        await self.session.send_realtime_input(activity_end={})
                        # Track user turn locally (for debugging/inspection)
                        self.conversation_history.append(
                            Content(role="user", parts=[Part(text=text)])
                        )
                        logger.info(f"   [OK] Sent successfully")
                        logger.info("=" * 80)

                # Audio streaming path - with automatic VAD
                if data.get("type") == "audio":
                    # Reset accumulator on first audio chunk
                    if not self.activity_open:
                        logger.info("=" * 80)
                        logger.info("[AUDIO] USER AUDIO INPUT - Starting Stream")
                        logger.info("=" * 80)
                        self.activity_open = True
                        self.current_model_text = []

                    import base64

                    audio_bytes = base64.b64decode(data["data"])  # PCM16 mono 16k
                    # Just send audio - Live API's automatic VAD will handle activity detection
                    await self.session.send_realtime_input(
                        media=Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")
                    )

                if data.get("type") == "audio_end":
                    logger.info("[AUDIO] Audio stream ended by client")
                    logger.info("=" * 80)
                    # Signal end of audio stream - Live API will handle the rest
                    if self.activity_open:
                        await self.session.send_realtime_input(audio_stream_end=True)
                        self.activity_open = False

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {self.client_ws.exception()}")
                    break

        except Exception as e:
            logger.error(f"Error forwarding from client: {e}", exc_info=True)
        finally:
            self.running = False

    async def forward_from_gemini(self):
        """Forward messages from Gemini to client.
        The Live API receive() generator completes after a turn completes.
        We restart a new receive() loop per turn to support multi-turn.
        """
        try:
            while True:
                async for message in self.session.receive():
                    logger.info(f"Received message from Gemini")

                    # Input transcription (user speech)
                    if (
                        message.server_content
                        and message.server_content.input_transcription
                    ):
                        user_tx = message.server_content.input_transcription.text
                        if user_tx:
                            await self.client_ws.send_json(
                                {"type": "input_transcription", "text": user_tx}
                            )

                    # Extract transcription (model speech)
                    if (
                        message.server_content
                        and message.server_content.output_transcription
                    ):
                        transcription = message.server_content.output_transcription.text
                        if transcription:
                            logger.info(f"Got transcription: {transcription[:50]}...")
                            self.current_model_text.append(transcription)
                            await self.client_ws.send_json(
                                {"type": "text_response", "text": transcription}
                            )

                    # Handle tool calls
                    if message.tool_call:
                        import time

                        logger.info("=" * 80)
                        logger.info(
                            f"[TOOL CALL] RECEIVED - {len(message.tool_call.function_calls)} function(s)"
                        )
                        logger.info("=" * 80)

                        function_responses = []

                        # Notify frontend about tool calls
                        await self.client_ws.send_json(
                            {
                                "type": "tool_call",
                                "data": {
                                    "functionCalls": [
                                        {"name": fc.name, "args": fc.args}
                                        for fc in message.tool_call.function_calls
                                    ]
                                },
                            }
                        )

                        # Execute functions and collect responses
                        for idx, fc in enumerate(message.tool_call.function_calls, 1):
                            logger.info(f"\n[CALL #{idx}]")
                            logger.info(f"   Function ID: {fc.id}")
                            logger.info(f"   Function Name: {fc.name}")
                            logger.info(f"   Arguments:")
                            for key, value in fc.args.items():
                                logger.info(f"      - {key}: {value}")

                            # Time the execution
                            start_time = time.time()
                            logger.info(f"   [EXEC] Executing...")

                            try:
                                result = await execute_hotel_function(fc.name, fc.args)
                                execution_time = (
                                    time.time() - start_time
                                ) * 1000  # Convert to ms

                                logger.info(
                                    f"   [SUCCESS] Completed in {execution_time:.2f}ms"
                                )
                                logger.info(f"   Response:")
                                logger.info(
                                    f"      {json.dumps(result, indent=6, ensure_ascii=False)}"
                                )

                                function_responses.append(
                                    types.FunctionResponse(
                                        name=fc.name, response=result, id=fc.id
                                    )
                                )
                            except Exception as e:
                                execution_time = (time.time() - start_time) * 1000
                                logger.error(
                                    f"   [ERROR] Failed after {execution_time:.2f}ms"
                                )
                                logger.error(f"      {str(e)}", exc_info=True)

                                # Send error response
                                function_responses.append(
                                    types.FunctionResponse(
                                        name=fc.name,
                                        response={"error": str(e)},
                                        id=fc.id,
                                    )
                                )

                        # Send tool responses back to model
                        logger.info(
                            f"\n[RESPONSE] Sending {len(function_responses)} function response(s) back to Live API"
                        )
                        logger.info("=" * 80)
                        await self.session.send_tool_response(
                            function_responses=function_responses
                        )

                    # Extract audio
                    if message.server_content and message.server_content.model_turn:
                        for part in message.server_content.model_turn.parts:
                            if (
                                part.inline_data
                                and part.inline_data.mime_type.startswith("audio")
                            ):
                                import base64

                                audio_b64 = base64.b64encode(
                                    part.inline_data.data
                                ).decode()
                                await self.client_ws.send_json(
                                    {"type": "audio_response", "data": audio_b64}
                                )

                    # Check for interruption
                    if message.server_content and message.server_content.interrupted:
                        logger.info("Model interrupted by user")
                        await self.client_ws.send_json({"type": "interrupted"})
                        # Reset accumulator on interruption
                        self.current_model_text = []

                    # Check turn complete
                    if message.server_content and message.server_content.turn_complete:
                        logger.info("=" * 80)
                        logger.info("[COMPLETE] TURN COMPLETE")
                        logger.info("=" * 80)
                        await self.client_ws.send_json({"type": "turn_complete"})

                        if self.current_model_text:
                            full_text = "".join(self.current_model_text)
                            logger.info(
                                f"   Model Response: {full_text[:100]}{'...' if len(full_text) > 100 else ''}"
                            )
                            logger.info(
                                f"   Response Length: {len(full_text)} characters"
                            )
                            model_turn = Content(
                                role="model", parts=[Part(text=full_text)]
                            )
                            self.conversation_history.append(model_turn)
                            logger.info(
                                f"   Updated History Length: {len(self.conversation_history)} turns"
                            )
                            self.current_model_text = []
                        logger.info("=" * 80)

                # End of inner loop means the turn finished; start listening for next turn
                await asyncio.sleep(0)

        except Exception as e:
            logger.error(f"Error forwarding from Gemini: {e}", exc_info=True)
        finally:
            self.running = False


async def websocket_handler(request):
    """Handle WebSocket connections from frontend."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    logger.info("New WebSocket connection from frontend")

    session = LiveAPISession(ws)

    try:
        # start() will block until the session ends (managed by async with)
        await session.start()
    except Exception as e:
        logger.error(f"WebSocket handler error: {e}", exc_info=True)
    finally:
        # Clean up
        try:
            await ws.close()
        except:
            pass

    return ws


async def index(request):
    """Serve the built frontend."""
    return web.FileResponse("../frontend/dist/index.html")


async def init_app():
    """Initialize the web application."""
    app = web.Application()
    app.router.add_get("/ws", websocket_handler)
    app.router.add_get("/", index)
    app.router.add_static("/assets", "../frontend/dist/assets")
    app.router.add_static("/", "../frontend/dist")
    return app


if __name__ == "__main__":
    logger.info("Starting Text-Only Backend...")
    web.run_app(init_app(), host="localhost", port=8081)
