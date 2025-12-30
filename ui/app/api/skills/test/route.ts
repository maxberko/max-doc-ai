// Test endpoint to verify execute flow
import { NextResponse } from "next/server";
import { skillExecutor } from "@/lib/claude-cli";

export async function POST() {
  try {
    // Create a test execution
    const handle = skillExecutor.execute("test-skill", {
      test: "data",
    });

    console.log(`[Test API] Created test execution ${handle.id}`);

    return NextResponse.json({
      success: true,
      executionId: handle.id,
      message: "Test execution created successfully",
    });
  } catch (error) {
    console.error("[Test API] Error:", error);
    return NextResponse.json(
      { success: false, error: String(error) },
      { status: 500 }
    );
  }
}

export async function GET() {
  const executionIds = skillExecutor.getAllExecutionIds();

  return NextResponse.json({
    executionCount: executionIds.length,
    executionIds,
    message: executionIds.length > 0
      ? "Executions found"
      : "No executions in memory",
  });
}
