"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ReleaseFormData } from "@/lib/types";

type WizardStep = 1 | 2 | 3 | 4;

interface ReleaseWizardProps {
  onSubmit?: (executionId: string) => void;
}

export default function ReleaseWizard({ onSubmit }: ReleaseWizardProps) {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState<WizardStep>(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form data
  const [formData, setFormData] = useState<ReleaseFormData>({
    feature: "",
    codeSource: "current",
    releaseDate: new Date().toISOString().split("T")[0],
  });

  const updateFormData = (updates: Partial<ReleaseFormData>) => {
    setFormData((prev) => ({ ...prev, ...updates }));
  };

  const handleNext = () => {
    setError(null);

    // Validate current step
    if (currentStep === 1 && !formData.feature.trim()) {
      setError("Please provide a feature description");
      return;
    }

    if (currentStep === 2) {
      if (formData.codeSource === "path" && !formData.repoPath) {
        setError("Please provide a repository path");
        return;
      }
      if (formData.codeSource === "github" && !formData.githubUrl) {
        setError("Please provide a GitHub URL");
        return;
      }
    }

    if (currentStep < 4) {
      setCurrentStep((prev) => (prev + 1) as WizardStep);
    }
  };

  const handleBack = () => {
    setError(null);
    if (currentStep > 1) {
      setCurrentStep((prev) => (prev - 1) as WizardStep);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setError(null);

    try {
      // Call execute API
      const response = await fetch("/api/skills/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          skill: "create-release",
          params: formData,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to start release execution");
      }

      const { executionId } = await response.json();

      // Navigate to progress page or call callback
      if (onSubmit) {
        onSubmit(executionId);
      } else {
        router.push(`/releases/${executionId}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {[1, 2, 3, 4].map((step) => (
            <div key={step} className="flex items-center">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  step <= currentStep
                    ? "bg-steel-azure text-white"
                    : "bg-alice-blue text-steel-blue"
                }`}
              >
                {step}
              </div>
              {step < 4 && (
                <div
                  className={`w-24 h-1 mx-2 ${
                    step < currentStep ? "bg-steel-azure" : "bg-alice-blue"
                  }`}
                />
              )}
            </div>
          ))}
        </div>
        <div className="flex justify-between mt-2">
          <span className="text-sm text-steel-blue">Feature</span>
          <span className="text-sm text-steel-blue">Code</span>
          <span className="text-sm text-steel-blue">Date</span>
          <span className="text-sm text-steel-blue">Review</span>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border-2 border-red-500 rounded-lg text-red-800">
          {error}
        </div>
      )}

      {/* Step content */}
      <div className="bg-white shadow-md border-2 border-steel-blue rounded-lg p-6 mb-6">
        {currentStep === 1 && (
          <div>
            <h2 className="text-2xl font-bold mb-4 text-steel-azure">Feature Description</h2>
            <p className="text-steel-blue mb-4">
              Describe the feature you're releasing. You can paste a PRD, provide a brief description, or just the feature name.
            </p>
            <textarea
              value={formData.feature}
              onChange={(e) => updateFormData({ feature: e.target.value })}
              placeholder="e.g., New dashboard analytics feature with customizable widgets..."
              className="w-full h-48 px-3 py-2 border-2 border-steel-blue rounded-lg focus:ring-2 focus:ring-harvest-orange focus:border-harvest-orange"
            />
          </div>
        )}

        {currentStep === 2 && (
          <div>
            <h2 className="text-2xl font-bold mb-4 text-steel-azure">Code Location</h2>
            <p className="text-steel-blue mb-4">
              Where should we find the code for this feature?
            </p>

            <div className="space-y-4">
              <label className="flex items-start">
                <input
                  type="radio"
                  name="codeSource"
                  value="current"
                  checked={formData.codeSource === "current"}
                  onChange={(e) =>
                    updateFormData({ codeSource: e.target.value as any })
                  }
                  className="mt-1 mr-3 text-steel-azure"
                />
                <div>
                  <div className="font-medium text-steel-azure">Current Codebase</div>
                  <div className="text-sm text-steel-blue">
                    Use the codebase in the current directory
                  </div>
                </div>
              </label>

              <label className="flex items-start">
                <input
                  type="radio"
                  name="codeSource"
                  value="path"
                  checked={formData.codeSource === "path"}
                  onChange={(e) =>
                    updateFormData({ codeSource: e.target.value as any })
                  }
                  className="mt-1 mr-3 text-steel-azure"
                />
                <div className="flex-1">
                  <div className="font-medium text-steel-azure">Custom Path</div>
                  <div className="text-sm text-steel-blue mb-2">
                    Specify a local directory path
                  </div>
                  {formData.codeSource === "path" && (
                    <input
                      type="text"
                      value={formData.repoPath || ""}
                      onChange={(e) =>
                        updateFormData({ repoPath: e.target.value })
                      }
                      placeholder="/path/to/repository"
                      className="w-full px-3 py-2 border-2 border-steel-blue rounded-lg focus:ring-2 focus:ring-harvest-orange focus:border-harvest-orange"
                    />
                  )}
                </div>
              </label>

              <label className="flex items-start">
                <input
                  type="radio"
                  name="codeSource"
                  value="github"
                  checked={formData.codeSource === "github"}
                  onChange={(e) =>
                    updateFormData({ codeSource: e.target.value as any })
                  }
                  className="mt-1 mr-3 text-steel-azure"
                />
                <div className="flex-1">
                  <div className="font-medium text-steel-azure">GitHub URL</div>
                  <div className="text-sm text-steel-blue mb-2">
                    Provide a GitHub repository URL
                  </div>
                  {formData.codeSource === "github" && (
                    <input
                      type="text"
                      value={formData.githubUrl || ""}
                      onChange={(e) =>
                        updateFormData({ githubUrl: e.target.value })
                      }
                      placeholder="https://github.com/user/repo"
                      className="w-full px-3 py-2 border-2 border-steel-blue rounded-lg focus:ring-2 focus:ring-harvest-orange focus:border-harvest-orange"
                    />
                  )}
                </div>
              </label>
            </div>
          </div>
        )}

        {currentStep === 3 && (
          <div>
            <h2 className="text-2xl font-bold mb-4 text-steel-azure">Release Date</h2>
            <p className="text-steel-blue mb-4">
              When is this feature being released?
            </p>
            <input
              type="date"
              value={formData.releaseDate}
              onChange={(e) => updateFormData({ releaseDate: e.target.value })}
              className="px-3 py-2 border-2 border-steel-blue rounded-lg focus:ring-2 focus:ring-harvest-orange focus:border-harvest-orange"
            />
          </div>
        )}

        {currentStep === 4 && (
          <div>
            <h2 className="text-2xl font-bold mb-4 text-steel-azure">Review & Confirm</h2>
            <p className="text-steel-blue mb-6">
              Please review your release details before starting the workflow.
            </p>

            <div className="space-y-4">
              <div>
                <h3 className="font-medium text-steel-azure mb-2">Feature</h3>
                <div className="bg-alice-blue p-3 rounded border-2 border-steel-blue">
                  {formData.feature}
                </div>
              </div>

              <div>
                <h3 className="font-medium text-steel-azure mb-2">Code Source</h3>
                <div className="bg-alice-blue p-3 rounded border-2 border-steel-blue">
                  {formData.codeSource === "current" && "Current codebase"}
                  {formData.codeSource === "path" && formData.repoPath}
                  {formData.codeSource === "github" && formData.githubUrl}
                </div>
              </div>

              <div>
                <h3 className="font-medium text-steel-azure mb-2">Release Date</h3>
                <div className="bg-alice-blue p-3 rounded border-2 border-steel-blue">
                  {formData.releaseDate}
                </div>
              </div>
            </div>

            <div className="mt-6 p-4 bg-white border-2 border-harvest-orange rounded-lg">
              <p className="text-sm text-steel-azure">
                This will start the complete release workflow including:
                researching the codebase, capturing screenshots, generating
                documentation, syncing to knowledge base, and creating
                announcements.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Navigation buttons */}
      <div className="flex justify-between">
        <button
          onClick={handleBack}
          disabled={currentStep === 1 || isSubmitting}
          className="px-6 py-2 border-2 border-steel-blue rounded-lg text-steel-azure hover:bg-alice-blue disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Back
        </button>

        {currentStep < 4 ? (
          <button
            onClick={handleNext}
            className="px-6 py-2 bg-steel-azure text-white rounded-lg hover:bg-steel-blue transition-colors"
          >
            Next
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="px-6 py-2 bg-harvest-orange text-white rounded-lg hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isSubmitting ? "Starting..." : "Start Release"}
          </button>
        )}
      </div>
    </div>
  );
}
