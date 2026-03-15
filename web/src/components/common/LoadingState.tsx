import { type FC } from "react";
import { Loader2 } from "lucide-react";

interface LoadingStateProps {
  message?: string;
}

export const LoadingState: FC<LoadingStateProps> = ({ message = "Carregando dados..." }) => {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-4 text-center">
      <Loader2 className="h-8 w-8 animate-spin text-indigo-500 dark:text-indigo-400 mb-4" />
      <p className="text-sm font-medium text-slate-600 dark:text-slate-400">{message}</p>
    </div>
  );
};
