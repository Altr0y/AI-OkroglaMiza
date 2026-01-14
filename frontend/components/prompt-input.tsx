// clear input

'use client';

import * as React from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { CornerDownLeft, X } from 'lucide-react';

const MAX_CHARS = 300;

export type PromptInputProps = Readonly<{
  disabled?: boolean;
  isLoading?: boolean;
  onSubmit: (query: string) => void;
  placeholder?: string;
  initialValue?: string;
  maxHeightPx?: number;
}>;

export function PromptInput({
  disabled = false,
  isLoading = false,
  onSubmit,
  placeholder = 'Enter your question ...',
  initialValue = '',
  maxHeightPx = 420,
}: PromptInputProps): React.JSX.Element {
  const [value, setValue] = React.useState<string>(
    initialValue.slice(0, MAX_CHARS)
  );

  const textareaRef = React.useRef<HTMLTextAreaElement | null>(null);
  const isClampedRef = React.useRef<boolean>(false);

  const charCount = value.length;

  const counterClass =
    charCount >= MAX_CHARS
      ? 'text-destructive'
      : charCount >= 290
      ? 'text-yellow-500 dark:text-yellow-400'
      : 'text-muted-foreground';

  const canSend =
    !disabled && !isLoading && charCount > 0 && charCount <= MAX_CHARS;

  const updateSize = React.useCallback((): void => {
    const el = textareaRef.current;
    if (!el) return;

    if (isClampedRef.current) {
      if (el.scrollHeight <= maxHeightPx) {
        isClampedRef.current = false;
        el.style.overflowY = 'hidden';
        el.style.height = 'auto';
        el.style.height = `${el.scrollHeight}px`;
      } else {
        el.style.height = `${maxHeightPx}px`;
        el.style.overflowY = 'auto';
      }
      return;
    }

    el.style.overflowY = 'hidden';
    el.style.height = 'auto';

    const next = el.scrollHeight;

    if (next > maxHeightPx) {
      isClampedRef.current = true;
      el.style.height = `${maxHeightPx}px`;
      el.style.overflowY = 'auto';
    } else {
      el.style.height = `${next}px`;
    }
  }, [maxHeightPx]);

  React.useEffect(() => {
    setValue(initialValue.slice(0, MAX_CHARS));
    isClampedRef.current = false;
    requestAnimationFrame(updateSize);
  }, [initialValue, updateSize]);

  React.useEffect(() => {
    requestAnimationFrame(updateSize);
  }, [value, updateSize]);

  React.useEffect(() => {
    const onResize = (): void => {
      requestAnimationFrame(updateSize);
    };
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, [updateSize]);

  const submit = React.useCallback((): void => {
    if (!canSend) return;
    onSubmit(value.trim());
  }, [canSend, onSubmit, value]);

  const clear = React.useCallback((): void => {
    setValue('');
    isClampedRef.current = false;
    requestAnimationFrame(updateSize);
  }, [updateSize]);

  return (
    <div className="w-full rounded-2xl border bg-background px-3 py-2 shadow-sm">
      <div className="flex items-end gap-1.5">
        <div className="relative flex-1 min-w-0">
          <Textarea
            ref={textareaRef}
            rows={1}
            wrap="soft"
            id = "textarea"
            value={value}
            maxLength={MAX_CHARS}
            placeholder={placeholder}
            disabled={disabled}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
              setValue(e.target.value.slice(0, MAX_CHARS));
            }}
            onKeyDown={(e: React.KeyboardEvent<HTMLTextAreaElement>) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                submit();
              }
            }}
            className="
              w-full
              resize-none
              border-0 shadow-none
              focus-visible:ring-0
              bg-transparent
              text-sm leading-6
              py-3 pr-10
              whitespace-pre-wrap break-words
              prompt-scrollbar
            "
            style={{ scrollbarGutter: 'stable' }}
          />

          {value.length > 0 && (
            <button
              type="button"
              onClick={clear}
              className="
                absolute
                top-2 right-2
                h-6 w-6
                rounded-md
                flex items-center justify-center
                text-muted-foreground
                hover:text-foreground
                hover:bg-muted
              "
              aria-label="Clear"
              title="Clear input"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>

        <div className="flex shrink-0 w-[64px] flex-col items-center gap-2 self-end">
          <Button
            type="button"
            onClick={submit}
            disabled={!canSend}
            className="h-10 w-10 rounded-xl p-0"
            aria-label="Send"
            title="Send Question"
          >
            <CornerDownLeft className="h-5 w-5" />
          </Button>

          <div
            className={`
              w-full
              text-center
              text-xs tabular-nums
              ${counterClass}
            `}
          >
            {charCount}/{MAX_CHARS}
          </div>
        </div>
      </div>
    </div>
  );
}