import { type FC } from 'react';
import { cn } from '@/lib/utils';
import { normalizeSector } from '@/lib/formatters';

interface SectorBadgeProps {
  sector?: string | null;
  className?: string;
}

export const SectorBadge: FC<SectorBadgeProps> = ({ sector, className }) => {
  const normalized = normalizeSector(sector);
  
  let colorClass = "bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300"; // Fallback / INDEFINIDO
  let label = normalized;

  if (normalized.includes("TI")) {
     colorClass = "bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300";
  } else if (normalized.includes("MANUTEN")) {
     colorClass = "bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-300";
     label = "MANUTENÇÃO";
  }

  return (
    <span className={cn("inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium border whitespace-nowrap", colorClass, className)}>
      {label}
    </span>
  );
};
