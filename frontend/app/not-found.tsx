import Link from 'next/link';
import { useTranslations } from 'next-intl';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';

export default function NotFound() {
  const t = useTranslations('NotFoundPage');

  return (
    <div className='flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black p-4'>
      <Card className='w-full max-w-md text-center'>
        <CardHeader className='space-y-4'>
          <div className='mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-zinc-100 dark:bg-zinc-800'>
            <span className='text-4xl font-bold text-zinc-400'>404</span>
          </div>
          <CardTitle className='text-2xl'>{t('title')}</CardTitle>
          <CardDescription className='text-base'>
            {t('description')}
          </CardDescription>
        </CardHeader>
        <CardContent className='space-y-4'>
          <Button asChild className='w-full'>
            <Link href='/'>{t('returnHomeButton')}</Link>
          </Button>
          <p className='text-sm text-zinc-500 dark:text-zinc-400'>
            {t('contactSupport')}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
