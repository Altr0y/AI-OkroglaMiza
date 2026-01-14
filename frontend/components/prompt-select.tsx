'use client';

import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { Button } from '@/components/ui/button';
import { useTranslations } from 'next-intl';

export type ModelItem = {
    key: string;
    model_id: string;
    temperature: number;
};

type PromptSelectProps = {
    models: ModelItem[];
    loading: boolean;
    error: string | null;
    selectedKeys: string[];
    onChange: (keys: string[]) => void;
};

export function PromptSelect({
    models,
    loading,
    error,
    selectedKeys,
    onChange,
}: PromptSelectProps) {
    const t = useTranslations('PromptButtons');
    const allKeys = models.map((m) => m.key);
    const allSelected =
        allKeys.length > 0 && selectedKeys.length === allKeys.length;

    const toggleSelectAll = () => {
        if (allKeys.length === 0) return;

        if (allSelected) {
            // Select 1 (always keep at least one)
            onChange([allKeys[0]]);
        } else {
            // Select all
            onChange(allKeys);
        }
    };

    const handleChange = (next: string[]) => {
        // enforce: at least 1 selected
        if (next.length === 0) return;
        onChange(next);
    };

    return (
        <div className="flex w-full flex-col gap-4">
            <div className="text-sm text-zinc-600 dark:text-zinc-300">
                {t('chooseModels')}:
            </div>

            {loading ? (
                <div className="text-sm text-zinc-500">{t('loadingModels')} ...</div>
            ) : error ? (
                <div className="text-sm text-red-600">{error}</div>
            ) : models.length === 0 ? (
                <div className="text-sm text-zinc-500">{t('zeroModels')}.</div>
            ) : (
                <>
                    {/* modeli + akcijski gumb v isti vrstici */}
                    {/* modeli + akcijski gumb v istem flowu */}
                    <div className="flex w-full flex-wrap items-center gap-2">
                        <ToggleGroup
                            type="multiple"
                            value={selectedKeys}
                            onValueChange={handleChange}
                            className="flex flex-wrap gap-2"
                        >
                            {models.map((m) => (
                                <ToggleGroupItem
                                    key={m.key}
                                    value={m.key}
                                    aria-label={`Select ${m.key}`}
                                    className="
                                    inline-flex items-center gap-2
                                    h-9 px-4
                                    !rounded-md
                                    text-sm font-medium
                                    transition-colors

                                    border border-input
                                    bg-background
                                    text-foreground

                                    hover:bg-accent hover:text-accent-foreground

                                    focus-visible:outline-none
                                    focus-visible:ring-2 focus-visible:ring-ring
                                    focus-visible:ring-offset-2

                                    data-[state=on]:bg-primary
                                    data-[state=on]:text-primary-foreground
                                    data-[state=on]:border-primary
                                    "
                                >
                                    <span>{m.key}</span>
                                    <span className="text-xs opacity-80">{m.model_id}</span>
                                </ToggleGroupItem>
                            ))}
                        </ToggleGroup>

                        {/* Select all / Select one */}
                        <Button
                            type="button"
                            size="sm"
                            onClick={toggleSelectAll}
                            title={allSelected ? t('selectOne') : t('selectAll')}
                            className="
                            h-9 shrink-0
                            bg-slate-300 text-slate-900 border border-slate-400 hover:bg-slate-400
                            focus-visible:ring-2 focus-visible:ring-slate-500 focus-visible:ring-offset-2
                            dark:bg-slate-700 dark:text-slate-100 dark:border-slate-600 dark:hover:bg-slate-600
                            dark:focus-visible:ring-slate-500
                            "
                        >
                            {allSelected ? t('selectOne') : t('selectAll')}
                        </Button>
                    </div>


                </>
            )}

            {selectedKeys.length > 0 && !loading && !error && models.length > 0 && (
                <div className="text-xs text-zinc-500">
                    {t('selected')}:{' '}
                    <span className="font-medium">
                        {selectedKeys.join(', ')} ({selectedKeys.length}/{allKeys.length})
                    </span>
                </div>
            )}
        </div>
    );
}
