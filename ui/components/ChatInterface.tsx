"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "assistant" | "user";
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  executionId: string;
  messages: Message[]; // Changed from initialMessages to messages (controlled)
  onNewMessage?: (message: Message) => void;
  disabled?: boolean;
}

export default function ChatInterface({
  executionId,
  messages,
  onNewMessage,
  disabled = false,
}: ChatInterfaceProps) {
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || sending || disabled) return;

    const userMessage: Message = {
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setInput("");
    setSending(true);

    // Notify parent component to add the message
    if (onNewMessage) {
      onNewMessage(userMessage);
    }

    try {
      const response = await fetch(`/api/skills/message/${executionId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input.trim() }),
      });

      if (!response.ok) {
        throw new Error("Failed to send message");
      }
    } catch (error) {
      console.error("Error sending message:", error);
      // Optionally show error to user
    } finally {
      setSending(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages && messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-4 ${
                message.role === "user"
                  ? "bg-steel-azure text-white"
                  : "bg-alice-blue text-steel-blue border-2 border-steel-blue"
              }`}
            >
              <div className="text-sm font-medium mb-1">
                {message.role === "user" ? "You" : "Claude"}
              </div>
              <div className="whitespace-pre-wrap">{message.content}</div>
              <div className="text-xs opacity-70 mt-2">
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t-2 border-steel-blue p-4 bg-white">
        <div className="flex space-x-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={
              disabled
                ? "Execution has completed"
                : "Type your message... (Enter to send)"
            }
            disabled={disabled || sending}
            rows={3}
            className="flex-1 px-3 py-2 border-2 border-steel-blue rounded-lg focus:ring-2 focus:ring-harvest-orange focus:border-harvest-orange resize-none disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
          <button
            onClick={sendMessage}
            disabled={disabled || sending || !input.trim()}
            className="px-6 py-2 bg-harvest-orange text-white rounded-lg hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors self-end"
          >
            {sending ? "Sending..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
