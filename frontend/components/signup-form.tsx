import { useTranslations } from 'next-intl';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from '@/components/ui/field';
import { Input } from '@/components/ui/input';
import { GoogleButton } from '@/components/ui/google-button';

export function SignupForm({ ...props }: React.ComponentProps<typeof Card>) {
  const t = useTranslations('SignupForm');

  return (
    <Card {...props}>
      <CardHeader>
        <CardTitle>{t('title')}</CardTitle>
        <CardDescription>{t('description')}</CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor='name'>{t('name')}</FieldLabel>
              <Input id='name' type='text' placeholder='John Doe' required />
            </Field>
            <Field>
              <FieldLabel htmlFor='email'>{t('email')}</FieldLabel>
              <Input
                id='email'
                type='email'
                placeholder='m@example.com'
                required
              />
              <FieldDescription>{t('emailDescription')}</FieldDescription>
            </Field>
            <Field>
              <FieldLabel htmlFor='password'>{t('password')}</FieldLabel>
              <Input id='password' type='password' required />
              <FieldDescription>{t('passwordDescription')}</FieldDescription>
            </Field>
            <Field>
              <FieldLabel htmlFor='confirm-password'>
                {t('confirmPassword')}
              </FieldLabel>
              <Input id='confirm-password' type='password' required />
              <FieldDescription>
                {t('confirmPasswordDescription')}
              </FieldDescription>
            </Field>
            <FieldGroup>
              <Field>
                <Button type='submit'>{t('createAccountButton')}</Button>
                <GoogleButton />
                <FieldDescription className='px-6 text-center'>
                  {t('alreadyHaveAccount')} <a href='/login'>{t('signIn')}</a>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  );
}
