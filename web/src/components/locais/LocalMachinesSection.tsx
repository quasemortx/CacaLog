import { useState } from "react";
import type { MaquinaRead, MaquinaCreate, MaquinaUpdate } from "@/types/local";
import { MachineForm } from "./MachineForm";
import { Trash2, Edit2, Plus, Server } from "lucide-react";

interface LocalMachinesSectionProps {
  localId: string;
  maquinas: MaquinaRead[];
  onCreate: (data: MaquinaCreate) => void;
  onUpdate: (maquina_id: number, data: MaquinaUpdate) => void;
  onDelete: (maquina_id: number) => void;
  isPendingCreate?: boolean;
  isPendingUpdate?: boolean;
  isPendingDelete?: boolean;
}

export const LocalMachinesSection = ({
  maquinas,
  onCreate,
  onUpdate,
  onDelete,
  isPendingCreate,
  isPendingUpdate,
  isPendingDelete
}: LocalMachinesSectionProps) => {
  const [isAdding, setIsAdding] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);

  const handleCreate = (data: MaquinaCreate | MaquinaUpdate) => {
    onCreate(data as MaquinaCreate);
    setIsAdding(false);
  };

  const handleUpdate = (data: MaquinaCreate | MaquinaUpdate) => {
    if (editingId) {
      onUpdate(editingId, data as MaquinaUpdate);
      setEditingId(null);
    }
  };

  const confirmDelete = (id: number) => {
    if (confirm("Tem certeza que deseja remover esta máquina? A exclusão não pode ser desfeita.")) {
      onDelete(id);
    }
  };

  return (
    <section className="bg-white dark:bg-slate-950 p-6 rounded-xl border space-y-4">
      <div className="flex justify-between items-center border-b pb-2 mb-4">
        <div>
          <h3 className="text-lg font-semibold flex items-center gap-2 dark:text-slate-200">
            <Server className="h-5 w-5 text-indigo-500" />
            Máquinas no Local ({maquinas.length})
          </h3>
          <p className="text-sm text-slate-500">Múltiplos modelos/processadores podem ser mapeados.</p>
        </div>
        {!isAdding && (
          <button 
            type="button"
            onClick={() => setIsAdding(true)}
            className="px-3 py-1.5 rounded-md font-medium text-indigo-700 bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-900/40 dark:text-indigo-300 dark:hover:bg-indigo-900/60 transition-colors flex items-center gap-1.5"
          >
            <Plus className="h-4 w-4" />
            Adicionar Máquina
          </button>
        )}
      </div>

      {/* Adding Form */}
      {isAdding && (
        <MachineForm 
          onSave={handleCreate} 
          onCancel={() => setIsAdding(false)} 
          isLoading={!!isPendingCreate} 
        />
      )}

      {/* Machines List */}
      <div className="space-y-3">
        {maquinas.length === 0 && !isAdding && (
          <div className="text-center py-6 text-slate-500 bg-slate-50 dark:bg-slate-900 rounded-lg border border-dashed text-sm">
            Nenhuma máquina cadastrada para este local.
          </div>
        )}

        {maquinas.map((m) => {
          if (editingId === m.id) {
            return (
              <MachineForm 
                key={m.id}
                initialData={m}
                onSave={handleUpdate} 
                onCancel={() => setEditingId(null)} 
                isLoading={!!isPendingUpdate} 
              />
            );
          }

          return (
            <div key={m.id} className="p-4 rounded-lg border bg-white dark:bg-slate-900 shadow-sm flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
              
              <div className="flex-1 space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-slate-900 dark:text-slate-100">{m.modelo}</span>
                  <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border">
                    Qtd: {m.quantidade}
                  </span>
                  <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-300">
                    {m.propriedade}
                  </span>
                </div>
                
                <div className="text-sm text-slate-500 dark:text-slate-400 flex flex-wrap gap-x-4 gap-y-1">
                  {m.processador && <span>CPU: {m.processador}</span>}
                  
                  {m.ram_gb !== undefined && m.ram_gb > 0 && (
                    <span>RAM: {m.ram_gb}GB {m.ram_tipo}</span>
                  )}
                  
                  {m.armazenamento_gb !== undefined && m.armazenamento_gb > 0 && (
                    <span>Armaz: {m.armazenamento_gb}GB {m.armazenamento_tipo}</span>
                  )}
                  
                  <span className="flex items-center gap-1.5 text-xs text-slate-400">
                    Vídeo: 
                    DP={m.video_dp} 
                    HDMI={m.video_hdmi} 
                    VGA={m.video_vga}
                  </span>
                </div>
              </div>

              <div className="flex gap-2">
                <button 
                  onClick={() => setEditingId(m.id)}
                  className="p-2 text-slate-500 hover:text-indigo-600 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-md transition-colors"
                  title="Editar Máquina"
                >
                  <Edit2 className="h-4 w-4" />
                </button>
                <button 
                  onClick={() => confirmDelete(m.id)}
                  disabled={isPendingDelete}
                  className="p-2 text-slate-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-950/30 rounded-md transition-colors disabled:opacity-50"
                  title="Excluir Máquina"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>

            </div>
          );
        })}
      </div>
    </section>
  );
};
