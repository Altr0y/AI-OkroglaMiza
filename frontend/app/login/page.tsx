'use client';

import { useState } from 'next';
import { useRouter } from 'next/navigation';
import { useTranslations } from 'next-intl';
import Image from 'next/image';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';

import { LoginForm } from '@/components/login-form';

export default function LoginPage() {
  const t = useTranslations('LoginPage');

  return (
    <div className='flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black p-4'>
      <LoginForm className='w-full max-w-sm' />
    </div>
  );
}
