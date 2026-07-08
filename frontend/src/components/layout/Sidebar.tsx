import { NavLink } from "react-router-dom";
import { Home, Search, FileText } from "lucide-react";

const navItems = [
  { to: "/", label: "Dashboard", icon: Home, end: true },
  { to: "/search", label: "Search papers", icon: Search, end: false },
  { to: "/workspace", label: "PDF workspace", icon: FileText, end: false },
];

export function Sidebar() {
  return (
    <aside className="flex w-56 shrink-0 flex-col border-r border-border bg-surface-1 px-3 py-4">
      <div className="mb-6 px-2 text-[15px] font-medium">OpenResearch</div>
      <nav className="flex flex-col gap-1">
        {navItems.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-2 rounded px-2.5 py-2 text-sm transition-colors ${
                isActive
                  ? "bg-surface-2 font-medium text-text-primary"
                  : "text-text-secondary hover:bg-surface-2/60"
              }`
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
