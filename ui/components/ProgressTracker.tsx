"use client";

import { useEffect, useState, useRef } from "react";
import {
  ExecutionStatus,
  SkillProgress,
  SkillExecutionEvent,
} from "@/lib/types";

interface ProgressTrackerProps {
  executionId: string;
  onComplete?: () => void;
}

export default function ProgressTracker({
  executionId,
  onComplete,
}: ProgressTrackerProps) {
  const [status, setStatus] = useState<ExecutionStatus>("pending");
  const [progress, setProgress] = useState<SkillProgress>({
    currentStep: null,
    completedSteps: [],
    filesCreated: [],
    urls: [],
    errors: [],
  });
  const [rawOutput, setRawOutput] = useState<string[]>([]);
  const [showRawOutput, setShowRawOutput] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [errorHint, setErrorHint] = useState<string | null>(null);

  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    // Connect to SSE stream
    const eventSource = new EventSource(
      `/api/skills/stream/${executionId}`
    );
    eventSourceRef.current = eventSource;

    eventSource.onmessage = (event) => {
      try {
        const skillEvent: SkillExecutionEvent = JSON.parse(event.data);
        handleEvent(skillEvent);
      } catch (err) {
        console.error("Failed to parse SSE event:", err);
      }
    };

    eventSource.onerror = (err) => {
      console.error("SSE error:", err);
      eventSource.close();
      if (status !== "complete" && status !== "failed") {
        setError("Connection lost. Please refresh the page.");
      }
    };

    // Cleanup on unmount
    return () => {
      eventSource.close();
    };
  }, [executionId]);

  const handleEvent = (event: SkillExecutionEvent) => {
    switch (event.type) {
      case "skill_started":
        setStatus("running");
        break;

      case "skill_progress":
        // Update progress from parsed data
        setProgress((prev) => ({
          ...prev,
          ...event.data,
        }));
        break;

      case "skill_output":
        // Store raw output
        if (event.data.text) {
          setRawOutput((prev) => [...prev, event.data.text]);
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

  return (
    <div className="space-y-6">
      {/* Status badge */}
      <div className="flex items-center space-x-4">
        <div
          className={`px-4 py-2 rounded-full text-sm font-medium ${
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

        {status === "running" && (
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-harvest-orange"></div>
            <span className="text-sm text-steel-blue">Processing...</span>
          </div>
        )}
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
        <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="animate-pulse w-3 h-3 bg-harvest-orange rounded-full"></div>
            <h3 className="text-lg font-medium text-steel-azure">Current Step</h3>
          </div>
          <p className="text-steel-blue">{progress.currentStep}</p>

          {/* Progress bar */}
          {progress.progressPercent !== undefined && (
            <div className="mt-4">
              <div className="flex justify-between text-sm text-steel-blue mb-1">
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
        <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-6">
          <h3 className="text-lg font-medium text-steel-azure mb-4">
            Completed Steps
          </h3>
          <ul className="space-y-2">
            {progress.completedSteps.map((step, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-green-500 mt-0.5">✓</span>
                <span className="text-steel-blue">{step}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Files created */}
      {progress.filesCreated.length > 0 && (
        <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-6">
          <h3 className="text-lg font-medium text-steel-azure mb-4">
            Files Created
          </h3>
          <ul className="space-y-2">
            {progress.filesCreated.map((file, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-harvest-orange">📄</span>
                <span className="text-steel-blue font-mono text-sm">{file}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* URLs */}
      {progress.urls.length > 0 && (
        <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-6">
          <h3 className="text-lg font-medium text-steel-azure mb-4">
            Generated URLs
          </h3>
          <ul className="space-y-3">
            {progress.urls.map((urlData, index) => (
              <li key={index} className="border-l-4 border-harvest-orange pl-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    {urlData.label && (
                      <div className="text-sm font-medium text-steel-azure mb-1">
                        {urlData.label}
                      </div>
                    )}
                    <a
                      href={urlData.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-steel-blue hover:text-harvest-orange break-all"
                    >
                      {urlData.url}
                    </a>
                  </div>
                  <span className="ml-2 px-2 py-1 text-xs bg-alice-blue text-steel-azure rounded">
                    {urlData.type}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Errors */}
      {progress.errors.length > 0 && (
        <div className="bg-red-50 border-2 border-red-500 rounded-lg p-6">
          <h3 className="text-lg font-medium text-red-900 mb-4">Errors</h3>
          <ul className="space-y-2">
            {progress.errors.map((err, index) => (
              <li key={index} className="text-red-800">
                {err}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Raw output (collapsible) */}
      <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-6">
        <button
          onClick={() => setShowRawOutput(!showRawOutput)}
          className="flex items-center justify-between w-full text-left"
        >
          <h3 className="text-lg font-medium text-steel-azure">Raw Output</h3>
          <span className="text-steel-blue">
            {showRawOutput ? "▼" : "▶"}
          </span>
        </button>

        {showRawOutput && (
          <div className="mt-4 bg-black text-alice-blue p-4 rounded-lg overflow-x-auto">
            <pre className="text-sm font-mono whitespace-pre-wrap">
              {rawOutput.join("")}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
