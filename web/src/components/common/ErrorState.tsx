import { type FC } from "react";
import { ServerCrash } from "lucide-react";

interface ErrorStateProps {
  error?: Error | null;
  message?: string;
}

export const ErrorState: FC<ErrorStateProps> = ({ error, message = "Ocorreu um erro ao carregar os dados." }) => {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-4 text-center">
      <div className="w-16 h-16 bg-red-50 dark:bg-red-900/20 rounded-full flex items-center justify-center mb-4 border border-red-100 dark:border-red-900/50">
         <ServerCrash className="h-8 w-8 text-red-500 dark:text-red-400" />
      </div>
      <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mb-1">{message}</h3>
      {error && <p className="text-sm text-slate-500 dark:text-slate-400 max-w-sm mt-1">{error.message}</p>}
    </div>
  );
};
