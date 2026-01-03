'use client';

import Image from 'next/image';
import { useTranslations } from 'next-intl';
import { Suspense } from 'react';

import { Header } from '@/components/ui/header';
import { Footer } from '@/components/ui/footer';

export default function Home() {
  const t = useTranslations('HomePage');

  return (
    <div className='flex min-h-screen flex-col font-sans'>
      <Header />

      <main className='relative flex flex-1 w-full items-start justify-center'>
        {/* Background Image */}
        <Image
          src='/background.png'
          alt='Background'
          fill
          className='object-fit'
          priority
        />
        {/* Background Image - Dark Mode*/}
        <Image
          src='/background-dark.png'
          alt='Background'
          fill
          className='object-fit hidden dark:block'
          priority
        />

        {/* Overlay for better readability */}
        <div className='absolute inset-0 bg-white/0 dark:bg-black/70 z-10'></div>

        {/* Content */}
        <div className='relative z-20 flex w-full max-w-3xl flex-col items-center justify-start pt-12 px-16'>
          <div className='flex flex-col items-center gap-6 text-center'>
            <Suspense fallback={<div>Loading...</div>}>
              <h1 className='text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50'>
                {t('title')}
              </h1>
              <p className='max-w-l text-lg text-zinc-600 dark:text-zinc-400'>
                {t('description2')}
              </p>
            </Suspense>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
