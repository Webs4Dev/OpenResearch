import { useNavigate } from "react-router-dom";
import { Search, FileText } from "lucide-react";

export function Dashboard() {
  const navigate = useNavigate();

  return (
    <div>
      <p className="mb-1 text-sm text-text-muted">Welcome back</p>
      <h1 className="mb-6 text-2xl font-medium">What are you working on today</h1>

      <div className="grid grid-cols-2 gap-3">
        <div className="card cursor-pointer hover:border-border-strong" onClick={() => navigate("/search")}>
          <Search size={20} />
          <p className="mb-1 mt-2 font-medium">Search papers</p>
          <p className="mb-3 text-sm text-text-secondary">
            Find and rank papers against your project.
          </p>
          <button className="btn-secondary">Open search</button>
        </div>

        <div className="card cursor-pointer hover:border-border-strong" onClick={() => navigate("/workspace")}>
          <FileText size={20} />
          <p className="mb-1 mt-2 font-medium">PDF workspace</p>
          <p className="mb-3 text-sm text-text-secondary">
            Upload a paper, then analyse it or ask it questions.
          </p>
          <button className="btn-secondary">Open workspace</button>
        </div>
      </div>
    </div>
  );
}
