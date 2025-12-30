// Debug endpoint to see all executions
import { NextResponse } from "next/server";
import { skillExecutor } from "@/lib/claude-cli";

export async function GET() {
  const executionIds = skillExecutor.getAllExecutionIds();

  const executions = executionIds.map((id) => {
    const execution = skillExecutor.getExecution(id);
    return {
      id,
      status: execution?.handle.status,
      skill: execution?.handle.skill,
      startedAt: execution?.handle.startedAt,
    };
  });

  return NextResponse.json({
    count: executionIds.length,
    executions,
    projectRoot: process.cwd(),
  });
}
