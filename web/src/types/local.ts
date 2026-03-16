export interface LocalBase {
  local_id: string;
  tipo_local: "SALA" | "LAB" | string;
  sala?: string;
  predio?: number;
  andar?: number;
  tipo_ambiente?: string;
  status?: string;
  observacao?: string;
  setor?: string;
  
  quantidade_projetores: number;
  saida_projetor?: string;
  tomada_padrao?: "ANTIGO" | "NOVO" | string;
  adaptador_dp_vga: number;
  adaptador_dp_hdmi: number;
  adaptador_hdmi_vga: number;
  adaptador_duplicador_vga: number;
  adaptador_outros?: string;
  
  ultimo_responsavel?: string;
  ultimo_contato?: string;
}

export type LocalCreate = LocalBase;

export type LocalUpdate = Partial<LocalBase>;

export interface LocalRead extends LocalBase {
  id: number;
  created_at: string;
  updated_at: string;
}

export interface MaquinaBase {
  modelo: string;
  quantidade: number;
  processador?: string;
  propriedade?: "PROPRIO" | "ALUGADO" | string;
  ram_gb?: number;
  ram_modelo?: string;
  ram_tipo?: string;
  armazenamento_gb?: number;
  armazenamento_modelo?: string;
  armazenamento_tipo?: "HDD" | "SSD_SATA" | "SSD_NVME" | string;
  video_dp: number;
  video_hdmi: number;
  video_vga: number;
}

export type MaquinaCreate = MaquinaBase;

export type MaquinaUpdate = Partial<MaquinaBase>;

export interface MaquinaRead extends MaquinaBase {
  id: number;
  local_ref_id: number;
  created_at: string;
  updated_at: string;
}

export interface LocalDetailRead {
  local: LocalRead;
  maquinas: MaquinaRead[];
}
