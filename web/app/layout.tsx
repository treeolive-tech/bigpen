import type { Metadata } from "next";
import Script from "next/script";

export const metadata: Metadata = {
  title: {
    template: `%s | ${process.env.SITE_NAME || "Djanx"}`,
    default: process.env.SITE_NAME || "Djanx",
  },
  description: process.env.SITE_DESCRIPTION || "",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        {/* eslint-disable-next-line @next/next/no-css-tags */}
        <link rel="stylesheet" href="/globals.css" />
      </head>
      <body>{children}</body>
      <Script src="/bootstrap.bundle.min.js" />
    </html>
  );
}
