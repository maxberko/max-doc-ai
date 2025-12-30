import ReleaseWizard from "@/components/ReleaseWizard";

export default function NewReleasePage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-steel-azure">
          Create New Release
        </h1>
        <p className="mt-2 text-steel-blue">
          Follow the wizard to generate comprehensive documentation for your feature release
        </p>
      </div>

      <ReleaseWizard />
    </div>
  );
}
