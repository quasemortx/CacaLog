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

  let response: Response;

  try {
    response = await fetch(url, { ...options, headers });
  } catch (networkError) {
    // Erro de rede puro: servidor offline, CORS bloqueando preflight, ou URL errada
    console.error("[fetchApi] Falha de rede ao conectar em:", url, networkError);
    throw new Error(
      `Erro de rede: não foi possível alcançar o backend em ${API_URL}. ` +
      `Verifique se o uvicorn está rodando na porta correta.`
    );
  }

  if (!response.ok) {
    let detail = "";
    try {
      const body = await response.json();
      detail = body?.detail || JSON.stringify(body);
    } catch {
      // body não é JSON
    }
    const msg = detail
      ? `[${response.status}] ${detail}`
      : `[${response.status}] ${response.statusText}`;
    console.error("[fetchApi] Erro HTTP:", url, msg);
    throw new Error(msg);
  }
  
  return await response.json();
}
