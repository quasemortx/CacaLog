import { type FC, useState } from 'react';
import { HistoryStatusBadge } from './HistoryStatusBadge';
import { formatDate } from '@/lib/formatters';
import type { HistoryItem } from '@/types/history';
import { MessageSquare, User, AtSign, ChevronDown, ChevronUp } from 'lucide-react';

interface HistoryTimelineItemProps {
  item: HistoryItem;
}

export const HistoryTimelineItem: FC<HistoryTimelineItemProps> = ({ item }) => {
  const [expanded, setExpanded] = useState(false);
  const formattedDate = formatDate(item.timestamp);
  
  // Extract time from the output of formatDate
  // e.g., "14/05/2024 14:00" -> "14:00", we can just split by space
  let datePart = formattedDate;
  let timePart = "";
  if (formattedDate.includes(" ")) {
     const parts = formattedDate.split(" ");
     datePart = parts[0];
     timePart = parts.slice(1).join(" ");
  }

  return (
    <div className="flex gap-4 md:gap-6 relative group">
      {/* Visual Timeline element */}
      <div className="flex flex-col items-center">
         <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center border-2 border-white dark:border-slate-950 z-10 shadow-sm relative group-hover:border-indigo-100 dark:group-hover:border-indigo-900/50 transition-colors">
            <div className="w-2.5 h-2.5 rounded-full bg-indigo-500" />
         </div>
         {/* Line connecting to next element */}
         <div className="w-px h-full bg-slate-200 dark:bg-slate-800 -mt-2 group-last:bg-transparent" />
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0 pb-8">
        <div className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm hover:shadow transition-shadow">
           <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-2 mb-3">
             <div className="flex flex-wrap items-center gap-3">
               <span className="text-base font-bold text-slate-800 dark:text-slate-100 bg-slate-50 dark:bg-slate-900 px-2 py-0.5 rounded border border-slate-100 dark:border-slate-800">
                 {item.local_id || "SISTEMA/GERAL"}
               </span>
               <HistoryStatusBadge status={item.status} />
             </div>
             <div className="flex flex-col sm:items-end text-xs font-medium text-slate-500">
               <span className="text-slate-700 dark:text-slate-300">{datePart}</span>
               <span>{timePart}</span>
             </div>
           </div>

           <div className="mb-3">
             <p className="text-sm font-medium text-slate-700 dark:text-slate-300 leading-relaxed max-w-3xl break-words whitespace-pre-wrap">
               {item.observacao || <span className="text-slate-400 italic font-normal">Nenhuma observação reportada.</span>}
             </p>
           </div>

           <div className="flex flex-wrap items-center gap-4 text-xs font-medium text-slate-500 pt-3 border-t border-slate-100 dark:border-slate-800">
              <div className="flex items-center gap-1.5">
                <User className="w-3.5 h-3.5 opacity-70" />
                <span>{item.responsavel || "Desconhecido"}</span>
              </div>
              {item.contato && (
                 <div className="flex items-center gap-1.5 text-slate-400">
                   <AtSign className="w-3.5 h-3.5 opacity-70" />
                   <span>{item.contato}</span>
                 </div>
              )}
           </div>

           {item.mensagem_original && item.mensagem_original !== item.observacao && (
              <div className="mt-3 text-xs">
                 <button 
                   onClick={() => setExpanded(!expanded)} 
                   className="flex items-center gap-1 text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 transition-colors font-medium border border-transparent hover:border-indigo-100 dark:hover:border-indigo-900/50 rounded px-1.5 py-0.5 -ml-1.5"
                 >
                   <MessageSquare className="w-3 h-3" />
                   Mensagem Original Completa
                   {expanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                 </button>
                 
                 {expanded && (
                    <div className="mt-2 p-3 bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded font-mono text-[11px] sm:text-xs text-slate-600 dark:text-slate-400 overflow-x-auto whitespace-pre-wrap break-words max-h-60 overflow-y-auto">
                      {item.mensagem_original}
                    </div>
                 )}
              </div>
           )}
        </div>
      </div>
    </div>
  );
};
