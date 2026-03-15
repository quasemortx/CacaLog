export interface InventoryItem {
  local_id: string;
  Sala?: string;
  Predio?: string | number;
  Andar?: string | number;
  TipoAmbiente?: string;
  Modelo?: string;
  BIOS?: string;
  TotalPCs?: string | number;
  Concluidos?: string | number;
  Pendentes?: string | number;
  Erros?: string | number;
  Status: string;
  Observacao?: string;
  Setor?: string;
  UltimoResponsavel?: string;
  UltimoContato?: string;
  UltimaAtualizacao?: string;
}

export interface InventoryResponse {
  items: InventoryItem[];
  total: number;
}
