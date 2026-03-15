import { type FC } from "react";
import { NavLink } from "react-router-dom";
import { LayoutDashboard, PackageSearch, History } from "lucide-react";
import { cn } from "@/lib/utils";

export const AppSidebar: FC = () => {
  const links = [
    { to: "/", icon: LayoutDashboard, label: "Dashboard" },
    { to: "/inventory", icon: PackageSearch, label: "Inventário" },
    { to: "/history", icon: History, label: "Histórico" },
  ];

  return (
    <aside className="w-64 flex-shrink-0 border-r bg-white dark:bg-slate-950 hidden md:flex md:flex-col">
      <div className="h-16 flex items-center px-6 border-b">
        <h1 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <PackageSearch className="h-6 w-6 text-indigo-600" />
          CaçaLog
        </h1>
      </div>
      <nav className="flex-1 overflow-y-auto px-4 py-6 space-y-2">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-md transition-colors text-sm font-medium",
                isActive
                  ? "bg-indigo-50 text-indigo-700 dark:bg-indigo-950/50 dark:text-indigo-300"
                  : "text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800"
              )
            }
          >
            <link.icon className="h-5 w-5" />
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};
