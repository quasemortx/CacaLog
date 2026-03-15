import { fetchApi } from "./client";
import type { InventoryResponse } from "@/types/inventory";

export interface InventoryFilters {
  q?: string;
  status?: string;
  setor?: string;
}

export async function getInventory(filters?: InventoryFilters): Promise<InventoryResponse> {
  const params = new URLSearchParams();
  if (filters?.q) params.append("q", filters.q);
  if (filters?.status) params.append("status", filters.status);
  if (filters?.setor) params.append("setor", filters.setor);

  const queryString = params.toString();
  const endpoint = `/api/inventory${queryString ? `?${queryString}` : ""}`;
  
  return fetchApi<InventoryResponse>(endpoint);
}
