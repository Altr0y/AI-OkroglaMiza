import { NextResponse } from 'next/server';

export async function GET() {
  const base =
    process.env.API_URL?.replace(/\/$/, '') ||
    'http://backend_ai:8000';

  try {
    const res = await fetch(`${base}/api/models`, {
      headers: { Accept: 'application/json' },
      cache: 'no-store',
    });

    const text = await res.text();

    return new Response(text, {
      status: res.status,
      headers: {
        'Content-Type': res.headers.get('content-type') ?? 'application/json',
      },
    });
  } catch (e) {
    return NextResponse.json(
      { error: 'Proxy fetch failed', message: String(e) },
      { status: 502 }
    );
  }
}
