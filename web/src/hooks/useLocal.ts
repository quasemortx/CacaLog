import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { 
  createLocal, getLocalDetail, updateLocal,
  createMaquina, updateMaquina, deleteMaquina
} from "../api/local";
import type { 
  LocalCreate, LocalUpdate,
  MaquinaCreate, MaquinaUpdate
} from "../types/local";

export function useLocalDetail(local_id: string | undefined) {
  return useQuery({
    queryKey: ["local", local_id],
    queryFn: () => getLocalDetail(local_id!),
    enabled: !!local_id,
  });
}

export function useCreateLocal() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: LocalCreate) => createLocal(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
    },
  });
}

export function useUpdateLocal() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ local_id, data }: { local_id: string, data: LocalUpdate }) => updateLocal(local_id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["local", variables.local_id] });
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
    },
  });
}

export function useCreateMaquina() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ local_id, data }: { local_id: string, data: MaquinaCreate }) => createMaquina(local_id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["local", variables.local_id] });
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
    },
  });
}

export function useUpdateMaquina() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (variables: { local_id: string, maquina_id: number, data: MaquinaUpdate }) => updateMaquina(variables.maquina_id, variables.data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["local", variables.local_id] });
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
    },
  });
}

export function useDeleteMaquina() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (variables: { local_id: string, maquina_id: number }) => deleteMaquina(variables.maquina_id),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["local", variables.local_id] });
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
    },
  });
}
