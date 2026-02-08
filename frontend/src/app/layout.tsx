import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { ThemeProvider } from '@/components/theme/ThemeProvider';
import { AuthProvider } from '@/providers/AuthProvider';
import ErrorBoundary from '@/components/ui/ErrorBoundary';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: {
    default: 'Todo App - Productivity for the Future',
    template: '%s | Todo App'
  },
  description: 'A modern, premium todo application built for 2026',
  keywords: ['todo', 'productivity', 'task management', 'modern UI', '2026'],
  authors: [{ name: 'Hackathon Team' }],
  creator: 'Hackathon Team',
  publisher: 'Hackathon Team',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://todo-app-2026.com',
    title: 'Todo App - Productivity for the Future',
    description: 'A modern, premium todo application built for 2026',
    siteName: 'Todo App',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Todo App - Productivity for the Future',
    description: 'A modern, premium todo application built for 2026',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'verification_code_goes_here',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body >
        <ErrorBoundary>
          <AuthProvider>
            <ThemeProvider
              attribute="class"
              defaultTheme="system"
              enableSystem
              disableTransitionOnChange
            >
              {children}
            </ThemeProvider>
          </AuthProvider>
        </ErrorBoundary>
      </body>
    </html>
  );
}