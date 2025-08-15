import type { Metadata } from "next";
import Script from "next/script";
import "./globals.css";


// Metadata
export const metadata: Metadata = {
  title: {
    template: `%s | ${process.env.SITE_NAME || "Djanx"}`,
    default: process.env.SITE_NAME || "Djanx",
  },
  description: process.env.SITE_DESCRIPTION || "",
  // metadataBase: new URL(""),
};

// Root Layout
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
      <Script src="/bootstrap.bundle.min.js" />
    </html>
  );
}
