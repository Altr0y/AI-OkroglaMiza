export function Footer() {
  return (
    <footer className='w-full border-t bg-white dark:bg-black'>
      <div className='flex h-16 items-center justify-center px-4 w-full'>
        <div className='flex items-center'>
          <span className='text-sm text-zinc-600 dark:text-zinc-400'>
            © {new Date().getFullYear()} Razvoj programske opreme - Group 5. All
            rights reserved.
          </span>
        </div>
      </div>
    </footer>
  );
}
