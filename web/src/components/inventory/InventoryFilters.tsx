import { type FC, type Dispatch, type SetStateAction } from "react";
import { Search, X } from "lucide-react";

export interface FilterState {
  search: string;
  status: string;
  setor: string;
  tipoAmbiente: string;
  predio: string;
  andar: string;
}

interface InventoryFiltersProps {
  filters: FilterState;
  setFilters: Dispatch<SetStateAction<FilterState>>;
  totalItems: number;
  filteredItemsCount: number;
  uniqueStatuses: string[];
  uniqueSectores: string[];
  uniqueAmbientes: string[];
  uniquePredios: string[];
  uniqueAndares: string[];
}

export const InventoryFilters: FC<InventoryFiltersProps> = ({
  filters,
  setFilters,
  totalItems,
  filteredItemsCount,
  uniqueStatuses,
  uniqueSectores,
  uniqueAmbientes,
  uniquePredios,
  uniqueAndares,
}) => {
  const handleClear = () => {
    setFilters({
      search: "",
      status: "",
      setor: "",
      tipoAmbiente: "",
      predio: "",
      andar: "",
    });
  };

  const hasFilters = Object.values(filters).some(val => val !== "");

  return (
    <div className="p-4 border-b bg-white dark:bg-slate-950 space-y-4">
      <div className="flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-4 w-4 text-slate-400" />
          </div>
          <input
            type="text"
            placeholder="Buscar por local, sala, modelo ou observação..."
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

      <div className="flex flex-wrap gap-3">
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
          value={filters.setor}
          onChange={(e) => setFilters(prev => ({ ...prev, setor: e.target.value }))}
        >
          <option value="">Todos os Setores</option>
          {uniqueSectores.map(s => <option key={s} value={s}>{s === "" ? "INDEFINIDO" : s}</option>)}
        </select>

        <select 
          className="h-9 px-3 rounded-md border text-sm bg-white dark:bg-slate-900 dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 min-w-[140px]"
          value={filters.tipoAmbiente}
          onChange={(e) => setFilters(prev => ({ ...prev, tipoAmbiente: e.target.value }))}
        >
          <option value="">Todos Ambientes</option>
          {uniqueAmbientes.map(a => <option key={a} value={a}>{a}</option>)}
        </select>

        <select 
          className="h-9 px-3 rounded-md border text-sm bg-white dark:bg-slate-900 dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 min-w-[140px]"
          value={filters.predio}
          onChange={(e) => setFilters(prev => ({ ...prev, predio: e.target.value }))}
        >
          <option value="">Todos os Prédios</option>
          {uniquePredios.map(p => <option key={p} value={p}>Prédio {p}</option>)}
        </select>

        <select 
          className="h-9 px-3 rounded-md border text-sm bg-white dark:bg-slate-900 dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 min-w-[140px]"
          value={filters.andar}
          onChange={(e) => setFilters(prev => ({ ...prev, andar: e.target.value }))}
        >
          <option value="">Todos os Andares</option>
          {uniqueAndares.map(a => <option key={a} value={a}>{a}º Andar</option>)}
        </select>

      </div>
      
      <div className="text-sm font-medium text-slate-500">
        Exibindo {filteredItemsCount} de {totalItems} itens
      </div>
    </div>
  );
};
