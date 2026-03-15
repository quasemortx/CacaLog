import { type FC, useState, useMemo } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { useHistory } from "@/hooks/useHistory";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { Clock } from "lucide-react";
import { type HistoryFilterState, HistoryFilters } from "@/components/history/HistoryFilters";
import { HistoryTimeline } from "@/components/history/HistoryTimeline";
import { parseDateSafely } from "@/lib/formatters";

export const HistoryPage: FC = () => {
  const { data, isLoading, isError, error } = useHistory();

  const [filters, setFilters] = useState<HistoryFilterState>({
    search: "",
    status: "",
    local_id: "",
    period: "all",
  });

  const rawItems = data?.items || [];

  const uniqueStatuses = useMemo(() => Array.from(new Set(rawItems.map(i => i.status || "EVENTO"))).sort(), [rawItems]);
  const uniqueLocalIds = useMemo(() => Array.from(new Set(rawItems.map(i => i.local_id || ""))).filter(Boolean).sort(), [rawItems]);

  const filteredItems = useMemo(() => {
    // API sends history as appended, so typically latest is at the end or reversed. 
    // Usually it's read top to bottom in Google Sheets which means oldest first.
    // So we reverse it to guarantee newest first.
    let result = [...rawItems].reverse();

    return result.filter(item => {
      if (filters.search) {
        const searchRegex = new RegExp(filters.search.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "i");
        const searchableText = `${item.local_id || ""} ${item.status || ""} ${item.observacao || ""} ${item.responsavel || ""} ${item.contato || ""} ${item.mensagem_original || ""}`;
        if (!searchRegex.test(searchableText)) return false;
      }

      if (filters.status && (item.status || "EVENTO") !== filters.status) return false;
      if (filters.local_id && (item.local_id || "") !== filters.local_id) return false;

      if (filters.period !== "all") {
        const itemDate = parseDateSafely(item.timestamp);
        if (itemDate) {
          const now = new Date();
          const msInDay = 24 * 60 * 60 * 1000;
          // Set to start of day for accurate day diffs if needed, or approximate with Math.floor
          // Taking simplified diff based on direct ms span
          const diffMs = now.getTime() - itemDate.getTime();
          const diffDays = diffMs / msInDay;
          
          if (filters.period === "today") {
            const isToday = itemDate.getDate() === now.getDate() && 
                            itemDate.getMonth() === now.getMonth() && 
                            itemDate.getFullYear() === now.getFullYear();
            if (!isToday) return false;
          } else if (filters.period === "7days") {
            if (diffDays > 7) return false;
          } else if (filters.period === "30days") {
            if (diffDays > 30) return false;
          }
        }
      }

      return true;
    });
  }, [rawItems, filters]);

  return (
    <AppShell title="Histórico">
      <div className="rounded-xl border bg-white shadow-sm dark:bg-slate-950 overflow-hidden flex flex-col h-[80vh] min-h-[600px] relative">
        <div className="p-4 border-b bg-white dark:bg-slate-950/80">
          <h3 className="text-lg font-medium flex gap-2 items-center">
            <Clock className="w-5 h-5 text-indigo-500" />
            Log de Atualizações
          </h3>
          <p className="text-sm text-slate-500 mt-1">
            Histórico completo de eventos auditados pelo CaçaLog.
          </p>
        </div>

        {(!isLoading && !isError) && (
           <HistoryFilters 
             filters={filters}
             setFilters={setFilters}
             totalItems={rawItems.length}
             filteredItemsCount={filteredItems.length}
             uniqueStatuses={uniqueStatuses}
             uniqueLocalIds={uniqueLocalIds}
           />
        )}

        <div className="flex-1 overflow-y-auto bg-slate-50/50 dark:bg-slate-900/10 p-4 md:p-6">
          {isLoading && <LoadingState message="Lendo arquivos de log central..." />}
          {isError && <ErrorState error={error as Error} />}
          
          {!isLoading && !isError && (
            <HistoryTimeline items={filteredItems} />
          )}
        </div>
      </div>
    </AppShell>
  );
};
