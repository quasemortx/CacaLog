import { type FC } from 'react';
import { cn } from '@/lib/utils';
import { normalizeStatus } from '@/lib/formatters';

interface StatusBadgeProps {
  status?: string | null;
  className?: string;
}

export const StatusBadge: FC<StatusBadgeProps> = ({ status, className }) => {
  const normalized = normalizeStatus(status);
  
  let colorClass = "bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300"; // Fallback Neutral
  let label = normalized;

  switch (normalized) {
    case "OK":
      colorClass = "bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300";
      break;
    case "PENDENTE":
      colorClass = "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300";
      break;
    case "ERRO":
      colorClass = "bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300";
      break;
    case "INCOMPATIVEL":
    case "INCOMPATÍVEL":
      colorClass = "bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-300";
      label = "INCOMPATÍVEL";
      break;
    case "NAO_AVALIADO":
    case "NÃO_AVALIADO":
    case "NÃO AVALIADO":
      colorClass = "bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-400";
      label = "NÃO AVALIADO";
      break;
    case "ATUALIZANDO":
      colorClass = "bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300";
      break;
  }

  return (
    <span className={cn("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold whitespace-nowrap", colorClass, className)}>
      {label}
    </span>
  );
};
