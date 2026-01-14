import { getRequestConfig } from 'next-intl/server';
import { cookies } from 'next/headers';
import { notFound } from 'next/navigation';

const locales = ['en', 'sl'];

export default getRequestConfig(async () => {
  const store = await cookies();
  const locale = store.get('locale')?.value || 'en';

  if (!locales.includes(locale as any)) notFound();

  return {
    locale,
    timeZone: 'Europe/Ljubljana',
    messages: (await import(`../messages/${locale}.json`)).default,
  };
});
