import type { Metadata } from "next";
import Script from "next/script";
import "./bootstrap.css"; // Import the compiled Bootstrap CSS
import "bootstrap-icons/font/bootstrap-icons.min.css";
import BackToTopBtn from "./home/globals/BackToTopBtn";

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
      <body>
        {children}
        <BackToTopBtn />
      </body>
      <Script src="/bootstrap.bundle.min.js" />
    </html>
  );
}
