// POST /api/skills/execute - Start skill execution
// Returns execution ID immediately, client connects to SSE stream for progress

import { NextRequest, NextResponse } from "next/server";
import { skillExecutor } from "@/lib/claude-cli";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { skill, params } = body;

    // Validate request
    if (!skill || typeof skill !== "string") {
      return NextResponse.json(
        { error: "Missing or invalid 'skill' parameter" },
        { status: 400 }
      );
    }

    if (!params || typeof params !== "object") {
      return NextResponse.json(
        { error: "Missing or invalid 'params' parameter" },
        { status: 400 }
      );
    }

    // Start execution (non-blocking)
    const handle = skillExecutor.execute(skill, params);

    console.log(`[Execute API] Created execution ${handle.id} for skill: ${skill}`);

    return NextResponse.json({
      executionId: handle.id,
      status: handle.status,
      skill: handle.skill,
      startedAt: handle.startedAt,
    });
  } catch (error) {
    console.error("Error starting skill execution:", error);
    return NextResponse.json(
      { error: "Failed to start skill execution" },
      { status: 500 }
    );
  }
}
