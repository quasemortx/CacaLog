import { type FC, type Dispatch, type SetStateAction } from "react";
import { Search, X, Calendar } from "lucide-react";

export type PeriodFilter = "all" | "today" | "7days" | "30days";

export interface HistoryFilterState {
  search: string;
  status: string;
  local_id: string;
  period: PeriodFilter;
}

interface HistoryFiltersProps {
  filters: HistoryFilterState;
  setFilters: Dispatch<SetStateAction<HistoryFilterState>>;
  totalItems: number;
  filteredItemsCount: number;
  uniqueStatuses: string[];
  uniqueLocalIds: string[];
}

export const HistoryFilters: FC<HistoryFiltersProps> = ({
  filters,
  setFilters,
  totalItems,
  filteredItemsCount,
  uniqueStatuses,
  uniqueLocalIds,
}) => {
  const handleClear = () => {
    setFilters({
      search: "",
      status: "",
      local_id: "",
      period: "all",
    });
  };

  const hasFilters = filters.search !== "" || filters.status !== "" || filters.local_id !== "" || filters.period !== "all";

  return (
    <div className="p-4 border-b bg-white dark:bg-slate-950 space-y-4">
      <div className="flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-4 w-4 text-slate-400" />
          </div>
          <input
            type="text"
            placeholder="Buscar em mensagem, ID, responsável..."
            className="h-10 w-full pl-9 pr-4 rounded-md border text-sm bg-slate-50 dark:bg-slate-900 dark:border-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={filters.search}
            onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
          />
        </div>
        
        {hasFilters && (
          <button 
            onClick={handleClear}
            className="h-10 px-4 flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200 transition-colors bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 rounded-md"
          >
            <X className="h-4 w-4" />
            Limpar Filtros
          </button>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <select 
          className="h-9 px-3 rounded-md border text-sm bg-white dark:bg-slate-900 dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 min-w-[140px]"
          value={filters.status}
          onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value }))}
        >
          <option value="">Todos os Status</option>
          {uniqueStatuses.map(s => <option key={s} value={s}>{s}</option>)}
        </select>

        <select 
          className="h-9 px-3 rounded-md border text-sm bg-white dark:bg-slate-900 dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 min-w-[140px]"
          value={filters.local_id}
          onChange={(e) => setFilters(prev => ({ ...prev, local_id: e.target.value }))}
        >
          <option value="">Todos os Locais</option>
          {uniqueLocalIds.map(id => <option key={id} value={id}>{id}</option>)}
        </select>

        <div className="relative inline-flex items-center">
          <div className="absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none">
             <Calendar className="h-3.5 w-3.5 text-slate-400" />
          </div>
          <select 
            className="h-9 pl-8 pr-3 rounded-md border text-sm bg-white dark:bg-slate-900 dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 min-w-[140px]"
            value={filters.period}
            onChange={(e) => setFilters(prev => ({ ...prev, period: e.target.value as PeriodFilter }))}
          >
            <option value="all">Todo o Período</option>
            <option value="today">Hoje</option>
            <option value="7days">Últimos 7 dias</option>
            <option value="30days">Últimos 30 dias</option>
          </select>
        </div>
      </div>
      
      <div className="text-sm font-medium text-slate-500">
        Exibindo {filteredItemsCount} de {totalItems} eventos no log
      </div>
    </div>
  );
};
