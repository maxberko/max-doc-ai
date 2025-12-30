"use client";

import { useEffect, useState, useRef } from "react";
import {
  ExecutionStatus,
  SkillProgress,
  SkillExecutionEvent,
} from "@/lib/types";
import ChatInterface from "./ChatInterface";

interface Message {
  role: "assistant" | "user";
  content: string;
  timestamp: Date;
}

interface ReleaseChatProps {
  executionId: string;
  onComplete?: () => void;
}

export default function ReleaseChat({
  executionId,
  onComplete,
}: ReleaseChatProps) {
  const [status, setStatus] = useState<ExecutionStatus>("pending");
  const [progress, setProgress] = useState<SkillProgress>({
    currentStep: null,
    completedSteps: [],
    filesCreated: [],
    urls: [],
    errors: [],
  });
  const [messages, setMessages] = useState<Message[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [errorHint, setErrorHint] = useState<string | null>(null);

  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    console.log(`[ReleaseChat] Connecting to SSE stream for execution ${executionId}`);

    // Connect to SSE stream
    const eventSource = new EventSource(
      `/api/skills/stream/${executionId}`
    );
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      console.log(`[ReleaseChat] SSE connection opened`);
    };

    eventSource.onmessage = (event) => {
      console.log(`[ReleaseChat] SSE message received:`, event.data.substring(0, 100));
      try {
        const skillEvent: SkillExecutionEvent = JSON.parse(event.data);
        handleEvent(skillEvent);
      } catch (err) {
        console.error("Failed to parse SSE event:", err, event.data);
      }
    };

    eventSource.onerror = (err) => {
      console.error("SSE error:", err);
      console.log(`[ReleaseChat] SSE readyState:`, eventSource.readyState);
      eventSource.close();
      if (status !== "complete" && status !== "failed") {
        setError("Connection lost. Please refresh the page.");
      }
    };

    // Cleanup on unmount
    return () => {
      console.log(`[ReleaseChat] Closing SSE connection`);
      eventSource.close();
    };
  }, [executionId]);

  const handleEvent = (event: SkillExecutionEvent) => {
    console.log(`[ReleaseChat] Received event:`, event.type, event.data);

    switch (event.type) {
      case "skill_started":
        console.log(`[ReleaseChat] Setting status to running`);
        setStatus("running");
        break;

      case "skill_progress":
        console.log(`[ReleaseChat] Updating progress`);
        // Update progress from parsed data
        setProgress((prev) => ({
          ...prev,
          ...event.data,
        }));
        break;

      case "skill_output":
        console.log(`[ReleaseChat] Adding message:`, event.data.text?.substring(0, 100));
        // Store output as messages from Claude
        if (event.data.text) {
          const newMessage: Message = {
            role: "assistant",
            content: event.data.text,
            timestamp: new Date(),
          };
          setMessages((prev) => {
            console.log(`[ReleaseChat] Messages before:`, prev.length, `after:`, prev.length + 1);
            return [...prev, newMessage];
          });
        }
        // Update progress from parsed data
        if (event.data.parsed) {
          setProgress((prev) => ({
            currentStep: event.data.parsed.currentStep ?? prev.currentStep,
            completedSteps: [
              ...prev.completedSteps,
              ...(event.data.parsed.completedSteps || []),
            ].filter((v, i, a) => a.indexOf(v) === i), // unique
            filesCreated: [
              ...prev.filesCreated,
              ...(event.data.parsed.filesCreated || []),
            ].filter((v, i, a) => a.indexOf(v) === i),
            urls: [
              ...prev.urls,
              ...(event.data.parsed.urls || []),
            ],
            errors: [
              ...prev.errors,
              ...(event.data.parsed.errors || []),
            ],
            progressPercent:
              event.data.parsed.progressPercent ?? prev.progressPercent,
          }));
        }
        break;

      case "skill_complete":
        setStatus("complete");
        if (onComplete) {
          onComplete();
        }
        break;

      case "skill_error":
        setStatus("failed");
        setError(event.data.error || "Execution failed");
        setErrorHint(event.data.hint || null);
        break;
    }
  };

  const handleNewUserMessage = (message: Message) => {
    // Add user message to state
    setMessages((prev) => [...prev, message]);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-12rem)]">
      {/* Chat Interface - Takes 2/3 on large screens */}
      <div className="lg:col-span-2 bg-white shadow-md border-2 border-steel-blue rounded-lg overflow-hidden">
        <div className="p-4 bg-steel-azure text-white border-b-2 border-steel-blue">
          <h2 className="text-xl font-bold">Conversation</h2>
          <p className="text-sm opacity-90">
            Chat with Claude to complete the release
          </p>
        </div>
        <div className="h-[calc(100%-5rem)]">
          <ChatInterface
            executionId={executionId}
            messages={messages}
            onNewMessage={handleNewUserMessage}
            disabled={status === "complete" || status === "failed"}
          />
        </div>
      </div>

      {/* Progress Panel - Takes 1/3 on large screens */}
      <div className="space-y-4 overflow-y-auto">
        {/* Status badge */}
        <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-4">
          <h3 className="text-lg font-medium text-steel-azure mb-3">Status</h3>
          <div
            className={`px-4 py-2 rounded-full text-sm font-medium text-center ${
              status === "pending"
                ? "bg-alice-blue text-steel-azure"
                : status === "running"
                ? "bg-steel-blue text-white"
                : status === "complete"
                ? "bg-green-100 text-green-800"
                : "bg-red-100 text-red-800"
            }`}
          >
            {status === "pending" && "Pending"}
            {status === "running" && "Running"}
            {status === "complete" && "Complete"}
            {status === "failed" && "Failed"}
            {status === "cancelled" && "Cancelled"}
          </div>
        </div>

        {/* Error message */}
        {error && (
          <div className="p-4 bg-red-50 border-2 border-red-500 rounded-lg">
            <div className="text-red-800 font-medium mb-2">{error}</div>
            {errorHint && (
              <div className="text-red-700 text-sm mt-2 p-3 bg-red-100 rounded border border-red-300">
                <strong>How to fix:</strong> {errorHint}
              </div>
            )}
          </div>
        )}

        {/* Current step */}
        {progress.currentStep && (
          <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-4">
            <div className="flex items-center space-x-3 mb-3">
              <div className="animate-pulse w-3 h-3 bg-harvest-orange rounded-full"></div>
              <h3 className="text-lg font-medium text-steel-azure">
                Current Step
              </h3>
            </div>
            <p className="text-steel-blue text-sm">{progress.currentStep}</p>

            {/* Progress bar */}
            {progress.progressPercent !== undefined && (
              <div className="mt-3">
                <div className="flex justify-between text-xs text-steel-blue mb-1">
                  <span>Progress</span>
                  <span>{progress.progressPercent}%</span>
                </div>
                <div className="w-full bg-alice-blue rounded-full h-2">
                  <div
                    className="bg-harvest-orange h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress.progressPercent}%` }}
                  ></div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Completed steps */}
        {progress.completedSteps.length > 0 && (
          <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-4">
            <h3 className="text-lg font-medium text-steel-azure mb-3">
              Completed Steps
            </h3>
            <ul className="space-y-2">
              {progress.completedSteps.map((step, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span className="text-steel-blue text-sm">{step}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Files created */}
        {progress.filesCreated.length > 0 && (
          <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-4">
            <h3 className="text-lg font-medium text-steel-azure mb-3">
              Files Created
            </h3>
            <ul className="space-y-2">
              {progress.filesCreated.map((file, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <span className="text-harvest-orange">📄</span>
                  <span className="text-steel-blue font-mono text-xs break-all">
                    {file}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* URLs */}
        {progress.urls.length > 0 && (
          <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-4">
            <h3 className="text-lg font-medium text-steel-azure mb-3">
              Generated URLs
            </h3>
            <ul className="space-y-3">
              {progress.urls.map((urlData, index) => (
                <li key={index} className="border-l-4 border-harvest-orange pl-3">
                  {urlData.label && (
                    <div className="text-xs font-medium text-steel-azure mb-1">
                      {urlData.label}
                    </div>
                  )}
                  <a
                    href={urlData.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-steel-blue hover:text-harvest-orange break-all"
                  >
                    {urlData.url}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Errors */}
        {progress.errors.length > 0 && (
          <div className="bg-red-50 border-2 border-red-500 rounded-lg p-4">
            <h3 className="text-lg font-medium text-red-900 mb-3">Errors</h3>
            <ul className="space-y-2">
              {progress.errors.map((err, index) => (
                <li key={index} className="text-red-800 text-sm">
                  {err}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
