export async function GET() {
  const base = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') || 'http://localhost:8000';

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
}