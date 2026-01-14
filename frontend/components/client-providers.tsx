'use client';

import { NextIntlClientProvider } from 'next-intl';
import { ThemeProvider } from '@/components/ui/theme-provider';
import { useEffect, useState } from 'react';

export default function ClientProviders({
  children,
  locale,
  messages,
}: Readonly<{
  children: React.ReactNode;
  locale: string;
  messages: any;
}>) {
  const [mounted, setMounted] = useState(false);

  const timeZone = 'Europe/Ljubljana';

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <NextIntlClientProvider locale={locale} messages={messages} timeZone={timeZone}>
        {children}
      </NextIntlClientProvider>
    );
  }

  return (
    <ThemeProvider
      attribute='class'
      defaultTheme='system'
      enableSystem
      disableTransitionOnChange
      enableColorScheme={false}
    >
      <NextIntlClientProvider locale={locale} messages={messages} timeZone={timeZone}>
        {children}
      </NextIntlClientProvider>
    </ThemeProvider>
  );
}
