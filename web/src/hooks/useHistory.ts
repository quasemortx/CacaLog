import { useQuery } from "@tanstack/react-query";
import { getHistory } from "@/api/history";
import type { HistoryFilters } from "@/api/history";

export function useHistory(filters?: HistoryFilters) {
  return useQuery({
    queryKey: ["history", filters],
    queryFn: () => getHistory(filters),
  });
}
