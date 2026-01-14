import Image from 'next/image';
import { ForgotPasswordForm } from '@/components/forgot-password-form';

export default function ForgotPasswordPage() {
  return (
    <div className="relative flex flex-1 items-center justify-center bg-zinc-50 dark:bg-black overflow-hidden">
      
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

      {/* Forgot Password Form */}
      <div className="relative z-10 w-full">
        <ForgotPasswordForm />
      </div>
    </div>
  );
}