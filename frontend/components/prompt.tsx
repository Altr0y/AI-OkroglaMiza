'use client';

import { useEffect, useState } from 'react';
import { PromptSelect, type ModelItem } from '@/components/prompt-select';

type ModelsResponse = {
    models: ModelItem[];
};

export function Prompt() {
    const [models, setModels] = useState<ModelItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedKeys, setSelectedKeys] = useState<string[]>([]);

    useEffect(() => {
        let cancelled = false;

        async function loadModels() {
            try {
                setLoading(true);
                setError(null);

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
                    setError(e?.message ?? 'Napaka pri nalaganju modelov.');
                    setModels([]);
                    setSelectedKeys([]);
                }
            } finally {
                if (!cancelled) setLoading(false);
            }
        }

        loadModels();

        return () => {
            cancelled = true;
        };
    }, []);

    return (
        <PromptSelect
            models={models}
            loading={loading}
            error={error}
            selectedKeys={selectedKeys}
            onChange={setSelectedKeys}
        />
    );
}