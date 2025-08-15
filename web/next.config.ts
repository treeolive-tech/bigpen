import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
        source: "/",
        destination: "/home",
        permanent: true,
      },
    ];
  },
  sassOptions: {
    includePaths: [path.join(__dirname, "styles")],
    // silenceDeprecations: ["all"],
    quietDeps: true, // Also helps suppress warnings from dependencies
  },
};

export default nextConfig;
