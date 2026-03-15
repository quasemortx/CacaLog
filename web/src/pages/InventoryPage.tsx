import { type FC, useState, useMemo } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { useInventory } from "@/hooks/useInventory";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { type FilterState, InventoryFilters } from "@/components/inventory/InventoryFilters";
import { InventoryTable } from "@/components/inventory/InventoryTable";
import { InventoryDetailDrawer } from "@/components/inventory/InventoryDetailDrawer";
import type { InventoryItem } from "@/types/inventory";

export const InventoryPage: FC = () => {
  const { data, isLoading, isError, error } = useInventory();
  
  const [filters, setFilters] = useState<FilterState>({
    search: "",
    status: "",
    setor: "",
    tipoAmbiente: "",
    predio: "",
    andar: "",
  });

  const [selectedItem, setSelectedItem] = useState<InventoryItem | null>(null);

  // Safely default backend parsed items to an empty array
  const rawItems = data?.items || [];

  // 1. Calculate possible unique filter options from the whole dataset provided by the backend.
  const uniqueStatuses = useMemo(() => Array.from(new Set(rawItems.map(i => i.Status || "NÃO AVALIADO"))).sort(), [rawItems]);
  const uniqueSectores = useMemo(() => Array.from(new Set(rawItems.map(i => i.Setor || ""))).sort(), [rawItems]);
  const uniqueAmbientes = useMemo(() => Array.from(new Set(rawItems.map(i => i.TipoAmbiente || "SALA"))).sort(), [rawItems]);
  const uniquePredios = useMemo(() => Array.from(new Set(rawItems.map(i => String(i.Predio || "")))).filter(Boolean).sort(), [rawItems]);
  const uniqueAndares = useMemo(() => Array.from(new Set(rawItems.map(i => String(i.Andar || "")))).filter(Boolean).sort(), [rawItems]);

  // 2. Client-side filtering logic
  const filteredItems = useMemo(() => {
    return rawItems.filter(item => {
      // Free Text Search
      if (filters.search) {
        const searchRegex = new RegExp(filters.search.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), "i");
        const searchableText = `${item.local_id || ""} ${item.Sala || ""} ${item.Modelo || ""} ${item.Observacao || ""}`;
        if (!searchRegex.test(searchableText)) return false;
      }

      // Exact Select Matches
      if (filters.status && (item.Status || "NÃO AVALIADO") !== filters.status) return false;
      if (filters.setor && (item.Setor || "") !== filters.setor) return false;
      if (filters.tipoAmbiente && (item.TipoAmbiente || "SALA") !== filters.tipoAmbiente) return false;
      if (filters.predio && String(item.Predio || "") !== filters.predio) return false;
      if (filters.andar && String(item.Andar || "") !== filters.andar) return false;

      return true;
    });
  }, [rawItems, filters]);

  return (
    <AppShell title="Inventário">
      <div className="rounded-xl border bg-white shadow-sm dark:bg-slate-950 flex flex-col h-[80vh] min-h-[600px] overflow-hidden relative">
        
        {(!isLoading && !isError) && (
          <InventoryFilters 
            filters={filters}
            setFilters={setFilters}
            totalItems={rawItems.length}
            filteredItemsCount={filteredItems.length}
            uniqueStatuses={uniqueStatuses}
            uniqueSectores={uniqueSectores}
            uniqueAmbientes={uniqueAmbientes}
            uniquePredios={uniquePredios}
            uniqueAndares={uniqueAndares}
          />
        )}
        
        <div className="flex-1 overflow-auto bg-slate-50/50 dark:bg-slate-950/50 relative">
          {isLoading && <LoadingState message="Buscando lista de inventário..." />}
          {isError && <ErrorState error={error as Error} />}
          
          {!isLoading && !isError && (
             <InventoryTable 
               items={filteredItems} 
               onRowClick={(item) => setSelectedItem(item)}
               selectedItemId={selectedItem?.local_id}
             />
          )}
        </div>
      </div>

      {/* Floating Detail Sidebar Drawer */}
      <InventoryDetailDrawer 
         item={selectedItem} 
         onClose={() => setSelectedItem(null)} 
      />
    </AppShell>
  );
};
