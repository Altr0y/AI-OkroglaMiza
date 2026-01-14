import Link from 'next/link';
import Image from 'next/image';
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

      {/* Content */}
      <Card className="relative z-10 w-full max-w-md text-center shadow-md">
        <CardHeader className="space-y-4">
          <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-zinc-100 dark:bg-zinc-800">
            <span className="text-4xl font-bold text-zinc-400">404</span>
          </div>
          <CardTitle className="text-2xl">{t('title')}</CardTitle>
          <CardDescription className="text-base">
            {t('description')}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button asChild className="w-full">
            <Link href="/">{t('returnHomeButton')}</Link>
          </Button>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">
            {t('contactSupport')}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}