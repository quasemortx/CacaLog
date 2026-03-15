import { fetchApi } from "./client";
import type { StatsResponse } from "@/types/stats";

export async function getStats(): Promise<StatsResponse> {
  return fetchApi<StatsResponse>("/api/stats");
}
