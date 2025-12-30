// GET /api/skills/stream/:id - Stream skill execution via SSE
// Server-Sent Events endpoint for real-time progress updates

import { NextRequest } from "next/server";
import { skillExecutor } from "@/lib/claude-cli";

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;

  console.log(`[Stream API] Request for execution ${id}`);
  console.log(`[Stream API] Available executions: ${skillExecutor.getAllExecutionIds().join(', ')}`);

  // Check if execution exists
  const execution = skillExecutor.getExecution(id);
  if (!execution) {
    console.log(`[Stream API] Execution ${id} not found`);
    return new Response("Execution not found", { status: 404 });
  }

  console.log(`[Stream API] Streaming execution ${id}`);

  // Create SSE stream
  const stream = new ReadableStream({
    start(controller) {
      const encoder = new TextEncoder();

      // Send existing events
      const existingEvents = skillExecutor.getExecutionEvents(id);
      for (const event of existingEvents) {
        const data = `data: ${JSON.stringify(event)}\n\n`;
        controller.enqueue(encoder.encode(data));
      }

      // Subscribe to new events
      const unsubscribe = skillExecutor.subscribeToExecution(id, (event) => {
        const data = `data: ${JSON.stringify(event)}\n\n`;
        controller.enqueue(encoder.encode(data));

        // Close stream only on completion (not on recoverable errors)
        if (event.type === "skill_complete") {
          // Wait a bit to ensure client receives final message
          setTimeout(() => {
            unsubscribe();
            controller.close();
          }, 500);
        } else if (event.type === "skill_error" && !event.data.recoverable) {
          // Only close on non-recoverable errors
          setTimeout(() => {
            unsubscribe();
            controller.close();
          }, 500);
        }
      });

      // Handle client disconnect
      request.signal.addEventListener("abort", () => {
        unsubscribe();
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
      "X-Accel-Buffering": "no", // Disable nginx buffering
    },
  });
}
