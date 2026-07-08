import { create } from "zustand";
import type { PDFAnalysisResponse, PDFIngestResponse } from "../api/types";

export interface ChatTurn {
  id: string;
  question: string;
  answer?: string;
  confidence?: number;
  foundInPages?: number[];
  status: "pending" | "done" | "error";
  errorMessage?: string;
}

interface WorkspaceState {
  file: File | null;
  ingestResult: PDFIngestResponse | null;
  analysisResult: PDFAnalysisResponse | null;
  chatHistory: ChatTurn[];

  setFile: (file: File | null) => void;
  setIngestResult: (result: PDFIngestResponse | null) => void;
  setAnalysisResult: (result: PDFAnalysisResponse | null) => void;
  addChatTurn: (turn: ChatTurn) => void;
  updateChatTurn: (id: string, patch: Partial<ChatTurn>) => void;
  reset: () => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  file: null,
  ingestResult: null,
  analysisResult: null,
  chatHistory: [],

  setFile: (file) => set({ file }),
  setIngestResult: (result) => set({ ingestResult: result }),
  setAnalysisResult: (result) => set({ analysisResult: result }),
  addChatTurn: (turn) =>
    set((state) => ({ chatHistory: [...state.chatHistory, turn] })),
  updateChatTurn: (id, patch) =>
    set((state) => ({
      chatHistory: state.chatHistory.map((t) => (t.id === id ? { ...t, ...patch } : t)),
    })),
  reset: () =>
    set({ file: null, ingestResult: null, analysisResult: null, chatHistory: [] }),
}));
