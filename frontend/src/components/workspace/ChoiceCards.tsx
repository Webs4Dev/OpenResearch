import { Target, MessageCircle, RefreshCw } from "lucide-react";

interface ChoiceCardsProps {
  filename: string;
  onSwap: () => void;
  onAnalyse: () => void;
  onIngestAndAsk: () => void;
}

export function ChoiceCards({ filename, onSwap, onAnalyse, onIngestAndAsk }: ChoiceCardsProps) {
  return (
    <div>
      <div className="mb-5 flex items-center gap-2.5 rounded bg-surface-1 px-3 py-2.5">
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium">{filename}</p>
          <p className="text-xs text-text-secondary">Ready · choose what to do with it</p>
        </div>
        <button className="btn-secondary px-2.5 py-1.5 text-xs" onClick={onSwap}>
          <RefreshCw size={13} />
          Swap PDF
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="card cursor-pointer hover:border-border-strong" onClick={onAnalyse}>
          <Target size={20} />
          <p className="mb-1 mt-2 font-medium">1. Analyse</p>
          <p className="mb-3 text-sm text-text-secondary">
            Score chunks against your project description and see them highlighted in the PDF.
          </p>
          <button className="btn-secondary">Analyse</button>
        </div>

        <div className="card cursor-pointer hover:border-border-strong" onClick={onIngestAndAsk}>
          <MessageCircle size={20} />
          <p className="mb-1 mt-2 font-medium">2. Ingest and ask</p>
          <p className="mb-3 text-sm text-text-secondary">
            Ingest the paper, then chat with questions scoped only to it.
          </p>
          <button className="btn-secondary">Ingest and ask</button>
        </div>
      </div>
    </div>
  );
}
