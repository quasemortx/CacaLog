export interface HistoryItem {
  timestamp: string;
  local_id: string;
  status: string;
  observacao: string;
  responsavel: string;
  contato: string;
  mensagem_original?: string;
  message_id?: string;
}

export interface HistoryResponse {
  items: HistoryItem[];
  total: number;
}
