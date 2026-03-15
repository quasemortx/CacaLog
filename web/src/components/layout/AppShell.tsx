import { type FC, type ReactNode } from "react";
import { AppSidebar } from "./AppSidebar";
import { PageHeader } from "../common/PageHeader";

interface AppShellProps {
  children: ReactNode;
  title: string;
}

export const AppShell: FC<AppShellProps> = ({ children, title }) => {
  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900">
      <AppSidebar />
      <div className="flex-1 flex flex-col">
        <PageHeader title={title} />
        <main className="flex-1 p-6 md:p-8">
          <div className="max-w-6xl mx-auto space-y-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
