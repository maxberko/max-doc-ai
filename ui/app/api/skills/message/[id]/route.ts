import { NextRequest, NextResponse } from "next/server";
import { skillExecutor } from "@/lib/claude-cli";

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  const { message } = await request.json();

  if (!message || typeof message !== "string") {
    return NextResponse.json({ error: "Message is required" }, { status: 400 });
  }

  const success = skillExecutor.sendMessage(id, message);

  if (!success) {
    return NextResponse.json(
      { error: "Failed to send message. Execution may have ended." },
      { status: 400 }
    );
  }

  return NextResponse.json({ success: true });
}
