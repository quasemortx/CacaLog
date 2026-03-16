import { type FC } from "react";

interface PageHeaderProps {
  title: string;
  description?: string;
}

export const PageHeader: FC<PageHeaderProps> = ({ title, description }) => {
  return (
    <header className="py-6 px-6 border-b bg-white dark:bg-slate-950 w-full mb-6 rounded-b-xl shadow-sm">
      <h2 className="text-xl font-bold text-slate-800 dark:text-slate-100">
        {title}
      </h2>
      {description && (
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          {description}
        </p>
      )}
    </header>
  );
};
