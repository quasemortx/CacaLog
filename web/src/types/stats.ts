export interface StatsResponse {
  total: number;
  by_status: Record<string, number>;
  by_setor: Record<string, number>;
}
