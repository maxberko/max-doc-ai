/** @type {import('next').NextConfig} */
const nextConfig = {
  // Tell Next.js not to bundle native modules like node-pty
  serverExternalPackages: ['node-pty'],

  // Ensure we can read files from parent directory (for config.yaml, output/, etc.)
  webpack: (config) => {
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
    };
    return config;
  },
};

module.exports = nextConfig;
