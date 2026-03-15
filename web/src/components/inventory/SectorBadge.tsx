import { type FC } from 'react';
import { cn } from '@/lib/utils';
import { normalizeSector } from '@/lib/formatters';

interface SectorBadgeProps {
  sector?: string | null;
  className?: string;
}

export const SectorBadge: FC<SectorBadgeProps> = ({ sector, className }) => {
  const normalized = normalizeSector(sector);
  
  let colorClass = "bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300 border-slate-200 dark:border-slate-700"; // Fallback / INDEFINIDO
  let label = normalized;

  if (normalized.includes("TI")) {
     colorClass = "bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300 border-blue-200 dark:border-blue-800/60";
  } else if (normalized.includes("MANUTEN")) {
     colorClass = "bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300 border-orange-200 dark:border-orange-800/60";
     label = "MANUTENÇÃO";
  }

  return (
    <span className={cn("inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide border whitespace-nowrap", colorClass, className)}>
      {label}
    </span>
  );
};
