'use client';

import Image from 'next/image';
import { useTranslations } from 'next-intl';
import { Suspense, useEffect, useState } from 'react';

import { SignupFormLanding } from '@/components/signup-form-landing';
import { Demo } from '@/components/demo';
import { createClient } from '@/utils/supabase/client';

export default function Home() {
  const t = useTranslations('HomePage');
  const [user, setUser] = useState<any>(null);
  const supabase = createClient();

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      setUser(user);
    };
    getUser();
  }, [supabase]);

  return (
    <main className='relative flex flex-1 w-full items-start justify-center'>
      {}
      <Image src='/background-light.svg' alt='Background' fill className='object-cover' priority />
      
      <div className='relative z-20 flex w-full max-w-7xl flex-col items-center justify-start pt-12 px-8'>

        <div className='flex flex-col items-center gap-6 text-center mb-8'>
          <Suspense fallback={<div>Loading...</div>}>
            <h1 className='text-3xl font-bold leading-10 tracking-tight text-black dark:text-zinc-50'>
              {t('title')}
            </h1>
            <p className='max-w-l text-lg text-zinc-600 dark:text-zinc-400'>
              {t('description2')}
            </p>
          </Suspense>
        </div>

        {}
        <div className='flex w-full gap-8'>
          {!user && <SignupFormLanding />}
          <Demo />
        </div>
      </div>
    </main>
  );
}