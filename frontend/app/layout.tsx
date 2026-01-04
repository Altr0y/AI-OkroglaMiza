import type { Metadata } from 'next';
import localFont from 'next/font/local';
import { Geist_Mono } from 'next/font/google';
import { cookies } from 'next/headers';
import { getMessages } from 'next-intl/server';
import './globals.css';
import ClientProviders from '@/components/client-providers';
import { Header } from '@/components/ui/header';
import { Footer } from '@/components/ui/footer';

const comfortaa = localFont({
  src: '../public/fonts/Comfortaa-VariableFont_wght.ttf',
  variable: '--font-comfortaa',
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'AI Roundtable',
  description: 'Next.js application for AI Roundtable',
};

export default async function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  const cookieStore = await cookies();
  const locale = cookieStore.get('locale')?.value || 'en';
  const messages = await getMessages({ locale });

  return (
    <html lang={locale} suppressHydrationWarning>
      <head />
      <body
        className={`${comfortaa.variable} ${geistMono.variable} antialiased`}
      >
        <ClientProviders locale={locale} messages={messages}>
          <Header />
          <div className='flex min-h-screen flex-col font-sans'>{children}</div>
          <Footer />
        </ClientProviders>
      </body>
    </html>
  );
}
