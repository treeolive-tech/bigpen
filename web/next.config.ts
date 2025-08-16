import type { NextConfig } from "next";

// Parse the API URL to extract components for remotePatterns
function parseApiURL(url: string) {
  const parsedURL = new URL(url);
  return {
    protocol: parsedURL.protocol.slice(0, -1) as "http" | "https", // Remove trailing ':'
    hostname: parsedURL.hostname,
    port: parsedURL.port || "", // Empty string if no port
    pathname: "/**", // Allow all paths under the API
  };
}

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
  images: {
    remotePatterns: [
      parseApiURL(process.env.API_URL || "http://localhost:8000/api"),
    ],
  },
};

export default nextConfig;
