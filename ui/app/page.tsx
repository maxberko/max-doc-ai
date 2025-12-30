import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-steel-azure">
          Welcome to max-doc-ai
        </h1>
        <p className="mt-4 text-lg text-steel-blue">
          Automate your product documentation workflow with AI-powered
          generation, screenshot capture, and knowledge base sync.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Link
          href="/releases/new"
          className="relative rounded-lg border-2 border-steel-blue bg-white px-6 py-5 shadow-md flex flex-col space-y-3 hover:border-harvest-orange hover:shadow-lg transition-all focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-harvest-orange"
        >
          <div className="flex-shrink-0">
            <span className="text-4xl">🚀</span>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-medium text-steel-azure">
              Create New Release
            </h3>
            <p className="text-sm text-steel-blue mt-1">
              Generate documentation, capture screenshots, and publish to your
              knowledge base
            </p>
          </div>
        </Link>

        <Link
          href="/docs"
          className="relative rounded-lg border-2 border-steel-blue bg-white px-6 py-5 shadow-md flex flex-col space-y-3 hover:border-harvest-orange hover:shadow-lg transition-all"
        >
          <div className="flex-shrink-0">
            <span className="text-4xl">📚</span>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-medium text-steel-azure">
              Browse Documentation
            </h3>
            <p className="text-sm text-steel-blue mt-1">
              View generated documentation, screenshots, and announcements
            </p>
          </div>
        </Link>

        <Link
          href="/settings"
          className="relative rounded-lg border-2 border-steel-blue bg-white px-6 py-5 shadow-md flex flex-col space-y-3 hover:border-harvest-orange hover:shadow-lg transition-all"
        >
          <div className="flex-shrink-0">
            <span className="text-4xl">⚙️</span>
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-medium text-steel-azure">
              Settings
            </h3>
            <p className="text-sm text-steel-blue mt-1">
              Configure knowledge base provider, screenshots, and output
              settings
            </p>
          </div>
        </Link>
      </div>

      <div className="bg-white border-2 border-steel-blue rounded-lg p-6 shadow-md">
        <h2 className="text-lg font-medium text-steel-azure mb-2">
          Getting Started
        </h2>
        <ol className="list-decimal list-inside space-y-2 text-steel-blue">
          <li>Configure your knowledge base provider in Settings</li>
          <li>Create your first release with the wizard</li>
          <li>Watch as AI generates comprehensive documentation</li>
          <li>Review and browse your published content</li>
        </ol>
      </div>
    </div>
  );
}
