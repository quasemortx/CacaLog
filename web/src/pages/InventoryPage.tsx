import { type FC } from "react";
import { AppShell } from "@/components/layout/AppShell";

export const InventoryPage: FC = () => {
  return (
    <AppShell title="Inventário">
      <div className="rounded-xl border bg-white shadow-sm dark:bg-slate-950 flex flex-col h-[600px]">
        <div className="p-4 border-b flex items-center justify-between">
          <div className="flex gap-2">
            <input 
              type="text" 
              placeholder="Buscar por local, modelo..."
              className="h-9 px-3 border rounded-md text-sm w-64"
              disabled
            />
            <select className="h-9 px-3 border rounded-md text-sm bg-white" disabled>
              <option>Status</option>
            </select>
          </div>
          <button className="h-9 px-4 bg-indigo-600 text-white rounded-md text-sm font-medium hover:bg-indigo-700 disabled:opacity-50" disabled>
            Sincronizar
          </button>
        </div>
        
        <div className="flex-1 flex items-center justify-center p-12 text-center text-slate-500">
          <div>
            <p className="mb-2">A tabela de inventário será carregada via API aqui.</p>
            <p className="text-sm">Aguardando integração futura.</p>
          </div>
        </div>
      </div>
    </AppShell>
  );
};
