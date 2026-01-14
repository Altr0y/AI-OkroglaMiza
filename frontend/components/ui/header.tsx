'use client';

import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { useTranslations } from 'next-intl';
import SettingsButton from "@/components/ui/settings-button";
import Image from 'next/image';
import { ModeToggle } from '@/components/mode-toggle';
import { Localization } from '@/components/localization';
import { createClient } from '@/utils/supabase/client';
import { LogOut } from 'lucide-react';
import { useRouter } from 'next/navigation'; 

export function Header() {
  const t = useTranslations('HomePage');
  const tLoginForm = useTranslations('LoginForm');
  const router = useRouter();
  
  const [user, setUser] = useState<any>(null);
  const supabase = createClient();

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser();
      setUser(user);
    };
    getUser();

    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      setUser(session?.user ?? null);
      
      if (event === 'SIGNED_OUT') {
        router.refresh();
      }
    });

    return () => subscription.unsubscribe();
  }, [supabase, router]);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    
    setUser(null);
    
    window.location.href = '/';
  };

  return (
    <header className='sticky top-0 z-50 w-full border-b bg-white dark:bg-black'>
      <div className='flex h-16 items-center justify-between px-4 w-full'>
        <div className='flex items-center gap-2'>
          <a href='/'>
            <Image src='/logo2.png' alt='AI Roundtable logo' width={50} height={10} priority />
          </a>
          <span className='text-xl font-bold'>{t('title')}</span>
        </div>

        <div className='flex items-center gap-2'>
          <Localization />
          <ModeToggle />
          <SettingsButton/>
          
          {user ? (
            <div className='flex items-center gap-3 ml-2'>
              <span className='hidden sm:inline-block text-sm font-medium text-zinc-600 dark:text-zinc-400'>
                {user.email?.split('@')[0]}
              </span>
              <Button 
                type='button'
                variant='ghost' 
                size='sm' 
                onClick={handleLogout}
                className='text-zinc-500 hover:text-red-500'
              >
                <LogOut className='w-4 h-4 mr-2' />
                Logout
              </Button>
            </div>
          ) : (
            <Button asChild variant='default' size='sm'>
              <a href='/login'>{tLoginForm('loginButton')}</a>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
}