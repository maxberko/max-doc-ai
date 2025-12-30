"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import ReleaseChat from "@/components/ReleaseChat";

export default function ReleasePage() {
  const params = useParams();
  const executionId = params.id as string;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-steel-azure">
            Release Workflow
          </h1>
          <p className="mt-2 text-steel-blue">
            Execution ID: <span className="font-mono text-sm">{executionId}</span>
          </p>
        </div>

        <Link
          href="/releases/new"
          className="px-4 py-2 border-2 border-steel-blue rounded-lg text-steel-azure hover:bg-alice-blue transition-colors"
        >
          Create New Release
        </Link>
      </div>

      <ReleaseChat executionId={executionId} />
    </div>
  );
}
