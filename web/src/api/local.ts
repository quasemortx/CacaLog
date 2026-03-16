import { fetchApi } from "./client";
import type { 
  LocalCreate, LocalRead, LocalUpdate, LocalDetailRead,
  MaquinaCreate, MaquinaRead, MaquinaUpdate 
} from "../types/local";

// Locais APIs
export const createLocal = async (data: LocalCreate): Promise<LocalRead> => {
  return await fetchApi<LocalRead>("/api/locais", {
    method: "POST",
    body: JSON.stringify(data),
  });
};

export const getLocalDetail = async (local_id: string): Promise<LocalDetailRead> => {
  return await fetchApi<LocalDetailRead>(`/api/locais/${local_id}`);
};

export const updateLocal = async (local_id: string, data: LocalUpdate): Promise<LocalRead> => {
  return await fetchApi<LocalRead>(`/api/locais/${local_id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
};

export const deleteLocal = async (local_id: string): Promise<void> => {
  await fetchApi<void>(`/api/locais/${local_id}`, {
    method: "DELETE",
  });
};

// Máquinas APIs
export const createMaquina = async (local_id: string, data: MaquinaCreate): Promise<MaquinaRead> => {
  return await fetchApi<MaquinaRead>(`/api/locais/${local_id}/maquinas`, {
    method: "POST",
    body: JSON.stringify(data),
  });
};

export const updateMaquina = async (maquina_id: number, data: MaquinaUpdate): Promise<MaquinaRead> => {
  return await fetchApi<MaquinaRead>(`/api/maquinas/${maquina_id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
};

export const deleteMaquina = async (maquina_id: number): Promise<void> => {
  await fetchApi<void>(`/api/maquinas/${maquina_id}`, {
    method: "DELETE",
  });
};
