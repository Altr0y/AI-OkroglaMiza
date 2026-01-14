import { Agent } from 'undici';
import { NextResponse } from 'next/server';

const TIMEOUT_MS = 10 * 60 * 1000;

const dispatcher = new Agent({
  headersTimeout: TIMEOUT_MS,
  bodyTimeout: TIMEOUT_MS,
});

export async function POST(req: Request) {
  const base =
    process.env.API_URL?.replace(/\/$/, '') ||
    'http://backend_ai:8000';

  const body = await req.text();

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    //console.log('Proxy url:', `${base}/api/round-table`);

    const upstream = await fetch(`${base}/api/round-table`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body,
      cache: 'no-store',
      signal: controller.signal,
      dispatcher,
    } as any);

    const text = await upstream.text();

    return new Response(text, {
      status: upstream.status,
      headers: {
        'Content-Type': upstream.headers.get('content-type') ?? 'application/json',
      },
    });
  } catch (e: any) {
    //console.error('UPSTREAM FETCH FAILED', e?.cause ?? e);

    if (e?.name === 'AbortError') {
      return NextResponse.json(
        { error: 'Upstream timeout (round-table took too long).' },
        { status: 504 }
      );
    }

    return NextResponse.json(
      {
        error: 'Proxy fetch failed',
        message: e?.message,
        cause: e?.cause ? String(e.cause) : undefined,
      },
      { status: 502 }
    );
  } finally {
    clearTimeout(timeoutId);
  }
}
