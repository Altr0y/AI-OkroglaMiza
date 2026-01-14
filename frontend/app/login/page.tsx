'use client';

import Image from 'next/image';
import { useTranslations } from 'next-intl';
import { LoginForm } from '@/components/login-form';

export default function LoginPage() {
  const t = useTranslations('LoginPage');

  return (
    <div className="relative flex flex-1 items-center justify-center bg-zinc-50 dark:bg-black p-4 overflow-hidden">
      
      {/* Background Image - Light */}
      <Image
        src="/background-accent-light.svg"
        alt="Background"
        fill
        priority
        className="object-cover z-0 dark:hidden pointer-events-none"
      />

      {/* Background Image - Dark */}
      <Image
        src="/background-accent-dark.svg"
        alt="Background"
        fill
        priority
        className="object-cover z-0 hidden dark:block pointer-events-none"
      />

      {/* Login Form */}
      <LoginForm className="relative z-10 w-full max-w-sm" />
    </div>
  );
}
