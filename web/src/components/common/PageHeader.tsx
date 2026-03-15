import { type FC } from "react";

interface PageHeaderProps {
  title: string;
}

export const PageHeader: FC<PageHeaderProps> = ({ title }) => {
  return (
    <header className="h-16 flex items-center px-6 border-b bg-white dark:bg-slate-950 sticky top-0 z-10 w-full">
      <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">
        {title}
      </h2>
    </header>
  );
};
