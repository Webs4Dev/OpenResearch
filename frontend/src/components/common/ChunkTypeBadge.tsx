const TONE_BY_TYPE: Record<string, string> = {
  method: "bg-chip-amber text-chip-amber-text",
  result: "bg-chip-teal text-chip-teal-text",
  background: "bg-surface-1 text-text-secondary",
};

const FALLBACK_TONE = "bg-surface-1 text-text-secondary";

export function ChunkTypeBadge({ type }: { type: string }) {
  const tone = TONE_BY_TYPE[type.toLowerCase()] ?? FALLBACK_TONE;
  return (
    <span className={`rounded px-2 py-0.5 text-[11px] font-medium ${tone}`}>{type}</span>
  );
}

/** Exposed so PdfChunkViewer can apply the same colors to in-PDF highlights. */
export const CHUNK_HIGHLIGHT_COLORS: Record<string, { fill: string; tag: string }> = {
  method: { fill: "rgba(239, 159, 39, 0.28)", tag: "#9A6A1E" },
  result: { fill: "rgba(93, 202, 165, 0.28)", tag: "#085041" },
  background: { fill: "rgba(156, 152, 143, 0.22)", tag: "#6B6862" },
};

export const FALLBACK_HIGHLIGHT = { fill: "rgba(59, 122, 100, 0.22)", tag: "#3B7A64" };
