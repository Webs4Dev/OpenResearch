import { useRef, useState } from "react";
import { Upload } from "lucide-react";

interface UploadDropzoneProps {
  onFileSelected: (file: File) => void;
}

export function UploadDropzone({ onFileSelected }: UploadDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFiles = (files: FileList | null) => {
    const file = files?.[0];
    if (file && file.type === "application/pdf") {
      onFileSelected(file);
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={() => inputRef.current?.click()}
      onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragOver(true);
      }}
      onDragLeave={() => setIsDragOver(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragOver(false);
        handleFiles(e.dataTransfer.files);
      }}
      className={`cursor-pointer rounded-xl border border-dashed px-6 py-8 text-center transition-colors ${
        isDragOver ? "border-border-accent bg-surface-1" : "border-border-strong"
      }`}
    >
      <Upload size={22} className="mx-auto" />
      <p className="mt-2 text-sm">Drop a PDF here or browse</p>
      <p className="mt-0.5 text-xs text-text-muted">One file at a time</p>
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
    </div>
  );
}
