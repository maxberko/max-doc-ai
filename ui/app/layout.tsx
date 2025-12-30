import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "max-doc-ai",
  description: "Visual documentation generation and knowledge base management",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-alice-blue">
        <nav className="border-b border-steel-blue bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-steel-azure">max-doc-ai</h1>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <a
                    href="/"
                    className="border-transparent text-steel-blue hover:border-steel-azure hover:text-steel-azure inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Home
                  </a>
                  <a
                    href="/releases/new"
                    className="border-transparent text-steel-blue hover:border-steel-azure hover:text-steel-azure inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    New Release
                  </a>
                  <a
                    href="/docs"
                    className="border-transparent text-steel-blue hover:border-steel-azure hover:text-steel-azure inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Documentation
                  </a>
                  <a
                    href="/settings"
                    className="border-transparent text-steel-blue hover:border-steel-azure hover:text-steel-azure inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Settings
                  </a>
                </div>
              </div>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
