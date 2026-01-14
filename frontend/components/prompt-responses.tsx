'use client';

import { useEffect, useMemo, useState } from 'react';
import { useTranslations } from 'next-intl';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Slot } from './slot';

type PromptResponsesProps = {
  loading?: boolean;
  error?: string | null;
  responses?: Record<string, string> | null;
  summary?: string | null;
};

type TabItem = {
  key: string;
  label: string;
  content: string;
};


export function PromptResponses({
  loading,
  error,
  responses,
  summary,
}: PromptResponsesProps) {
  const t = useTranslations('PromptResponses');
  const [showSlot, setShowSlot] = useState(true);
  // if (loading) {
  //   return <div className="text-sm text-zinc-500">Generiram odgovore…</div>;
  // }

  // if (error) {
  //   return <div className="text-sm text-red-600">{error}</div>;
  // }      to sem prestavila pod use memo, org je blo nad

  const tabs = useMemo<TabItem[]>(() => {
    const items: TabItem[] = [];

    if (responses) {
      for (const [modelKey, text] of Object.entries(responses)) {
        items.push({
          key: modelKey,
          label: modelKey,
          content: text ?? '',
        });
      }
    }

    if (summary) {
      items.push({
        key: '__summary__',
        label: 'Summary',
        content: summary,
      });
    }

    return items;
  }, [responses, summary]);

  loading = true;
  if (loading) {
    return <div className="text-sm text-zinc-500"><Slot open={loading}/></div>;
  }

  if (error) {
    return <div className="text-sm text-red-600">{error}</div>;
  }

  if (tabs.length === 0) {
    return (
      <div className="text-sm text-zinc-600 dark:text-zinc-400">
        {t('placeholderBeforeSend')}
      </div>
    );
  }

  return <PromptResponsesTabs tabs={tabs} />;
}

function PromptResponsesTabs({ tabs }: { tabs: TabItem[] }) {
    const tpr = useTranslations('PromptResponses');
  const [active, setActive] = useState(tabs[0]?.key ?? '');

  // če pride nov response (npr. nova vprašanja), poskrbi, da je active tab veljaven
  useEffect(() => {
    if (!tabs.some((t) => t.key === active)) {
      setActive(tabs[0]?.key ?? '');
    }
  }, [tabs, active]);

  return (
    <Card className="rounded-2xl">
      <CardContent className="pt-0">
        <Tabs value={active} onValueChange={setActive} className="w-full">
          <TabsList className="mb-4 flex h-auto w-full flex-wrap justify-start gap-2">
            {tabs.map((t) => (
              <TabsTrigger
                key={t.key}
                value={t.key}
                className={` data-[state=active]:font-semibold
                  ${t.key === '__summary__'
                    ? 'ml-auto border border-border bg-muted text-muted-foreground data-[state=active]:bg-primary data-[state=active]:text-primary-foreground'
                    : ''
                  }
                `}
              >
                {t.key === '__summary__' ? tpr('summary') : t.label}
              </TabsTrigger>
            ))}
          </TabsList>

          {tabs.map((t) => (
            <TabsContent key={t.key} value={t.key} className="mt-0">
              <div className="whitespace-pre-wrap text-sm leading-6 text-zinc-800 dark:text-zinc-100">
                {t.content}
              </div>
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
    </Card>
  );
}