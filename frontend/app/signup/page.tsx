import { SignupForm } from '@/components/signup-form';

export default function Page() {
  return (
    <div className='flex flex-1 items-center justify-center bg-zinc-50 dark:bg-black p-4'>
      <SignupForm className='w-full max-w-sm' />
    </div>
  );
}
