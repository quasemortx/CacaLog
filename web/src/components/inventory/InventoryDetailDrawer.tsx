import { type FC, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import type { InventoryItem } from '@/types/inventory';
import { StatusBadge } from './StatusBadge';
import { SectorBadge } from './SectorBadge';
import { formatDate } from '@/lib/formatters';
import { X, Server, LayoutTemplate, MapPin, HardDrive, Clock, Mail, MessageSquare } from 'lucide-react';

interface InventoryDetailDrawerProps {
  item: InventoryItem | null;
  onClose: () => void;
}

export const InventoryDetailDrawer: FC<InventoryDetailDrawerProps> = ({ item, onClose }) => {
  const navigate = useNavigate();
  
  // Close on Escape key press
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!item) return null;

  const DetailRow: FC<{ label: string; value: React.ReactNode; icon?: React.ReactNode }> = ({ label, value, icon }) => (
    <div className="flex flex-col py-3 border-b border-slate-100 dark:border-slate-800 last:border-0 hover:bg-slate-50/50 dark:hover:bg-slate-900/30 px-2 rounded transition-colors">
      <span className="text-xs font-medium text-slate-500 flex items-center gap-1.5 mb-1">
        {icon && <span className="opacity-70">{icon}</span>}
        {label}
      </span>
      <span className="text-sm text-slate-900 dark:text-slate-100 font-medium break-words">
        {value === undefined || value === null || value === "" ? <span className="text-slate-300 dark:text-slate-600">—</span> : value}
      </span>
    </div>
  );

  return (
    <>
      <div 
         className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-40 transition-opacity"
         onClick={onClose}
      />
      
      <div className="fixed inset-y-0 right-0 w-full md:w-[450px] bg-white dark:bg-slate-950 shadow-2xl z-50 transform transition-transform duration-300 ease-in-out border-l flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b bg-slate-50/80 dark:bg-slate-900/80 backdrop-blur">
           <div>
             <h2 className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-indigo-800 dark:from-indigo-400 dark:to-indigo-300 bg-clip-text text-transparent">
               {item.local_id || "Ambiente Desconhecido"}
             </h2>
             <div className="flex items-center gap-2 mt-2">
               <StatusBadge status={item.Status} />
               <SectorBadge sector={item.Setor} />
             </div>
           </div>
           
           <button 
             onClick={onClose}
             className="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors text-slate-500"
           >
             <X className="w-5 h-5" />
           </button>
        </div>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-8 pb-32">
           
           {/* Section 1: Identificação */}
           <section>
             <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider mb-4 border-b pb-2 flex items-center gap-2">
                <MapPin className="w-4 h-4 text-indigo-500" />
                Identificação Local
             </h3>
             <div className="space-y-1">
                <DetailRow label="Sala" value={item.Sala} />
                <DetailRow label="Prédio" value={item.Predio ? `Prédio ${item.Predio}` : ""} />
                <DetailRow label="Andar" value={item.Andar ? `${item.Andar}º Andar` : ""} />
                <DetailRow label="Tipo de Ambiente" value={item.TipoAmbiente} />
             </div>
           </section>

           {/* Section 2: Técnico */}
           <section>
             <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider mb-4 border-b pb-2 flex items-center gap-2">
                <Server className="w-4 h-4 text-indigo-500" />
                Hardware
             </h3>
             <div className="space-y-1">
                <DetailRow label="Modelo" value={item.Modelo} icon={<HardDrive className="w-3.5 h-3.5" />} />
                <DetailRow label="Versão de BIOS" value={item.BIOS} icon={<LayoutTemplate className="w-3.5 h-3.5" />} />
             </div>
           </section>

           {/* Section 3: Acompanhamento Progressivo */}
           <section>
             <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider mb-4 border-b pb-2">
                Progresso
             </h3>
             
             <div className="grid grid-cols-4 gap-2 mb-4">
                <div className="bg-slate-50 dark:bg-slate-900 rounded p-3 text-center border">
                   <div className="text-[10px] text-slate-500 uppercase font-semibold mb-1">Total</div>
                   <div className="text-xl font-bold text-slate-800 dark:text-slate-200">{item.TotalPCs || (item.TotalPCs === 0 ? 0 : "—")}</div>
                </div>
                <div className="bg-green-50 dark:bg-green-900/20 rounded p-3 text-center border border-green-100 dark:border-green-800/50">
                   <div className="text-[10px] text-green-600 dark:text-green-400 uppercase font-semibold mb-1">Prontos</div>
                   <div className="text-xl font-bold text-green-700 dark:text-green-300">{item.Concluidos || (item.Concluidos === 0 ? 0 : "—")}</div>
                </div>
                <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded p-3 text-center border border-yellow-100 dark:border-yellow-800/50">
                   <div className="text-[10px] text-yellow-600 dark:text-yellow-400 uppercase font-semibold mb-1">Pend.</div>
                   <div className="text-xl font-bold text-yellow-700 dark:text-yellow-300">{item.Pendentes || (item.Pendentes === 0 ? 0 : "—")}</div>
                </div>
                <div className="bg-red-50 dark:bg-red-900/20 rounded p-3 text-center border border-red-100 dark:border-red-800/50">
                   <div className="text-[10px] text-red-600 dark:text-red-400 uppercase font-semibold mb-1">Erros</div>
                   <div className="text-xl font-bold text-red-700 dark:text-red-300">{item.Erros || (item.Erros === 0 ? 0 : "—")}</div>
                </div>
             </div>

             <div className="bg-slate-50/50 dark:bg-slate-900/30 rounded-lg p-3 mt-4 border border-slate-100 dark:border-slate-800">
                <span className="text-xs font-medium text-slate-500 flex items-center gap-1.5 mb-2">
                   <MessageSquare className="w-3.5 h-3.5" /> Observação Central
                </span>
                <p className="text-sm font-medium text-slate-800 dark:text-slate-200 leading-relaxed break-words whitespace-pre-wrap">
                   {item.Observacao || <span className="text-slate-400 italic">Sem observações.</span>}
                </p>
             </div>
           </section>

           {/* Section 4: Auditoria */}
           <section>
             <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider mb-4 border-b pb-2 flex items-center gap-2">
                <Clock className="w-4 h-4 text-indigo-500" />
                Rastreamento
             </h3>
             <div className="space-y-1">
                <DetailRow label="Atualizado Em" value={formatDate(item.UltimaAtualizacao)} />
                <DetailRow label="Técnico" value={item.UltimoResponsavel} icon={<Mail className="w-3.5 h-3.5" />} />
                <DetailRow label="Contato" value={item.UltimoContato} />
             </div>
           </section>
        </div>
        
        {/* Footer */}
        <div className="border-t p-4 bg-slate-50 dark:bg-slate-900 flex justify-between absolute bottom-0 w-full">
           <button 
             onClick={() => {
               onClose();
               navigate(`/locais/${item.local_id}/editar`);
             }}
             className="px-4 py-2 bg-white dark:bg-slate-800 border-2 border-indigo-600 text-indigo-700 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-slate-700 rounded-md text-sm font-bold transition-colors"
           >
             Editar Local
           </button>
           <button 
             onClick={onClose}
             className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md text-sm font-medium transition-colors"
           >
             Fechar Detalhes
           </button>
        </div>
      </div>
    </>
  );
};
