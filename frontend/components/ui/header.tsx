import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  NavigationMenuViewport,
} from '@/components/ui/navigation-menu';
import { Button } from '@/components/ui/button';
import { useTranslations } from 'next-intl';
import SettingsButton from "@/components/ui/settings-button";
import Image from 'next/image';

import { ModeToggle } from '@/components/mode-toggle';
import { Localization } from '@/components/localization';

export function Header() {
  const t = useTranslations('HomePage');
  const tLoginForm = useTranslations('LoginForm');

  return (
    <header className='sticky top-0 z-50 w-full border-b bg-white dark:bg-black'>
      <div className='flex h-16 items-center justify-between px-4 w-full'>
        {/* Left side - Logo/Brand */}
        <div className='flex items-center'>
          <a href='/'>
            <Image
              src='/logo2.png'
              alt='AI Roundtable logo'
              width={50}
              height={10}
              priority
            />
          </a>
          
          <span className='text-xl font-bold'>{t('title')}</span>
        </div>

        {/* Right side - Navigation items */}
        <div className='flex items-center gap-2'>
          <Localization />
          <ModeToggle />
          <SettingsButton/>
          <Button asChild variant='default' size='sm'>
            <a href='/login'>{tLoginForm('loginButton')}</a>
          </Button>
          
        </div>
      </div>
    </header>
  );
}
