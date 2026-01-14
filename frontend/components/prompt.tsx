'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { PromptSelect, type ModelItem } from '@/components/prompt-select';
import { PromptInput } from '@/components/prompt-input';
import { PromptResponses } from '@/components/prompt-responses';

type ModelsResponse = {
  models: ModelItem[];
};

type RoundTableResponse = {
  responses: Record<string, string>;
  summary: string;
};

const USE_MOCK = false;
const MOCK_RESPONSE : RoundTableResponse= {
  "responses": {
    "qwen": "Based on the search results, I cannot determine in which year Slovenia declared independence. The provided web search results only contain information about the video game \"DoomRL\" (a roguelike adaptation of Doom), with no information about Slovenia's independence history.",
    "ministral": "Based on the search results provided, I cannot determine when Slovenia declared independence (Katerega leta se je osamosvojila Slovenija). The available information pertains only to the game *DoomRL* and does not mention Slovenian independence.",
    "deepseek": "Based on the search results, I cannot determine \"osamosvojila slovenija\" directly. The information provided does not include any details about a player named \"Katerega.\""
  },
  "summary": "The original question does not provide factual information about Slovenia's declaration of independence. Based on the provided data, none of the responses address this topic."

};


export function Prompt() {
  const t = useTranslations('Prompt');
  const [models, setModels] = useState<ModelItem[]>([]);
  const [modelsLoading, setModelsLoading] = useState(true);
  const [modelsError, setModelsError] = useState<string | null>(null);

  const [selectedKeys, setSelectedKeys] = useState<string[]>([]);

  const [chatLoading, setChatLoading] = useState(false);
  const [chatError, setChatError] = useState<string | null>(null);
  const [responses, setResponses] = useState<Record<string, string> | null>(null);
  const [summary, setSummary] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadModels() {
      try {
        setModelsLoading(true);
        setModelsError(null);

        const res = await fetch('/api/models', {
          headers: { Accept: 'application/json' },
          cache: 'no-store',
        });

        if (!res.ok) {
          const text = await res.text().catch(() => '');
          throw new Error(`GET /api/models failed (${res.status}). ${text}`);
        }

        const data = (await res.json()) as ModelsResponse;

        if (!cancelled) {
          const list = Array.isArray(data?.models) ? data.models : [];
          setModels(list);
          setSelectedKeys(list.length ? [list[0].key] : []);
        }
      } catch (e: any) {
        if (!cancelled) {
          setModelsError(e?.message ?? t('errLoadingModels'));
          setModels([]);
          setSelectedKeys([]);
        }
      } finally {
        if (!cancelled) setModelsLoading(false);
      }
    }

    loadModels();

    return () => {
      cancelled = true;
    };
  }, []);

const sendQuestion = async (query: string) => {
  setChatLoading(true);
  setChatError(null);
  setResponses(null);
  setSummary(null);

  try {
    if (USE_MOCK) {
      await new Promise<void>((resolve) => setTimeout(resolve, 500));
      setResponses(MOCK_RESPONSE.responses);
      setSummary(MOCK_RESPONSE.summary);
      return;
    }

    // REAL BACKEND
    const res = await fetch('/api/round-table', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        query,
        selected_agents: selectedKeys,
      }),
    });

    if (!res.ok) {
      const text = await res.text().catch(() => '');
      throw new Error(`POST /api/round-table failed (${res.status}). ${text}`);
    }

    const data = (await res.json()) as RoundTableResponse;
    setResponses(data.responses ?? null);
    setSummary(data.summary ?? null);
  } catch (e: unknown) {
    const msg =
      e instanceof Error ? e.message : t('errSendPrompt');
    setChatError(msg);
  } finally {
    setChatLoading(false);
  }
};


  const showChatUI = selectedKeys.length > 0;

  return (
    <div className="flex w-full flex-col gap-6 mb-16">
      <PromptSelect
        models={models}
        loading={modelsLoading}
        error={modelsError}
        selectedKeys={selectedKeys}
        onChange={(keys) => {
          setSelectedKeys(keys);
          // reset output if selection changes
          setResponses(null);
          setSummary(null);
          setChatError(null);
        }}
      />

      {showChatUI && (
        <>
          <PromptInput
            onSubmit={sendQuestion}
            isLoading={chatLoading}
            disabled={modelsLoading || !!modelsError}
            placeholder={t('placeholderPrompt')}
          />

          <PromptResponses
            loading={chatLoading}
            error={chatError}
            responses={responses}
            summary={summary}
          />
        </>
      )}
    </div>
  );
}
