import { useState, type FormEvent } from "react";
import type { MaquinaCreate, MaquinaUpdate, MaquinaRead } from "@/types/local";
import { Save, X } from "lucide-react";

interface MachineFormProps {
  initialData?: MaquinaRead | null;
  onSave: (data: MaquinaCreate | MaquinaUpdate) => void;
  onCancel: () => void;
  isLoading: boolean;
}

const defaultValues: MaquinaCreate = {
  modelo: "",
  quantidade: 1,
  processador: "",
  propriedade: "PROPRIO",
  ram_gb: 0,
  ram_modelo: "",
  ram_tipo: "",
  armazenamento_gb: 0,
  armazenamento_modelo: "",
  armazenamento_tipo: "SSD_SATA",
  video_dp: 0,
  video_hdmi: 0,
  video_vga: 0,
};

export const MachineForm = ({ initialData, onSave, onCancel, isLoading }: MachineFormProps) => {
  const [formData, setFormData] = useState<MaquinaCreate | MaquinaUpdate>(
    initialData || defaultValues
  );
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const handleChange = (field: keyof MaquinaCreate, value: string | number) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    setErrors((prev) => ({ ...prev, [field]: "" }));
  };

  const handleNumber = (field: keyof MaquinaCreate, value: string) => {
    const parsed = parseInt(value, 10);
    handleChange(field, isNaN(parsed) ? 0 : parsed);
  };

  const validate = () => {
    const newErrors: Record<string, string> = {};
    if (!formData.modelo?.trim()) newErrors.modelo = "Obrigatório";
    if (formData.quantidade === undefined || formData.quantidade < 1) newErrors.quantidade = "Mín 1";
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSave(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border border-indigo-200 dark:border-indigo-900 bg-indigo-50/50 dark:bg-indigo-950/20 p-5 rounded-lg space-y-4">
      <div className="flex justify-between items-center border-b border-indigo-100 dark:border-indigo-900 pb-2 mb-2">
        <h4 className="font-medium text-indigo-900 dark:text-indigo-300">
          {initialData ? "Editar Modelo" : "Adicionar Modelo de Máquina"}
        </h4>
        <button type="button" onClick={onCancel} className="text-slate-400 hover:text-slate-600">
          <X className="h-4 w-4" />
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Identificação */}
        <div className="space-y-1">
          <label className="text-sm font-medium dark:text-slate-300 text-slate-700">Modelo (Ex: Optiplex 390)</label>
          <input 
            required
            placeholder="Ex: Optiplex 390"
            className="w-full h-9 px-3 text-sm rounded-md border dark:bg-slate-900 dark:border-slate-800" 
            value={formData.modelo || ""} 
            onChange={(e) => handleChange("modelo", e.target.value)} 
          />
          {errors.modelo && <span className="text-red-500 text-xs">{errors.modelo}</span>}
        </div>
        
        <div className="space-y-1">
          <label className="text-sm font-medium dark:text-slate-300 text-slate-700">Quantidade</label>
          <input 
            type="number" min="1" required
            className="w-full h-9 px-3 text-sm rounded-md border dark:bg-slate-900 dark:border-slate-800" 
            value={formData.quantidade !== undefined ? formData.quantidade : 1} 
            onChange={(e) => handleNumber("quantidade", e.target.value)} 
          />
          {errors.quantidade && <span className="text-red-500 text-xs">{errors.quantidade}</span>}
        </div>

        <div className="space-y-1">
          <label className="text-sm font-medium dark:text-slate-300 text-slate-700">Propriedade</label>
          <select 
            className="w-full h-9 px-3 text-sm rounded-md border dark:bg-slate-900 dark:border-slate-800"
            value={formData.propriedade || ""}
            onChange={(e) => handleChange("propriedade", e.target.value)}
          >
            <option value="PROPRIO">PRÓPRIO</option>
            <option value="ALUGADO">ALUGADO</option>
          </select>
        </div>

        <div className="space-y-1">
          <label className="text-sm font-medium dark:text-slate-300 text-slate-700">Processador</label>
          <input 
            placeholder="Ex: i5-11400"
            className="w-full h-9 px-3 text-sm rounded-md border dark:bg-slate-900 dark:border-slate-800" 
            value={formData.processador || ""} 
            onChange={(e) => handleChange("processador", e.target.value)} 
          />
        </div>

        {/* Hardware details - Memory & Disk */}
        <div className="space-y-1">
          <label className="text-sm font-medium dark:text-slate-300 text-slate-700">RAM (GB)</label>
          <input 
            type="number" min="0"
            className="w-full h-9 px-3 text-sm rounded-md border dark:bg-slate-900 dark:border-slate-800" 
            value={formData.ram_gb !== undefined ? formData.ram_gb : ""} 
            onChange={(e) => handleNumber("ram_gb", e.target.value)} 
          />
        </div>

        <div className="space-y-1 flex gap-2">
          <div className="w-1/2">
            <label className="text-sm font-medium dark:text-slate-300 text-slate-700 block mb-1">Tipo RAM</label>
            <input 
              placeholder="Ex: DDR4"
              className="w-full h-9 px-3 text-sm rounded-md border dark:bg-slate-900 dark:border-slate-800" 
              value={formData.ram_tipo || ""} 
              onChange={(e) => handleChange("ram_tipo", e.target.value)} 
            />
          </div>
          <div className="w-1/2">
            <label className="text-sm font-medium dark:text-slate-300 text-slate-700 block mb-1">Freq/Modelo</label>
            <input 
              placeholder="Ex: 2666MHz"
              className="w-full h-9 px-3 text-sm rounded-md border dark:bg-slate-900 dark:border-slate-800" 
              value={formData.ram_modelo || ""} 
              onChange={(e) => handleChange("ram_modelo", e.target.value)} 
            />
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-sm font-medium dark:text-slate-300 text-slate-700">Armaz. (GB)</label>
          <input 
            type="number" min="0" placeholder="Ex: 256"
            className="w-full h-9 px-3 text-sm rounded-md border dark:bg-slate-900 dark:border-slate-800" 
            value={formData.armazenamento_gb !== undefined ? formData.armazenamento_gb : ""} 
            onChange={(e) => handleNumber("armazenamento_gb", e.target.value)} 
          />
        </div>

        <div className="space-y-1 flex gap-2">
          <div className="w-1/2">
            <label className="text-sm font-medium dark:text-slate-300 text-slate-700 block mb-1">Tipo Disk</label>
            <select 
              className="w-full h-9 px-3 text-sm rounded-md border dark:bg-slate-900 dark:border-slate-800"
              value={formData.armazenamento_tipo || ""}
              onChange={(e) => handleChange("armazenamento_tipo", e.target.value)}
            >
              <option value="SSD_SATA">SSD SATA</option>
              <option value="SSD_NVME">SSD NVME</option>
              <option value="HDD">HDD</option>
            </select>
          </div>
          <div className="w-1/2">
            <label className="text-sm font-medium dark:text-slate-300 text-slate-700 block mb-1">Detalhes</label>
            <input 
              placeholder="Ex: Kingston"
              className="w-full h-9 px-3 text-sm rounded-md border dark:bg-slate-900 dark:border-slate-800" 
              value={formData.armazenamento_modelo || ""} 
              onChange={(e) => handleChange("armazenamento_modelo", e.target.value)} 
            />
          </div>
        </div>
      </div>
      
      {/* Video Outputs */}
      <div>
        <label className="text-sm font-medium dark:text-slate-300 text-slate-700 block mb-1">Saídas de Vídeo (Qtd.)</label>
        <div className="flex gap-4">
          <label className="text-xs flex items-center gap-2"><span className="w-10">DisplayP</span>
            <input type="number" min="0" className="w-16 h-8 px-2 border rounded dark:bg-slate-900" value={formData.video_dp} onChange={(e) => handleNumber("video_dp", e.target.value)} />
          </label>
          <label className="text-xs flex items-center gap-2"><span className="w-10">HDMI</span>
            <input type="number" min="0" className="w-16 h-8 px-2 border rounded dark:bg-slate-900" value={formData.video_hdmi} onChange={(e) => handleNumber("video_hdmi", e.target.value)} />
          </label>
          <label className="text-xs flex items-center gap-2"><span className="w-10">VGA</span>
            <input type="number" min="0" className="w-16 h-8 px-2 border rounded dark:bg-slate-900" value={formData.video_vga} onChange={(e) => handleNumber("video_vga", e.target.value)} />
          </label>
        </div>
      </div>

      <div className="flex justify-end gap-2 pt-2">
        <button type="button" onClick={onCancel} className="px-3 py-1.5 text-sm rounded-md font-medium text-slate-700 hover:bg-white/50 dark:text-slate-300">
          Cancelar
        </button>
        <button type="submit" disabled={isLoading} className="px-3 py-1.5 text-sm rounded-md font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2">
          <Save className="h-3.5 w-3.5" />
          {isLoading ? "Salvando..." : "Salvar"}
        </button>
      </div>
    </form>
  );
};
