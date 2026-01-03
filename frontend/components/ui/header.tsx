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
import Image from 'next/image';

import { ModeToggle } from '@/components/mode-toggle';
import { Localization } from '@/components/localization';

export function Header() {
  const t = useTranslations('HomePage');

  return (
    <header className='sticky top-0 z-50 w-full border-b bg-white dark:bg-black'>
      <div className='flex h-16 items-center justify-between px-4 w-full'>
        {/* Left side - Logo/Brand */}
        <div className='flex items-center'>
          <Image
            src='/logo.png'
            alt='AI Roundtable logo'
            width={50}
            height={10}
            priority
          />

          <span className='text-xl font-bold'>{t('title')}</span>
        </div>

        {/* Right side - Navigation items */}
        <div className='flex items-center gap-2'>
          <Localization />
          <ModeToggle />
          <Button
            asChild
            variant='default'
            size='sm'
            className='bg-zinc-100 text-black hover:bg-zinc-200 dark:bg-zinc-900 dark:text-white dark:hover:bg-zinc-800'
          >
            <a href='/login'>Login</a>
          </Button>
        </div>
      </div>
    </header>
  );
}
