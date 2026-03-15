import { type FC } from "react";
import { SearchX } from "lucide-react";

interface EmptyStateProps {
  message?: string;
}

export const EmptyState: FC<EmptyStateProps> = ({ message = "Nenhum resultado encontrado." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-slate-400">
      <SearchX className="h-12 w-12 mb-4" />
      <p className="text-sm">{message}</p>
    </div>
  );
};
