import Link from 'next/link';
import { useTranslations } from 'next-intl';

import { GoogleButton } from '@/components/ui/google-button';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

export function SignupFormLanding({
  ...props
}: React.ComponentProps<typeof Card>) {
  const t = useTranslations('SignupFormLanding');

  return (
    <div className='flex-1 flex flex-col justify-center gap-6 p-8 bg-[#e8f0f8] dark:bg-card border py-6 shadow-sm rounded-2xl'>
      <div className='bg-white dark:bg-black/20 border rounded-xl p-6 space-y-4'>
        <GoogleButton />

        <div className='flex items-center gap-4'>
          <div className='flex-1 h-px bg-zinc-300 dark:bg-zinc-700'></div>
          <span className='text-sm text-zinc-500'>{t('or')}</span>
          <div className='flex-1 h-px bg-zinc-300 dark:bg-zinc-700'></div>
        </div>

        <Button
          variant='outline'
          className='w-full border py-6 shadow-sm'
          asChild
        >
          <Link href='/signup'>{t('signUpWithEmail')}</Link>
        </Button>
      </div>

      <p className='text-sm text-center text-zinc-600 dark:text-zinc-400'>
        {t('description')}
        <Link
          href='/terms'
          className='text-blue-600 dark:text-blue-400 hover:underline'
        >
          {t('terms')}
        </Link>{' '}
        {t('and')}{' '}
        <Link
          href='/privacy'
          className='text-blue-600 dark:text-blue-400 hover:underline'
        >
          {t('privacyPolicy')}.
        </Link>
      </p>
    </div>
  );
}
