import { RefreshCw } from "lucide-react";

export function Spinner({ label }: { label: string }) {
  return (
    <div className="flex flex-col items-center gap-2 py-10 text-sm text-text-secondary">
      <RefreshCw size={20} className="animate-spin" />
      <p>{label}</p>
    </div>
  );
}
