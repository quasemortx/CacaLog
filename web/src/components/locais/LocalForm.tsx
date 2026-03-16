import { useState, type FormEvent } from "react";
import type { LocalCreate, LocalUpdate, LocalRead } from "@/types/local";
import { Save } from "lucide-react";

interface LocalFormProps {
  initialData?: LocalRead | null;
  onSubmit: (data: LocalCreate | LocalUpdate) => void;
  isLoading: boolean;
}

const defaultValues: LocalCreate = {
  local_id: "",
  tipo_local: "SALA",
  sala: "",
  predio: 1,
  andar: 1,
  tipo_ambiente: "SALA",
  status: "NAO_AVALIADO",
  observacao: "",
  setor: "INDEFINIDO",
  quantidade_projetores: 0,
  saida_projetor: "",
  tomada_padrao: "NOVO",
  adaptador_dp_vga: 0,
  adaptador_dp_hdmi: 0,
  adaptador_hdmi_vga: 0,
  adaptador_duplicador_vga: 0,
  adaptador_outros: "",
  ultimo_responsavel: "",
  ultimo_contato: "",
};

export const LocalForm = ({ initialData, onSubmit, isLoading }: LocalFormProps) => {
  const isEditing = !!initialData;
  const [formData, setFormData] = useState<LocalCreate | LocalUpdate>(
    initialData || defaultValues
  );

  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const handleChange = (field: keyof LocalCreate, value: string | number) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    setErrors((prev) => ({ ...prev, [field]: "" }));
  };

  const handleNumber = (field: keyof LocalCreate, value: string) => {
    const parsed = parseInt(value, 10);
    handleChange(field, isNaN(parsed) ? 0 : parsed);
  };

  const validate = () => {
    const newErrors: Record<string, string> = {};
    if (!formData.local_id?.trim()) newErrors.local_id = "Campo obrigatório";
    if (!formData.tipo_local?.trim()) newErrors.tipo_local = "Campo obrigatório";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8 bg-white dark:bg-slate-950 p-6 rounded-xl border">
      
      {/* Seção 1 — Identificação do Local */}
      <section>
        <h3 className="text-lg font-semibold border-b pb-2 mb-4 dark:text-slate-200">1. Identificação do Local</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">ID Local (Ex: S-123)</label>
            <input 
              required
              disabled={isEditing}
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.local_id} 
              onChange={(e) => handleChange("local_id", e.target.value)} 
            />
            {errors.local_id && <span className="text-red-500 text-xs">{errors.local_id}</span>}
          </div>
          
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Tipo de Local</label>
            <select 
              required
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500"
              value={formData.tipo_local}
              onChange={(e) => handleChange("tipo_local", e.target.value)}
            >
              <option value="SALA">SALA</option>
              <option value="LAB">LAB</option>
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Sala (Nome/Número)</label>
            <input 
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.sala || ""} 
              onChange={(e) => handleChange("sala", e.target.value)} 
            />
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Prédio</label>
            <input 
              type="number"
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.predio !== undefined ? formData.predio : ""} 
              onChange={(e) => handleNumber("predio", e.target.value)} 
            />
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Andar</label>
            <input 
              type="number"
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.andar !== undefined ? formData.andar : ""} 
              onChange={(e) => handleNumber("andar", e.target.value)} 
            />
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Tipo de Ambiente</label>
            <input 
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.tipo_ambiente || ""} 
              onChange={(e) => handleChange("tipo_ambiente", e.target.value)} 
            />
          </div>
        </div>
      </section>

      {/* Seção 2 — Estado Atual */}
      <section>
        <h3 className="text-lg font-semibold border-b pb-2 mb-4 dark:text-slate-200">2. Estado Atual</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Status</label>
            <select 
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500"
              value={formData.status || ""}
              onChange={(e) => handleChange("status", e.target.value)}
            >
              <option value="NAO_AVALIADO">NÃO AVALIADO</option>
              <option value="OK">OK</option>
              <option value="PENDENTE">PENDENTE</option>
              <option value="ERRO">ERRO</option>
              <option value="INCOMPATIVEL">INCOMPATÍVEL</option>
              <option value="ATUALIZANDO">ATUALIZANDO</option>
            </select>
          </div>
          
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Setor Responsável</label>
            <select 
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500"
              value={formData.setor || ""}
              onChange={(e) => handleChange("setor", e.target.value)}
            >
              <option value="INDEFINIDO">INDEFINIDO</option>
              <option value="TI">TI</option>
              <option value="Manutenção">Manutenção</option>
            </select>
          </div>
          
          <div className="col-span-1 md:col-span-2 space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Observação Geral</label>
            <textarea 
              rows={2}
              className="w-full p-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.observacao || ""} 
              onChange={(e) => handleChange("observacao", e.target.value)} 
            />
          </div>
        </div>
      </section>

      {/* Seção 3 — Infraestrutura */}
      <section>
        <h3 className="text-lg font-semibold border-b pb-2 mb-4 dark:text-slate-200">3. Infraestrutura</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Qtd. Projetores</label>
            <input 
              type="number"
              min="0"
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.quantidade_projetores !== undefined ? formData.quantidade_projetores : 0} 
              onChange={(e) => handleNumber("quantidade_projetores", e.target.value)} 
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Saída Projetor</label>
            <input 
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.saida_projetor || ""} 
              onChange={(e) => handleChange("saida_projetor", e.target.value)} 
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Tomada Padrão</label>
            <select 
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500"
              value={formData.tomada_padrao || ""}
              onChange={(e) => handleChange("tomada_padrao", e.target.value)}
            >
              <option value="NOVO">NOVO (3 pinos)</option>
              <option value="ANTIGO">ANTIGO</option>
            </select>
          </div>
          
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Adpt. DP-VGA</label>
            <input 
              type="number" min="0"
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.adaptador_dp_vga !== undefined ? formData.adaptador_dp_vga : 0} 
              onChange={(e) => handleNumber("adaptador_dp_vga", e.target.value)} 
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Adpt. DP-HDMI</label>
            <input 
              type="number" min="0"
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.adaptador_dp_hdmi !== undefined ? formData.adaptador_dp_hdmi : 0} 
              onChange={(e) => handleNumber("adaptador_dp_hdmi", e.target.value)} 
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Adpt. HDMI-VGA</label>
            <input 
              type="number" min="0"
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.adaptador_hdmi_vga !== undefined ? formData.adaptador_hdmi_vga : 0} 
              onChange={(e) => handleNumber("adaptador_hdmi_vga", e.target.value)} 
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Adpt. Dup-VGA</label>
            <input 
              type="number" min="0"
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.adaptador_duplicador_vga !== undefined ? formData.adaptador_duplicador_vga : 0} 
              onChange={(e) => handleNumber("adaptador_duplicador_vga", e.target.value)} 
            />
          </div>
          <div className="col-span-1 md:col-span-2 space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Outros Adaptadores</label>
            <input 
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.adaptador_outros || ""} 
              onChange={(e) => handleChange("adaptador_outros", e.target.value)} 
            />
          </div>
        </div>
      </section>

      {/* Seção 4 — Auditoria Operacional */}
      <section>
        <h3 className="text-lg font-semibold border-b pb-2 mb-4 dark:text-slate-200">4. Última Auditoria</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Último Responsável</label>
            <input 
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.ultimo_responsavel || ""} 
              onChange={(e) => handleChange("ultimo_responsavel", e.target.value)} 
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-medium dark:text-slate-300">Contato / Celular</label>
            <input 
              className="w-full h-10 px-3 rounded-md border dark:bg-slate-900 dark:border-slate-800 focus:ring-2 focus:ring-indigo-500" 
              value={formData.ultimo_contato || ""} 
              onChange={(e) => handleChange("ultimo_contato", e.target.value)} 
            />
          </div>
        </div>
      </section>

      <div className="flex justify-end pt-4 gap-3 border-t">
        <button 
          type="button"
          onClick={() => window.history.back()}
          className="px-4 py-2 rounded-md font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 dark:text-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700"
        >
          Cancelar
        </button>
        <button 
          type="submit"
          disabled={isLoading}
          className="px-4 py-2 rounded-md font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 flex items-center gap-2"
        >
          <Save className="h-4 w-4" />
          {isLoading ? "Salvando..." : "Salvar Local"}
        </button>
      </div>
    </form>
  );
};
