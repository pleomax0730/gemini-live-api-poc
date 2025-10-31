import { useState, useEffect, useRef, useCallback } from 'react';
import './App.css';
import { Message, ToolCall, WebSocketMessage, TOOL_DEFINITIONS } from './types';

function App() {
    const [ws, setWs] = useState<WebSocket | null>(null);
    const [connected, setConnected] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [isRecording, setIsRecording] = useState(false);
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [textInput, setTextInput] = useState('');
    const [toolCalls, setToolCalls] = useState<ToolCall[]>(
        TOOL_DEFINITIONS.map(tool => ({
            id: tool.id,
            name: tool.name,
            status: 'idle' as const,
        }))
    );
    const wsRef = useRef<WebSocket | null>(null);
    const connectionPromiseRef = useRef<Promise<WebSocket> | null>(null);

    const audioContextRef = useRef<AudioContext | null>(null);
    const recordingContextRef = useRef<AudioContext | null>(null);
    const mediaStreamRef = useRef<MediaStream | null>(null);
    const audioQueueRef = useRef<Float32Array[]>([]);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const isPlayingRef = useRef(false);
    const nextStartTimeRef = useRef(0);
    const currentAssistantMessageIdRef = useRef<string | null>(null);
    const currentUserMessageIdRef = useRef<string | null>(null);
    const isRecordingRef = useRef(false);

    // Auto-scroll to bottom
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleWebSocketMessage = useCallback((message: WebSocketMessage) => {
        console.log('Received message:', message);

        switch (message.type) {
            case 'session_ready':
                console.log('Session ready');
                // Initialize audio context
                if (!audioContextRef.current) {
                    audioContextRef.current = new AudioContext({ sampleRate: 24000 });
                    nextStartTimeRef.current = 0;
                }
                break;

            case 'audio_response':
                // Stream audio chunks immediately (low-latency playback)
                playAudioChunkImmediately(message.data as string);
                setIsSpeaking(true);
                break;

            case 'input_transcription':
                // Accumulate user transcription into a single message per turn
                if (message.text) {
                    updateLastUserMessage(message.text || '');
                }
                break;

            case 'output_transcription':
                // Update assistant message with transcription
                if (message.text) {
                    updateLastAssistantMessage(message.text || '');
                }
                break;

            case 'text_response':
                // Update assistant message with text response (from text-only backend)
                if (message.text) {
                    updateLastAssistantMessage(message.text || '');
                }
                break;

            case 'tool_call':
                // Update tool call status
                handleToolCall(message.data as any);
                break;

            case 'turn_complete':
                // Turn complete, but audio continues playing until finished
                setIsSpeaking(false);
                // Reset current assistant message ID for next turn
                currentAssistantMessageIdRef.current = null;
                currentUserMessageIdRef.current = null;
                break;

            case 'interrupted':
                setIsSpeaking(false);
                stopAllAudio();
                break;

            case 'error':
                console.error('Error from server:', message.data);
                break;
        }
    }, []);

    // Lazy connect to WebSocket only when needed
    const connectWebSocket = useCallback((): Promise<WebSocket> => {
        // Return existing connection if already open
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            return Promise.resolve(wsRef.current);
        }

        // Return existing connection promise if already connecting
        if (connectionPromiseRef.current) {
            return connectionPromiseRef.current;
        }

        // Create new connection
        connectionPromiseRef.current = new Promise((resolve, reject) => {
            const websocket = new WebSocket('ws://localhost:8081/ws');

            websocket.onopen = () => {
                console.log('WebSocket connected');
                setConnected(true);
                wsRef.current = websocket;
                setWs(websocket);
                connectionPromiseRef.current = null;
                resolve(websocket);
            };

            websocket.onmessage = (event) => {
                const message: WebSocketMessage = JSON.parse(event.data);
                handleWebSocketMessage(message);
            };

            websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                setConnected(false);
                connectionPromiseRef.current = null;
                reject(error);
            };

            websocket.onclose = () => {
                console.log('WebSocket disconnected');
                setConnected(false);
                wsRef.current = null;
            };
        });

        return connectionPromiseRef.current;
    }, [handleWebSocketMessage]);

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            ws?.close();
        };
    }, [ws]);

    const addMessage = (type: 'user' | 'assistant', text: string) => {
        const newMessage: Message = {
            id: Date.now().toString(),
            type,
            text,
            timestamp: new Date(),
        };
        setMessages(prev => [...prev, newMessage]);
    };

    const updateLastAssistantMessage = (text: string) => {
        setMessages(prev => {
            const newMessages = [...prev];

            // Try to find the current assistant message being accumulated
            if (currentAssistantMessageIdRef.current) {
                const messageIndex = newMessages.findIndex(
                    msg => msg.id === currentAssistantMessageIdRef.current
                );

                if (messageIndex !== -1) {
                    // Accumulate text to the existing message
                    newMessages[messageIndex] = {
                        ...newMessages[messageIndex],
                        text: newMessages[messageIndex].text + text,
                    };
                    return newMessages;
                }
            }

            // No current message, create a new one
            const newMessageId = Date.now().toString();
            currentAssistantMessageIdRef.current = newMessageId;

            newMessages.push({
                id: newMessageId,
                type: 'assistant',
                text,
                timestamp: new Date(),
            });

            return newMessages;
        });
    };

    const updateLastUserMessage = (text: string) => {
        setMessages(prev => {
            const newMessages = [...prev];

            if (currentUserMessageIdRef.current) {
                const idx = newMessages.findIndex(m => m.id === currentUserMessageIdRef.current);
                if (idx !== -1) {
                    newMessages[idx] = {
                        ...newMessages[idx],
                        text: newMessages[idx].text + text,
                    };
                    return newMessages;
                }
            }

            const newId = Date.now().toString();
            currentUserMessageIdRef.current = newId;
            newMessages.push({
                id: newId,
                type: 'user',
                text,
                timestamp: new Date(),
            });
            return newMessages;
        });
    };

    const handleToolCall = (toolCallData: any) => {
        if (toolCallData.functionCalls) {
            toolCallData.functionCalls.forEach((fc: any) => {
                setToolCalls(prev =>
                    prev.map(tool =>
                        tool.id === fc.name
                            ? { ...tool, status: 'running', timestamp: new Date(), args: fc.args }
                            : tool
                    )
                );

                // Mark as completed after 2 seconds (simulated)
                setTimeout(() => {
                    setToolCalls(prev =>
                        prev.map(tool =>
                            tool.id === fc.name ? { ...tool, status: 'completed' } : tool
                        )
                    );

                    // Reset to idle after 3 more seconds
                    setTimeout(() => {
                        setToolCalls(prev =>
                            prev.map(tool =>
                                tool.id === fc.name ? { ...tool, status: 'idle' } : tool
                            )
                        );
                    }, 3000);
                }, 2000);
            });
        }
    };

    const playAudioChunkImmediately = async (base64Audio: string) => {
        try {
            // Decode base64 to PCM data
            const binaryString = atob(base64Audio);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }

            // Convert PCM16 to Float32
            const pcm16 = new Int16Array(bytes.buffer);
            const float32 = new Float32Array(pcm16.length);
            for (let i = 0; i < pcm16.length; i++) {
                float32[i] = pcm16[i] / 32768.0;
            }

            // Add to queue
            audioQueueRef.current.push(float32);

            // Start playback if not already playing
            if (!isPlayingRef.current) {
                playNextChunk();
            }
        } catch (error) {
            console.error('Error processing audio chunk:', error);
        }
    };

    const playNextChunk = async () => {
        if (audioQueueRef.current.length === 0) {
            isPlayingRef.current = false;
            return;
        }

        isPlayingRef.current = true;

        try {
            // Ensure audio context exists
            if (!audioContextRef.current) {
                audioContextRef.current = new AudioContext({ sampleRate: 24000 });
            }

            const audioContext = audioContextRef.current;

            // Resume audio context if suspended (browser autoplay policy)
            if (audioContext.state === 'suspended') {
                await audioContext.resume();
            }

            // Get next chunk
            const chunk = audioQueueRef.current.shift();
            if (!chunk) {
                isPlayingRef.current = false;
                return;
            }

            // Create audio buffer for this chunk
            const audioBuffer = audioContext.createBuffer(1, chunk.length, 24000);
            audioBuffer.copyToChannel(new Float32Array(chunk), 0);

            // Create source and schedule playback
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);

            // Calculate when to start this chunk
            const currentTime = audioContext.currentTime;
            if (nextStartTimeRef.current < currentTime) {
                nextStartTimeRef.current = currentTime;
            }

            source.start(nextStartTimeRef.current);

            // Update next start time
            nextStartTimeRef.current += audioBuffer.duration;

            // Play next chunk when this one finishes
            source.onended = () => {
                playNextChunk();
            };
        } catch (error) {
            console.error('Error playing audio chunk:', error);
            isPlayingRef.current = false;
            playNextChunk(); // Try next chunk
        }
    };

    const stopAllAudio = () => {
        try {
            // Clear queue
            audioQueueRef.current = [];
            isPlayingRef.current = false;

            // Reset timing
            if (audioContextRef.current) {
                nextStartTimeRef.current = audioContextRef.current.currentTime;
            }
        } catch (error) {
            // Ignore errors when stopping
        }
    };

    const startRecording = async () => {
        try {
            // Ensure WebSocket is connected
            await connectWebSocket();

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaStreamRef.current = stream;
            const audioContext = new AudioContext({ sampleRate: 16000 });
            recordingContextRef.current = audioContext;

            const source = audioContext.createMediaStreamSource(stream);
            const processor = audioContext.createScriptProcessor(4096, 1, 1);

            source.connect(processor);
            processor.connect(audioContext.destination);

            processor.onaudioprocess = (e) => {
                if (!isRecordingRef.current || !wsRef.current) return;

                const inputData = e.inputBuffer.getChannelData(0);

                // Convert Float32 to PCM16
                const pcm16 = new Int16Array(inputData.length);
                for (let i = 0; i < inputData.length; i++) {
                    const s = Math.max(-1, Math.min(1, inputData[i]));
                    pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
                }

                // Convert to base64
                const bytes = new Uint8Array(pcm16.buffer);
                const base64 = btoa(String.fromCharCode(...bytes));

                // Send to WebSocket - Live API will handle VAD automatically
                wsRef.current.send(JSON.stringify({
                    type: 'audio',
                    data: base64,
                }));
            };

            setIsRecording(true);
            isRecordingRef.current = true;
        } catch (error) {
            console.error('Error starting recording:', error);
        }
    };

    const stopRecording = () => {
        setIsRecording(false);
        isRecordingRef.current = false;

        if (recordingContextRef.current) {
            recordingContextRef.current.close();
            recordingContextRef.current = null;
        }

        if (mediaStreamRef.current) {
            mediaStreamRef.current.getTracks().forEach(t => t.stop());
            mediaStreamRef.current = null;
        }

        // Signal end of audio stream
        if (wsRef.current) {
            wsRef.current.send(JSON.stringify({ type: 'audio_end' }));
        }
    };

    const sendTextMessage = async () => {
        if (!textInput.trim()) return;

        const messageText = textInput;
        addMessage('user', messageText);
        setTextInput('');

        // Reset current assistant message for next response
        currentAssistantMessageIdRef.current = null;

        try {
            // Ensure WebSocket is connected
            const websocket = await connectWebSocket();

            // Send the message
            websocket.send(JSON.stringify({
                type: 'text',
                text: messageText,
            }));
        } catch (error) {
            console.error('Failed to send message:', error);
        }
    };

    return (
        <div className="app">
            {/* Main Content */}
            <div className="main-container">
                <div className="conversation-panel">
                    <div className="messages-container">
                        {messages.length === 0 ? (
                            <div className="empty-state">
                                <h2>How can I help you today?</h2>
                                <p>Ask about room availability, make a reservation, or request hotel services</p>
                            </div>
                        ) : (
                            messages.map((message) => (
                                <div key={message.id} className={`message ${message.type}`}>
                                    <div>
                                        <div className={`message-avatar ${message.type}`}>
                                            {message.type === 'user' ? 'U' : 'H'}
                                        </div>
                                        <div className="message-content">
                                            <div className="message-text">{message.text}</div>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                        {isSpeaking && !currentAssistantMessageIdRef.current && (
                            <div className="message assistant">
                                <div>
                                    <div className="message-avatar assistant">H</div>
                                    <div className="message-content">
                                        <div className="typing-indicator">
                                            <span></span>
                                            <span></span>
                                            <span></span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Area */}
                    <div className="input-area">
                        <div className="input-wrapper">
                            <button
                                className={`record-button ${isRecording ? 'recording' : ''}`}
                                onMouseDown={startRecording}
                                onMouseUp={stopRecording}
                                onMouseLeave={isRecording ? stopRecording : undefined}
                                onTouchStart={startRecording}
                                onTouchEnd={stopRecording}
                                title="Hold to speak"
                            >
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
                                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                                    <line x1="12" y1="19" x2="12" y2="22"></line>
                                </svg>
                            </button>

                            <textarea
                                className="text-input"
                                placeholder="Message Hotel Agent..."
                                value={textInput}
                                onChange={(e) => setTextInput(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' && !e.shiftKey) {
                                        e.preventDefault();
                                        sendTextMessage();
                                    }
                                }}
                                rows={1}
                            />

                            <button
                                className="send-button"
                                onClick={sendTextMessage}
                                disabled={!textInput.trim()}
                            >
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <line x1="22" y1="2" x2="11" y2="13"></line>
                                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>

                {/* Tool Activity Panel */}
                <div className="tool-panel">
                    <div className="tool-panel-header">
                        <h3>Function Calls</h3>
                        <div className="status-indicator">
                            <div className={`status-dot ${connected ? 'connected' : 'disconnected'}`} />
                            <span>{connected ? 'Connected' : 'Disconnected'}</span>
                        </div>
                    </div>
                    <div className="tool-list">
                        {TOOL_DEFINITIONS.map((toolDef) => {
                            const toolState = toolCalls.find(t => t.id === toolDef.id);
                            const status = toolState?.status || 'idle';

                            return (
                                <div key={toolDef.id} className={`tool-card ${status}`}>
                                    <div
                                        className="tool-icon"
                                        style={{ backgroundColor: toolDef.color }}
                                    >
                                        {toolDef.icon}
                                    </div>
                                    <div className="tool-info">
                                        <div className="tool-name">{toolDef.name}</div>
                                        <div className="tool-description">{toolDef.description}</div>
                                    </div>
                                    <div className="tool-status">
                                        {status === 'running' && <div className="spinner"></div>}
                                        {status === 'completed' && <div className="checkmark">✓</div>}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;

