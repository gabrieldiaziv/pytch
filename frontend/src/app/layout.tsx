import "@/styles/globals.css";

import { Kumbh_Sans as FontSans } from "next/font/google";
import { headers } from "next/headers";

import { ThemeProvider } from "@/app/_components/theme-provider";
import { TRPCReactProvider } from "@/trpc/react";
import { Providers } from "./providers";

import { type Metadata } from "next";
import Header from "./_components/header";
import dynamic from "next/dynamic";

// page loading bar
const ProgressBar = dynamic(() => import("@/app/_components/ProgressBar"), {
  ssr: true,
});


export const fontSans = FontSans({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Pytch",
  description: "☁️",
  icons: [{ rel: "icon", url: "/favicon.ico" }],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`min-h-screen bg-background antialiased ${fontSans.className}`}
    >
      <body>
        <ProgressBar />
        <Providers>
          <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
            <Header />
            <TRPCReactProvider headers={headers()}>
              {children}
            </TRPCReactProvider>
          </ThemeProvider>
        </Providers>
      </body>
    </html>
  );
}
