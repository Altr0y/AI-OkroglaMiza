'use client';

import Image from 'next/image';
import { useTranslations } from 'next-intl';
import { useEffect, useState } from 'react';

import { Landing } from '@/components/landing';
import { Prompt } from '@/components/prompt';
import { createClient } from '@/utils/supabase/client';

export default function Home() {
  const t = useTranslations('Prompt');
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const supabase = createClient();

  useEffect(() => {
    const getUser = async () => {
      const { data, error } = await supabase.auth.getUser();
      setUser(data?.user ?? null);
      setLoading(false);
    };

    getUser();
  }, []);

  return (
    <main className="relative flex flex-1 w-full items-start justify-center">
      {/* Background Image */}
      <Image
        src='/background-light.svg'
        alt='Background'
        fill
        className='object-cover'
        priority
      />
      {/* Background Image - Dark Mode*/}
      <Image
        src='/background-dark.svg'
        alt='Background'
        fill
        className='object-cover hidden dark:block'
        priority
      />
      <div className="relative z-20 flex w-full max-w-7xl flex-col items-center justify-start pt-12 px-8">
        {loading ? (
          <div>{t('loadingUser')} ...</div>
        ) : user ? (
          <Prompt />
        ) : (
          <Landing />
        )}
      </div>
    </main>
  );
}
