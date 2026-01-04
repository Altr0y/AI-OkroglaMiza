import { Button } from '@/components/ui/button';
import { useTranslations } from 'next-intl';

export function Demo() {
  const t = useTranslations('Demo');

  return (
    <div className='flex-1 flex flex-col gap-4 p-8 bg-[#e8f0f8] border py-6 shadow-sm dark:bg-card rounded-2xl'>
      {/* Question Header */}
      <div className='flex items-center gap-2'>
        <div className='flex-1 h-px bg-zinc-400'></div>
        <span className='text-sm font-medium text-zinc-700 dark:text-zinc-300'>
          {t('title')}
        </span>
        <div className='flex-1 h-px bg-zinc-400'></div>
      </div>

      {/* Model Cards */}
      <div className='grid grid-cols-4 gap-3 dark:text-black'>
        {[
          {
            name: 'Model A',
            color: 'bg-blue-100 border-blue-400',
            score: 90,
          },
          {
            name: 'Model B',
            color: 'bg-red-100 border-red-400',
            score: 88,
          },
          {
            name: 'Model C',
            color: 'bg-green-100 border-green-400',
            score: 77,
          },
          {
            name: 'Model D',
            color: 'bg-yellow-100 border-yellow-400',
            score: 79,
          },
        ].map((model) => (
          <div
            key={model.name}
            className={`${model.color} border-2 rounded-lg p-3 text-xs`}
          >
            <h3 className='font-semibold text-center mb-2'>{model.name}</h3>
            <p className='text-zinc-600 text-[10px] leading-tight mb-3 line-clamp-6'>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
            <div className='h-2 bg-gradient-to-r from-red-400 via-yellow-400 to-green-400 rounded-full mb-1'></div>
            <p className='text-xs font-medium'>
              {t('score')}: {model.score}
            </p>
          </div>
        ))}
      </div>

      {/* Action Buttons */}
      <div className='flex gap-3'>
        <Button variant='outline' size='sm' className='flex-1 bg-white'>
          ⇄ {t('compareButton')}
        </Button>
        <Button
          variant='outline'
          size='sm'
          className='flex-1 bg-blue-500 text-white hover:bg-blue-600'
        >
          ✓ {t('bestButton')}
        </Button>
        <Button variant='outline' size='sm' className='flex-1 bg-white'>
          ↻ {t('reRunButton')}
        </Button>
      </div>

      {/* Follow-up Input */}
      <div className='flex items-center gap-2 bg-zinc-700 rounded-lg px-4 py-2'>
        <span className='text-zinc-400 text-sm'>
          {t('followUpQuestionInput')}
        </span>
        <span className='ml-auto text-zinc-400'>↵</span>
      </div>
    </div>
  );
}
