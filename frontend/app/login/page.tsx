'use client';

import { useTranslations } from 'next-intl';

import { LoginForm } from '@/components/login-form';

export default function LoginPage() {
  const t = useTranslations('LoginPage');

  return (
    <div className='flex flex-1 items-center justify-center bg-zinc-50 dark:bg-black p-4'>
      <LoginForm className='w-full max-w-sm' />
    </div>
  );
}
