import { fetchApi } from "./client";
import type { HistoryResponse } from "@/types/history";

export interface HistoryFilters {
  q?: string;
  local_id?: string;
}

export async function getHistory(filters?: HistoryFilters): Promise<HistoryResponse> {
  const params = new URLSearchParams();
  if (filters?.q) params.append("q", filters.q);
  if (filters?.local_id) params.append("local_id", filters.local_id);

  const queryString = params.toString();
  const endpoint = `/api/history${queryString ? `?${queryString}` : ""}`;
  
  return fetchApi<HistoryResponse>(endpoint);
}
