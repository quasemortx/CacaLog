import { type FC } from 'react';
import type { InventoryItem } from '@/types/inventory';
import { StatusBadge } from './StatusBadge';
import { SectorBadge } from './SectorBadge';
import { formatDate } from '@/lib/formatters';
import { EmptyState } from '@/components/common/EmptyState';

interface InventoryTableProps {
  items: InventoryItem[];
  onRowClick: (item: InventoryItem) => void;
  selectedItemId?: string;
}

export const InventoryTable: FC<InventoryTableProps> = ({ items, onRowClick, selectedItemId }) => {
  if (items.length === 0) {
    return <EmptyState message="Nenhuma máquina encontrada nos filtros indicados." />;
  }

  return (
    <div className="min-w-full inline-block align-middle pb-16">
      <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
        <thead className="bg-slate-50 dark:bg-slate-900 sticky top-0 shadow-sm z-10">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Local ID</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Sala / Ambiente</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Setor</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Observação</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Atualizado Em</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200 dark:divide-slate-800 bg-white dark:bg-slate-950">
          {items.map((item, i) => {
             const key = item.local_id || `temp-${i}`;
             const isSelected = key === selectedItemId;
             return (
               <tr 
                  key={key} 
                  onClick={() => onRowClick(item)}
                  className={`cursor-pointer transition-colors ${
                    isSelected 
                      ? "bg-indigo-50/70 dark:bg-indigo-900/40" 
                      : "hover:bg-slate-50 dark:hover:bg-slate-900/40"
                  }`}
               >
                 <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-indigo-700 dark:text-indigo-400">
                   {item.local_id || "—"}
                 </td>
                 <td className="px-6 py-4 whitespace-nowrap">
                   <div className="text-sm font-medium text-slate-900 dark:text-slate-100">{item.Sala || "—"}</div>
                   <div className="text-xs text-slate-500">{item.TipoAmbiente || "SALA"}</div>
                 </td>
                 <td className="px-6 py-4 whitespace-nowrap">
                   <StatusBadge status={item.Status} />
                 </td>
                 <td className="px-6 py-4 whitespace-nowrap">
                   <SectorBadge sector={item.Setor} />
                 </td>
                 <td className="px-6 py-4">
                   <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2 max-w-sm" title={item.Observacao}>
                      {item.Observacao || "—"}
                   </p>
                 </td>
                 <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-500 dark:text-slate-400">
                   {formatDate(item.UltimaAtualizacao)}
                 </td>
               </tr>
             )
          })}
        </tbody>
      </table>
    </div>
  );
};
