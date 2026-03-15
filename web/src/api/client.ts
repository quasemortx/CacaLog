const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const API_KEY = import.meta.env.VITE_API_KEY || "";

export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const baseUrl = API_URL.replace(/\/$/, "");
  const path = endpoint.replace(/^\//, "");
  const url = `${baseUrl}/${path}`;
  
  const headers = new Headers(options.headers || {});
  headers.set("Content-Type", "application/json");
  if (API_KEY) {
    headers.set("X-API-KEY", API_KEY);
  }

  try {
    const response = await fetch(url, { ...options, headers });
    
    if (!response.ok) {
      let errorMsg = `HTTP Error ${response.status}: ${response.statusText}`;
      try {
        const errorBody = await response.json();
        if (errorBody && errorBody.detail) {
          errorMsg = `API Error: ${errorBody.detail}`;
        }
      } catch (e) {
        // Body was probably not JSON, ignore parsing error
      }
      throw new Error(errorMsg);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === "TypeError" && error.message.includes("Failed to fetch")) {
        throw new Error("Erro de rede: O servidor backend (FastAPI) parece estar offline, inacessível ou bloqueado por CORS.");
      }
      throw error;
    }
    throw new Error("Ocorreu um erro desconhecido ao comunicar com a API.");
  }
}
