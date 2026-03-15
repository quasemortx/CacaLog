import { type FC } from "react";
import { ServerCrash } from "lucide-react";

interface ErrorStateProps {
  error?: Error | null;
  message?: string;
}

export const ErrorState: FC<ErrorStateProps> = ({ error, message = "Ocorreu um erro ao carregar os dados." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-red-500">
      <ServerCrash className="h-12 w-12 mb-4" />
      <h3 className="text-lg font-medium mb-2">{message}</h3>
      {error && <p className="text-sm opacity-80">{error.message}</p>}
    </div>
  );
};
