import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const base =
    process.env.API_URL?.replace(/\/$/, '') ||
    process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') ||
    'http://localhost:8000';

  const body = await req.text();

  // npr. 10 minut (nastavi po potrebi)
  const TIMEOUT_MS = 10 * 60 * 1000;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const upstream = await fetch(`${base}/api/round-table`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body,
      cache: 'no-store',
      signal: controller.signal,
    });

    const text = await upstream.text();

    return new Response(text, {
      status: upstream.status,
      headers: {
        'Content-Type': upstream.headers.get('content-type') ?? 'application/json',
      },
    });
  } catch (e: any) {
    // če timeout/abort
    if (e?.name === 'AbortError') {
      return NextResponse.json(
        { error: 'Upstream timeout (round-table took too long).' },
        { status: 504 }
      );
    }

    return NextResponse.json(
      { error: `Proxy fetch failed: ${e?.message ?? 'unknown error'}` },
      { status: 502 }
    );
  } finally {
    clearTimeout(timeoutId);
  }
}
