import { type FC } from "react";
import { AppShell } from "@/components/layout/AppShell";

export const HistoryPage: FC = () => {
  return (
    <AppShell title="Histórico">
      <div className="rounded-xl border bg-white shadow-sm dark:bg-slate-950 overflow-hidden">
        <div className="p-4 border-b">
          <h3 className="text-lg font-medium">Log de Atualizações</h3>
          <p className="text-sm text-slate-500">Histórico de mensagens do WhatsApp e mudanças de status.</p>
        </div>
        <div className="p-12 text-center text-slate-500">
          <p>O feed do webhook de histórico será exibido aqui em formato de timeline.</p>
        </div>
      </div>
    </AppShell>
  );
};
