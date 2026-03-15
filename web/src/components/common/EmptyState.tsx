import { type FC } from "react";
import { SearchX } from "lucide-react";

interface EmptyStateProps {
  message?: string;
}

export const EmptyState: FC<EmptyStateProps> = ({ message = "Nenhum resultado encontrado." }) => {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-4 text-center">
      <div className="w-16 h-16 bg-slate-100 dark:bg-slate-800/50 rounded-full flex items-center justify-center mb-4 border border-slate-200 dark:border-slate-800">
         <SearchX className="h-8 w-8 text-slate-400 dark:text-slate-500" />
      </div>
      <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-1">Nada por aqui</h3>
      <p className="text-sm text-slate-500 dark:text-slate-400 max-w-sm">{message}</p>
    </div>
  );
};
