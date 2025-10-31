# Hotel Agent Center

A voice-enabled hotel concierge system powered by Google Gemini Live API with real-time audio and function calling capabilities.

## 🏗️ Project Structure

```
hotel-agent-center/
├── backend/                      # Python backend
│   ├── backend.py               # Main server with Live API integration
│   ├── hotel_tools.py           # Function definitions (6 tools)
│   ├── hotel_functions.py       # Mock implementations
│   └── hotel_system_instruction.py  # AI system prompt
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── App.tsx              # Main React component
│   │   ├── App.css              # ChatGPT-style UI
│   │   ├── types.ts             # TypeScript types
│   │   ├── main.tsx             # Entry point
│   │   └── index.css            # Global styles
│   ├── package.json             # Node dependencies
│   ├── vite.config.ts           # Vite configuration
│   └── tsconfig.json            # TypeScript config
├── docs/                        # Live API documentation
├── pyproject.toml               # Python dependencies (uv)
├── uv.lock                      # Lock file for reproducible builds
├── run.bat                      # Quick start (Windows)
├── run.sh                       # Quick start (Linux/Mac)
└── README.md                    # This file
```

## ✨ Features

- 🎤 **Real-time Voice Interaction** - Speak naturally with the AI agent
- 💬 **Text Chat** - Alternative text-based communication
- 🛠️ **6 Hotel Functions**:
  - Check Room Availability
  - Make Reservation
  - Check Reservation
  - Cancel Reservation
  - Get Hotel Amenities
  - Request Room Service
- 🎨 **Modern UI** - ChatGPT-inspired clean design
- ⚡ **Lazy Connection** - WebSocket connects only when needed
- 📊 **Detailed Logging** - Full visibility into tool calls and execution

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ with [uv](https://github.com/astral-sh/uv) installed
- Node.js 18+
- Google Cloud credentials (Vertex AI)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/pleomax0730/gemini-live-api-poc.git
   cd hotel-agent-center
   ```

2. **Place your Google Cloud credentials**
   ```bash
   # Put your credentials JSON file in the root directory
   # Named: telligent-dev-cb65da0697d7.json (or update backend/backend.py)
   ```

3. **Install dependencies**
   
   **Backend:**
   ```bash
   uv sync
   ```
   
   **Frontend:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Build frontend**
   ```bash
   cd frontend
   npm run build
   cd ..
   ```

5. **Run the application**
   
   **Windows:**
   ```bash
   run.bat
   ```
   
   **Linux/Mac:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

6. **Open your browser**
   ```
   http://localhost:8081
   ```

## 📝 Manual Setup (Alternative)

### Backend

```bash
cd backend
uv run backend.py
```

The backend will:
- Start on port 8081
- Serve the frontend from `../frontend/dist`
- Connect to Google Gemini Live API
- Handle WebSocket connections

### Frontend (Development)

```bash
cd frontend
npm run dev
```

This starts Vite dev server on port 3000 (for development only).

## 🛠️ Configuration

### Backend Settings

Edit `backend/backend.py`:

```python
PROJECT_ID = "your-project-id"
LOCATION = "us-central1"
MODEL_ID = "gemini-live-2.5-flash-preview-native-audio-09-2025"
CREDENTIALS_PATH = "../your-credentials.json"
```

### Port Configuration

- Backend: 8081 (change in `backend/backend.py` line 402)
- Frontend Dev Server: 3000 (change in `frontend/vite.config.ts`)

## 📊 Tool Functions

### 1. Check Room Availability
Check available rooms for specific dates and room types.

### 2. Make Reservation
Create a new room reservation with guest details.

### 3. Check Reservation
Look up existing reservation by confirmation number.

### 4. Cancel Reservation
Cancel an existing reservation.

### 5. Get Hotel Amenities
Get information about hotel facilities and services.

### 6. Request Room Service
Order room service to a specific room.

## 🎨 Frontend Features

- **Lazy WebSocket Connection** - Connects only when needed
- **Real-time Tool Call Animations** - Visual feedback for function execution
- **Audio + Text Support** - Multiple input methods
- **ChatGPT-style Interface** - Clean, modern design
- **Connection Status** - Always visible connection state

## 🔧 Development

### Backend Development

```bash
cd backend
uv run backend.py
```

Logs are written to `backend_text_only.log` with detailed information:
- User inputs
- Tool calls with arguments
- Execution timing
- Full JSON responses
- Turn completions

### Frontend Development

```bash
cd frontend
npm run dev
```

Changes hot-reload automatically.

### Building for Production

```bash
cd frontend
npm run build
```

Output goes to `frontend/dist/`.

## 📦 Dependencies

### Backend (Python)
- `google-genai` - Gemini Live API client
- `aiohttp` - Async web server
- Other dependencies in `pyproject.toml`

### Frontend (TypeScript/React)
- React 18
- TypeScript
- Vite
- Dependencies in `frontend/package.json`

## 🔒 Security Notes

- Credentials file (`*.json`) is gitignored
- Logs are gitignored
- Never commit sensitive information
- Use environment variables for production

## 📖 Documentation

Additional documentation in the `docs/` folder:
- Live API Overview
- Best Practices
- Built-in Tools Reference
- Interactive Conversations Guide
- Audio Streaming Details

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8081
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8081 | xargs kill -9
```

### Frontend Not Loading
- Ensure frontend is built: `cd frontend && npm run build`
- Check backend is serving from correct path

### Audio Not Working
- Check browser permissions for microphone
- Ensure HTTPS in production (required for audio)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - feel free to use for your projects!

## 🙏 Acknowledgments

- Google Gemini Live API
- React and Vite communities
- ChatGPT UI inspiration

---

Built with ❤️ using Google Gemini Live API
