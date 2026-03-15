import { type FC } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { useStats } from "@/hooks/useStats";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";

export const DashboardPage: FC = () => {
  const { data, isLoading, isError, error } = useStats();

  let content;

  if (isLoading) {
    content = <LoadingState message="Carregando estatísticas da API..." />;
  } else if (isError) {
    content = <ErrorState error={error as Error} />;
  } else if (data) {
    const errorOrPendingCount = 
      (data.by_status["PENDENTE"] || 0) + 
      (data.by_status["ERRO"] || 0) + 
      (data.by_status["INCOMPATÍVEL"] || 0);
      
    const okCount = data.by_status["OK"] || 0;
    const coverage = data.total > 0 ? ((okCount / data.total) * 100).toFixed(1) : "0.0";

    content = (
      <>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-950">
            <h3 className="text-sm font-medium text-slate-500">Total Inventariado</h3>
            <div className="mt-2 text-2xl font-bold">{data.total}</div>
          </div>
          <div className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-950">
            <h3 className="text-sm font-medium text-slate-500">Com Erro/Pendente</h3>
            <div className="mt-2 text-2xl font-bold">{errorOrPendingCount}</div>
          </div>
          <div className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-950">
            <h3 className="text-sm font-medium text-slate-500">Máquinas OK</h3>
            <div className="mt-2 text-2xl font-bold">{okCount}</div>
          </div>
          <div className="rounded-xl border bg-white p-6 shadow-sm dark:bg-slate-950">
            <h3 className="text-sm font-medium text-slate-500">Cobertura (OK)</h3>
            <div className="mt-2 text-2xl font-bold">{coverage}%</div>
          </div>
        </div>

        <div className="mt-8 rounded-xl border bg-white shadow-sm dark:bg-slate-950 overflow-hidden">
          <div className="p-6 border-b">
            <h3 className="text-lg font-medium">Distribuição por Status</h3>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {Object.entries(data.by_status).map(([status, count]) => (
                <div key={status} className="border p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                  <span className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">{status}</span>
                  <span className="block mt-1 text-xl font-bold text-slate-700 dark:text-slate-200">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {Object.keys(data.by_setor).length > 0 && (
          <div className="mt-8 rounded-xl border bg-white shadow-sm dark:bg-slate-950 overflow-hidden">
            <div className="p-6 border-b">
              <h3 className="text-lg font-medium">Distribuição por Setor</h3>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(data.by_setor).map(([setor, count]) => (
                  <div key={setor} className="border p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                    <span className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">{setor}</span>
                    <span className="block mt-1 text-xl font-bold text-slate-700 dark:text-slate-200">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </>
    );
  }

  return <AppShell title="Dashboard">{content}</AppShell>;
};
