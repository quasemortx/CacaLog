import { type FC } from 'react';
import { cn } from '@/lib/utils';
import { normalizeStatus } from '@/lib/formatters';

interface StatusBadgeProps {
  status?: string | null;
  className?: string;
}

export const StatusBadge: FC<StatusBadgeProps> = ({ status, className }) => {
  const normalized = normalizeStatus(status);
  
  let colorClass = "bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300 border-slate-200 dark:border-slate-700"; // Fallback Neutral
  let label = normalized;

  switch (normalized) {
    case "OK":
      colorClass = "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300 border-green-200 dark:border-green-800/60";
      break;
    case "PENDENTE":
      colorClass = "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800/60";
      break;
    case "ERRO":
      colorClass = "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300 border-red-200 dark:border-red-800/60";
      break;
    case "INCOMPATIVEL":
    case "INCOMPATÍVEL":
      colorClass = "bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300 border-orange-200 dark:border-orange-800/60";
      label = "INCOMPATÍVEL";
      break;
    case "NAO_AVALIADO":
    case "NÃO_AVALIADO":
    case "NÃO AVALIADO":
      colorClass = "bg-slate-100 text-slate-600 dark:bg-slate-800/60 dark:text-slate-400 border-slate-200 dark:border-slate-700/60";
      label = "NÃO AVALIADO";
      break;
    case "ATUALIZANDO":
      colorClass = "bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300 border-blue-200 dark:border-blue-800/60";
      break;
  }

  return (
    <span className={cn("inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide border whitespace-nowrap", colorClass, className)}>
      {label}
    </span>
  );
};
