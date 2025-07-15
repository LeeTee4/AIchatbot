import type { Route } from "./+types/chat";
import { useState, useRef, useEffect } from "react";
import { Layout } from "../components/Layout";
import { ApiService, type ChatMessage } from "../services/api";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Chat - Lee Electronics AI Assistant" },
    { name: "description", content: "Chat with our AI assistant for instant help" },
  ];
}

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      content: "Hello! I'm Lee Electronics' AI assistant. How can I help you today?",
      isUser: false,
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<"connected" | "disconnected" | "checking">("checking");
  const [backendInfo, setBackendInfo] = useState<any>(null);
  const [connectionError, setConnectionError] = useState<string>("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    checkConnection();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const checkConnection = async () => {
    setConnectionStatus("checking");
    setConnectionError("");
    try {
      const isConnected = await ApiService.testConnection();
      if (isConnected) {
        setConnectionStatus("connected");
        // Get backend status info
        try {
          const statusInfo = await ApiService.getBackendStatus();
          setBackendInfo(statusInfo);
        } catch (e) {
          // Don't fail if we can't get status info
          console.warn("Couldn't get backend status:", e);
        }
      } else {
        setConnectionStatus("disconnected");
        setConnectionError("Backend connection failed. Make sure Django server is running on port 8000.");
      }
    } catch (error) {
      setConnectionStatus("disconnected");
      setConnectionError(`Connection error: ${error instanceof Error ? error.message : 'Unknown error'}`);
      console.error("Connection check failed:", error);
    }
  };

  const testEcho = async () => {
    try {
      const echoResponse = await ApiService.testEcho("Connection test");
      const testMessage: ChatMessage = {
        id: Date.now().toString(),
        content: `🔧 Backend Test: ${echoResponse}`,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, testMessage]);
      setConnectionStatus("connected");
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        content: `❌ Backend Test Failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
      setConnectionStatus("disconnected");
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputValue.trim(),
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await ApiService.sendMessage(userMessage.content);
      
      const botMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: response,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
      setConnectionStatus("connected");
      setConnectionError(""); // Clear any previous errors
    } catch (error) {
      console.error("Send message error:", error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}. Please try again.`,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
      setConnectionStatus("disconnected");
      setConnectionError(error instanceof Error ? error.message : 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 mb-6 p-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">AI Assistant</h1>
              <p className="text-gray-600">Ask me anything about Lee Electronics</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${
                  connectionStatus === "connected" ? "bg-green-500" : 
                  connectionStatus === "disconnected" ? "bg-red-500" : "bg-yellow-500"
                }`}></div>
                <span className="text-sm text-gray-600">
                  {connectionStatus === "connected" ? "Connected" : 
                   connectionStatus === "disconnected" ? "Disconnected" : "Checking..."}
                </span>
              </div>
              {connectionStatus === "disconnected" && (
                <button
                  onClick={checkConnection}
                  className="text-blue-600 text-sm hover:text-blue-800 px-3 py-1 border border-blue-300 rounded"
                >
                  Retry
                </button>
              )}
              
            </div>
          </div>
          
          {/* Connection Error */}
          {connectionError && (
            <div className="mt-4 p-3 bg-red-50 rounded-lg text-sm text-red-700">
              <p><strong>Connection Issue:</strong> {connectionError}</p>
              <p className="mt-1 text-xs">You can still try sending messages - the connection test might be overly strict.</p>
            </div>
          )}
        </div>

        {/* Chat Container */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 flex flex-col h-[600px]">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.isUser ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                    message.isUser
                      ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white"
                      : "bg-gray-100 text-gray-900"
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  <p className={`text-xs mt-2 ${
                    message.isUser ? "text-blue-200" : "text-gray-500"
                  }`}>
                    {formatTime(message.timestamp)}
                  </p>
                </div>
              </div>
            ))}
            
            {/* Loading indicator */}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-2xl px-4 py-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <div className="border-t border-gray-200 p-6">
            <form onSubmit={handleSubmit} className="flex space-x-4">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 border text-black border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputValue.trim()}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-xl font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg transition-all duration-200"
              >
                {isLoading ? (
                  <svg className="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                )}
              </button>
            </form>
            
            {/* Quick Actions */}
            <div className="mt-4 flex flex-wrap gap-2">
              {[
                "What products do you offer?",
                "What's your return policy?",
                "How can I contact support?",
                "Tell me about warranties"
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setInputValue(suggestion)}
                  className="text-sm bg-gray-100 text-gray-700 px-3 py-2 rounded-lg hover:bg-gray-200 transition-colors duration-200"
                  disabled={isLoading}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
