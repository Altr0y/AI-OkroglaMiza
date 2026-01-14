"use client";

import * as React from "react";
import { useTranslations } from 'next-intl';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "🍇", "7️⃣"] as const;

const PAY_TABLE: Record<string, number> = {
  "7️⃣": 12,
  "⭐": 8,
  "🔔": 6,
  "🍇": 5,
  "🍋": 4,
  "🍒": 3,
};

function randSymbol() {
  return SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)];
}

function clamp(n: number, min: number, max: number) {
  return Math.max(min, Math.min(max, n));
}

function evaluate(result: string[], bet: number) {
  const [a, b, c] = result;

  if (a === b && b === c) {
    const mult = PAY_TABLE[a] ?? 3;
    return { win: bet * mult };
  }

  if (a === b || b === c || a === c) {
    const pair = a === b ? a : b === c ? b : a;
    const mult = Math.max(2, Math.floor((PAY_TABLE[pair] ?? 3) / 2));
    return { win: bet * mult };
  }

  return { win: 0 };
}

export type SlotProps = {
  open: boolean;
  initialCredits?: number;
  initialBet?: number;
  centerInParent?: boolean;
  className?: string;
};

function LoadingDots() {
  return (
    <span className="inline-flex items-center gap-1" aria-hidden="true">
      <span className="h-1 w-1 rounded-full bg-foreground/40 animate-bounce [animation-delay:0ms]" />
      <span className="h-1 w-1 rounded-full bg-foreground/40 animate-bounce [animation-delay:120ms]" />
      <span className="h-1 w-1 rounded-full bg-foreground/40 animate-bounce [animation-delay:240ms]" />
    </span>
  );
}

function Stat({
  label,
  value,
  tone = "neutral",
}: {
  label: string;
  value: number;
  tone?: "neutral" | "win" | "lose";
}) {
  const toneClasses =
    tone === "win"
      ? "border-emerald-500/35 bg-emerald-500/20 text-emerald-800 dark:text-emerald-200 dark:bg-emerald-400/20"
      : tone === "lose"
      ? "border-amber-500/35 bg-amber-500/20 text-amber-900 dark:text-amber-200 dark:bg-amber-300/20"
      : "border-border/60 bg-muted/60 text-foreground";

  return (
    <div className={`min-w-[94px] rounded-md border px-2 py-1 text-center ${toneClasses}`}>
      <div className="text-[10px] leading-4 text-muted-foreground">{label}</div>
      <div className="text-sm leading-5 font-semibold tabular-nums">{value}</div>
    </div>
  );
}

export function Slot({
  open,
  initialCredits = 100,
  initialBet = 5,
  centerInParent = true,
  className,
}: SlotProps) {

  const tsl = useTranslations('Slot');

  const [credits, setCredits] = React.useState(initialCredits);
  const [bet, setBet] = React.useState(initialBet);

  const [lastWin, setLastWin] = React.useState(0);
  const [totalWon, setTotalWon] = React.useState(0);

  const [reels, setReels] = React.useState<string[]>(["⭐", "🍒", "🔔"]);
  const [spinning, setSpinning] = React.useState(false);

  // UI effects for credits
  const [creditsFlash, setCreditsFlash] = React.useState<"none" | "win" | "lose">("none");
  const [creditsBump, setCreditsBump] = React.useState(false);

  const intervalsRef = React.useRef<number[]>([]);
  const timersRef = React.useRef<number[]>([]);
  const prevCreditsRef = React.useRef<number>(initialCredits);

  const canSpin = open && !spinning && credits >= bet;

  const clearAllTimers = React.useCallback(() => {
    intervalsRef.current.forEach(clearInterval);
    timersRef.current.forEach(clearTimeout);
    intervalsRef.current = [];
    timersRef.current = [];
  }, []);

  React.useEffect(() => clearAllTimers, [clearAllTimers]);

  // Animate credits changes (bump + flash)
  React.useEffect(() => {
    const prev = prevCreditsRef.current;
    if (credits === prev) return;

    const delta = credits - prev;
    prevCreditsRef.current = credits;

    setCreditsBump(true);
    const bumpId = window.setTimeout(() => setCreditsBump(false), 220);
    timersRef.current.push(bumpId);

    setCreditsFlash(delta > 0 ? "win" : "lose");
    const flashId = window.setTimeout(() => setCreditsFlash("none"), 450);
    timersRef.current.push(flashId);
  }, [credits]);

  async function spin() {
    if (!canSpin) return;

    setSpinning(true);
    setLastWin(0);

    // subtract bet
    setCredits((c) => c - bet);

    clearAllTimers();

    // flicker
    intervalsRef.current = reels.map((_, i) =>
      window.setInterval(() => {
        setReels((r) => {
          const next = [...r];
          next[i] = randSymbol();
          return next;
        });
      }, 90 + i * 25)
    );

    const final = [randSymbol(), randSymbol(), randSymbol()];
    const stopAt = [520, 720, 920];

    await Promise.all(
      stopAt.map(
        (t, i) =>
          new Promise<void>((resolve) => {
            const id = window.setTimeout(() => {
              clearInterval(intervalsRef.current[i]);
              setReels((r) => {
                const next = [...r];
                next[i] = final[i];
                return next;
              });
              resolve();
            }, t);
            timersRef.current.push(id);
          })
      )
    );

    const res = evaluate(final, bet);

    setLastWin(res.win);
    setTotalWon((tw) => tw + res.win);
    setCredits((c) => c + res.win);

    const done = window.setTimeout(() => setSpinning(false), 160);
    timersRef.current.push(done);
  }

  function reset() {
    if (spinning) return;
    setCredits(initialCredits);
    setBet(initialBet);
    setLastWin(0);
    setTotalWon(0);
    setReels(["⭐", "🍒", "🔔"]);
  }

  if (!open) return null;

  const wrapperClass = centerInParent ? "w-full flex items-center justify-center" : "w-full";

  const creditToneClasses =
    creditsFlash === "win"
      ? "border-emerald-500/35 bg-emerald-500/20 text-emerald-800 dark:text-emerald-200 dark:bg-emerald-400/20"
      : creditsFlash === "lose"
      ? "border-amber-500/35 bg-amber-500/20 text-amber-900 dark:text-amber-200 dark:bg-amber-300/20"
      : "border-border/60 bg-muted/60 text-foreground";

  return (
    <div className={wrapperClass}>
      <Card
        className={[
          "w-full max-w-[340px] border border-border/60 bg-muted/20",
          className ?? "",
        ].join(" ")}
      >
        <CardContent className="p-3 flex flex-col items-center gap-3">
          {/* TOP: waiting label + animated dots */}
          <div className="w-full flex items-center justify-center gap-2 text-xs text-muted-foreground">
            <span>{tsl('generatingAnswers')}</span>
            <LoadingDots />
          </div>

          {/* Reels */}
          <div className="rounded-md border border-border/60 bg-background/50 px-2 py-1.5">
            <div className="grid grid-cols-3 gap-2">
              {reels.map((s, i) => (
                <div
                  key={i}
                  className={[
                    "h-10 w-10 rounded-md border border-border/60 bg-background grid place-items-center",
                    spinning ? "animate-pulse" : "",
                  ].join(" ")}
                >
                  <span className="text-xl leading-none select-none">{s}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Stats*/}
          <div className="flex flex-wrap justify-center gap-2">
            <Stat label={tsl('bet')} value={bet} tone="neutral" />
            <Stat label={tsl('winnings')} value={lastWin} tone={lastWin > 0 ? "win" : "neutral"} />
            <Stat label={tsl('totalWon')} value={totalWon} tone="neutral" />
          </div>

          {/* Controls */}
          <div className="flex items-center justify-center gap-2">
            <Button
              size="sm"
              variant="secondary"
              className="h-8 w-8 p-0"
              onClick={() => setBet((b) => clamp(b - 1, 1, 50))}
              disabled={spinning}
              aria-label="Decrease Bet"
            >
              −
            </Button>

            <Button size="sm" className="h-8 px-4" onClick={spin} disabled={!canSpin}>
              Spin
            </Button>

            <Button
              size="sm"
              variant="secondary"
              className="h-8 w-8 p-0"
              onClick={() => setBet((b) => clamp(b + 1, 1, 50))}
              disabled={spinning}
              aria-label="Increase Bet"
            >
              +
            </Button>

            <Button
              size="sm"
              variant="outline"
              className="h-8 px-3"
              onClick={reset}
              disabled={spinning}
            >
              Reset
            </Button>
          </div>

          {/* Credits pill w/ flash + bump (bolj opaque) */}
          <div className="flex justify-center">
            <div
              className={[
                "inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-[11px] font-medium tabular-nums",
                "transition-transform duration-200",
                creditsBump ? "scale-[1.05]" : "scale-100",
                creditToneClasses,
              ].join(" ")}
            >
              {tsl('credit')} <span className="font-semibold">{credits}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
