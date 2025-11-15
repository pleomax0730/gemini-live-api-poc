import { useState, useEffect, useRef, useCallback } from 'react';
import './App.css';
import { Message, ToolCall, WebSocketMessage, ActivityLog, TOOL_DEFINITIONS } from './types';
import { useAudioRecording } from './hooks/useAudioRecording';
import { useAudioPlayback } from './hooks/useAudioPlayback';
import { useWebSocketConnection } from './hooks/useWebSocketConnection';

function App() {
    // UI State
    const [messages, setMessages] = useState<Message[]>([]);
    const [textInput, setTextInput] = useState('');
    const [toolCalls, setToolCalls] = useState<ToolCall[]>(
        TOOL_DEFINITIONS.map(tool => ({
            id: tool.id,
            name: tool.name,
            status: 'idle' as const,
        }))
    );
    const [activityLogs, setActivityLogs] = useState<ActivityLog[]>([]);
    const [expandedLogIds, setExpandedLogIds] = useState<Set<string>>(new Set());

    // Refs
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const functionCallStartTimes = useRef<Map<string, number>>(new Map());
    const currentAssistantMessageIdRef = useRef<string | null>(null);
    const currentUserMessageIdRef = useRef<string | null>(null);

    // WebSocket Message Handler
    const handleWebSocketMessage = useCallback((message: WebSocketMessage) => {
        console.log('Received message:', message);

        switch (message.type) {
            case 'session_ready':
                console.log('Session ready');
                break;

            case 'audio_response':
                playAudioChunk(message.data as string);
                break;

            case 'input_transcription':
                if (message.text) {
                    updateLastUserMessage(message.text || '');
                }
                break;

            case 'output_transcription':
            case 'text_response':
                if (message.text) {
                    updateLastAssistantMessage(message.text || '');
                }
                break;

            case 'tool_call':
                handleToolCall(message.data as any);
                break;

            case 'turn_complete':
                currentAssistantMessageIdRef.current = null;
                currentUserMessageIdRef.current = null;
                break;

            case 'interrupted':
                stopAudio();
                break;

            case 'error':
                console.error('Error from server:', message.data);
                break;
        }
    }, []);

    // Custom Hooks
    const { connected, connect, sendMessage } = useWebSocketConnection({
        url: 'ws://localhost:8081/ws',
        onMessage: handleWebSocketMessage,
    });

    const { isRecording, toggleRecording } = useAudioRecording({
        onAudioData: async (base64Audio) => {
            await connect();
            sendMessage({ type: 'audio', data: base64Audio });
        },
    });

    const { isSpeaking, playAudioChunk, stopAudio } = useAudioPlayback();

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Message Management
    const updateLastAssistantMessage = (text: string) => {
        setMessages(prev => {
            const newMessages = [...prev];

            if (currentAssistantMessageIdRef.current) {
                const messageIndex = newMessages.findIndex(
                    msg => msg.id === currentAssistantMessageIdRef.current
                );

                if (messageIndex !== -1) {
                    newMessages[messageIndex] = {
                        ...newMessages[messageIndex],
                        text: newMessages[messageIndex].text + text,
                    };
                    return newMessages;
                }
            }

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

    const addMessage = (type: 'user' | 'assistant', text: string) => {
        const newMessage: Message = {
            id: Date.now().toString(),
            type,
            text,
            timestamp: new Date(),
        };
        setMessages(prev => [...prev, newMessage]);
    };

    // Tool Call Management
    const handleToolCall = (toolCallData: any) => {
        if (toolCallData.functionCalls) {
            toolCallData.functionCalls.forEach((fc: any) => {
                const logId = `${fc.name}-${Date.now()}`;
                const startTime = Date.now();
                functionCallStartTimes.current.set(logId, startTime);

                const activityLog: ActivityLog = {
                    id: logId,
                    type: 'function_call',
                    timestamp: new Date(),
                    status: 'executing',
                    functionName: fc.name,
                    args: fc.args,
                };
                setActivityLogs(prev => [activityLog, ...prev]);

                setToolCalls(prev =>
                    prev.map(tool =>
                        tool.id === fc.name
                            ? { ...tool, status: 'running', timestamp: new Date(), args: fc.args }
                            : tool
                    )
                );

                setTimeout(() => {
                    const executionTime = Date.now() - startTime;

                    setActivityLogs(prev =>
                        prev.map(log =>
                            log.id === logId
                                ? { ...log, status: 'complete', executionTime, result: { success: true } }
                                : log
                        )
                    );

                    setToolCalls(prev =>
                        prev.map(tool =>
                            tool.id === fc.name ? { ...tool, status: 'completed' } : tool
                        )
                    );

                    functionCallStartTimes.current.delete(logId);

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

    // Text Message Handling
    const sendTextMessage = async () => {
        if (!textInput.trim()) return;

        const messageText = textInput;
        addMessage('user', messageText);
        setTextInput('');

        currentAssistantMessageIdRef.current = null;

        try {
            await connect();
            sendMessage({ type: 'text', text: messageText });
        } catch (error) {
            console.error('Failed to send message:', error);
        }
    };

    // Recording Control
    const handleRecordingToggle = async () => {
        if (!isRecording) {
            await connect();
        } else {
            sendMessage({ type: 'audio_end' });
        }
        toggleRecording();
    };

    // Helper Functions
    const toggleExpandLog = (logId: string) => {
        setExpandedLogIds(prev => {
            const newSet = new Set(prev);
            if (newSet.has(logId)) {
                newSet.delete(logId);
            } else {
                newSet.add(logId);
            }
            return newSet;
        });
    };

    const clearActivityLogs = () => {
        setActivityLogs([]);
    };

    const formatJson = (data: unknown): string => {
        try {
            return JSON.stringify(data, null, 2);
        } catch {
            return String(data);
        }
    };

    const formatTime = (date: Date): string => {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const seconds = date.getSeconds().toString().padStart(2, '0');
        const ms = date.getMilliseconds().toString().padStart(3, '0');
        return `${hours}:${minutes}:${seconds}.${ms}`;
    };

    return (
        <div className="app">
            {/* Main Content */}
            <div className="main-container">
                {/* Activity Panel */}
                <div className="activity-panel">
                    <div className="activity-header">
                        <h3>Function Activity</h3>
                        <div className="activity-header-actions">
                            <span className="activity-count">{activityLogs.length} calls</span>
                            <button className="clear-button" onClick={clearActivityLogs}>
                                Clear
                            </button>
                        </div>
                    </div>
                    <div className="activity-list">
                        {activityLogs.length === 0 ? (
                            <div className="empty-logs">No function calls yet</div>
                        ) : (
                            activityLogs.map((log) => (
                                <div key={log.id} className={`activity-log-item ${log.status}`}>
                                    <div className="log-header">
                                        <span className={`status-badge ${log.status}`}>
                                            {log.status === 'executing' && '⟳'}
                                            {log.status === 'complete' && '✓'}
                                            {log.status === 'error' && '✗'}
                                            {log.status === 'pending' && '○'}
                                            {' '}{log.status}
                                        </span>
                                        {log.executionTime !== undefined && (
                                            <span className="execution-time">{log.executionTime}ms</span>
                                        )}
                                    </div>
                                    <div className="log-function-name">{log.functionName}</div>
                                    <div className="log-timestamp">{formatTime(log.timestamp)}</div>

                                    {log.args && (
                                        <div className="json-section">
                                            <button
                                                className="json-toggle"
                                                onClick={() => toggleExpandLog(`${log.id}-args`)}
                                            >
                                                {expandedLogIds.has(`${log.id}-args`) ? '▼' : '▶'} Args
                                            </button>
                                            {expandedLogIds.has(`${log.id}-args`) && (
                                                <pre className="json-viewer">{formatJson(log.args)}</pre>
                                            )}
                                        </div>
                                    )}

                                    {log.result !== undefined && (
                                        <div className="json-section">
                                            <button
                                                className="json-toggle"
                                                onClick={() => toggleExpandLog(`${log.id}-result`)}
                                            >
                                                {expandedLogIds.has(`${log.id}-result`) ? '▼' : '▶'} Result
                                            </button>
                                            {expandedLogIds.has(`${log.id}-result`) && (
                                                <pre className="json-viewer">{formatJson(log.result)}</pre>
                                            )}
                                        </div>
                                    )}
                                </div>
                            ))
                        )}
                    </div>
                </div>

                {/* Conversation Panel */}
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
                                onClick={handleRecordingToggle}
                                title={isRecording ? "Stop recording" : "Start recording"}
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
