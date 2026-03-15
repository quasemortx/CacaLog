import { type FC } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { useHistory } from "@/hooks/useHistory";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { Clock } from "lucide-react";

export const HistoryPage: FC = () => {
  const { data, isLoading, isError, error } = useHistory();

  return (
    <AppShell title="Histórico">
      <div className="rounded-xl border bg-white shadow-sm dark:bg-slate-950 overflow-hidden flex flex-col h-[700px]">
        <div className="p-4 border-b">
          <h3 className="text-lg font-medium flex gap-2 items-center">
            <Clock className="w-5 h-5 text-indigo-500" />
            Log de Atualizações
          </h3>
          <p className="text-sm text-slate-500 mt-1">
            Histórico de eventos reportados pelo WhatsApp agrupados do mais recente ao antigo.
          </p>
        </div>
        <div className="flex-1 overflow-auto bg-slate-50 dark:bg-slate-900/50 p-6">
          {isLoading && <LoadingState message="Lendo arquivos de log central..." />}
          {isError && <ErrorState error={error as Error} />}
          {!isLoading && !isError && data?.items && data.items.length === 0 && (
            <EmptyState message="O histórico de modificações está vazio." />
          )}
          {!isLoading && !isError && data?.items && data.items.length > 0 && (
             <div className="space-y-4">
                {data.items.slice(0).reverse().map((item, i) => (
                   <div key={i} className="flex gap-4 p-4 rounded-lg border bg-white dark:bg-slate-950 shadow-sm">
                     <div className="flex flex-col items-center gap-1 w-24 flex-shrink-0 text-slate-500 text-xs text-right mt-1">
                        <span className="font-semibold">{item.timestamp?.split(" ")[0] || "-"}</span>
                        <span>{item.timestamp?.split(" ")[1] || "-"}</span>
                     </div>
                     <div className="w-px bg-slate-200 dark:bg-slate-800 relative hidden sm:block">
                        <span className="absolute left-1/2 top-1.5 -translate-x-1/2 w-2 h-2 rounded-full bg-indigo-500 border border-white dark:border-slate-950"></span>
                     </div>
                     <div className="flex-1 space-y-1">
                        <div className="flex justify-between items-start">
                           <span className="font-bold text-slate-800 dark:text-slate-100">{item.local_id || "Geral"}</span>
                           <span className="text-xs bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded text-slate-600 dark:text-slate-300 font-medium">
                              {item.status || "EVENTO"}
                           </span>
                        </div>
                        <p className="text-sm text-slate-600 dark:text-slate-300 break-words">{item.observacao || item.mensagem_original || "-"}</p>
                        <p className="text-xs text-slate-400 mt-2 font-medium flex gap-1">
                          👤 {item.responsavel} {item.contato && `(${item.contato})`}
                        </p>
                     </div>
                   </div>
                ))}
             </div>
          )}
        </div>
      </div>
    </AppShell>
  );
};
