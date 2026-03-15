import { type FC, useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { useInventory } from "@/hooks/useInventory";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";

export const InventoryPage: FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const { data, isLoading, isError, error } = useInventory(
    searchTerm ? { q: searchTerm } : undefined
  );

  return (
    <AppShell title="Inventário">
      <div className="rounded-xl border bg-white shadow-sm dark:bg-slate-950 flex flex-col h-[700px]">
        <div className="p-4 border-b flex items-center justify-between">
          <div className="flex gap-2">
            <input 
              type="text" 
              placeholder="Buscar por local, modelo..."
              className="h-9 px-3 border rounded-md text-sm w-64 bg-slate-50 dark:bg-slate-900"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="text-sm font-medium text-slate-500 px-4">
            {data?.items ? `${data.total} itens` : "0 itens"}
          </div>
        </div>
        
        <div className="flex-1 overflow-auto">
          {isLoading && <LoadingState message="Buscando lista de inventário..." />}
          {isError && <ErrorState error={error as Error} />}
          {!isLoading && !isError && data?.items && data.items.length === 0 && (
            <EmptyState message="Nenhuma máquina encontrada nos filtros indicados." />
          )}
          {!isLoading && !isError && data?.items && data.items.length > 0 && (
             <div className="min-w-full inline-block align-middle">
               <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
                 <thead className="bg-slate-50 dark:bg-slate-900 sticky top-0">
                   <tr>
                     <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Local ID</th>
                     <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
                     <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Setor</th>
                     <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Observação</th>
                     <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Atualizado</th>
                   </tr>
                 </thead>
                 <tbody className="divide-y divide-slate-200 dark:divide-slate-800 bg-white dark:bg-slate-950">
                    {data.items.map((item, i) => (
                      <tr key={item.local_id || i} className="hover:bg-slate-50 dark:hover:bg-slate-900">
                         <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900 dark:text-slate-100">{item.local_id || "-"}</td>
                         <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500 dark:text-slate-400">
                           <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200">
                             {item.Status || "NÃO AVALIADO"}
                           </span>
                         </td>
                         <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500 dark:text-slate-400">{item.Setor || "-"}</td>
                         <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500 dark:text-slate-400 truncate max-w-xs">{item.Observacao || "-"}</td>
                         <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500 dark:text-slate-400">{item.UltimaAtualizacao || "-"}</td>
                      </tr>
                    ))}
                 </tbody>
               </table>
             </div>
          )}
        </div>
      </div>
    </AppShell>
  );
};
