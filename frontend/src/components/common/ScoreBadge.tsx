interface ScoreBadgeProps {
  score: number;
}

/** Green badge for high scores, amber for mid, neutral for low — keeps the
 * signal glanceable without needing to read the number. */
export function ScoreBadge({ score }: ScoreBadgeProps) {
  const tone =
    score >= 80
      ? "bg-chip-success text-text-success"
      : score >= 60
      ? "bg-chip-amber text-chip-amber-text"
      : "bg-surface-1 text-text-secondary";

  return (
    <span className={`h-fit shrink-0 rounded px-2 py-0.5 text-xs font-medium ${tone}`}>
      {score}
    </span>
  );
}
