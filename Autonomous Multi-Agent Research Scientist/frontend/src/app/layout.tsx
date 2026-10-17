import type { Metadata } from "next";
import {
  Cabin,
  Fustat,
  IBM_Plex_Mono,
  Instrument_Serif,
  Inter,
  Manrope,
  Noto_Sans,
  Schibsted_Grotesk,
} from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const ibmPlexMono = IBM_Plex_Mono({
  variable: "--font-ibm-plex-mono",
  weight: ["400", "500", "600"],
  subsets: ["latin"],
  display: "swap",
});

const manrope = Manrope({
  variable: "--font-manrope",
  subsets: ["latin"],
  display: "swap",
});

const cabin = Cabin({
  variable: "--font-cabin",
  subsets: ["latin"],
  display: "swap",
});

const instrumentSerif = Instrument_Serif({
  variable: "--font-instrument-serif",
  weight: ["400"],
  subsets: ["latin"],
  display: "swap",
});

const schibstedGrotesk = Schibsted_Grotesk({
  variable: "--font-schibsted-grotesk",
  subsets: ["latin"],
  display: "swap",
});

const notoSans = Noto_Sans({
  variable: "--font-noto-sans",
  subsets: ["latin"],
  display: "swap",
});

const fustat = Fustat({
  variable: "--font-fustat",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "AMRS — Autonomous Multi-Agent Research Scientist",
  description:
    "A multi-agent AI platform that turns a single research question into a complete, evidence-checked deliverable package.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${ibmPlexMono.variable} ${manrope.variable} ${cabin.variable} ${instrumentSerif.variable} ${schibstedGrotesk.variable} ${notoSans.variable} ${fustat.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
