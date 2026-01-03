'use client';

import { ChevronDown } from 'lucide-react';
import { useLocale, useTranslations } from 'next-intl';
import { useRouter } from 'next/navigation';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export function Localization() {
  const t = useTranslations('Localization');
  const locale = useLocale();
  const router = useRouter();

  function setLocale(l: string) {
    document.cookie = `locale=${l}; path=/; max-age=${
      60 * 60 * 24 * 365
    }; SameSite=Lax`;

    // Refresh the page to apply new locale
    router.refresh();
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant='ghost' className='p-2 focus-visible:ring-0'>
          <div className='hidden sm:flex'>
            {t('locale', { locale: locale })}
          </div>
          <ChevronDown className='size-4' />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align='end'>
        <DropdownMenuItem onClick={() => setLocale('sl')}>
          Slovenščina
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setLocale('en')}>
          English
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
