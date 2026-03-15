import { useQuery } from "@tanstack/react-query";
import { getInventory } from "@/api/inventory";
import type { InventoryFilters } from "@/api/inventory";

export function useInventory(filters?: InventoryFilters) {
  return useQuery({
    queryKey: ["inventory", filters],
    queryFn: () => getInventory(filters),
  });
}
