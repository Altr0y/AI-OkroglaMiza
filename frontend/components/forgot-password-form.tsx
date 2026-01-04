'use client';

import { ChevronLeftIcon } from 'lucide-react';
import { useTranslations } from 'next-intl';

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export function ForgotPasswordForm() {
  const t = useTranslations('ForgotPasswordForm');

  return (
    <div className='relative flex h-auto min-h-screen items-center justify-center overflow-x-hidden px-4 py-10 sm:px-6 lg:px-8'>
      <Card className='z-1 w-full border-none shadow-md sm:max-w-md'>
        <CardHeader className='gap-6'>
          <div>
            <CardTitle className='mb-1.5 text-2xl'>{t('title')}</CardTitle>
            <CardDescription className='text-base'>
              {t('description')}
            </CardDescription>
          </div>
        </CardHeader>

        <CardContent className='space-y-4'>
          {/* ForgotPassword Form */}

          <form className='space-y-4' onSubmit={(e) => e.preventDefault()}>
            {/* Email */}
            <div className='space-y-1'>
              <Label className='leading-5' htmlFor='userEmail'>
                {t('email')}*
              </Label>
              <Input
                type='email'
                id='userEmail'
                placeholder={t('emailPlaceholder')}
              />
            </div>

            <Button className='w-full' type='submit'>
              {t('resetPasswordButton')}
            </Button>
          </form>

          <a
            href='/login'
            className='group mx-auto flex w-fit items-center gap-2'
          >
            <ChevronLeftIcon className='size-5 transition-transform duration-200 group-hover:-translate-x-0.5' />
            <span>{t('backToLogin')}</span>
          </a>
        </CardContent>
      </Card>
    </div>
  );
}
