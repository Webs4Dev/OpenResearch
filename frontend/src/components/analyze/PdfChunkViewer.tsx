import { useMemo, useState, useEffect, useRef } from "react";
import { Document, Page } from "react-pdf";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { RelevantChunk } from "../../api/types";
import { CHUNK_HIGHLIGHT_COLORS, FALLBACK_HIGHLIGHT } from "../common/ChunkTypeBadge";
import "react-pdf/dist/Page/TextLayer.css";

interface PdfChunkViewerProps {
  file: File;
  chunks: RelevantChunk[];
  activeChunkId: number | null;
  onChunkClick: (chunkId: number) => void;
}

function escapeHtml(value: string) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

export function PdfChunkViewer({ file, chunks, activeChunkId, onChunkClick }: PdfChunkViewerProps) {
  const [numPages, setNumPages] = useState<number | null>(null);
  const [pageNumber, setPageNumber] = useState<number>(chunks[0]?.page_no ?? 1);

  // Render at the container's actual pixel width instead of a fixed value.
  // react-pdf already multiplies this by devicePixelRatio internally, so a
  // wider container gives sharper text, not just a bigger box.
  const containerRef = useRef<HTMLDivElement>(null);
  const [containerWidth, setContainerWidth] = useState(420);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const observer = new ResizeObserver((entries) => {
      const width = entries[0]?.contentRect.width;
      if (width) setContainerWidth(Math.floor(width));
    });
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  // Jump to whichever page the active chunk lives on.
  useEffect(() => {
    const active = chunks.find((c) => c.chunk_id === activeChunkId);
    if (active?.page_no) setPageNumber(active.page_no);
  }, [activeChunkId, chunks]);

  const pageChunks = useMemo(
    () => chunks.filter((c) => c.page_no === pageNumber && c.chunk_text),
    [chunks, pageNumber]
  );

  // react-pdf calls this per text-layer span. We wrap a span text in <mark>
  // if it is a substring of one of this page relevant chunk texts -- a
  // heuristic that works well since chunk_text is the concatenation of many
  // such spans. This is a stand-in for real bounding-box highlighting; see
  // the README note about adding bounding boxes server-side for pixel-exact
  // highlights instead of text-containment matching.
  const customTextRenderer = ({ str }: { str: string }) => {
    const trimmed = str.trim();
    if (trimmed.length < 4) return escapeHtml(str);

    const match = pageChunks.find((c) => c.chunk_text?.includes(trimmed));
    if (!match) return escapeHtml(str);

    const colors = CHUNK_HIGHLIGHT_COLORS[match.chunk_type.toLowerCase()] ?? FALLBACK_HIGHLIGHT;
    const isActive = match.chunk_id === activeChunkId;
    const outline = isActive ? `outline:2px solid ${colors.tag};outline-offset:1px;` : "";
    return `<mark data-chunk-id="${match.chunk_id}" style="background:${colors.fill};border-radius:2px;${outline}">${escapeHtml(
      str
    )}</mark>`;
  };

  return (
    <div>
      <div className="mb-1.5 flex items-center justify-between">
        <button
          className="btn-secondary px-2 py-1 text-xs"
          disabled={pageNumber <= 1}
          onClick={() => setPageNumber((p) => Math.max(1, p - 1))}
        >
          <ChevronLeft size={14} />
        </button>
        <span className="text-xs text-text-secondary">
          Page {pageNumber} of {numPages ?? "..."}
        </span>
        <button
          className="btn-secondary px-2 py-1 text-xs"
          disabled={!numPages || pageNumber >= numPages}
          onClick={() => setPageNumber((p) => (numPages ? Math.min(numPages, p + 1) : p))}
        >
          <ChevronRight size={14} />
        </button>
      </div>

      <div
        ref={containerRef}
        className="overflow-auto rounded-lg border border-border bg-surface-2"
        onClick={(e) => {
          const target = (e.target as HTMLElement).closest("mark[data-chunk-id]");
          const id = target?.getAttribute("data-chunk-id");
          if (id) onChunkClick(Number(id));
        }}
      >
        <Document
          file={file}
          onLoadSuccess={({ numPages: n }) => setNumPages(n)}
          loading={<p className="p-6 text-sm text-text-secondary">Loading PDF...</p>}
          error={<p className="p-6 text-sm text-red-600">Could not load this PDF.</p>}
        >
          <Page
            pageNumber={pageNumber}
            width={containerWidth || 420}
            customTextRenderer={customTextRenderer}
            renderAnnotationLayer={false}
          />
        </Document>
      </div>
    </div>
  );
}