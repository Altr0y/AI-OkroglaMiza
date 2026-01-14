import { useTranslations } from 'next-intl';

import { Suspense} from 'react';
import { SignupFormLanding } from '@/components/signup-form-landing';
import { Demo } from '@/components/demo';

export function Landing() {
  const t = useTranslations('HomePage');
  return (
    <div>
        <div className="flex flex-col items-center gap-6 text-center mb-8">
          <Suspense fallback={<div> {t('loading')} ...</div>}>
            <h1 className="text-3xl font-bold leading-10 tracking-tight text-black dark:text-zinc-50">
              {t('title')}
            </h1>
            <p className="max-w-l text-lg text-zinc-600 dark:text-zinc-400">
              {t('description2')}
            </p>
          </Suspense>
        </div>
          <div className="flex w-full gap-8">
            <SignupFormLanding />
            <Demo />
          </div>
          </div>
  );
}
