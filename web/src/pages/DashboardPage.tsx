import { type FC } from "react";
import { AppShell } from "@/components/layout/AppShell";

export const DashboardPage: FC = () => {
  return (
    <AppShell title="Dashboard">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-950">
          <h3 className="text-sm font-medium text-slate-500">Total Inventariado</h3>
          <div className="mt-2 text-2xl font-bold">---</div>
        </div>
        <div className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-950">
          <h3 className="text-sm font-medium text-slate-500">Com Erro/Pendente</h3>
          <div className="mt-2 text-2xl font-bold">---</div>
        </div>
        <div className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-950">
          <h3 className="text-sm font-medium text-slate-500">Atualizados Hoje</h3>
          <div className="mt-2 text-2xl font-bold">---</div>
        </div>
        <div className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-950">
          <h3 className="text-sm font-medium text-slate-500">Cobertura</h3>
          <div className="mt-2 text-2xl font-bold">---%</div>
        </div>
      </div>

      <div className="mt-8 rounded-xl border bg-white shadow-sm dark:bg-slate-950 overflow-hidden">
        <div className="p-6 border-b">
          <h3 className="text-lg font-medium">Atividades Recentes</h3>
        </div>
        <div className="p-12 text-center text-slate-500">
          <p>Os gráficos e atualizações recentes serão exibidos aqui.</p>
        </div>
      </div>
    </AppShell>
  );
};
