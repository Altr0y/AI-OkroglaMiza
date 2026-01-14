<<<<<<< HEAD
'use client'

import { Button } from '@/components/ui/button';
import { useState } from "react"
import { useTranslations } from 'next-intl'

export function Footer() {
  const [open, setOpen] = useState(false)

  const tr = useTranslations('AboutUsPage')

  return (
    <footer className='w-full border-t bg-white dark:bg-black'>
      <div className='flex h-16 items-center justify-between px-4 w-full'>
        <div className='w-25'></div>                                                              {/* right spacer */}
        <span className='text-sm text-zinc-600 dark:text-zinc-400 ml-16'>
          © {new Date().getFullYear()} Razvoj programske opreme - Group 5. All rights reserved.   {/* middle text */}
        </span>
        <div>
          
          <Button variant="outline" className='w-25 text-sm text-zinc-600 dark:text-zinc-400 hover:text-zinc-800 dark:hover:text-zinc-200 hover:bg-gray-300 dark:hover:bg-zinc-800 transition-colors mr-4'
          onClick={() => setOpen(true)}>
            {tr('about us')}                                                                      {/* left button */}
          </Button>
        </div>
      </div>
      {open && (                                                                                   /* about us box*/
         <div className='fixed inset-0 z-50 flex items-center justify-center bg-black/50'>
          <div className='w-[64rem] max-w-full rounded-lg bg-white dark:bg-black p-6'>
            <div className='flex items-center justify-between items-start'>
              <h2 className='text-xl font-bold p-2'>{tr('about us')}</h2>
              <Button variant="ghost" className='' onClick={() => setOpen(false)}>                             {/* close button*/}
                {tr('close')}
              </Button>
            </div>
            <hr></hr>
            <div className="mt-4 text-sm text-zinc-700 dark:text-zinc-300 space-y-2">             {/* Text        */}
              <p className='ml-2 mb-4'>
                {tr('paragraph 1')}
              </p>
              <p className='ml-2 mb-4'>
                {tr('paragraph 2')}
              </p>
              <p className='ml-2 mb-4'>
                {tr('paragraph 3')}
              </p>
              <p className='ml-2 mb-4'>
                {tr('paragraph 4')}
              </p>
            </div>
          </div>
        </div>
      )}


=======
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
>>>>>>> dev
    </footer>
  );
}
